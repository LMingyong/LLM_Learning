# BigBird

| 字段 | 内容 |
|------|------|
| 论文 | Big Bird: Transformers for Longer Sequences |
| 作者 | Zaheer et al. (Google Research) |
| 链接 | [arXiv:2007.14062](https://arxiv.org/abs/2007.14062) |
| 一句话 | **局部窗口 + 全局 token + 随机块**，线性复杂度稀疏注意力，并证明万能近似与图灵完备。 |

## 怎么读

1. **[`example.html`](./example.html)** — **全流程讲解**（推荐先读）  
   注意力设计 → 具体算法（含伪代码）→ 硬件优化（块稀疏 / GPU）→ 工程落地清单
2. **[`index.html`](./index.html)** — 浅色**逐段精读**  
   每段：中文小结 → Original → 译文；对照/搜索/名词表

## 文件

| 文件 | 说明 |
|------|------|
| `example.html` | 设计→算法→硬件→工程全流程 |
| `index.html` | 逐段精读页 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_bigbird_example.py   # 全流程页
python3 tools/build_bigbird_page.py      # 逐段精读
```

内容数据：`tools/bigbird_paragraphs.py`（精读页）

相关：[Watts–Strogatz](../watts-strogatz/) · [Longformer](../longformer/) · [稀疏注意力专题](../sparse-attention/)
