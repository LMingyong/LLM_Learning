"""Fine-grained DeltaNet / Delta Attention paragraphs.

Paper: Parallelizing Linear Transformers with the Delta Rule over Sequence Length
arXiv:2406.06484 (Yang, Wang, Zhang, Shen, Kim — NeurIPS 2024).

Focus: Abstract, Intro motivation, §2.1–2.2 linear→delta rule, §3 chunkwise
parallelism (WY / Householder), architecture & hybrids, key experiments.
"""

FORMULA_WALL = [
    {
        "tag": "Linear · 加性更新",
        "latex": r"S_t = S_{t-1} + v_t k_t^\top,\quad o_t = S_t q_t",
        "note": "只加不改；L>d 时易发生 key 碰撞。",
    },
    {
        "tag": "DeltaNet · 递推形式",
        "latex": r"S_t = S_{t-1}(I-\beta_t k_t k_t^\top)+\beta_t v_t k_t^\top",
        "note": "广义 Householder：先擦旧再写新。",
        "wide": True,
    },
    {
        "tag": "写入强度",
        "latex": r"\beta_t=\sigma(W_\beta x_t)\in(0,1)",
        "note": "β=1 完全覆盖；β=0 记忆不变。",
    },
    {
        "tag": "伪 value（WY 视角）",
        "latex": r"u_t=\beta_t\bigl(v_t-S_{t-1}k_t\bigr),\quad S_t=\sum_{i=1}^{t} u_i k_i^\top",
        "note": "DeltaNet = 线性注意力，但 value 换成纠错后的 u。",
        "wide": True,
    },
]

