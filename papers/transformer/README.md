# 原始 Transformer · Attention Is All You Need

> **arXiv:1706.03762** · Vaswani et al. · NIPS 2017  
> 精读页：[index.html](./index.html) · 原文：[paper.pdf](./paper.pdf)

本仓库的**从零起点**：讲清 Q / K / V、缩放点积四步、多头注意力，以及 \(O(N^2)\) 从哪来。读完再进稀疏注意力。

## 粒度说明

核心方法（§3.2）按**计算步骤**拆开，不是整节一段：

1. 点积打分 → 2. 除以 \(\sqrt{d_k}\) → 3. softmax（可加掩码）→ 4. 加权 \(V\)  
5. 再拆多头：分头投影 → 各算各的 → Concat → \(W^O\)

标了「导读」的卡片是教学补充（形状、直觉），不是论文原句。

## 建议读法

1. 打开 [`index.html`](./index.html)，先读「从零」节  
2. 精读 §3.2.1 与 §3.2.2（不要跳）  
3. §4 表 1 最后一行接到稀疏  
4. 下一站：[`../sparse-attention/`](../sparse-attention/)

## 重建

```bash
python3 tools/build_transformer_page.py
```

相关：[稀疏注意力](../sparse-attention/) · [Linear Attention](../linear-attention/) · [Longformer](../longformer/)
