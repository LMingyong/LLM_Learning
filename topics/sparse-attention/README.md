# Sparse Attention（稀疏注意力）

| 字段 | 内容 |
|------|------|
| 类型 | 专题精读（对照多篇原文） |
| 入口 | **[`index.html`](./index.html)**（浅色长文 + 示意图） |

## 本页特点

- 对照 **Longformer / BigBird / Sparse Transformer / NSA** 技术报告重写
- 加长中文讲解，少堆术语卡片
- 内嵌 SVG：五种连边图案、四步流水线、NSA 三路结构
- 本地 PDF：`papers/` 目录

## 文件

| 路径 | 说明 |
|------|------|
| `index.html` | 精读主入口 |
| `papers/*.pdf` | 原文 PDF |
| `../flash-attention/` | 相关专题：Flash 如何高效算「留下的边」 |

重新生成页面：

```bash
python3 tools/build_sparse_readable.py
```
