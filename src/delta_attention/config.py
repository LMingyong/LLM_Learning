"""KDA 层配置。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class KDAConfig:
    """单个 Kimi Delta Attention 层的超参。

    教学实现令 key_dim == value_dim == ``head_dim``，使状态形状
    ``[B, H, D, D]`` 便于观察；这不改变 delta rule 本身。
    """

    hidden_size: int = 256
    num_heads: int = 4
    head_dim: int = 64
    conv_kernel_size: int = 4
    gate_rank: int = 64
    chunk_size: int = 32
    use_short_conv: bool = True
    norm_eps: float = 1e-5
    # log-decay 下界（负数）：防止数值上过度遗忘到 0
    gate_lower_bound: float = -5.0

    def validate(self) -> None:
        if self.hidden_size != self.num_heads * self.head_dim:
            raise ValueError("hidden_size 必须等于 num_heads * head_dim")
        if self.conv_kernel_size < 1:
            raise ValueError("conv_kernel_size 必须为正")
        if self.chunk_size < 1:
            raise ValueError("chunk_size 必须为正")
        if self.gate_rank < 1:
            raise ValueError("gate_rank 必须为正")
        if self.gate_lower_bound >= 0:
            raise ValueError("gate_lower_bound 必须为负（log-decay）")
