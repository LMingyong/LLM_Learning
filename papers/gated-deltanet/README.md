# Gated DeltaNet

| 字段 | 内容 |
|------|------|
| 论文 | Gated Delta Networks: Improving Mamba2 with Delta Rule |
| 链接 | [arXiv:2412.06464](https://arxiv.org/abs/2412.06464) · [`paper.pdf`](./paper.pdf) |
| 一句话 | **Gated delta rule**：标量遗忘门 α × delta 擦写 β；打赢 Mamba2 与纯 DeltaNet。 |

## 怎么读

1. （建议）[`../deltanet/`](../deltanet/) — 理论原点；[`../deltanet-parallel/`](../deltanet-parallel/) — 可扩展训练  
2. **[`index.html`](./index.html)** — 本篇逐段精读 + 公式墙  
3. （下一步）[`../kda/`](../kda/) — 通道级 `Diag(α)`  

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 精读主入口（KaTeX 公式卡） |
| `notes.md` | 短公式卡 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_gated_deltanet_page.py
```

相关：[DeltaNet 原点](../deltanet/) · [并行训练](../deltanet-parallel/) · [KDA](../kda/) · [官方代码](https://github.com/NVlabs/GatedDeltaNet)
