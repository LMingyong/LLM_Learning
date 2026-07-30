# Sparse Attention（稀疏注意力）

| 字段 | 内容 |
|------|------|
| 类型 | 专题精读（跨多篇论文） |
| 入口 | [`index.html`](./index.html) |

## 覆盖内容

- 稀疏注意力在算什么、掩码/路由如何定义
- 主流模式：滑动窗口、全局+局部、块稀疏、Top-k 路由
- 算子四步：掩码 → 分数 → softmax → 加权 V
- 工程落地：HF `sliding_window`、Flash `window_size`、vLLM、长序列训练

## 关联专题

- [Flash Attention](../flash-attention/) — 稀疏定义「算哪些块」，Flash 定义「块怎么在片上算」
