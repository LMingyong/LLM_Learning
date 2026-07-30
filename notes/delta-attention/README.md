# Delta Attention / Kimi Delta Attention（学习笔记）

本文对应论文 [Kimi Linear (arXiv:2510.26692)](https://arxiv.org/abs/2510.26692) 中的核心模块
**Kimi Delta Attention (KDA)**。目标是把「为什么需要它」和「每一步在算什么」讲清楚，
方便对照 `src/delta_attention` 里的教学代码阅读。

## 1. Softmax Attention 的瓶颈

标准因果注意力为每个历史 token 保留 `(k, v)`：

- 时间复杂度：约 `O(L²)`
- KV cache：约 `O(L · d)`

上下文变长后，解码吞吐与显存都会被 cache 卡住。线性注意力家族试图用一块
**固定大小** 的状态矩阵 `S` 压缩历史，使每步开销与序列长度无关。

## 2. 从线性注意力到 Delta Rule

最朴素的线性注意力可以写成在线外积累加：

```text
S_t = S_{t-1} + k_t v_tᵀ
o_t = S_tᵀ q_t
```

问题：只加不改，长上下文里旧关联会互相干扰。

**DeltaNet** 引入联想记忆里的 delta rule：先按当前 key「擦除」旧内容，再写入新 value：

```text
S_t = (I - β_t k_t k_tᵀ) S_{t-1} + β_t k_t v_tᵀ
```

等价写法（更直观）：

```text
v̂_t = k_tᵀ S_{t-1}          # 用当前 key 读出预测
e_t  = v_t - v̂_t            # 预测误差（delta）
S_t  = S_{t-1} + β_t k_t e_tᵀ
```

若内存里已经把 `k_t` 映射到接近 `v_t`，误差接近 0，就不会反复把同一关联叠上去。

## 3. Gated DeltaNet：标量遗忘

Gated DeltaNet 再加一个 **标量** 衰减 `α_t ∈ (0,1]`：

```text
S_t = α_t (I - β_t k_t k_tᵀ) S_{t-1} + β_t k_t v_tᵀ
```

整个 head 的所有通道共用同一个遗忘速度，表达能力仍受限。

## 4. KDA 的关键：通道级对角门控

KDA 把标量 `α_t` 换成对角阵 `Diag(α_t)`，其中 `α_t ∈ (0,1]^{d}`：

```text
S_t = (I - β_t k_t k_tᵀ) Diag(α_t) S_{t-1} + β_t k_t v_tᵀ
```

逐步展开（与本仓库 `recurrent_kda` 一致）：

```text
1) 遗忘： S ← Diag(exp(g_t)) S          # g_t ≤ 0，逐通道衰减
2) 预测： v̂ ← k_tᵀ S
3) 纠错： S ← S + β_t · k_t · (v_t - v̂)ᵀ
4) 读取： o_t ← (q_t / √d)ᵀ S
```

直觉：

| 符号 | 角色 |
|------|------|
| `k_t` | 地址：决定改写/查询哪条「记忆行」 |
| `v_t` | 内容：希望写进该地址的值 |
| `q_t` | 查询：从更新后的 `S` 读出 |
| `exp(g_t)` | 每条地址通道各自的遗忘率 |
| `β_t` | 本次纠错写入的强度 |

状态形状固定为 `[heads, d, d]`（教学实现里取 key_dim = value_dim = d），
**不随序列变长**，这是相对 KV cache 的核心收益。

## 5. 与 Softmax 的对比（单头）

```text
普通因果注意力                         Kimi Delta Attention

token1 → (k1,v1) ─┐                   token1 → update ─┐
token2 → (k2,v2) ─┼→ 不断增长的 KV     token2 → update ─┼→ 固定大小矩阵 S
  ...             │                   ...              │
tokent → (kt,vt) ─┘                   tokent → update ─┘
         ↑ q_t 与每个 key 比对                  ↑ o_t = q_tᵀ S

cache: O(t · d)                       state: O(d · d) / head
```

Kimi Linear 并不是「全部换成 KDA」，而是 **KDA : 全注意力 ≈ 3 : 1** 的混合堆叠，
用少量全局层补足精确远距检索，同时用大量线性层压低 cache。

## 6. 本仓库代码怎么读

1. `src/delta_attention/recurrent.py` — 逐步 recurrence（正确性金标准）
2. `src/delta_attention/layer.py` — 投影、短卷积、门控参数化、输出门
3. `examples/delta_attention_demo.py` — 形状与 cache 续写演示
4. `tests/` — chunk 等价性、β=0 仅衰减、因果性、cache 一致性

生产场景请优先使用官方 Flash Linear Attention / FlashKDA kernel；
这里的实现刻意保留中间变量与注释，方便对照论文公式。

## 7. 延伸阅读

- Gated DeltaNet 原论文：[arXiv:2412.06464](https://arxiv.org/abs/2412.06464)
- FLA 仓库中的 KDA kernel：[fla-org/flash-linear-attention](https://github.com/fla-org/flash-linear-attention)
- Sebastian Raschka 的 Gated DeltaNet 导读：[LLMs-from-scratch / deltanet](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/08_deltanet)
