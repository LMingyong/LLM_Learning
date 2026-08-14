# Longformer

| 字段 | 内容 |
|------|------|
| 论文 | Longformer: The Long-Document Transformer |
| 作者 | Iz Beltagy, Matthew E. Peters, Arman Cohan (AllenAI) |
| 链接 | [arXiv:2004.05150](https://arxiv.org/abs/2004.05150) · [GitHub](https://github.com/allenai/longformer) |
| 一句话 | 用**滑动窗口局部注意力 + 任务驱动全局注意力**把自注意力复杂度降到近线性，专攻长文档。 |

## 怎么读

打开精读页：

**[`index.html`](./index.html)**

内容包括：四种注意力图案图解、枢纽车站类比、多层感受野、对称全局注意力、两套 QKV、任务上如何设全局位、LED 与后续影响。

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 浅色长文详解（主入口） |
| `paper.pdf` | 原文 PDF |

重新生成：

```bash
python3 tools/build_longformer_page.py
```

先读：[原始 Transformer](../transformer/) · [稀疏注意力专题](../sparse-attention/)
