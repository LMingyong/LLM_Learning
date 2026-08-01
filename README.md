# LLM Learning

用于存放 LLM 学习笔记、论文精读与可运行教学代码。

## 论文精读（每篇一个文件夹）

入口：[`papers/`](./papers/)

| 论文 | 精读入口 |
|------|----------|
| **Longformer**（局部+全局） | [`papers/longformer/index.html`](./papers/longformer/index.html) |
| **BigBird**（局部+全局+随机） | [`papers/bigbird/index.html`](./papers/bigbird/index.html) |
| Attention Residuals | [`papers/attention-residuals/index.html`](./papers/attention-residuals/index.html) |
| **Linear Attention**（Transformers are RNNs） | [`papers/linear-attention/index.html`](./papers/linear-attention/index.html) |
| **Kimi Linear / Delta Attention** | [`papers/kimi-linear-delta-attention/index.html`](./papers/kimi-linear-delta-attention/index.html) |
| Watts–Strogatz（小世界） | [`papers/watts-strogatz/index.html`](./papers/watts-strogatz/index.html) |

## 技术专题（两个文件夹，各一篇 HTML）

入口：[`topics/`](./topics/)

| 专题 | 精读入口 |
|------|----------|
| **稀疏注意力** Sparse Attention | [`topics/sparse-attention/index.html`](./topics/sparse-attention/index.html) |
| **Flash Attention** | [`topics/flash-attention/index.html`](./topics/flash-attention/index.html) |

约定：`papers/<slug>/` 单篇论文；`topics/<slug>/` 跨论文专题。均提供 HTML 精读（对照翻译、段末小结、名词、引用）。

## 代码模块

| 模块 | 说明 |
|------|------|
| [`src/delta_attention`](./src/delta_attention) | Kimi Delta Attention 教学向 PyTorch 实现 |

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python3 examples/delta_attention_demo.py
pytest -q
```

## 参考

- [Attention Residuals](https://arxiv.org/abs/2603.15031)
- [Kimi Linear](https://arxiv.org/abs/2510.26692)
- [FLA / Flash Linear Attention](https://github.com/fla-org/flash-linear-attention)
