# LLM Learning

用于存放 LLM 学习笔记、论文精读与可运行教学代码。

## 统一约定

全部学习单元都在 [`papers/<slug>/`](./papers/)：

```text
papers/<slug>/
  README.md
  paper.pdf      # 单篇论文；跨论文专题可省略
  index.html     # 精读入口
  …              # 可选：notes、教学代码、demo、测试
```

| 单元 | 入口 |
|------|------|
| **Longformer** | [`papers/longformer/`](./papers/longformer/) |
| **BigBird** | [`papers/bigbird/`](./papers/bigbird/) |
| Attention Residuals | [`papers/attention-residuals/`](./papers/attention-residuals/) |
| **Linear Attention** | [`papers/linear-attention/`](./papers/linear-attention/) |
| **DeltaNet 原点（理论）** | [`papers/deltanet/`](./papers/deltanet/) |
| **并行训练 DeltaNet** | [`papers/deltanet-parallel/`](./papers/deltanet-parallel/) |
| **Gated DeltaNet** | [`papers/gated-deltanet/`](./papers/gated-deltanet/) |
| **Kimi Linear / KDA** | [`papers/kda/`](./papers/kda/) |
| Watts–Strogatz | [`papers/watts-strogatz/`](./papers/watts-strogatz/) |
| NSA | [`papers/nsa/`](./papers/nsa/) |
| Sparse Transformer | [`papers/sparse-transformer/`](./papers/sparse-transformer/) |
| 稀疏注意力专题 | [`papers/sparse-attention/`](./papers/sparse-attention/) |
| Flash Attention 专题 | [`papers/flash-attention/`](./papers/flash-attention/) |

> **谱系**：Linear Attention（2006）→ **DeltaNet 原点**（2102）→ 并行训练（2406）→ Gated DeltaNet（2412）→ KDA（2510）。

## KDA 教学代码

| 路径 | 说明 |
|------|------|
| [`papers/kda/kda/`](./papers/kda/kda/) | 教学向 PyTorch |
| [`papers/kda/demo.py`](./papers/kda/demo.py) | 形状与 cache 演示 |
| [`papers/kda/test_kda.py`](./papers/kda/test_kda.py) | 方程级测试 |

```bash
pip install -e ".[dev]"
python3 papers/kda/demo.py
pytest -q papers/kda
```

## 重建精读页

```bash
python3 tools/build_deltanet_page.py
python3 tools/build_delta_attention_page.py   # → deltanet-parallel/
python3 tools/build_gated_deltanet_page.py
python3 tools/build_kimi_linear_page.py
python3 tools/build_linear_attention_page.py
```
