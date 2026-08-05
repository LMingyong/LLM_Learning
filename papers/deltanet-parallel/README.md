# 并行训练 DeltaNet（2024）

| 字段 | 内容 |
|------|------|
| 论文 | Parallelizing Linear Transformers with the Delta Rule over Sequence Length |
| 链接 | [arXiv:2406.06484](https://arxiv.org/abs/2406.06484) · [`paper.pdf`](./paper.pdf) |
| 一句话 | 给 **同一套 delta rule** 一套可沿序列并行的训练算法，并扩到 1.3B LM。 |

> 理论原点（为何用 delta、容量界）在 [`../deltanet/`](../deltanet/)（arXiv:2102.11174）。本夹讲 **怎么高效训练**。

## 怎么读

1. （建议）[`../deltanet/`](../deltanet/) — 先补 Linear → delta 理论桥  
2. **[`index.html`](./index.html)** — 逐段精读（小结 → Original → 译文 + 公式卡）  
3. **[`notes.md`](./notes.md)** — 短公式卡  
4. 下一篇：[`../gated-deltanet/`](../gated-deltanet/)（标量门 α）  
5. 再下一篇：[`../kda/`](../kda/)（通道门 + 混合）

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 精读主入口 |
| `notes.md` | 公式速查 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_delta_attention_page.py
```

相关：[理论原点](../deltanet/) · [Linear Attention](../linear-attention/) · [Gated DeltaNet](../gated-deltanet/) · [KDA](../kda/) · [FLA](https://github.com/fla-org/flash-linear-attention)
