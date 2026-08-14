# Flash Attention（闪存注意力专题）

| 字段 | 内容 |
|------|------|
| 类型 | 跨论文专题（无单篇 `paper.pdf`） |
| 入口 | [`index.html`](./index.html) |

覆盖 HBM 瓶颈、在线 softmax、FlashAttention-1/2/3，以及与稀疏注意力的组合。

## 关联

- [原始 Transformer](../transformer/) — 先搞清全注意力公式
- [Sparse Attention](../sparse-attention/) — 稀疏模式减少 Flash 内循环加载的 key 块

```bash
python3 tools/build_topic_html.py
```
