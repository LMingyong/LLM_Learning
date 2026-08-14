# 原始 Transformer · 速记

论文：[arXiv:1706.03762](https://arxiv.org/abs/1706.03762) · 精读：[`index.html`](./index.html)

## 必须能默写

**缩放点积**

$$
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
$$

四步：\(QK^\top\)（\(N\times N\)）→ 除 \(\sqrt{d_k}\) → softmax → 乘 \(V\)。

**多头**（Base：\(h=8,\; d_k=64,\; d_{\mathrm{model}}=512\)）

$$
\mathrm{head}_i=\mathrm{Attention}(QW_i^Q,KW_i^K,VW_i^V),\quad
\mathrm{MultiHead}=\mathrm{Concat}(\mathrm{heads})W^O
$$

**子层包装**

$$
x\leftarrow\mathrm{LayerNorm}(x+\mathrm{Sublayer}(x))
$$

## 三种注意力来源

| 位置 | Q | K,V | 掩码 |
|------|---|-----|------|
| 编码器自注意 | 源 | 源 | 无 |
| 解码器自注意 | 目标 | 目标 | 因果（未来 = \(-\infty\)） |
| 交叉注意 | 目标 | 源 | 无 |

## 接到稀疏

全注意力 = 每个 query 看所有 key。稀疏 = 同一公式，softmax 只在允许集合 \(S(i)\) 上做。原文 §4 已写「只看半径 \(r\) 的邻域」。
