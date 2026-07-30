"""KDA 递推核心：逐步 recurrence 与分块版本。

公式（单 token、单 head，与笔记一致）::

    S ← Diag(exp(g_t)) S
    v̂ ← k_tᵀ S
    S ← S + β_t · k_t · (v_t - v̂)ᵀ
    o_t ← (q_t / √d)ᵀ S

其中 ``g_t ≤ 0``，``β_t ∈ (0, 1)``。
"""

from __future__ import annotations

import torch
from torch import Tensor


def recurrent_kda(
    q: Tensor,
    k: Tensor,
    v: Tensor,
    log_decay: Tensor,
    beta: Tensor,
    initial_state: Tensor | None = None,
) -> tuple[Tensor, Tensor]:
    """逐 token 执行 KDA 更新。

    参数形状
    --------
    q, k, v, log_decay : ``[B, T, H, D]``
    beta               : ``[B, T, H]``
    initial_state      : ``[B, H, D, D]`` 或 ``None``

    返回
    ----
    output : ``[B, T, H, D]``
    state  : ``[B, H, D, D]``
    """

    batch, time, heads, dim = q.shape
    # 状态在 fp32 中累加，避免 bf16/半精度下长时间递推漂移
    accum_dtype = torch.float64 if q.dtype == torch.float64 else torch.float32
    state = (
        torch.zeros(batch, heads, dim, dim, device=q.device, dtype=accum_dtype)
        if initial_state is None
        else initial_state.to(dtype=accum_dtype)
    )
    outputs: list[Tensor] = []
    scale = dim**-0.5

    for t in range(time):
        q_t = q[:, t].to(accum_dtype)
        k_t = k[:, t].to(accum_dtype)
        v_t = v[:, t].to(accum_dtype)
        decay_t = log_decay[:, t].to(accum_dtype).exp()  # (B, H, D) ∈ (0, 1]
        beta_t = beta[:, t].to(accum_dtype)  # (B, H)

        # 1) 通道级遗忘：左乘对角阵 Diag(exp(g))
        state = state * decay_t.unsqueeze(-1)

        # 2) 用当前 key 读出预测值，并计算 delta
        predicted = torch.einsum("bhd,bhdv->bhv", k_t, state)
        error = v_t - predicted

        # 3) 秩一纠错写入
        state = state + beta_t[..., None, None] * torch.einsum(
            "bhd,bhv->bhdv", k_t, error
        )

        # 4) 查询（使用更新后的 S）
        out_t = torch.einsum("bhd,bhdv->bhv", q_t * scale, state)
        outputs.append(out_t.to(dtype=v.dtype))

    return torch.stack(outputs, dim=1), state


def chunked_kda(
    q: Tensor,
    k: Tensor,
    v: Tensor,
    log_decay: Tensor,
    beta: Tensor,
    initial_state: Tensor | None = None,
    chunk_size: int = 32,
    detach_between_chunks: bool = False,
) -> tuple[Tensor, Tensor]:
    """按 chunk 调用 :func:`recurrent_kda`，数值上应与逐步版本一致。

    官方实现用 DPLR/WY 表示做真正的块内并行；这里只做「边界递推 + 块内逐步」，
    用于学习与正确性对照，并限制反向图瞬时占用。
    """

    if chunk_size < 1:
        raise ValueError("chunk_size 必须为正")

    state = initial_state
    outputs: list[Tensor] = []
    for start in range(0, q.shape[1], chunk_size):
        end = min(start + chunk_size, q.shape[1])
        chunk_out, state = recurrent_kda(
            q[:, start:end],
            k[:, start:end],
            v[:, start:end],
            log_decay[:, start:end],
            beta[:, start:end],
            state,
        )
        outputs.append(chunk_out)
        if detach_between_chunks:
            assert state is not None
            state = state.detach()

    assert state is not None
    return torch.cat(outputs, dim=1), state
