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
| **DeltaNet / Delta Attention** | [`papers/delta-attention/`](./papers/delta-attention/) |
| **Kimi Linear / KDA** | [`papers/kda/`](./papers/kda/) |
| Watts–Strogatz | [`papers/watts-strogatz/`](./papers/watts-strogatz/) |
| NSA | [`papers/nsa/`](./papers/nsa/) |
| Sparse Transformer | [`papers/sparse-transformer/`](./papers/sparse-transformer/) |
| 稀疏注意力专题 | [`papers/sparse-attention/`](./papers/sparse-attention/) |
| Flash Attention 专题 | [`papers/flash-attention/`](./papers/flash-attention/) |

> **Delta Attention ≠ KDA**：前者是 DeltaNet（arXiv:2406.06484）；后者是 Kimi Linear 里的 Kimi Delta Attention（arXiv:2510.26692）。两篇分夹存放。

## KDA 教学代码

| 路径 | 说明 |
|------|------|
| [`papers/kda/kda/`](./papers/kda/kda/) | 教学向 PyTorch |
| [`papers/kda/demo.py`](./papers/kda/demo.py) | 形状与 cache 演示 |
| [`papers/kda/test_kda.py`](./papers/kda/test_kda.py) | 方程级测试 |

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3 papers/kda/demo.py
pytest -q
```

## 参考

- [DeltaNet](https://arxiv.org/abs/2406.06484)
- [Kimi Linear](https://arxiv.org/abs/2510.26692)
- [FLA / Flash Linear Attention](https://github.com/fla-org/flash-linear-attention)
