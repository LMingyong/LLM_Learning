# BigBird

| 字段 | 内容 |
|------|------|
| 论文 | Big Bird: Transformers for Longer Sequences |
| 作者 | Zaheer et al. (Google Research) |
| 链接 | [arXiv:2007.14062](https://arxiv.org/abs/2007.14062) |
| 一句话 | **局部窗口 + 全局 token + 随机块**，线性复杂度稀疏注意力，并证明万能近似与图灵完备。 |

## 怎么读

**[`index.html`](./index.html)**

覆盖：三块积木图解、图稀疏化 / 小世界直觉、ITC vs ETC、块稀疏工程意义、与 Longformer 对照。

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 浅色长文详解 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_bigbird_page.py
```

相关：[Longformer](../longformer/) · [稀疏注意力专题](../../topics/sparse-attention/)
