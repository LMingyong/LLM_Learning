# DeltaNet 原点 · Linear Transformers Are Secretly Fast Weight Programmers

> **arXiv:2102.11174** · Schlag, Irie, Schmidhuber · ICML 2021  
> 精读页：[index.html](./index.html) · 原文：[paper.pdf](./paper.pdf)

这是 **DeltaNet 理论原点**：证明 Linear Attention ≡ Fast Weight Programmer，推出加性写入的容量上限，并把写入指令换成 delta rule（带可学习 β）。

## 和旁边几夹的区别

| 夹 | 论文 | 你要带走的 |
|---|---|---|
| 本夹 `deltanet/` | 2102.11174 | **为什么**要用 delta（容量 / 串扰 / 指令集） |
| [`../deltanet-parallel/`](../deltanet-parallel/) | 2406.06484 | **怎么**高效训练同一套 delta rule |
| [`../gated-deltanet/`](../gated-deltanet/) | 2412.06464 | 再加标量遗忘门 α |
| [`../kda/`](../kda/) | 2510.26692 | 通道级 Diag(α) + 混合架构 |

## 从 Linear Attention 过来差在哪？

1. Linear Attention 的固定状态 \(W\) = 联想记忆（FWP）  
2. 加法写入在 \(L > d_{\mathrm{dot}}\) 时必然串扰  
3. 因此写入要从「只加」升级到「先读 \(\bar v\)，再写 \(\beta(v-\bar v)\)」

导读节把这三步写进了精读页最前面。

## 建议阅读顺序

1. [`../linear-attention/`](../linear-attention/) — 加性固定状态  
2. **本页** — 容量界 + delta 指令  
3. [`../deltanet-parallel/`](../deltanet-parallel/) — WY / 分块并行  
4. [`../gated-deltanet/`](../gated-deltanet/) → [`../kda/`](../kda/)

## 重建页面

```bash
python tools/build_deltanet_page.py
```

相关：[Linear Attention](../linear-attention/) · [并行训练](../deltanet-parallel/) · [Gated DeltaNet](../gated-deltanet/) · [KDA](../kda/)
