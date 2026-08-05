# Papers

统一约定：每个学习单元一个文件夹。

```text
papers/<slug>/
  README.md
  paper.pdf      # 原文（单篇论文；专题可省略）
  index.html     # 精读页
  …              # 可选：notes、教学代码、demo、测试
```

- **单篇论文**：有 `paper.pdf`，精读在同目录 `index.html`。
- **跨论文专题**：可无 `paper.pdf`，用 `index.html` 串联多篇。

## 已收录

| 文件夹 | 说明 |
|--------|------|
| [longformer](./longformer/) | Longformer (arXiv:2004.05150) |
| [bigbird](./bigbird/) | BigBird (arXiv:2007.14062) |
| [watts-strogatz](./watts-strogatz/) | Watts–Strogatz (Nature 1998) |
| [attention-residuals](./attention-residuals/) | Attention Residuals (arXiv:2603.15031) |
| [linear-attention](./linear-attention/) | Linear Attention (arXiv:2006.16236) |
| [deltanet](./deltanet/) | **DeltaNet 原点 / FWP** (arXiv:2102.11174) |
| [deltanet-parallel](./deltanet-parallel/) | **并行训练 DeltaNet** (arXiv:2406.06484) |
| [gated-deltanet](./gated-deltanet/) | **Gated DeltaNet** (arXiv:2412.06464) |
| [kda](./kda/) | **Kimi Linear / KDA** (arXiv:2510.26692) — 含教学代码 |
| [nsa](./nsa/) | Native Sparse Attention (arXiv:2502.11089) |
| [sparse-transformer](./sparse-transformer/) | Sparse Transformer (arXiv:1904.10509) |
| [sparse-attention](./sparse-attention/) | 专题：稀疏注意力 |
| [flash-attention](./flash-attention/) | 专题：Flash Attention |
