# 并行训练 DeltaNet · 速记

## 和原点的分工

| | `../deltanet/` | 本夹 |
|---|---|---|
| 论文 | 2102.11174 | 2406.06484 |
| 问题 | 为什么 delta？ | 怎么并行算 delta？ |
| 关键词 | FWP、容量、β | WY、chunkwise、1.3B |

## 公式锚点

\[
S_t = S_{t-1}(I - \beta_t k_t k_t^\top) + \beta_t v_t k_t^\top
\]

块内用 WY 表示一串 Householder，块间递推——训练可并行。

## 下一跳

Gated DeltaNet：前面再乘标量 α。
