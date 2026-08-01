# Kimi Linear / Delta Attention

| 字段 | 内容 |
|------|------|
| 论文 | Kimi Linear: An Expressive, Efficient Attention Architecture |
| 链接 | [arXiv:2510.26692](https://arxiv.org/abs/2510.26692) · [`paper.pdf`](./paper.pdf) |
| 一句话 | 以 **Kimi Delta Attention (KDA)** 为核心的混合线性注意力：通道级门控 + delta rule，KDA:MLA≈3:1。 |

## 怎么读（推荐顺序）

1. **[`index.html`](./index.html)** — 浅色**逐段精读**（小结 → Original → 译文）
2. **[`notes.md`](./notes.md)** — 更短的公式卡片
3. **`src/delta_attention/recurrent.py`** — 逐步递推金标准
4. **`examples/delta_attention_demo.py`** — 形状与 cache 续写

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 逐段精读页 |
| `notes.md` | 公式与读码指引 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_kimi_linear_page.py
```

内容数据：`tools/kimi_linear_paragraphs.py`

相关：[Linear Attention 源头](../linear-attention/) · [Attention Residuals](../attention-residuals/) · [官方 KDA kernel](https://github.com/fla-org/flash-linear-attention/tree/main/fla/ops/kda)
