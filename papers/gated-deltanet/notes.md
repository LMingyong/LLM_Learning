# Gated DeltaNet 公式笔记

论文：[arXiv:2412.06464](https://arxiv.org/abs/2412.06464)  
精读：[`index.html`](./index.html)

## 三式对照

**Mamba2**

$$
S_t = \alpha_t S_{t-1} + v_t k_t^{\top}
$$

**DeltaNet**

$$
S_t = S_{t-1}(I-\beta_t k_t k_t^{\top}) + \beta_t v_t k_t^{\top}
$$

**Gated DeltaNet（式 10）**

$$
S_t = S_{t-1}\bigl(\alpha_t(I-\beta_t k_t k_t^{\top})\bigr) + \beta_t v_t k_t^{\top}
$$

| 极限 | 行为 |
|------|------|
| `α → 0` | 快速清空记忆 |
| `α → 1` | 退化为纯 DeltaNet |

## 阅读顺序

1. [`../deltanet/`](../deltanet/)（理论）→ [`../deltanet-parallel/`](../deltanet-parallel/)（训练）  
2. 本页 / [`index.html`](./index.html)  
3. [`../kda/`](../kda/)（`Diag(α)`）
