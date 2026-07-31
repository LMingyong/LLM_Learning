# BigBird

| 字段 | 内容 |
|------|------|
| 论文 | Big Bird: Transformers for Longer Sequences |
| 作者 | Zaheer et al. (Google Research) |
| 链接 | [arXiv:2007.14062](https://arxiv.org/abs/2007.14062) |
| 一句话 | **局部窗口 + 全局 token + 随机块**，线性复杂度稀疏注意力，并证明万能近似与图灵完备。 |

## 怎么读

**[`index.html`](./index.html)** — 浅色**逐段精读**：

- 每段：中文小结 → Original → 译文
- 支持对照 / 仅译文 / 仅原文；`J`/`K` 跳段；名词表与搜索
- 覆盖 Abstract → Intro → Related → §2 架构 → §3 理论 → NLP/基因组实验 → 块稀疏工程要点

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 逐段精读页（由脚本生成） |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_bigbird_page.py
```

内容数据：`tools/bigbird_paragraphs.py`

相关：[Longformer](../longformer/) · [稀疏注意力专题](../../topics/sparse-attention/)
