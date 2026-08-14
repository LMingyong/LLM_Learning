"""Content definitions for sparse / flash attention topic pages."""

from __future__ import annotations

from typing import Any

Para = dict[str, Any]
Sec = dict[str, Any]


def _p(en: str, zh: str, summary: str, terms: list[str] = None, extra: str = "") -> Para:
    return {"en": en, "zh": zh, "summary": summary, "terms": terms or [], "extra": extra}


SPARSE_ATTENTION: dict[str, Any] = {
    "title": "稀疏注意力 · Sparse Attention",
    "nav_title": "Sparse Attention",
    "subtitle": "操作方式 · 主流范式 · 工程落地",
    "hero": "稀疏注意力精读",
    "hero_desc": "先读 papers/transformer（原始 QKV / 多头）。再从「谁和谁算注意力」出发，把 O(L²) 全连接变成可训练、可部署的长上下文方案。",
    "chips": [
        {"label": "核心", "value": "稀疏掩码 / 路由"},
        {"label": "复杂度", "value": "O(L·w) 或 O(L·k)"},
        {"label": "主流", "value": "局部 + 全局 token"},
        {"label": "落地", "value": "块稀疏 + Flash 兼容"},
    ],
    "formula": """标准因果注意力（query t 看所有过去 key s≤t）：
  scores[t,s] = (Q[t]·K[s]) / √d
  Attn[t] = softmax(scores[t,0:t+1]) · V[0:t+1]

稀疏注意力：只在允许集合 S(t) 上算 softmax
  Attn[t] = softmax(scores[t, S(t)]) · V[S(t)]

常见 S(t)：
  ① 滑动窗口 |t-s| ≤ w
  ② 全局 token：s ∈ {sink, CLS, 特殊位}
  ③ 块稀疏：按 block 整块允许
  ④ 学习路由：Top-k key / Top-k block""",
    "sections": [
        {
            "id": "baseline",
            "title": "0. 从全注意力说起",
            "paras": [
                _p(
                    "Standard causal self-attention computes, for each token position t, a weighted sum of all previous value vectors V_s where s ≤ t. The weight comes from softmax over dot-product scores between query Q_t and keys K_s. Complexity is O(L²·d) in sequence length L and O(L²) in memory if you materialize the full attention matrix.",
                    "标准因果自注意力：对每个位置 t，用 Q_t 与所有 s≤t 的 K_s 做 softmax 加权，再对 V_s 求和。时间复杂度 O(L²·d)；若显式存完整注意力矩阵，空间也是 O(L²)。",
                    "全注意力 = 每个 query 与所有合法 key 两两交互。",
                    ["causal attention", "attention matrix"],
                ),
                _p(
                    "In practice, the bottleneck is rarely the FLOPs alone. For long contexts, storing the L×L attention scores or even the KV cache (L·d per layer per head) dominates GPU HBM. Sparse attention attacks the quadratic growth by forbidding most (t,s) pairs before softmax.",
                    "实践中瓶颈不只在算力：长上下文时，L×L 分数矩阵或 KV cache（每层每头 L·d）占满 HBM。稀疏注意力在 softmax 之前就禁止绝大多数 (t,s) 配对。",
                    "稀疏的目标：少算 + 少存，而不是换一种等价的全连接。",
                    ["KV cache", "HBM"],
                ),
            ],
        },
        {
            "id": "what",
            "title": "1. 稀疏注意力在做什么",
            "paras": [
                _p(
                    "Sparse attention means: each query only attends to a subset of keys, encoded by a sparsity pattern or mask M where M[t,s]=1 if allowed and 0 otherwise. Causal models further require s≤t. The output is still softmax-normalized, but only over allowed keys.",
                    "稀疏注意力：每个 query 只关注 key 的一个子集。用掩码 M[t,s]∈{0,1} 表示是否允许（因果模型还要求 s≤t）。输出仍是 softmax，但只在允许的位置上归一化。",
                    "本质 = 改「谁和谁连边」，不是改 softmax 公式本身。",
                    ["sparsity mask", "attention mask"],
                ),
                _p(
                    "Operationally, implementations skip forbidden pairs: either never compute those dot products, or compute blocks and zero out. Modern stacks prefer block-sparse layouts so GPU tensor cores can run dense micro-kernels on each allowed block.",
                    "实现上：禁止的 (t,s) 不算点积，或按块算完再屏蔽。现代实现偏好块稀疏——在允许的块内仍用密集矩阵乘，方便 Tensor Core。",
                    "工程关键：稀疏是「跳过计算」，块稀疏是「稀疏 + 仍像 dense 一样快」。",
                    ["block-sparse", "Tensor Core"],
                ),
                _p(
                    "Three levers practitioners use: (1) pattern design—what pairs are allowed; (2) density—how many keys per query; (3) whether the pattern is fixed at architecture design, learned during training, or chosen per input at inference.",
                    "实践三个旋钮：① 模式设计（允许哪些配对）；② 密度（每个 query 看多少 key）；③ 模式是固定、训练学出，还是推理时按输入动态选。",
                    "固定模式易优化；学习路由更灵活但更贵。",
                    ["sparsity pattern"],
                ),
            ],
        },
        {
            "id": "patterns",
            "title": "2. 主流稀疏模式（怎么连边）",
            "paras": [
                _p(
                    "Sliding window (local attention): each token attends only to the previous w tokens (and itself). Complexity O(L·w). Used in Mistral-style models, StreamingLLM extensions, and as a building block in hybrids. Limitation: information must propagate hop-by-hop across windows.",
                    "滑动窗口（局部注意力）：每个 token 只看前 w 个位置。复杂度 O(L·w)。Mistral 等模型、StreamingLLM 都用到。局限：远距离信息必须逐窗传递。",
                    "最常用、最易与 Flash 类 kernel 结合的模式之一。",
                    ["sliding window", "local attention"],
                    '<div class="pre">窗口 w=3 时 query t 允许 key: [t-3, t-2, t-1, t]</div>',
                ),
                _p(
                    "Global + local hybrid: add a small set of global tokens (e.g. first token, learned sinks) that every position can attend to, plus local windows. Longformer uses local window + global memory tokens; BigBird adds random global blocks. This fixes long-range reach without full L².",
                    "全局 + 局部混合：少数「全局 token」（首位、sink、可学习全局位）对所有位置可见，再加局部窗口。Longformer = 窗口 + 全局记忆；BigBird = 窗口 + 随机全局块。兼顾远距与效率。",
                    "工业界长文本最常见骨架：90% 局部 + 少量全局。",
                    ["Longformer", "BigBird", "attention sink"],
                ),
                _p(
                    "Strided / dilated patterns: attend every r-th token (Sparse Transformer) or use dilated windows. Reduces density further while keeping multi-hop paths. Less common in LLMs today but appears in vision and audio transformers.",
                    "步长 / 空洞模式：每隔 r 个 token 才连边（Sparse Transformer），或空洞窗口。密度更低，靠多跳传递信息。当今 LLM 较少，视觉/语音 Transformer 更多。",
                    "适合归纳偏置强的模态；纯语言 LLM 里已被窗口+全局取代。",
                    ["Sparse Transformer", "dilated attention"],
                ),
                _p(
                    "Block sparse: partition sequence into blocks of size B; allow attention only between certain block pairs (e.g. same block, previous block, global blocks). Complexity O(L·B) or O(#allowed blocks·B²). Easier to map to tiled GPU kernels.",
                    "块稀疏：序列划成长度 B 的块；只允许特定块对之间计算（同块、前一块、全局块等）。复杂度与「允许的块对数 × B²」相关，天然适配分块 GPU kernel。",
                    "与 Flash Attention 的 tiling 哲学一致，是落地首选表示。",
                    ["block sparse"],
                ),
            ],
        },
        {
            "id": "learned",
            "title": "3. 学习式稀疏（谁重要由模型决定）",
            "paras": [
                _p(
                    "Routing / Top-k attention: a router scores candidate keys or blocks and selects top-k per query. Examples: Routing Transformer (k-means buckets), Reformer (LSH hashing), NSA (Native Sparse Attention with hierarchical compression + selection). Training teaches which tokens matter; inference cost scales with k not L.",
                    "路由 / Top-k：路由器给候选 key 或块打分，每 query 只保留 top-k。代表：Routing Transformer（聚类桶）、Reformer（LSH）、NSA（分层压缩+选择）。训练学「看谁」；推理成本随 k 而非 L 增长。",
                    "表达力高，但路由本身有开销；k 与质量权衡。",
                    ["Top-k attention", "NSA", "Reformer"],
                ),
                _p(
                    "Learned block routing: first compress tokens into blocks (mean pool, strided conv, or learned pooling), then attend over block summaries and optionally fine-grained tokens inside selected blocks. This is how many 'sparse long-context' systems keep both recall and speed.",
                    "学习式块路由：先把 token 压成块表示，再在块级做选择，必要时只对入选块内做细粒度注意力。许多「稀疏长上下文」系统用这套兼顾召回与速度。",
                    "两阶段：粗选块 → 细选 token，是 NSA 类方法的核心操作。",
                    ["block routing"],
                ),
                _p(
                    "KV cache sparsification at inference: keep full attention during training but prune cache entries at decode (e.g. keep salient tokens, merge others). Related to H2O, StreamingLLM sinks, SnapKV. This is sparse attention on the memory axis, not always on the FLOP axis during prefill.",
                    "推理期 KV 稀疏：训练仍全注意力，解码时剪 cache（保留重要 token、合并其余）。H2O、StreamingLLM、SnapKV 等。这是「存」上的稀疏，prefill 阶段未必省算力。",
                    "部署向技巧：长对话续写常先从这里省显存。",
                    ["KV cache pruning", "StreamingLLM"],
                ),
            ],
        },
        {
            "id": "ops",
            "title": "4. 操作方式（算子层面怎么走）",
            "paras": [
                _p(
                    "Step 1 — Build mask or index list: for each query row t, store allowed key indices S(t) or a block bitmask. In PyTorch: additive mask with -inf on forbidden positions before softmax.",
                    "步骤 1 — 构造掩码或索引表：为每个 query 记录允许的 key 下标 S(t)，或块级 bitmask。PyTorch 常在 softmax 前对禁止位加 -inf。",
                    "掩码是语义；索引表是高效实现。",
                    ["additive mask"],
                ),
                _p(
                    "Step 2 — Compute scores only for allowed pairs. Naive: still form full QK^T then mask (simple but wastes FLOPs). Better: gather K/V subsets per query, or use block-sparse GEMM libraries (xFormers blocksparse, Triton block mask).",
                    "步骤 2 — 只对允许位置算分数。朴素：仍算完整 QK^T 再 mask（简单但浪费）。更好：按索引 gather K/V，或用块稀疏 GEMM（xFormers、Triton 块掩码）。",
                    "别在 GPU 上算完再扔掉——要跳过乘法。",
                    ["gather", "block-sparse GEMM"],
                ),
                _p(
                    "Step 3 — Softmax over allowed set only. Normalization denominator uses only allowed keys. For causal local window, each row has fixed support size → stable kernels.",
                    "步骤 3 — 仅在允许集合上做 softmax。归一化分母只含合法 key。滑动窗口每行支持集大小固定 → kernel 友好。",
                    "稀疏 softmax 与全连接 softmax 数学形式相同，支持集不同。",
                    ["softmax"],
                ),
                _p(
                    "Step 4 — Weighted sum of V. Same as dense attention but V is restricted to allowed indices. For block sparse, multiply small tile of Q with tile of K, softmax tile, multiply with tile of V, accumulate.",
                    "步骤 4 — 对允许的 V 加权求和。块稀疏下：小块 Q×K → softmax → ×V → 累加，循环块。",
                    "与 Flash Attention 相同：分块 + 在线 softmax（见 Flash 专题）。",
                    ["tiling"],
                ),
                _p(
                    "Backward pass: gradients flow only through allowed edges. Block-sparse frameworks store mask during forward or recompute allowed blocks. Sparsity must be defined before softmax for stable autograd.",
                    "反向：梯度只流经允许的边。实现需在前向保存掩码或重算允许块。稀疏结构须在 softmax 前确定。",
                    "训练稀疏模型时，掩码模式要可微或固定。",
                    ["backward pass"],
                ),
            ],
        },
        {
            "id": "mainstream",
            "title": "5. 主流使用方式（2024–2026 实践）",
            "paras": [
                _p(
                    "Long-context LLM stacks: hybrid layers—most layers use sliding window or linear attention (Mamba, GDN, KDA), a minority use full attention every N layers (e.g. 1 full per 4 local). Sparse pattern is part of architecture, not a runtime flag.",
                    "长上下文 LLM：混合层堆叠——多数层用滑动窗口或线性注意力（Mamba/GDN/KDA），每 N 层插一层全注意力。稀疏模式是架构的一部分，不是运行时开关。",
                    "「3 局部 + 1 全局」是当下最常见工程配方。",
                    ["hybrid attention"],
                ),
                _p(
                    "Hugging Face / PyTorch: `attn_mask` (bool or float), `sliding_window` in model config (Mistral), `local_attention` + `global_tokens` in Longformer. FlashAttention-2 supports `window_size` for fused local attention.",
                    "HF/PyTorch：`attn_mask`；Mistral 的 `sliding_window`；Longformer 的 local+global。FlashAttention-2 支持 `window_size` 融合局部注意力。",
                    "落地优先查：模型 config 是否自带窗口；能否走 Flash 窗口 kernel。",
                    ["Hugging Face", "window_size"],
                ),
                _p(
                    "Inference: PagedAttention (vLLM) organizes KV cache in blocks for batching; sparse attention reduces how many cache blocks each query reads. Prefix caching + sparse patterns can compound savings.",
                    "推理：vLLM 的 PagedAttention 把 KV 分页；稀疏注意力减少每 query 读取的 cache 块数。前缀缓存 + 稀疏可叠加省显存。",
                    "稀疏改变「读 cache 的范围」，分页改变「cache 怎么存」。",
                    ["PagedAttention", "vLLM"],
                ),
                _p(
                    "Training long sequences: sequence parallel + sparse attention avoids all-to-all on full L² activations. Ring attention shards sequence; block-sparse keeps per-device work sub-quadratic. Still need correct mask across shards.",
                    "长序列训练：序列并行 + 稀疏避免 L² 激活的全局交换。Ring Attention 切序列；块稀疏让每卡工作量次二次。跨 shard 掩码必须一致。",
                    "分布式时稀疏掩码要随分片对齐，否则因果性破。",
                    ["sequence parallel", "Ring Attention"],
                ),
            ],
        },
        {
            "id": "tradeoffs",
            "title": "6. 取舍与选型",
            "paras": [
                _p(
                    "Expressivity vs cost: full attention is upper bound; local-only risks losing long-range dependencies; global tokens and periodic full layers restore reach. Learned routing adds capacity but routing FLOPs and memory for candidate scoring.",
                    "表达力 vs 成本：全注意力是上界；纯局部易丢长依赖；全局 token / 周期性全层补回远距。学习路由更强，但路由本身要算力与候选存储。",
                    "没有免费午餐：省 L² 就要接受归纳偏置或路由误差。",
                    [],
                ),
                _p(
                    "When to choose what: fixed window for deployment simplicity; global+local for document QA; learned sparse for very long training with budget for custom kernels; KV pruning for long chat inference without retraining.",
                    "选型：固定窗口 → 部署简单；全局+局部 → 文档 QA；学习稀疏 → 超长训练且能写 kernel；KV 剪枝 → 长对话推理且不重训。",
                    "先问瓶颈是 prefill 算力、decode 显存，还是训练通信。",
                    [],
                ),
            ],
        },
    ],
    "glossary": [
        ("稀疏注意力", "每个 query 只与 key 子集计算注意力，避免完整 L×L 连接。"),
        ("sparsity mask", "掩码 M[t,s]，1 表示允许注意力，0 表示禁止。"),
        ("causal attention", "因果掩码：query 只能看 s≤t 的 key。"),
        ("sliding window", "滑动窗口：只看最近 w 个 token。"),
        ("local attention", "局部注意力，通常指滑动窗口或邻域限制。"),
        ("global token", "全局 token：所有位置都能 attend 的特殊位置（如首位、sink）。"),
        ("attention sink", "少数 token 长期吸引大量注意力质量的现象；常被选为全局位。"),
        ("block sparse", "按块组织的稀疏模式；块内密集、块间稀疏。"),
        ("block-sparse GEMM", "在允许块上执行密集矩阵乘的稀疏实现。"),
        ("Top-k attention", "每个 query 只对分数最高的 k 个 key 做 softmax。"),
        ("routing", "用路由器为 query 选择参与注意力的 key/块。"),
        ("NSA", "Native Sparse Attention：分层压缩 + 块级选择的稀疏注意力方案。"),
        ("Longformer", "局部窗口 + 全局记忆 token 的长序列 Transformer。"),
        ("BigBird", "局部 + 全局 + 随机块稀疏的注意力变体。"),
        ("Reformer", "用 LSH 近似注意力，哈希桶内全连接。"),
        ("Sparse Transformer", "早期固定步长/模式稀疏自注意力。"),
        ("KV cache", "解码时缓存历史 K/V，避免重复计算。"),
        ("KV cache pruning", "推理时丢弃或合并不重要的 cache 条目。"),
        ("StreamingLLM", "用 attention sink 稳定超长流式生成的技术。"),
        ("hybrid attention", "同一模型内混合全注意力、局部、线性等层。"),
        ("PagedAttention", "vLLM 将 KV cache 分页管理以提升批处理效率。"),
        ("window_size", "FlashAttention 等 kernel 的滑动窗口参数。"),
        ("additive mask", "在 logits 上加 -inf 禁止注意力连接。"),
        ("sequence parallel", "把序列维切到多卡并行训练。"),
        ("Ring Attention", "环状传递 KV 块以训练超长序列。"),
        ("Tensor Core", "NVIDIA GPU 上的矩阵乘加速单元；块稀疏为其优化。"),
        ("HBM", "GPU 高带宽显存；注意力大矩阵的主要瓶颈所在。"),
        ("attention matrix", "L×L 的注意力分数或权重矩阵。"),
        ("tiling", "把大矩阵分成小块在 SRAM 中计算。"),
    ],
    "refs": [
        {
            "title": "Attention Is All You Need",
            "why": "原始 Transformer；稀疏路线的前置（QKV / 多头 / O(N²)）。",
            "url": "../transformer/index.html",
            "level": "必读",
        },
        {
            "title": "Longformer: The Long-Document Transformer",
            "why": "全局+局部混合的经典范式；理解「滑动窗口 + 全局 token」操作方式的首选。",
            "url": "https://arxiv.org/abs/2004.05150",
            "level": "必读",
        },
        {
            "title": "Big Bird: Transformers for Longer Sequences",
            "why": "块稀疏 + 随机全局；理论连通性与工程块掩码。",
            "url": "https://arxiv.org/abs/2007.14062",
            "level": "必读",
        },
        {
            "title": "Generating Long Sequences with Sparse Transformers",
            "why": "早期固定稀疏模式（步长、局部块）与多跳传递直觉。",
            "url": "https://arxiv.org/abs/1904.10509",
            "level": "重点",
        },
        {
            "title": "Reformer: The Efficient Transformer",
            "why": "LSH 路由式稀疏；学习式「选桶」与近似注意力。",
            "url": "https://arxiv.org/abs/2001.04451",
            "level": "重点",
        },
        {
            "title": "Efficient Streaming Language Models with Attention Sinks",
            "why": "推理侧 KV / 全局 sink；长对话部署必读。",
            "url": "https://arxiv.org/abs/2309.17453",
            "level": "重点",
        },
        {
            "title": "Native Sparse Attention (NSA)",
            "why": "2025 前后学习式块稀疏长上下文代表；粗选+细选操作范式。",
            "url": "https://arxiv.org/abs/2502.11089",
            "level": "扩展",
        },
    ],
    "related": {
        "label": "Flash Attention 专题",
        "href": "../flash-attention/index.html",
    },
}


