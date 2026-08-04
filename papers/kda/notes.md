# Kimi Delta Attention（KDA）学习笔记

对应论文 [Kimi Linear (arXiv:2510.26692)](https://arxiv.org/abs/2510.26692)。

**不要和 DeltaNet 搞混：**

| 夹 | 论文 | 要点 |
|----|------|------|
| [`../delta-attention/`](../delta-attention/) | arXiv:2406.06484 | delta rule 擦写 + 可扩展并行训练 |
| **本夹** | arXiv:2510.26692 | 通道级 `Diag(α)` + KDA:MLA=3:1 |

精读与公式墙：[`index.html`](./index.html)

## 谱系（抽出单列）

**DeltaNet（前驱，见另一夹）**

$$
S_t = (I - \beta_t k_t k_t^{\top}) S_{t-1} + \beta_t k_t v_t^{\top}
$$

**GDN（标量遗忘）**

$$
S_t = \alpha_t (I - \beta_t k_t k_t^{\top}) S_{t-1} + \beta_t k_t v_t^{\top}
$$

**KDA（本篇，式 1）**

$$
S_t = (I - \beta_t k_t k_t^{\top})\,\mathrm{Diag}(\alpha_t)\, S_{t-1} + \beta_t k_t v_t^{\top}
$$

## 四步递推（对齐 `kda/recurrent.py`）

1. 遗忘：`S ← Diag(exp(g_t)) S`
2. 预测：`v̂ ← k_tᵀ S`
3. 纠错：`S ← S + β_t k_t (v_t − v̂)ᵀ`
4. 读取：`o_t ← (q_t / √d)ᵀ S`

## 本夹代码

```bash
pip install -e ".[dev]"
python3 papers/kda/demo.py
pytest -q papers/kda
```

1. `kda/recurrent.py` — 金标准递推  
2. `kda/layer.py` — 投影 / 短卷积 / 门控  
3. `demo.py` / `test_kda.py`
