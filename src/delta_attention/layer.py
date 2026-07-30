"""完整的 Kimi Delta Attention 层（投影 + 门控 + 递推）。"""

from __future__ import annotations

import math
from dataclasses import dataclass

import torch
from torch import Tensor, nn
from torch.nn import functional as F

from .config import KDAConfig
from .recurrent import chunked_kda


def l2_normalize(x: Tensor, eps: float = 1e-6) -> Tensor:
    """在 float32 上做末维 L2 归一化，再还原 dtype。"""

    dtype = x.dtype
    return F.normalize(x.float(), p=2.0, dim=-1, eps=eps).to(dtype)


class RMSNorm(nn.Module):
    def __init__(self, dim: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(dim))
        self.eps = eps

    def forward(self, x: Tensor) -> Tensor:
        rms = x.float().pow(2).mean(dim=-1, keepdim=True).add(self.eps).rsqrt()
        return (x.float() * rms).to(x.dtype) * self.weight


class CausalDepthwiseConv1d(nn.Module):
    """因果 depthwise 短卷积，为 Q/K/V 提供局部归纳偏置。"""

    def __init__(self, channels: int, kernel_size: int) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.weight = nn.Parameter(torch.empty(channels, 1, kernel_size))
        nn.init.normal_(self.weight, mean=0.0, std=0.02)

    def forward(
        self, x: Tensor, cache: Tensor | None = None
    ) -> tuple[Tensor, Tensor]:
        # x: [B, T, C]
        if cache is not None:
            history = torch.cat((cache, x), dim=1)
            y = F.conv1d(history.transpose(1, 2), self.weight, groups=x.shape[-1])
        else:
            padded = F.pad(x.transpose(1, 2), (self.kernel_size - 1, 0))
            y = F.conv1d(padded, self.weight, groups=x.shape[-1])

        if self.kernel_size == 1:
            new_cache = x[:, :0]
        else:
            source = torch.cat((cache, x), dim=1) if cache is not None else x
            missing = self.kernel_size - 1 - source.shape[1]
            if missing > 0:
                source = F.pad(source, (0, 0, missing, 0))
            new_cache = source[:, -(self.kernel_size - 1) :].detach()

        return F.silu(y.transpose(1, 2)), new_cache


@dataclass
class KDAState:
    """解码续写所需状态：矩阵记忆 + 短卷积历史。"""

    memory: Tensor  # [B, H, D, D]
    q_conv: Tensor | None = None
    k_conv: Tensor | None = None
    v_conv: Tensor | None = None


class KimiDeltaAttention(nn.Module):
    """带神经参数化的完整 KDA 序列混合层。"""

    def __init__(self, config: KDAConfig) -> None:
        super().__init__()
        config.validate()
        self.config = config
        width = config.num_heads * config.head_dim

        self.q_proj = nn.Linear(config.hidden_size, width, bias=False)
        self.k_proj = nn.Linear(config.hidden_size, width, bias=False)
        self.v_proj = nn.Linear(config.hidden_size, width, bias=False)

        if config.use_short_conv:
            self.q_conv = CausalDepthwiseConv1d(width, config.conv_kernel_size)
            self.k_conv = CausalDepthwiseConv1d(width, config.conv_kernel_size)
            self.v_conv = CausalDepthwiseConv1d(width, config.conv_kernel_size)

        # 低秩瓶颈预测逐通道 forget logits
        self.forget_proj = nn.Sequential(
            nn.Linear(config.hidden_size, config.gate_rank, bias=False),
            nn.Linear(config.gate_rank, width, bias=False),
        )
        self.beta_proj = nn.Linear(config.hidden_size, config.num_heads, bias=False)

        # 每 head 一个基率 + 每通道 timescale（log 空间）
        self.A_log = nn.Parameter(
            torch.log(torch.empty(config.num_heads).uniform_(1.0, 16.0))
        )
        dt = torch.exp(
            torch.empty(width).uniform_(math.log(0.001), math.log(0.1))
        ).clamp_min(1e-4)
        self.dt_bias = nn.Parameter(dt + torch.log(-torch.expm1(-dt)))

        self.output_gate = nn.Linear(config.hidden_size, width, bias=True)
        self.output_norm = RMSNorm(config.head_dim, config.norm_eps)
        self.out_proj = nn.Linear(width, config.hidden_size, bias=False)

    def _project(
        self, x: Tensor, state: KDAState | None
    ) -> tuple[Tensor, Tensor, Tensor, tuple[Tensor | None, Tensor | None, Tensor | None]]:
        q_raw, k_raw, v_raw = self.q_proj(x), self.k_proj(x), self.v_proj(x)
        if self.config.use_short_conv:
            q, q_cache = self.q_conv(q_raw, None if state is None else state.q_conv)
            k, k_cache = self.k_conv(k_raw, None if state is None else state.k_conv)
            v, v_cache = self.v_conv(v_raw, None if state is None else state.v_conv)
        else:
            q, k, v = F.silu(q_raw), F.silu(k_raw), F.silu(v_raw)
            q_cache = k_cache = v_cache = None
        return q, k, v, (q_cache, k_cache, v_cache)

    def forward(
        self,
        x: Tensor,
        state: KDAState | None = None,
        use_cache: bool = False,
    ) -> tuple[Tensor, KDAState | None]:
        batch, time, _ = x.shape
        heads, dim = self.config.num_heads, self.config.head_dim
        q, k, v, conv_caches = self._project(x, state)

        q = l2_normalize(q.view(batch, time, heads, dim))
        k = l2_normalize(k.view(batch, time, heads, dim))
        v = v.view(batch, time, heads, dim)

        raw_dt = self.forget_proj(x).view(batch, time, heads, dim)
        dt_bias = self.dt_bias.view(1, 1, heads, dim)
        # softplus > 0，再乘 -exp(A_log) => log_decay ≤ 0
        log_decay = -self.A_log.exp().view(1, 1, heads, 1) * F.softplus(raw_dt + dt_bias)
        log_decay = log_decay.clamp(min=self.config.gate_lower_bound, max=-1e-6)
        beta = torch.sigmoid(self.beta_proj(x))

        output, final_memory = chunked_kda(
            q,
            k,
            v,
            log_decay,
            beta,
            None if state is None else state.memory,
            chunk_size=self.config.chunk_size,
        )

        gate = torch.sigmoid(self.output_gate(x).view(batch, time, heads, dim))
        output = self.output_norm(output) * gate
        output = self.out_proj(output.reshape(batch, time, heads * dim))

        new_state = None
        if use_cache:
            new_state = KDAState(final_memory.detach(), *conv_caches)
        return output, new_state
