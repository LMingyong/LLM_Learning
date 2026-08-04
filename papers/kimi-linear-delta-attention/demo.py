"""KDA 形状与 cache 续写演示。"""

from __future__ import annotations

import torch

from delta_attention import KDAConfig, KimiDeltaAttention, recurrent_kda


def demo_layer() -> None:
    torch.manual_seed(0)
    config = KDAConfig(
        hidden_size=128,
        num_heads=4,
        head_dim=32,
        gate_rank=32,
        chunk_size=16,
    )
    layer = KimiDeltaAttention(config).eval()

    x = torch.randn(2, 48, config.hidden_size)
    y, _ = layer(x)
    print(f"layer input : {tuple(x.shape)}")
    print(f"layer output: {tuple(y.shape)}")

    prefix, cache = layer(x[:, :32], use_cache=True)
    suffix, _ = layer(x[:, 32:], state=cache, use_cache=True)
    y_cached = torch.cat((prefix, suffix), dim=1)
    max_diff = (y_cached - y).abs().max().item()
    print(f"cache vs full max |diff|: {max_diff:.3e}")


def demo_recurrent_shapes() -> None:
    torch.manual_seed(1)
    b, t, h, d = 1, 5, 2, 8
    q = torch.nn.functional.normalize(torch.randn(b, t, h, d), dim=-1)
    k = torch.nn.functional.normalize(torch.randn(b, t, h, d), dim=-1)
    v = torch.randn(b, t, h, d)
    log_decay = -torch.nn.functional.softplus(torch.randn(b, t, h, d))
    beta = torch.sigmoid(torch.randn(b, t, h))

    out, state = recurrent_kda(q, k, v, log_decay, beta)
    print(f"recurrent out  : {tuple(out.shape)}")
    print(f"recurrent state: {tuple(state.shape)}  # 固定大小，与 T 无关")


if __name__ == "__main__":
    demo_recurrent_shapes()
    demo_layer()
