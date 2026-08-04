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
| **Longformer**（局部+全局） | [`papers/longformer/index.html`](./papers/longformer/index.html) |
| **BigBird**（局部+全局+随机） | [`papers/bigbird/index.html`](./papers/bigbird/index.html) |
| Attention Residuals | [`papers/attention-residuals/index.html`](./papers/attention-residuals/index.html) |
| **Linear Attention**（Transformers are RNNs） | [`papers/linear-attention/index.html`](./papers/linear-attention/index.html) |
| **Kimi Linear / Delta Attention** | [`papers/kimi-linear-delta-attention/`](./papers/kimi-linear-delta-attention/) |
| Watts–Strogatz（小世界） | [`papers/watts-strogatz/index.html`](./papers/watts-strogatz/index.html) |
| Native Sparse Attention (NSA) | [`papers/nsa/`](./papers/nsa/) |
| Sparse Transformer | [`papers/sparse-transformer/`](./papers/sparse-transformer/) |
| **稀疏注意力专题** | [`papers/sparse-attention/index.html`](./papers/sparse-attention/index.html) |
| **Flash Attention 专题** | [`papers/flash-attention/index.html`](./papers/flash-attention/index.html) |

## Kimi Linear / KDA 教学代码

代码与论文材料同夹，不再放在仓库根 `src/`：

| 路径 | 说明 |
|------|------|
| [`papers/kimi-linear-delta-attention/delta_attention/`](./papers/kimi-linear-delta-attention/delta_attention/) | 教学向 PyTorch |
| [`papers/kimi-linear-delta-attention/demo.py`](./papers/kimi-linear-delta-attention/demo.py) | 形状与 cache 演示 |
| [`papers/kimi-linear-delta-attention/test_kda.py`](./papers/kimi-linear-delta-attention/test_kda.py) | 方程级测试 |

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3 papers/kimi-linear-delta-attention/demo.py
pytest -q
```

## 参考

- [Attention Residuals](https://arxiv.org/abs/2603.15031)
- [Kimi Linear](https://arxiv.org/abs/2510.26692)
- [FLA / Flash Linear Attention](https://github.com/fla-org/flash-linear-attention)