FLASH_ATTENTION: dict[str, Any] = {
    "title": "Flash Attention · 闪存注意力",
    "nav_title": "Flash Attention",
    "subtitle": "IO 感知 · 分块 · 在线 Softmax",
    "hero": "Flash Attention 精读",
    "hero_desc": "Flash 不是新的注意力公式，而是把标准注意力写成 GPU 内存层次友好的分块算法，避免物化 L×L 矩阵。",
    "chips": [
        {"label": "核心", "value": "SRAM 分块 + 在线 softmax"},
        {"label": "收益", "value": "省 HBM 读写"},
        {"label": "版本", "value": "FA-1 / FA-2 / FA-3"},
        {"label": "关系", "value": "可与稀疏掩码结合"},
    ],
    "formula": """朴素实现（慢在哪）：
  S = Q K^T / √d          # 写出 L×L 到 HBM  ← 巨大读写
  P = softmax(S)          # 再读一遍 S
  O = P V                 # 再读 P

Flash Attention 思想：
  把 Q,K,V 切成小块 (tile)，在 SRAM 里完成：
    局部 QK^T → 在线 softmax 统计量 (m, l) → 累加 PV
  永不存完整 L×L 的 S 或 P

在线 softmax（单 query 行，分块键 K^(1), K^(2), ...）：
  维护 running max m 与 sum l
  每来一块：更新 m,l，并重缩放已有输出累加器""",
    "sections": [
        {
            "id": "problem",
            "title": "0. 为什么需要 Flash Attention",
            "paras": [
                _p(
                    "Naive attention on GPU: load Q,K from HBM, compute S=QK^T (writes L×L to HBM), read S for softmax, write P, read P and V for output. Attention is memory-bound: FLOPs are cheap relative to HBM traffic. The L×L intermediate dominates memory for long L.",
                    "朴素 GPU 注意力：Q,K 从 HBM 加载，算 S=QK^T 并写回 HBM（L×L），再读 S 做 softmax 得 P，再读 P 和 V。注意力是内存瓶颈：FLOP 便宜，HBM 往返昂贵。L 大时 L×L 中间矩阵是噩梦。",
                    "问题不在公式，而在「算子怎么搬数据」。",
                    ["HBM", "memory-bound"],
                ),
                _p(
                    "GPU hierarchy: HBM is large but slow; on-chip SRAM (shared memory / L1) is tiny but fast. Standard kernels don't fuse the attention pipeline, so intermediates spill to HBM repeatedly. Flash Attention is an IO-aware algorithm: minimize HBM reads/writes, not just FLOPs.",
                    "GPU 层次：HBM 大但慢；片上 SRAM 小但快。普通 kernel 不融合注意力流水线，中间结果反复落 HBM。Flash 是 IO 感知算法：最小化 HBM 读写，而非只减 FLOP。",
                    "Flash = 算法 + 实现，针对内存墙而非改数学。",
                    ["SRAM", "IO-aware"],
                ),
            ],
        },
        {
            "id": "naive",
            "title": "1. 朴素注意力在硬件上怎么走",
            "paras": [
                _p(
                    "For one head, shapes: Q,K,V ∈ R^{L×d}. Step A: GEMM QK^T costs O(L²d) FLOPs and produces L² elements. Step B: softmax rows of S. Step C: GEMM PV. Each step touches HBM-sized tensors. Total HBM traffic scales with L² for S and P, even though final output is only L×d.",
                    "单头：Q,K,V 为 L×d。A：QK^T 产生 L² 元素；B：行 softmax；C：P×V。每步都碰 HBM 级张量。HBM 流量随 L² 增长，而最终输出只有 L×d。",
                    "L² 中间量是「隐形杀手」——训练反传还要再来一遍。",
                    ["GEMM"],
                ),
                _p(
                    "Training backward needs S or P (or recomputation). Materializing S costs O(L²) memory per head per layer, limiting batch and context. Flash's forward never forms full S/P in HBM; backward recomputes blocks on the fly from Q,K,V stored tiles.",
                    "训练反向需要 S 或 P（或重算）。存 S 每层每头 O(L²) 限制 batch 与上下文。Flash 前向不在 HBM 存完整 S/P；反向用 Q,K,V 分块重算。",
                    "省显存使更长上下文、更大 batch 成为可能——这是最大工程价值。",
                    ["recomputation"],
                ),
            ],
        },
        {
            "id": "online",
            "title": "2. 在线 Softmax（Flash 的数学核心）",
            "paras": [
                _p(
                    "Softmax for row vector x split into chunks x^(1), x^(2), ... Cannot compute max and sum globally before seeing all chunks. Online algorithm maintains running max m and running sum of exponentials l. When a new chunk arrives, update m_new = max(m_old, max(x^(chunk))), rescale previous accumulator, add new contributions.",
                    "行 softmax 分块时，不能先看完全部再归一化。在线算法维护 running max m 与 exp 之和 l。新块到来：m_new=max(m_old, max(chunk))，重缩放旧累加器，加入新块贡献。",
                    "分块算注意力必须在线 softmax，否则数学不等价。",
                    ["online softmax"],
                ),
                _p(
                    "For attention output O = softmax(S)V, similarly accumulate weighted V with rescaling when m increases. Milakov & Gimelshein (2018) and FlashAttention cite this for stable fused softmax. Result is bitwise-exact to standard softmax (up to floating order).",
                    "输出 O=softmax(S)V 同样用重缩放累加 V。与标准 softmax 数值等价（浮点顺序内精确）。Flash 把它嵌进 attention 循环。",
                    "这是 Flash 能「分块还不改结果」的理论保证。",
                    ["online softmax"],
                    """<div class="pre">新块 j：m_j = max(m_{j-1}, max(S^(j)))
l_j = e^{m_{j-1}-m_j} l_{j-1} + sum(e^{S^(j)-m_j})
O_j = e^{m_{j-1}-m_j} O_{j-1} + e^{S^(j)-m_j} V^(j)</div>""",
                ),
            ],
        },
        {
            "id": "fa1",
            "title": "3. FlashAttention-1 怎么做",
            "paras": [
                _p(
                    "Tiling: choose block sizes B_c (keys), B_r (queries) fitting SRAM. Outer loop over query blocks; inner loop over key blocks. Load tile Q_r, K_c, V_c to SRAM, compute S_rc = Q_r K_c^T, apply online softmax update to output accumulator O_r, without writing S_rc to HBM.",
                    "分块：选 B_c（key 块）、B_r（query 块）放进 SRAM。外循环 query 块，内循环 key 块。载入 Q_r,K_c,V_c，算 S_rc=Q_r K_c^T，在线更新 O_r，不写 S_rc 到 HBM。",
                    "FA-1 伪代码结构：外 Q 内 K，片上完成 softmax+乘 V。",
                    ["tiling", "SRAM"],
                ),
                _p(
                    "Causal masking: for block where query index < key index, skip or mask inside tile before softmax. Same tiling works with local window: skip key tiles outside window without loading them.",
                    "因果掩码：query 块在 key 块「未来」则跳过或在块内 mask。滑动窗口同理：窗口外的 key 块不加载。",
                    "稀疏模式与 Flash 结合点：少加载块 = 少 HBM。",
                    ["causal masking", "sliding window"],
                ),
                _p(
                    "FlashAttention-1 contribution: prove IO complexity drops from Ω(L²) HBM accesses for naive to O(L²·d²/M) where M is SRAM size—when d²<M, sub-quadratic in HBM traffic sense. Delivered 2–4× wall-clock speedups on A100 for typical LLM shapes.",
                    "FA-1 理论：HBM 访问从 Ω(L²) 降到 O(L²d²/M)。A100 上典型 LLM 形状 2–4× 加速，且显存大幅下降。",
                    "第一次把「注意力=融合 kernel」做成标准件。",
                    ["FlashAttention-1"],
                ),
            ],
        },
        {
            "id": "fa2",
            "title": "4. FlashAttention-2 优化了什么",
            "paras": [
                _p(
                    "FA-2 improves work partitioning: fewer non-matmul ops, better warp occupancy, sequence-parallel within a block (split Q processing across warps). Reorders loops to reduce idle warps. Keeps same IO analysis but higher FLOP utilization—often ~2× over FA-1.",
                    "FA-2：更好工作划分，减少非 matmul 操作，提高 warp 占用；块内序列并行。循环重排减少空转。IO 分析同类，FLOP 利用率更高，常比 FA-1 再快约 2×。",
                    "FA-2 是今天 HF/vLLM 默认后端的常见版本。",
                    ["FlashAttention-2", "warp"],
                ),
                _p(
                    "Supports head dimension up to 256, multi-query attention variants, sliding window (`window_size`), ALiBi, dropout in kernel. Backward pass also tiled with recomputation—no L×L stash. Interface: `flash_attn_func(q,k,v, causal=True, window_size=(-1,-1))`.",
                    "支持 head_dim≤256、滑动窗口 window_size、ALiBi、dropout。反向同样分块重算。接口如 flash_attn_func(..., causal=True, window_size=(w,w))。",
                    "部署时查：causal 与 window 参数是否与模型一致。",
                    ["window_size", "ALiBi"],
                ),
            ],
        },
        {
            "id": "fa3",
            "title": "5. FlashAttention-3 与前沿",
            "paras": [
                _p(
                    "FlashAttention-3 targets Hopper (H100): exploits Tensor Memory Accelerator (TMA), warp-specialized pipelining, FP8 low-precision paths. Asynchronous data movement overlaps GEMM with softmax. Focus on very large heads and datacenter inference/training throughput.",
                    "FA-3 面向 Hopper：TMA、warp 专业化流水线、FP8。异步搬数据与 GEMM/softmax 重叠。面向大 head、数据中心吞吐。",
                    "新硬件特性 → 新 kernel；算法骨架仍是在线 softmax + tiling。",
                    ["FlashAttention-3", "FP8", "TMA"],
                ),
                _p(
                    "Ecosystem: FlashAttention-2/3 in PyTorch SDPA backend, HuggingFace `attn_implementation='flash_attention_2'`, vLLM, Megatron-LM. PagedAttention (vLLM) is orthogonal—memory layout for KV cache; Flash is compute kernel. Often used together.",
                    "生态：PyTorch SDPA、HF flash_attention_2、vLLM、Megatron。PagedAttention 管 KV 怎么存；Flash 管注意力怎么算。常一起用。",
                    "Flash 解决算子；PagedAttention 解决 batch 调度。",
                    ["SDPA", "PagedAttention"],
                ),
            ],
        },
        {
            "id": "algo",
            "title": "6. 完整前向流程（逐步）",
            "paras": [
                _p(
                    "Input: Q,K,V on HBM. Choose tiles Br×Bc. For each query tile i: initialize online stats (m_i, l_i, O_i) in SRAM. For each key tile j (causal: j≤i): load K_j,V_j; compute S_ij=Q_i K_j^T; apply mask; online_softmax_update(S_ij, V_j → O_i, m_i, l_i). After all j, write O_i to HBM.",
                    "输入 Q,K,V 在 HBM。对每个 query 块 i：初始化 m,l,O。对每个合法 key 块 j：加载 K_j,V_j；S_ij=Q_iK_j^T；mask；在线更新 O_i。完成后写 O_i。",
                    "整段注意力一次 kernel 调用完成，无 L×L 落盘。",
                    ["forward pass"],
                    '<div class="flow"><ol><li>选块大小 Br,Bc（受 SRAM 限制）</li><li>外循环：query 块 i</li><li>内循环：key 块 j（因果/窗口过滤）</li><li>片上：S_ij = Q_i K_j^T → mask → online softmax → 累加 O_i</li><li>写出 O_i</li></ol></div>',
                ),
                _p(
                    "Backward: recompute S_ij per tile during backward pass (or store minimal stats). Gradients dQ,dK,dV accumulated tile-wise. Recomputation trades extra compute for memory—favorable on modern GPUs.",
                    "反向：按块重算 S_ij（或存少量统计量），分块累加 dQ,dK,dV。用额外计算换显存——在 GPU 上通常划算。",
                    "训练能跑更长序列，主要靠这套重算哲学。",
                    ["backward pass"],
                ),
            ],
        },
        {
            "id": "decode",
            "title": "7. 推理场景：Prefill 与 Decode",
            "paras": [
                _p(
                    "Prefill (many queries at once): FlashAttention shines—large matmuls, high parallelism, tiling amortizes overhead. This is the main training and long-prompt inference path.",
                    "Prefill（一次很多 query）：Flash 最强——大矩阵乘、并行度高、分块摊销开销。训练与长 prompt 推理主战场。",
                    "长上下文 prefill 省 HBM 最明显。",
                    ["prefill"],
                ),
                _p(
                    "Decode (one new token per step): sequence length of Q is 1; kernel becomes memory-latency sensitive. FlashAttention with KV cache reads full history K,V each step—still O(L) per layer. FlashDecoding / split-K variants batch across heads and sequence chunks to improve occupancy.",
                    "Decode（每步 1 个新 token）：Q 长度 1，受延迟与 KV 读取影响。每步仍要读全长 K,V——每层 O(L)。FlashDecoding 等通过分 head、分 K 块提高占用率。",
                    "Decode 瓶颈常在 KV cache 带宽，不是 softmax 本身。",
                    ["decode", "FlashDecoding", "KV cache"],
                ),
            ],
        },
        {
            "id": "sparse",
            "title": "8. 与稀疏注意力的关系",
            "paras": [
                _p(
                    "FlashAttention does not require dense attention—it skips loading key tiles that are fully masked (causal future, outside sliding window, block-sparse forbidden blocks). Sparse pattern reduces inner loop iterations and HBM loads.",
                    "Flash 不要求全连接：完全被 mask 的 key 块可不加载（未来位、窗口外、块稀疏禁止块）。稀疏让内循环更短、HBM 更少。",
                    "稀疏定义「算哪些块」；Flash 定义「块怎么在片上算」。",
                    ["block-sparse"],
                ),
                _p(
                    "Block-sparse Flash: bitmask over (query_block, key_block) pairs. Inside allowed blocks, run standard Flash tile kernel. NSA-style hierarchical sparse can use Flash for dense sub-blocks after routing selects them.",
                    "块稀疏 Flash：对 (query块,key块) 用 bitmask。允许块内走标准 Flash tile。NSA 路由选中区域后再用 Flash 做密集子块。",
                    "长上下文 SOTA 常是「稀疏路由 + Flash 密集子算子」。",
                    ["NSA"],
                ),
            ],
        },
        {
            "id": "when",
            "title": "9. 何时真的更快",
            "paras": [
                _p(
                    "Flash wins when: long L, moderate d, GPU with limited HBM bandwidth (A100/H100), training with activation checkpointing. Less dramatic for very small L (kernel launch overhead) or when already using highly fused cuBLAS paths on tiny sequences.",
                    "Flash 赢在长 L、适中 d、HBM 带宽受限、训练要 checkpoint。短序列优势小（启动开销）。",
                    "不是魔法：短 prompt、极小 batch 未必快很多。",
                    [],
                ),
                _p(
                    "Checklist: (1) `torch.backends.cuda.enable_flash_sdp(True)` or explicit flash_attn; (2) dtype fp16/bf16; (3) head_dim supported; (4) causal flag matches model; (5) for local models set window_size; (6) fallback to SDPA/math if head size or mask type unsupported.",
                    "检查清单：启用 flash SDPA 或 flash_attn；fp16/bf16；head_dim 合法；causal 一致；局部模型设 window_size；不支持则回退 math。",
                    "落地先跑通 fallback，再查 kernel 是否真被调用。",
                    ["SDPA"],
                ),
            ],
        },
    ],
    "glossary": [
        ("Flash Attention", "IO 感知的分块注意力实现，避免物化 L×L 矩阵。"),
        ("HBM", "GPU 高带宽显存，容量大、延迟高，注意力瓶颈常在此。"),
        ("SRAM", "片上高速存储（共享内存/L1），Flash 分块目标所在地。"),
        ("IO-aware", "算法设计以最小化内存读写为目标，而非最小 FLOP。"),
        ("memory-bound", "算子耗时受内存带宽限制，而非计算单元饱和。"),
        ("tiling", "把大矩阵切成小块以适应 SRAM 并减少 HBM 往返。"),
        ("online softmax", "分块计算 softmax 时在线维护 max 与 sum 的技巧。"),
        ("GEMM", "通用矩阵乘，QK^T 与 PV 都是 GEMM。"),
        ("recomputation", "反向时不存中间激活，前向时重算以省显存。"),
        ("FlashAttention-1", "首版 Flash：证明 IO 复杂度并给出分块前向。"),
        ("FlashAttention-2", "改进并行与循环顺序，更高 GPU 利用率。"),
        ("FlashAttention-3", "Hopper 架构、TMA、FP8 等硬件特化版本。"),
        ("warp", "GPU 上 32 线程的执行组；占用率影响速度。"),
        ("causal masking", "禁止 query 看未来 key 的掩码。"),
        ("sliding window", "FlashAttention-2 的 window_size 局部注意力参数。"),
        ("window_size", "滑动窗口半径；(-1,-1) 表示全注意力。"),
        ("prefill", "推理时一次性处理输入 prompt 的阶段。"),
        ("decode", "自回归逐 token 生成阶段。"),
        ("FlashDecoding", "优化 decode 阶段 KV 读取的 Flash 变体。"),
        ("KV cache", "解码缓存历史 K/V。"),
        ("PagedAttention", "vLLM KV 分页；与 Flash 计算互补。"),
        ("SDPA", "PyTorch scaled_dot_product_attention，可后端到 Flash。"),
        ("TMA", "Hopper Tensor Memory Accelerator，异步大块传输。"),
        ("FP8", "8 位浮点；FA-3 低精度路径。"),
        ("block-sparse", "块级稀疏；与 Flash 块循环天然契合。"),
        ("forward pass", "前向计算。"),
        ("backward pass", "反向传播。"),
        ("ALiBi", "注意力线性偏置位置编码；Flash kernel 可选支持。"),
        ("NSA", "可与 Flash 子块组合的学习式稀疏注意力。"),
    ],
    "refs": [
        {
            "title": "FlashAttention: Fast and Memory-Efficient Exact Attention (FA-1)",
            "why": "原始论文：IO 模型、在线 softmax、分块前向；理解 Flash 的必读。",
            "url": "https://arxiv.org/abs/2205.14135",
            "level": "必读",
        },
        {
            "title": "FlashAttention-2: Faster Attention with Better Parallelism",
            "why": "工程主流版本；并行策略与 window_size 等接口。",
            "url": "https://arxiv.org/abs/2307.08621",
            "level": "必读",
        },
        {
            "title": "FlashAttention-3: Fast and Accurate Attention with FP8 (Hopper)",
            "why": "H100 路径、TMA、FP8；硬件演进后的 kernel 设计。",
            "url": "https://arxiv.org/abs/2407.08608",
            "level": "重点",
        },
        {
            "title": "Online normalizer calculation for softmax",
            "why": "在线 softmax 数值技巧的来源之一。",
            "url": "https://arxiv.org/abs/1805.02867",
            "level": "重点",
        },
        {
            "title": "Efficient Streaming Language Models with Attention Sinks",
            "why": "理解 decode 阶段 KV 与 sink；与 Flash decode 优化对照。",
            "url": "https://arxiv.org/abs/2309.17453",
            "level": "扩展",
        },
        {
            "title": "PagedAttention (vLLM paper)",
            "why": "KV 内存管理；与 Flash 计算层配合构成推理栈。",
            "url": "https://arxiv.org/abs/2309.06180",
            "level": "扩展",
        },
    ],
    "related": {
        "label": "Sparse Attention 专题",
        "href": "../sparse-attention/index.html",
    },
}
