# Watts–Strogatz（小世界网络）

| 字段 | 内容 |
|------|------|
| 论文 | Collective dynamics of ‘small-world’ networks |
| 作者 | Duncan J. Watts & Steven H. Strogatz |
| 出处 | Nature 393, 440–442 (1998) |
| DOI | [10.1038/30918](https://doi.org/10.1038/30918) |
| 一句话 | 对环格子做概率 **p** 随机重连，得到**高聚类 + 短路径**的小世界网络。 |

## 怎么读

**[`index.html`](./index.html)** — 浅色**逐段精读**：

- 每段：中文小结 → Original → 译文
- 覆盖：动机、重连构造（Fig.1）、L/C 定义、小世界区间（Fig.2）、Table 1 实证、疾病动力学（Fig.3）、结语
- 末节桥接 BigBird：窗口≈局部边，随机注意力≈捷径，但工程上「不删窗、只加边」

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 逐段精读页 |
| `paper.pdf` | 原文 PDF（Nature 扫描件） |

```bash
python3 tools/build_watts_strogatz_page.py
```

内容数据：`tools/watts_strogatz_paragraphs.py`

相关：[BigBird 精读](../bigbird/) · [BigBird 全流程](../bigbird/example.html) · [稀疏注意力专题](../sparse-attention/)
