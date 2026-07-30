"""教学向 Kimi Delta Attention（KDA）实现。

本包优先可读性与公式对应关系，不追求生产级 Triton kernel 性能。
"""

from .config import KDAConfig
from .layer import KDAState, KimiDeltaAttention
from .recurrent import chunked_kda, recurrent_kda

__all__ = [
    "KDAConfig",
    "KDAState",
    "KimiDeltaAttention",
    "chunked_kda",
    "recurrent_kda",
]
