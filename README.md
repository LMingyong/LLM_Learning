# LLM Learning

用于存放 LLM 学习笔记与可运行教学代码的仓库。

当前已落地模块：

| 模块 | 说明 |
|------|------|
| [notes/delta-attention](notes/delta-attention/README.md) | Kimi Delta Attention（KDA）原理笔记 |
| [src/delta_attention](src/delta_attention) | 教学向 PyTorch 实现（可读优先，非生产 kernel） |

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 跑通核心示例
python examples/delta_attention_demo.py

# 单元测试
pytest -q
```

## 参考

- 论文：[Kimi Linear: An Expressive, Efficient Attention Architecture](https://arxiv.org/abs/2510.26692)
- 官方 kernel：[fla-org/flash-linear-attention](https://github.com/fla-org/flash-linear-attention)
- 模型权重：[moonshotai/Kimi-Linear-48B-A3B-Instruct](https://huggingface.co/moonshotai/Kimi-Linear-48B-A3B-Instruct)