SECTIONS = [
    {
        "id": "abstract",
        "title": "Abstract 摘要",
        "paras": [
            {
                "en": "Transformers with linear attention and state-space models have been suggested as linear-time alternatives to softmax attention, but still underperform especially on in-context retrieval.",
                "zh": "线性注意力 Transformer 与状态空间模型被当作 softmax 注意力的线性时间替代，但在上下文检索上仍明显偏弱。",
                "summary": "问题：线性时间模型，检索仍跟不上全注意力。",
                "terms": ["linear attention", "in-context retrieval"],
            },
            {
                "en": "More expressive variants that replace the additive outer-product update with the delta rule (DeltaNet) are better at associative recall, yet prior training algorithms did not parallelize over sequence length and were inefficient on modern hardware.",
                "zh": "把加性外积更新换成 delta rule 的变体（DeltaNet）更擅长联想回忆，但以往训练算法无法沿序列长度并行，硬件效率差。",
                "summary": "矛盾：表达力有了，训练却串行。",
                "terms": ["DeltaNet", "delta rule"],
            },
            {
                "en": "This work gives a hardware-efficient algorithm for training linear transformers with the delta rule via a memory-efficient representation of products of Householder matrices, enabling scaling DeltaNet to standard LM settings.",
                "zh": "本文给出硬件友好的 delta-rule 线性注意力训练算法：用 Householder 乘积的省内存表示，使 DeltaNet 能扩到常规语言模型设定。",
                "summary": "贡献一句话：把 DeltaNet 训到能上卡、能扩规模。",
                "terms": ["Householder", "WY representation"],
            },
            {
                "en": "A 1.3B model trained on 100B tokens outperforms Mamba and GLA on perplexity and zero-shot downstream (including recall). Hybrids with sliding-window or two global attention layers beat strong transformer baselines.",
                "zh": "1.3B / 100B tokens 设定下，困惑度与零样本下游（含回忆）优于 Mamba 与 GLA；与滑窗或两层全局注意力的混合还超过强 Transformer 基线。",
                "summary": "结果数字：1.3B·100B；纯 DeltaNet 打赢线性族，混合打赢 Transformer。",
                "terms": ["Mamba", "GLA", "hybrid"],
            },
        ],
    },
    {
        "id": "intro",
        "title": "1 Introduction 引言（关键）",
        "paras": [
            {
                "en": "Softmax attention is accurate and matmul-friendly, but quadratic in length and requires a growing KV cache. Linear attention rearranges into a matrix-valued RNN for constant-memory inference, yet historically lagged on language modeling until gated variants narrowed the gap.",
                "zh": "Softmax 注意力准且吃 matmul，但长度二次且 KV cache 增长。线性注意力可重排成矩阵值 RNN 做常数内存推理，历史上语言模型偏弱，直到门控变体缩小差距。",
                "summary": "场景：要线性时间，又要检索——两者一直难兼得。",
                "terms": ["KV cache", "linear attention"],
            },
            {
                "en": "Gated linear transformers and time-varying SSMs (e.g. Mamba) remain weak on recall-intensive tasks. Schlag et al. proposed DeltaNet: retrieve the value bound to the current key and update it with a delta-rule correction—effective on synthetic/small LM, but trained sequentially.",
                "zh": "门控线性模型与时变 SSM（如 Mamba）在回忆密集型任务仍弱。Schlag 等提出 DeltaNet：用当前 key 取回绑定 value，再按 delta rule 纠错——合成/小模型有效，但训练是串行的。",
                "summary": "前作 DeltaNet：语义对了，算法还没法大规模训。",
                "terms": ["DeltaNet", "associative recall"],
            },
            {
                "en": "We reparameterize DeltaNet as a matrix RNN with generalized Householder transitions, apply the WY representation so chunkwise parallel linear-attention training extends to DeltaNet, and scale to 1.3B / 100B tokens plus hybrid designs.",
                "zh": "我们把 DeltaNet 重参数化为广义 Householder 转移的矩阵 RNN，用 WY 表示把分块并行线性注意力训练推广到 DeltaNet，并扩到 1.3B/100B tokens 及混合设计。",
                "summary": "本文路径：Householder → WY → chunk 并行 → 规模化 + 混合。",
                "terms": ["chunkwise", "WY representation"],
            },
        ],
    },
    {
        "id": "linear",
        "title": "2.1 线性注意力回顾",
        "paras": [
            {
                "en": "Linear attention replaces the exp kernel with a feature-map dot product, enabling a recurrent state S_t that accumulates key–value associations without a KV cache.",
                "zh": "线性注意力用特征映射点积替换 exp 核，得到累积 KV 关联的递推状态 S_t，无需 KV cache。",
                "summary": "固定大小状态 = 线性时间推理的前提。",
                "terms": ["feature map", "S"],
                "formulas": [
                    {
                        "tag": "简化线性注意力",
                        "latex": r"S_t=S_{t-1}+v_t k_t^\top,\quad o_t=S_t q_t",
                        "note": "φ 常取恒等；分母归一化多项工作会去掉。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Fully parallel form is O(L²d) matmul-heavy; pure recurrence is O(Ld²) but low arithmetic intensity. Chunkwise parallel form interpolates: propagate S chunk-to-chunk, keep intra-chunk parallel.",
                "zh": "全并行形式 O(L²d)、吃 matmul；纯递推 O(Ld²) 但算术强度低。分块并行折中：块间传 S，块内并行。",
                "summary": "训练工程母题：块大小 C 在并行度与 FLOPs 之间插值。",
                "terms": ["chunkwise"],
                "formulas": [
                    {
                        "tag": "块间状态 / 块内输出（线性）",
                        "latex": r"S_{[t+1]}=S_{[t]}+V_{[t+1]}^\top K_{[t+1]},\quad O_{[t+1]}=Q_{[t+1]}S_{[t]}^\top+(Q_{[t+1]}K_{[t+1]}^\top\odot M_C)V_{[t+1]}",
                        "wide": True,
                    },
                ],
            },
        ],
    },
    {
        "id": "delta",
        "title": "2.2 DeltaNet：delta 更新规则",
        "paras": [
            {
                "en": "Pure additive updates cannot deallocate old associations; when L>d keys collide. DeltaNet retrieves the old value bound to the current key, mixes it with the new value by writing strength β_t, then removes-and-writes.",
                "zh": "纯加性更新无法腾出旧关联；L>d 时 key 碰撞。DeltaNet 用当前 key 取回旧 value，按写入强度 β_t 与新 value 插值，再「擦旧+写新」。",
                "summary": "核心直觉：按地址纠错，而不是无脑累加。",
                "terms": ["delta rule", "β", "associative recall"],
                "figure": "delta_steps",
                "formulas": [
                    {
                        "tag": "读旧 / 混合新",
                        "latex": r"v_t^{\mathrm{old}}=S_{t-1}k_t,\quad v_t^{\mathrm{new}}=\beta_t v_t+(1-\beta_t)v_t^{\mathrm{old}}",
                        "wide": True,
                    },
                    {
                        "tag": "擦写更新",
                        "latex": r"S_t=S_{t-1}-\underbrace{v_t^{\mathrm{old}}k_t^\top}_{\mathrm{remove}}+\underbrace{v_t^{\mathrm{new}}k_t^\top}_{\mathrm{write}}",
                        "wide": True,
                    },
                    {
                        "tag": "紧凑递推",
                        "latex": r"S_t=S_{t-1}(I-\beta_t k_t k_t^\top)+\beta_t v_t k_t^\top",
                        "note": "与后文 Householder / WY 推导同一式。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "β_t=σ(W_β x_t)∈(0,1) is writing strength: β=1 fully replaces the binding; β=0 leaves memory unchanged. Output is still o_t=S_t q_t; recurrent cost matches vanilla linear attention O(Ld²).",
                "zh": "β_t=σ(W_β x_t)∈(0,1) 是写入强度：β=1 完全替换绑定；β=0 记忆不动。输出仍是 o_t=S_t q_t；递推代价与普通线性注意力同为 O(Ld²)。",
                "summary": "多出来的几乎只有一个标量门 β。",
                "terms": ["β"],
                "formulas": [
                    {
                        "tag": "写入强度",
                        "latex": r"\beta_t=\sigma(W_\beta x_t)\in(0,1)",
                    },
                ],
            },
        ],
    },
    {
        "id": "parallel",
        "title": "3 沿序列并行：WY / 分块",
        "paras": [
            {
                "en": "S_t admits an additive form Σ u_i k_iᵀ with pseudo-values u_i=β_i(v_i−v_i^{old}). After building U, the rest is ordinary linear attention. Naively forming u_t needs materializing S_{t−1}.",
                "zh": "S_t 可写成 Σ u_i k_iᵀ，伪 value u_i=β_i(v_i−v_i^{old})。构造完 U 后其余同普通线性注意力。朴素算 u_t 却要物化 S_{t−1}。",
                "summary": "观察：DeltaNet ≈ 换了 value 的线性注意力。",
                "terms": ["u", "WY representation"],
                "formulas": [
                    {
                        "tag": "伪 value",
                        "latex": r"u_t=\beta_t(v_t-S_{t-1}k_t),\quad S_t=\sum_{i=1}^{t}u_i k_i^\top",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Using the WY representation for products of Householder matrices, u_t can be computed in O(d) memory without materializing S. Chunkwise matrices U and W then unlock the same chunk-to-chunk parallel schedule as linear attention.",
                "zh": "借助 Householder 乘积的 WY 表示，可在 O(d) 内存算 u_t 而不物化 S。再构造分块矩阵 U、W，即可沿用线性注意力的块间并行日程。",
                "summary": "算法关键：省内存表示 → 才能把 chunk 并行搬过来。",
                "terms": ["Householder", "chunkwise", "WY representation"],
                "figure": "chunk",
                "formulas": [
                    {
                        "tag": "块间更新（示意）",
                        "latex": r"S_{[t+1]}=S_{[t]}+(U_{[t+1]}-W_{[t+1]}S_{[t]}^\top)^\top K_{[t+1]}",
                        "wide": True,
                    },
                    {
                        "tag": "块内输出（示意）",
                        "latex": r"O_{[t+1]}=Q_{[t+1]}S_{[t]}^\top+(Q_{[t+1]}K_{[t+1]}^\top\odot M)(U_{[t+1]}-W_{[t+1]}S_{[t]}^\top)",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "On H100, the chunkwise kernel is substantially faster than recurrence (e.g. ~5.5×–13× across lengths/head dims in Table 1); speedups grow with L and d_head.",
                "zh": "H100 上分块核相对递推明显加速（表 1：约 5.5×–13×，随 L 与 d_head 增大更明显）。",
                "summary": "工程证据：不是纸上并行，卡上真更快。",
                "terms": ["FlashLinearAttention"],
            },
        ],
    },
    {
        "id": "arch",
        "title": "3.3–3.4 架构与混合",
        "paras": [
            {
                "en": "DeltaNet Transformer follows LLaMA-style blocks, swapping self-attention for DeltaNet. Keys/queries use SiLU then L2-normalization (stable Householder eigenvalues; L2 makes I−kkᵀ a true projection).",
                "zh": "DeltaNet Transformer 沿用 LLaMA 式块，自注意力换成 DeltaNet。q/k 用 SiLU 再 L2 归一化（稳住 Householder 特征值；L2 使 I−kkᵀ 成为真正投影）。",
                "summary": "实现细节：SiLU + L2Norm，而不是早期的 ELU+1 / L1。",
                "terms": ["SiLU", "L2Norm"],
                "formulas": [
                    {
                        "tag": "q / k",
                        "latex": r"k_t=\frac{\mathrm{SiLU}(W_K x_t)}{\|\mathrm{SiLU}(W_K x_t)\|_2},\quad q_t=\frac{\mathrm{SiLU}(W_Q x_t)}{\|\mathrm{SiLU}(W_Q x_t)\|_2}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Practical hybrids: short convolution after QKV; interleave sliding-window MQA; or replace only two layers with global attention. These address local shifts and precise retrieval that pure content-based linear attention lacks.",
                "zh": "实用混合：QKV 后加短卷积；交织滑窗 MQA；或仅两层换成全局注意力。用来补纯内容寻址线性注意力缺少的局部移位与精确检索。",
                "summary": "混合不是投降，是给有限状态记忆配「局部/全局外挂」。",
                "terms": ["hybrid", "sliding window", "short convolution"],
            },
        ],
    },
    {
        "id": "expts",
        "title": "4 实验要点",
        "paras": [
            {
                "en": "Synthetic: on hard MQAR, DeltaNet is perfect even without convolution and beats Mamba in low-dimension settings. RegBench and MAD also show strong recall (esp. Fuzzy / Noisy / Selective Copy), with a weaker Memorize score.",
                "zh": "合成：困难 MQAR 上即便无卷积也满分，低维设定优于 Mamba。RegBench 与 MAD 回忆项强（尤其 Fuzzy/Noisy/Selective Copy），Memorize 偏弱。",
                "summary": "画像：纠错写入擅长「找回来」，不等于全能记忆。",
                "terms": ["MQAR", "RegBench", "MAD"],
            },
            {
                "en": "Language modeling (1.3B / 100B tokens): DeltaNet beats Mamba/GLA/RetNet on perplexity and zero-shot; hybrids with sliding or two global layers further beat Transformer++ on several suites.",
                "zh": "语言建模（1.3B / 100B tokens）：困惑度与零样本上 DeltaNet 优于 Mamba/GLA/RetNet；滑窗或两层全局的混合在多项上进一步超过 Transformer++。",
                "summary": "规模结论：delta rule 可扩；混合往往更强。",
                "terms": ["Transformer++", "hybrid"],
            },
        ],
    },
    {
        "id": "bridge",
        "title": "桥接到 GDN / KDA",
        "paras": [
            {
                "en": "This paper is the scalable DeltaNet (delta attention) baseline: error-correcting writes without a channel-wise forget gate. Gated DeltaNet later adds a scalar decay α; Kimi Delta Attention (KDA) upgrades α to Diag(α) and hybridizes with MLA.",
                "zh": "本文是可扩展的 DeltaNet（delta attention）基线：有纠错写入，尚无通道级遗忘门。随后 Gated DeltaNet 加入标量衰减 α；Kimi Delta Attention（KDA）把 α 升级为 Diag(α)，并与 MLA 混合。",
                "summary": "阅读地图：本文 → GDN → KDA（本仓库 papers/kda/）。",
                "terms": ["Gated DeltaNet", "KDA"],
            },
            {
                "en": "In this repo: read this page’s formulas first; then papers/kda/ for channel-wise gating + teaching code. Do not conflate DeltaNet’s β-only update with KDA’s Diag(α) forget.",
                "zh": "本仓库：先读本页公式；再读 papers/kda/ 看通道门控与教学代码。勿把 DeltaNet 仅含 β 的更新与 KDA 的 Diag(α) 遗忘混为一谈。",
                "summary": "拆夹原因：两篇论文，两套公式。",
                "terms": ["KDA"],
            },
        ],
    },
]

GLOSSARY = [
    ("DeltaNet", "使用 delta rule 更新矩阵状态 S 的线性 Transformer 变体；本文给出可扩展并行训练。"),
    ("delta rule", "按预测误差纠错写入：擦除旧绑定再写入新 value。"),
    ("linear attention", "用特征点积替代 softmax，使注意力可写成固定大小状态递推。"),
    ("β", "写入强度 / 学习率门，控制本次纠错幅度。"),
    ("S", "矩阵值递推状态（联想记忆）。"),
    ("u", "伪 value：β(v−Sold)，使 DeltaNet 外观像换了 V 的线性注意力。"),
    ("Householder", "I−βkkᵀ 一类秩一修正；DeltaNet 转移的代数结构。"),
    ("WY representation", "把一串 Householder 乘积压成紧凑因子，避免物化 d×d 状态。"),
    ("chunkwise", "块间递推状态、块内并行 matmul 的训练日程。"),
    ("associative recall", "上下文中按 key 找回 value 的能力；MQAR 等任务测量。"),
    ("KV cache", "softmax 注意力推理缓存的历史 K/V。"),
    ("MQAR", "Multi-query associative recall 合成任务。"),
    ("RegBench", "基于概率有限自动机的上下文语言学习基准。"),
    ("MAD", "Mechanistic Architecture Design 合成探针套件。"),
    ("Mamba", "选择性状态空间模型基线。"),
    ("GLA", "Gated Linear Attention 基线。"),
    ("RetNet", "带非数据相关指数衰减的线性注意力基线。"),
    ("Transformer++", "LLaMA 风格 Transformer 基线。"),
    ("hybrid", "DeltaNet 与滑窗/全局注意力等混合堆叠。"),
    ("sliding window", "局部滑窗 softmax 注意力。"),
    ("short convolution", "QKV 后的轻量深度卷积。"),
    ("SiLU", "本文 q/k 非线性；相对早期 ELU+1。"),
    ("L2Norm", "对 q/k 的 L2 归一化，稳住并增强投影性质。"),
    ("FlashLinearAttention", "作者开源的线性注意力/DeltaNet 算子库。"),
    ("feature map", "φ：把 q/k 映射到特征空间。"),
    ("in-context retrieval", "依赖当前上下文检索信息的能力。"),
    ("Gated DeltaNet", "在 DeltaNet 上加标量遗忘门 α 的后续工作。"),
    ("KDA", "Kimi Delta Attention：通道级 Diag(α) + delta rule（见 papers/kda/）。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "DeltaNet（并行 delta rule）",
        "why": "逐段精读对象；可扩展 Delta Attention。",
        "url": "./paper.pdf",
        "ext": "https://arxiv.org/abs/2406.06484",
    },
    {
        "level": "下游",
        "title": "Kimi Linear / KDA",
        "why": "通道级遗忘门 + 与 MLA 的 3:1 混合。",
        "url": "../kda/index.html",
        "ext": "https://arxiv.org/abs/2510.26692",
    },
    {
        "level": "相关",
        "title": "Gated DeltaNet",
        "why": "在 DeltaNet 上加标量门 α 的直接后续。",
        "url": "https://arxiv.org/abs/2412.06464",
        "ext": "",
    },
    {
        "level": "前驱",
        "title": "Linear Attention（Transformers are RNNs）",
        "why": "固定大小状态 S 的经典源头。",
        "url": "../linear-attention/index.html",
        "ext": "https://arxiv.org/abs/2006.16236",
    },
    {
        "level": "代码",
        "title": "Flash Linear Attention",
        "why": "官方并行 DeltaNet / 线性注意力算子。",
        "url": "https://github.com/fla-org/flash-linear-attention",
        "ext": "",
    },
]
