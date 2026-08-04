# DeltaNet / Delta Attention

| 字段 | 内容 |
|------|------|
| 论文 | Parallelizing Linear Transformers with the Delta Rule over Sequence Length |
| 链接 | [arXiv:2406.06484](https://arxiv.org/abs/2406.06484) · [`paper.pdf`](./paper.pdf) |
| 一句话 | 给 **delta rule 线性注意力（DeltaNet）** 一套可沿序列并行的训练算法，并扩到 1.3B LM。 |

## 怎么读

1. **[`index.html`](./index.html)** — 逐段精读（小结 → Original → 译文 + 公式卡）
2. 再读后续升级：[`../kda/`](../kda/)（通道级门控 KDA）

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 精读主入口 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_delta_attention_page.py
```

相关：[Linear Attention](../linear-attention/) · [KDA / Kimi Linear](../kda/) · [Gated DeltaNet](https://arxiv.org/abs/2412.06464) · [FLA](https://github.com/fla-org/flash-linear-attention)
