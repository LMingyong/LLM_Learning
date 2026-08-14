# Sparse Attention（稀疏注意力专题）

| 字段 | 内容 |
|------|------|
| 类型 | 跨论文专题（无单篇 `paper.pdf`） |
| 入口 | **[`index.html`](./index.html)**（浅色长文 + 示意图） |

**先读** [`../transformer/`](../transformer/)（原始 Transformer：QKV / 多头 / \(O(N^2)\)），再读本专题。

对照 **Longformer / BigBird / Sparse Transformer / NSA** 梳理稀疏连边怎么选、怎么落地。

## 文件

| 路径 | 说明 |
|------|------|
| `index.html` | 专题精读主入口 |

相关：[`../transformer/`](../transformer/)（从零） · [`../longformer/`](../longformer/) · [`../bigbird/`](../bigbird/) · [`../nsa/`](../nsa/) · [`../sparse-transformer/`](../sparse-transformer/) · [`../flash-attention/`](../flash-attention/)

```bash
python3 tools/build_sparse_readable.py
```
