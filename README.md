# LLM Learning

用于存放 LLM 学习笔记、论文精读与可运行教学代码。目标是：**从原始 Transformer 讲起**，再分叉到稀疏注意力与线性注意力两条现代路线。

## 统一约定

全部学习单元都在 [`papers/<slug>/`](./papers/)：

```text
papers/<slug>/
  README.md
  paper.pdf      # 单篇论文；跨论文专题可省略
  index.html     # 精读入口
  …              # 可选：notes、教学代码、demo、测试
```

精读页标准：每段 = **中文小结** → Original（或导读）→ 译文；关键公式独立成卡（KaTeX）。核心方法按计算步骤拆，不整节一段。

---

## 阅读顺序（请按这个走）

先读完 **第 0 站**，再选一条线。两条线都从同一公式分叉：

\[
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}(QK^\top/\sqrt{d_k})\,V
\]

- **稀疏**：公式不动，改「谁和谁连边」（掩码更稀）  
- **线性**：改公式，不再造 \(N\times N\) 分数表  

第一遍建议先走稀疏，再走线性，不要拧在一起。

### 第 0 站 · 从零（必读）

| 顺序 | 打开 | 你要带走的 |
|------|------|------------|
| 1 | [`papers/transformer/`](./papers/transformer/) | Q / K / V；缩放点积四步；多头；残差+FFN；位置编码；**\(O(N^2)\) 从哪来** |

读法：先读精读页「从零」导读，再精读 §3.2.1 与 §3.2.2，不要跳。§4 表 1 最后一行已经点名「只看 \(r\) 个邻居」——那就是稀疏的入口。

### 路线 A · 稀疏注意力（改连边）

同一套 softmax 注意力，只允许一部分 \((i,j)\)。

| 顺序 | 打开 | 你要带走的 |
|------|------|------------|
| A1 | [`papers/sparse-attention/`](./papers/sparse-attention/) | 总览：掩码、窗口、全局 token、块稀疏 |
| A2 | [`papers/sparse-transformer/`](./papers/sparse-transformer/) | 早期固定稀疏图案（\(O(N\sqrt{N})\)） |
| A3 | [`papers/longformer/`](./papers/longformer/) | 滑窗局部 + 任务驱动全局 |
| A4 | [`papers/watts-strogatz/`](./papers/watts-strogatz/) | 小世界图：为什么要加随机边（给 BigBird 垫） |
| A5 | [`papers/bigbird/`](./papers/bigbird/) | 窗口 + 全局 + 随机；先 `example.html` 再逐段精读 |
| A6 | [`papers/nsa/`](./papers/nsa/) | 可训练层次稀疏（压缩 / 选块 / 窗口） |
| A7 | [`papers/flash-attention/`](./papers/flash-attention/) | 正交：仍可是全注意力，但 IO 友好；常与稀疏块一起用 |

### 路线 B · 线性注意力（改公式）

不造 \(N\times N\)，用固定大小状态。必须先有第 0 站。

| 顺序 | 打开 | 你要带走的 |
|------|------|------------|
| B1 | [`papers/linear-attention/`](./papers/linear-attention/) | \(\varphi(q)^\top\varphi(k)\) + 结合律；因果形式 = RNN |
| B2 | [`papers/deltanet/`](./papers/deltanet/) | 容量/串扰 → delta 写入（理论原点，2021） |
| B3 | [`papers/deltanet-parallel/`](./papers/deltanet-parallel/) | 同一套 delta 的分块并行训练（2024） |
| B4 | [`papers/gated-deltanet/`](./papers/gated-deltanet/) | 再乘标量遗忘门 \(\alpha\) |
| B5 | [`papers/kda/`](./papers/kda/) | 通道级 \(\mathrm{Diag}(\alpha)\) + 混合；可跑教学代码 |

### 旁支

| 打开 | 何时读 |
|------|--------|
| [`papers/attention-residuals/`](./papers/attention-residuals/) | 有余力时：注意力残差视角，不挡主线 |

---

## 目录（按文件夹）

| 单元 | 入口 |
|------|------|
| **原始 Transformer（从零）** | [`papers/transformer/`](./papers/transformer/) |
| 稀疏注意力专题 | [`papers/sparse-attention/`](./papers/sparse-attention/) |
| Sparse Transformer | [`papers/sparse-transformer/`](./papers/sparse-transformer/) |
| Longformer | [`papers/longformer/`](./papers/longformer/) |
| Watts–Strogatz | [`papers/watts-strogatz/`](./papers/watts-strogatz/) |
| BigBird | [`papers/bigbird/`](./papers/bigbird/) |
| NSA | [`papers/nsa/`](./papers/nsa/) |
| Flash Attention 专题 | [`papers/flash-attention/`](./papers/flash-attention/) |
| Linear Attention | [`papers/linear-attention/`](./papers/linear-attention/) |
| DeltaNet 原点（理论） | [`papers/deltanet/`](./papers/deltanet/) |
| 并行训练 DeltaNet | [`papers/deltanet-parallel/`](./papers/deltanet-parallel/) |
| Gated DeltaNet | [`papers/gated-deltanet/`](./papers/gated-deltanet/) |
| Kimi Linear / KDA | [`papers/kda/`](./papers/kda/) |
| Attention Residuals | [`papers/attention-residuals/`](./papers/attention-residuals/) |

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
python3 tools/build_transformer_page.py
python3 tools/build_sparse_readable.py
python3 tools/build_linear_attention_page.py
python3 tools/build_deltanet_page.py
python3 tools/build_delta_attention_page.py   # → deltanet-parallel/
python3 tools/build_gated_deltanet_page.py
python3 tools/build_kimi_linear_page.py
```
