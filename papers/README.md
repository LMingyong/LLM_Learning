# Papers

统一约定：每个学习单元一个文件夹。

```text
papers/<slug>/
  README.md      # 索引
  paper.pdf      # 原文（单篇论文；专题可省略）
  index.html     # 精读页
```

- **单篇论文**：有 `paper.pdf`，精读在同目录 `index.html`。
- **跨论文专题**：同样放在 `papers/`，可无 `paper.pdf`，用 `index.html` 串联多篇。

## 已收录

| 文件夹 | 说明 |
|--------|------|
| [longformer](./longformer/) | Longformer (arXiv:2004.05150) — 局部+全局 |
| [bigbird](./bigbird/) | BigBird (arXiv:2007.14062) — 局部+全局+随机块 |
| [watts-strogatz](./watts-strogatz/) | Watts–Strogatz (Nature 1998) — 小世界网络 |
| [attention-residuals](./attention-residuals/) | Attention Residuals (arXiv:2603.15031) |
| [linear-attention](./linear-attention/) | Linear Attention / Transformers are RNNs (arXiv:2006.16236) |
| [kimi-linear-delta-attention](./kimi-linear-delta-attention/) | Kimi Linear / KDA (arXiv:2510.26692) |
| [nsa](./nsa/) | Native Sparse Attention (arXiv:2502.11089) |
| [sparse-transformer](./sparse-transformer/) | Sparse Transformer (arXiv:1904.10509) |
| [sparse-attention](./sparse-attention/) | **专题**：稀疏注意力谱系 |
| [flash-attention](./flash-attention/) | **专题**：Flash Attention |
