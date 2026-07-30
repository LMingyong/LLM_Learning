# Flash Attention（闪存注意力）

| 字段 | 内容 |
|------|------|
| 类型 | 专题精读（跨多篇论文） |
| 入口 | [`index.html`](./index.html) |

## 覆盖内容

- 朴素注意力的 HBM 瓶颈与 IO-aware 思路
- 在线 softmax（分块仍与全量等价）
- FlashAttention-1 / 2 / 3 差异
- 完整前向/反向分块流程
- Prefill vs Decode、与稀疏注意力的组合

## 关联专题

- [Sparse Attention](../sparse-attention/) — 稀疏模式减少 Flash 内循环加载的 key 块
