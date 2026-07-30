"""KDA 递推与层行为的方程级测试。"""

from __future__ import annotations

import torch

from delta_attention import KDAConfig, KimiDeltaAttention, chunked_kda, recurrent_kda


def test_chunking_matches_recurrent_and_grads() -> None:
    torch.manual_seed(0)
    shape = (2, 7, 2, 4)
    q, k, v, raw_gate = [
        torch.randn(shape, dtype=torch.float64, requires_grad=True) for _ in range(4)
    ]
    beta = torch.sigmoid(torch.randn(2, 7, 2, dtype=torch.float64, requires_grad=True))
    log_decay = -torch.nn.functional.softplus(raw_gate)

    ref_out, ref_state = recurrent_kda(q, k, v, log_decay, beta)
    ref_loss = ref_out.square().sum() + ref_state.square().sum()
    ref_grads = torch.autograd.grad(ref_loss, (q, k, v, raw_gate), retain_graph=True)

    chunk_out, chunk_state = chunked_kda(q, k, v, log_decay, beta, chunk_size=3)
    chunk_loss = chunk_out.square().sum() + chunk_state.square().sum()
    chunk_grads = torch.autograd.grad(chunk_loss, (q, k, v, raw_gate))

    torch.testing.assert_close(chunk_out, ref_out, rtol=1e-10, atol=1e-10)
    torch.testing.assert_close(chunk_state, ref_state, rtol=1e-10, atol=1e-10)
    for actual, expected in zip(chunk_grads, ref_grads, strict=True):
        torch.testing.assert_close(actual, expected, rtol=1e-9, atol=1e-9)


def test_zero_beta_only_decays_memory() -> None:
    q = torch.randn(1, 3, 1, 2)
    k = torch.randn_like(q)
    v = torch.randn_like(q)
    log_decay = torch.full_like(q, -0.2)
    initial = torch.randn(1, 1, 2, 2)

    _, final = recurrent_kda(q, k, v, log_decay, torch.zeros(1, 3, 1), initial)
    expected = initial
    for t in range(3):
        expected = expected * torch.exp(log_decay[:, t]).unsqueeze(-1)
    torch.testing.assert_close(final, expected)


def test_identical_key_value_write_is_small_when_already_memorized() -> None:
    """若 S 已正确映射 k→v，则 delta 纠错应接近 0。"""

    torch.manual_seed(4)
    k = torch.nn.functional.normalize(torch.randn(1, 1, 1, 4), dim=-1)
    v = torch.randn(1, 1, 1, 4)
    # 构造已记住的状态：S = kᵀ 伪逆意义上的简单外积近似
    # 对单位向量 k，S = kᵀ? 我们令 S 满足 kᵀ S = v，取 S = k.unsqueeze(-1) * v.unsqueeze(-2)
    # einsum k,S -> v：用 S[b,h,d_k,d_v] = k[..., :, None] * v[..., None, :]
    state0 = torch.einsum("bhd,bhv->bhdv", k[:, 0], v[:, 0])
    q = k.clone()
    log_decay = torch.zeros_like(k)  # exp(0)=1，不遗忘
    beta = torch.ones(1, 1, 1)

    pred_before = torch.einsum("bhd,bhdv->bhv", k[:, 0], state0)
    torch.testing.assert_close(pred_before, v[:, 0], rtol=1e-5, atol=1e-5)

    _, state1 = recurrent_kda(q, k, v, log_decay, beta, state0)
    torch.testing.assert_close(state1, state0, rtol=1e-5, atol=1e-5)


def test_layer_cache_matches_full_pass() -> None:
    torch.manual_seed(2)
    config = KDAConfig(
        hidden_size=16, num_heads=2, head_dim=8, gate_rank=4, chunk_size=3
    )
    layer = KimiDeltaAttention(config).eval()
    x = torch.randn(1, 6, 16)

    full, _ = layer(x)
    prefix, cache = layer(x[:, :4], use_cache=True)
    suffix, _ = layer(x[:, 4:], state=cache, use_cache=True)
    torch.testing.assert_close(
        torch.cat((prefix, suffix), dim=1), full, rtol=1e-5, atol=1e-5
    )


def test_causal_prefix_stable_under_future_tokens() -> None:
    torch.manual_seed(3)
    config = KDAConfig(hidden_size=16, num_heads=2, head_dim=8, gate_rank=4)
    layer = KimiDeltaAttention(config).eval()
    prefix = torch.randn(1, 4, 16)
    extension = torch.randn(1, 3, 16)

    short, _ = layer(prefix)
    long, _ = layer(torch.cat((prefix, extension), dim=1))
    torch.testing.assert_close(short, long[:, :4], rtol=1e-5, atol=1e-5)


def test_config_validation() -> None:
    try:
        KDAConfig(hidden_size=15, num_heads=2, head_dim=8).validate()
        raised = False
    except ValueError:
        raised = True
    assert raised
