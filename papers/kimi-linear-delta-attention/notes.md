# Delta Attention / Kimi Delta Attention（学习笔记）

本文对应论文 [Kimi Linear (arXiv:2510.26692)](https://arxiv.org/abs/2510.26692) 中的核心模块
**Kimi Delta Attention (KDA)**。材料都在本夹：`paper.pdf`、精读 `index.html`、教学代码 `delta_attention/`。

更完整的逐段精读与 **KaTeX 公式墙** 见 [`index.html`](./index.html)。

## 1. Softmax Attention 的瓶颈

- 时间复杂度：约 `O(L²)`
- KV cache：约 `O(L · d)`

线性注意力用固定大小状态矩阵 `S` 压缩历史，使每步开销与序列长度无关。

## 2. 谱系公式（抽出单列）

**Linear（只加不改）**

$$
S_t = S_{t-1} + k_t v_t^{\top},\quad o_t = S_t^{\top} q_t
$$

**DeltaNet（delta rule）**

$$
S_t = (I - \beta_t k_t k_t^{\top}) S_{t-1} + \beta_t k_t v_t^{\top}
$$

等价展开：

$$
\hat{v}_t = k_t^{\top} S_{t-1},\quad
e_t = v_t - \hat{v}_t,\quad
S_t = S_{t-1} + \beta_t k_t e_t^{\top}
$$

**GDN（标量遗忘）**

$$
S_t = \alpha_t (I - \beta_t k_t k_t^{\top}) S_{t-1} + \beta_t k_t v_t^{\top}
$$

**KDA（通道级对角门，式 1）**

$$
S_t = (I - \beta_t k_t k_t^{\top})\,\mathrm{Diag}(\alpha_t)\, S_{t-1} + \beta_t k_t v_t^{\top}
$$

## 3. 四步递推（对齐 `delta_attention/recurrent.py`）

1. 遗忘：`S ← Diag(exp(g_t)) S`（`g_t ≤ 0`，逐通道）
2. 预测：`v̂ ← k_tᵀ S`
3. 纠错：`S ← S + β_t · k_t · (v_t − v̂)ᵀ`
4. 读取：`o_t ← (q_t / √d)ᵀ S`

| 符号 | 角色 |
|------|------|
| `k_t` | 地址 |
| `v_t` | 内容 |
| `q_t` | 查询 |
| `exp(g_t)` | 每通道遗忘率 |
| `β_t` | 写入强度 |

状态形状固定为 `[heads, d, d]`（教学实现 key_dim = value_dim = d），**不随序列变长**。

## 4. 本夹代码怎么读

1. `delta_attention/recurrent.py` — 逐步 recurrence（正确性金标准）
2. `delta_attention/layer.py` — 投影、短卷积、门控、输出门
3. `demo.py` — 形状与 cache 续写
4. `test_kda.py` — chunk 等价、β=0、因果性、cache

```bash
pip install -e ".[dev]"
python3 papers/kimi-linear-delta-attention/demo.py
pytest -q papers/kimi-linear-delta-attention
```

生产请用官方 FlashKDA / FLA kernel。

## 5. 延伸阅读

- 精读页：[index.html](./index.html)
- Linear Attention 源头：[../linear-attention/](../linear-attention/)
- Gated DeltaNet：[arXiv:2412.06464](https://arxiv.org/abs/2412.06464)
- FLA KDA ops：[fla-org/flash-linear-attention](https://github.com/fla-org/flash-linear-attention)
