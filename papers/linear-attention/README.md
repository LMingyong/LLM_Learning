# Linear Attention

| 字段 | 内容 |
|------|------|
| 论文 | Transformers are RNNs: Fast Autoregressive Transformers with Linear Attention |
| 作者 | Katharopoulos, Vyas, Pappas, Fleuret |
| 出处 | ICML 2020 |
| 链接 | [arXiv:2006.16236](https://arxiv.org/abs/2006.16236) · [官网](https://linear-transformers.com/) |
| 一句话 | 用核特征 + 结合律把自注意力降到 **O(N)**；因果形式下 Transformer = 双状态 RNN。 |

**先读** [`../transformer/`](../transformer/)（稠密 softmax 注意力），再读本页：这里把 \(N\times N\) 换成核特征 + 结合律。

## 怎么读

**[`index.html`](./index.html)** — 浅色**逐段精读**：

- 每段：中文小结 → Original → 译文
- 重点：§3.2 线性化推导、§3.3 因果常数内存、§3.4 RNN 形式
- 末节桥接 DeltaNet / GDN / KDA

上一篇：[原始 Transformer](../transformer/)  
接着读：[DeltaNet 原点](../deltanet/) · [并行训练](../deltanet-parallel/) · [KDA](../kda/)

## 文件

| 文件 | 说明 |
|------|------|
| `index.html` | 逐段精读页 |
| `paper.pdf` | 原文 PDF |

```bash
python3 tools/build_linear_attention_page.py
```

内容数据：`tools/linear_attention_paragraphs.py`
