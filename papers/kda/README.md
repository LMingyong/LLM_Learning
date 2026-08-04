# Kimi Linear / KDA

| 字段 | 内容 |
|------|------|
| 论文 | Kimi Linear: An Expressive, Efficient Attention Architecture |
| 链接 | [arXiv:2510.26692](https://arxiv.org/abs/2510.26692) · [`paper.pdf`](./paper.pdf) |
| 一句话 | **Kimi Delta Attention (KDA)** = Gated DeltaNet + 通道级 `Diag(α)`；层间 KDA:MLA≈3:1。 |

> 与 [`../delta-attention/`](../delta-attention/)（DeltaNet，arXiv:2406.06484）是**不同论文**：那边是可扩展 delta rule 基线；本夹是 Kimi 的通道门控升级 + 混合架构。

## 怎么读

1. （建议）先读 [`../delta-attention/index.html`](../delta-attention/index.html) 搞清擦写
2. **[`index.html`](./index.html)** — 本篇逐段精读 + 公式墙
3. **[`notes.md`](./notes.md)** — 短公式卡
4. **[`kda/recurrent.py`](./kda/recurrent.py)** — 逐步递推金标准
5. **[`demo.py`](./demo.py)** — 形状与 cache 续写

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 逐段精读（KaTeX 公式卡） |
| `notes.md` | 公式与读码指引 |
| `paper.pdf` | 原文 PDF |
| `kda/` | 教学向 PyTorch 实现 |
| `demo.py` | 形状 / cache 演示 |
| `test_kda.py` | 递推与层行为测试 |

```bash
python3 tools/build_kimi_linear_page.py
pip install -e ".[dev]"
python3 papers/kda/demo.py
pytest -q papers/kda
```

相关：[DeltaNet](../delta-attention/) · [Linear Attention](../linear-attention/) · [官方 KDA kernel](https://github.com/fla-org/flash-linear-attention/tree/main/fla/ops/kda)
