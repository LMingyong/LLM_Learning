# Topics 专题精读

与 `papers/`（单篇论文）并列：`topics/` 放**跨论文的技术专题**。

```text
topics/<topic-slug>/
  README.md
  index.html    # 交互式精读：对照翻译 + 段末小结 + 名词 + 引用
```

## 已收录

| 文件夹 | 说明 |
|--------|------|
| [sparse-attention](./sparse-attention/) | 稀疏注意力：操作方式、主流范式、工程落地 |
| [flash-attention](./flash-attention/) | Flash Attention：分块、在线 softmax、FA-1/2/3 |

生成 HTML：`python3 tools/build_topic_html.py`
