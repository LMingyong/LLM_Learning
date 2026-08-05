"""Fine-grained Gated DeltaNet paragraphs.

Paper: Gated Delta Networks: Improving Mamba2 with Delta Rule
arXiv:2412.06464 (Yang, Kautz, Hatamizadeh — ICLR 2025).

Focus: Abstract/Intro complementarity of gate vs delta, §2 prelim,
§3 gated delta rule + online learning view, hybrids, key experiments.
"""

FORMULA_WALL = [
    {
        "tag": "Mamba2 · 标量衰减",
        "latex": r"S_t=\alpha_t S_{t-1}+v_t k_t^\top",
        "note": "全体关联同一比例遗忘；擦除不够定点。",
    },
    {
        "tag": "DeltaNet · 定点擦写",
        "latex": r"S_t=S_{t-1}(I-\beta_t k_t k_t^\top)+\beta_t v_t k_t^\top",
        "note": "按 key 纠错；难快速清空整块记忆。",
        "wide": True,
    },
    {
        "tag": "式 (10) · Gated Delta Rule",
        "latex": r"S_t=S_{t-1}\bigl(\alpha_t(I-\beta_t k_t k_t^\top)\bigr)+\beta_t v_t k_t^\top",
        "note": "α→0 快速清空；α→1 退化为纯 DeltaNet。",
        "wide": True,
    },
    {
        "tag": "读出",
        "latex": r"o_t=S_t q_t",
        "note": "状态大小固定，与序列长度无关。",
    },
]

SECTIONS = [
    {
        "id": "abstract",
        "title": "Abstract 摘要",
        "paras": [
            {
                "en": "Linear Transformers are efficient alternatives to standard Transformers, but retrieval and long-context performance remain limited. Recent work explored two mechanisms: gating for adaptive memory control, and the delta update rule for precise memory modifications.",
                "zh": "线性 Transformer 是标准注意力的高效替代，但检索与长上下文仍受限。近期工作探索两类机制：门控做自适应记忆控制，以及 delta 更新做精确记忆修改。",
                "summary": "两条线：门控管「忘多少」，delta 管「改哪条」。",
                "terms": ["gating", "delta rule", "linear attention"],
            },
            {
                "en": "These mechanisms are complementary: gating enables rapid memory erasure while the delta rule facilitates targeted updates. We introduce the gated delta rule and a parallel training algorithm optimized for modern hardware.",
                "zh": "二者互补：门控擅长快速擦除，delta 擅长定点更新。我们提出 gated delta rule，并给出面向现代硬件的并行训练算法。",
                "summary": "本文公式核心：把 α 和 β 装进同一个递推。",
                "terms": ["gated delta rule"],
            },
            {
                "en": "Gated DeltaNet surpasses Mamba2 and DeltaNet on language modeling, common-sense reasoning, in-context retrieval, length extrapolation, and long-context understanding. Hybrids with sliding-window attention or Mamba2 further improve efficiency and quality.",
                "zh": "Gated DeltaNet 在语言建模、常识推理、上下文检索、长度外推与长上下文理解上超过 Mamba2 与 DeltaNet；与滑窗注意力或 Mamba2 的混合进一步提升效率与质量。",
                "summary": "结论：单模打赢两前驱；混合还能再抬一手。",
                "terms": ["Gated DeltaNet", "Mamba2", "hybrid"],
            },
        ],
    },
    {
        "id": "intro",
        "title": "1 Introduction 引言（关键）",
        "paras": [
            {
                "en": "Linear Transformers store outer-product key–value associations in a fixed-size state. When sequence length exceeds dimensionality, memory collisions hinder exact retrieval.",
                "zh": "线性 Transformer 用固定大小状态存外积 KV 关联；序列长度超过维度后，「记忆碰撞」阻碍精确检索。",
                "summary": "有限状态容量是一切门控/纠错动机的源头。",
                "terms": ["associative memory", "memory collision"],
            },
            {
                "en": "Mamba2 uses a scalar gate α_t that uniformly decays all associations—fast to clear, but not targeted. DeltaNet softly replaces one key’s binding via β_t—precise, but slow to flush irrelevant context.",
                "zh": "Mamba2 用标量门 α_t 均匀衰减全部关联——清空快，但不定点。DeltaNet 用 β_t 软替换某一 key 的绑定——精确，但难快速冲掉无关上下文。",
                "summary": "一张表：α=全局刮板，β=局部橡皮擦。",
                "terms": ["Mamba2", "DeltaNet", "α", "β"],
                "figure": "compare",
            },
            {
                "en": "Gated delta rule unifies both: α_t→0 clears memory promptly; α_t→1 recovers pure delta updates. Training extends DeltaNet’s WY/chunkwise algorithm with gating terms.",
                "zh": "Gated delta rule 统一二者：α_t→0 迅速清空；α_t→1 退回纯 delta。训练在 DeltaNet 的 WY/分块算法上并入门控项。",
                "summary": "工程承诺：表达力升级，并行训练日程可复用。",
                "terms": ["gated delta rule", "WY representation", "chunkwise"],
            },
        ],
    },
    {
        "id": "prelim",
        "title": "2 预备：Mamba2 与 DeltaNet",
        "paras": [
            {
                "en": "Vanilla linear attention accumulates S_t = S_{t−1} + v_t k_tᵀ. Mamba2 adds scalar decay α_t so every association shrinks by the same factor each step.",
                "zh": "朴素线性注意力累加 S_t=S_{t−1}+v_t k_tᵀ。Mamba2 加标量衰减 α_t，每一步所有关联按同一比例缩小。",
                "summary": "Mamba2 = 加性写入 + 全局遗忘。",
                "terms": ["Mamba2", "α"],
                "formulas": [
                    {
                        "tag": "线性注意力",
                        "latex": r"S_t=S_{t-1}+v_t k_t^\top,\quad o_t=S_t q_t",
                    },
                    {
                        "tag": "Mamba2",
                        "latex": r"S_t=\alpha_t S_{t-1}+v_t k_t^\top,\quad \alpha_t\in(0,1)",
                        "note": "全体一起忘，无法只擦某一条绑定。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "DeltaNet retrieves the old value for the current key, mixes with the new value by writing strength β, then remove-and-write—equivalent to a generalized Householder transition.",
                "zh": "DeltaNet 取回当前 key 的旧 value，按写入强度 β 与新 value 混合，再擦写——等价于广义 Householder 转移。",
                "summary": "DeltaNet = 定点纠错，缺快速整页清空。",
                "terms": ["DeltaNet", "β", "Householder"],
                "formulas": [
                    {
                        "tag": "DeltaNet",
                        "latex": r"S_t=S_{t-1}(I-\beta_t k_t k_t^\top)+\beta_t v_t k_t^\top",
                        "wide": True,
                    },
                ],
            },
        ],
    },
    {
        "id": "rule",
        "title": "3.1 Gated Delta Rule（核心公式）",
        "paras": [
            {
                "en": "Equation (10): apply scalar gate α_t before / around the Householder delta transition, then write β_t v_t k_tᵀ. This is the gated delta rule.",
                "zh": "式 (10)：在 Householder 型 delta 转移上乘标量门 α_t，再写入 β_t v_t k_tᵀ。这就是 gated delta rule。",
                "summary": "必背：S ← α(I−βkkᵀ)S + βvkᵀ。",
                "terms": ["gated delta rule", "Eq.10"],
                "figure": "gdn_steps",
                "formulas": [
                    {
                        "tag": "式 (10)",
                        "latex": r"S_t=S_{t-1}\bigl(\alpha_t(I-\beta_t k_t k_t^\top)\bigr)+\beta_t v_t k_t^\top",
                        "note": "α 管全局寿命，β 管本次纠错强度。",
                        "wide": True,
                    },
                    {
                        "tag": "极限行为",
                        "latex": r"\alpha_t\to 0\;\Rightarrow\;\text{快速清空};\quad \alpha_t\to 1\;\Rightarrow\;\text{纯 DeltaNet}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Through an online-learning view (Table 1), Gated DeltaNet relaxes the retention regularizer with α_t while keeping a delta-style regression term on the (gated) prediction error—combining selective forgetting with associative-recall objectives.",
                "zh": "从在线学习视角（表 1）：Gated DeltaNet 用 α_t 放松「贴近旧状态」正则，同时保留对（门控后）预测误差的 delta 风格回归项——兼具选择性遗忘与联想回忆目标。",
                "summary": "理论口令：遗忘松弛 + 重构纠错，一张目标函数写清。",
                "terms": ["online learning", "associative recall"],
            },
            {
                "en": "Training extends the WY / UT chunkwise algorithm of scalable DeltaNet by folding α into the Householder products, preserving matmul-heavy kernels for Tensor Cores.",
                "zh": "训练把 α 折进 Householder 乘积，扩展可扩展 DeltaNet 的 WY/UT 分块算法，保持吃 Tensor Core 的 matmul 核。",
                "summary": "算法：不是另起炉灶，是在 DeltaNet 并行日程上加门。",
                "terms": ["WY representation", "chunkwise", "UT transform"],
            },
        ],
    },
    {
        "id": "arch",
        "title": "架构与混合",
        "paras": [
            {
                "en": "Practical parameterization mirrors recent linear RNNs: short convolution + SiLU on q/k/v paths, L2-normalized q/k, linear maps for α/β, and an output gate.",
                "zh": "实践参数化对齐近期线性 RNN：q/k/v 路径短卷积 + SiLU，q/k 再 L2Norm，α/β 线性映射，外加输出门。",
                "summary": "零件清单与 DeltaNet/KDA 家族一脉相承。",
                "terms": ["ShortConv", "SiLU", "L2Norm", "output gate"],
            },
            {
                "en": "Hybrids: interleave Gated DeltaNet with sliding-window attention, or mix with Mamba2 layers, to gain local precision / complementary inductive bias and higher training throughput.",
                "zh": "混合：与滑窗注意力交织，或与 Mamba2 层混合，补局部精度/归纳偏置，并抬高训练吞吐。",
                "summary": "纯 GDN 已强；混合是工程上的再加速与再补强。",
                "terms": ["hybrid", "sliding window", "Mamba2"],
                "figure": "hybrid",
            },
        ],
    },
    {
        "id": "expts",
        "title": "4 实验要点",
        "paras": [
            {
                "en": "On S-NIAH retrieval suites, Gated DeltaNet holds accuracy farther in length than Mamba2 (which collapses) and is more robust than DeltaNet on harder haystack variants—evidence that gate+delta helps long-context retrieval.",
                "zh": "S-NIAH 检索套件上，Gated DeltaNet 在更长长度仍稳住精度（Mamba2 崩得更快），在更难 haystack 变体上也比 DeltaNet 更稳——说明门+delta 有助于长上下文检索。",
                "summary": "检索：互补机制不是论文故事，有长度曲线撑着。",
                "terms": ["S-NIAH", "in-context retrieval"],
            },
            {
                "en": "Across LM / reasoning / long-context suites, Gated DeltaNet consistently beats Mamba2 and DeltaNet; hybrids further improve efficiency–quality trade-offs. Code: NVlabs/GatedDeltaNet.",
                "zh": "语言建模 / 推理 / 长上下文套件上 Gated DeltaNet 稳定超过 Mamba2 与 DeltaNet；混合进一步改善效率–质量折中。代码：NVlabs/GatedDeltaNet。",
                "summary": "产品结论：GDN 是 Delta→KDA 谱系里关键的一环。",
                "terms": ["Gated DeltaNet"],
            },
        ],
    },
    {
        "id": "bridge",
        "title": "谱系位置：DeltaNet → GDN → KDA",
        "paras": [
            {
                "en": "Reading map in this repo: papers/deltanet (2021 theory) → papers/deltanet-parallel (2024 scalable training) → this page (scalar α + δ) → papers/kda (channel-wise Diag(α) + MLA hybrid).",
                "zh": "本仓库阅读地图：papers/deltanet（2021 理论原点）→ papers/deltanet-parallel（2024 可扩展训练）→ 本页（标量 α + δ）→ papers/kda（通道级 Diag(α) + MLA 混合）。",
                "summary": "四步：理论原点 → 练得动 → 全局门 → 通道门。",
                "terms": ["KDA", "DeltaNet"],
            },
            {
                "en": "Do not confuse folders: DeltaNet has β only; Gated DeltaNet adds scalar α; KDA replaces α with Diag(α_t) per channel.",
                "zh": "分夹勿混：DeltaNet 只有 β；Gated DeltaNet 加标量 α；KDA 把 α 换成逐通道 Diag(α_t)。",
                "summary": "公式差一个符号量级，论文就该分开放。",
                "terms": ["Diag(α_t)", "α", "β"],
                "formulas": [
                    {
                        "tag": "对照三式",
                        "latex": r"\begin{aligned}\mathrm{DeltaNet}&:\;S\leftarrow S(I-\beta kk^\top)+\beta vk^\top\\ \mathrm{GDN}&:\;S\leftarrow S(\alpha(I-\beta kk^\top))+\beta vk^\top\\ \mathrm{KDA}&:\;S\leftarrow (I-\beta kk^\top)\mathrm{Diag}(\alpha)S+\beta vk^\top\end{aligned}",
                        "wide": True,
                    },
                ],
            },
        ],
    },
]

GLOSSARY = [
    ("Gated DeltaNet", "结合标量遗忘门 α 与 delta rule β 的线性注意力架构（本文）。"),
    ("gated delta rule", "S←S(α(I−βkkᵀ))+βvkᵀ：全局遗忘 + 定点纠错。"),
    ("DeltaNet", "仅用 delta rule 的线性注意力；理论见 papers/deltanet，可扩展训练见 papers/deltanet-parallel。"),
    ("Mamba2", "带标量衰减的加性状态更新：S←αS+vkᵀ。"),
    ("α", "数据相关标量遗忘/衰减因子。"),
    ("β", "delta 写入强度 / 学习率。"),
    ("delta rule", "按 key 读出旧值、按误差纠错写入的更新。"),
    ("gating", "数据相关的记忆清除/保留控制。"),
    ("linear attention", "固定大小状态的线性复杂度注意力族。"),
    ("associative memory", "把 key 映射到 value 的可写可读状态 S。"),
    ("memory collision", "序列过长导致有限维度状态无法区分过多 KV 绑定。"),
    ("Householder", "I−βkkᵀ 型秩一修正转移。"),
    ("WY representation", "紧凑表示一串 Householder 乘积，支撑分块并行。"),
    ("UT transform", "把 WY 因子写成可 matmul 的块三角形式。"),
    ("chunkwise", "块间递推、块内并行的训练日程。"),
    ("online learning", "把递推看成逐步最小化在线目标的闭式更新。"),
    ("associative recall", "上下文中按 key 找回 value 的能力。"),
    ("S-NIAH", "长上下文检索探针套件（needle-in-a-haystack 变体）。"),
    ("hybrid", "GDN 与滑窗注意力或 Mamba2 等混合堆叠。"),
    ("sliding window", "局部滑窗 softmax 注意力。"),
    ("ShortConv", "QKV 后的轻量短卷积。"),
    ("SiLU", "常用激活；配合 L2Norm 稳定 q/k。"),
    ("L2Norm", "对 q/k 的 L2 归一化。"),
    ("output gate", "输出侧数据相关门。"),
    ("KDA", "Kimi Delta Attention：把 α 升级为 Diag(α)（papers/kda）。"),
    ("Diag(α_t)", "通道级对角遗忘；相对 GDN 的标量 α。"),
    ("Eq.10", "本文 gated delta rule 主公式。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "Gated DeltaNet",
        "why": "逐段精读对象；标量门 + delta rule。",
        "url": "./paper.pdf",
        "ext": "https://arxiv.org/abs/2412.06464",
    },
    {
        "level": "前驱",
        "title": "DeltaNet 原点（2021）",
        "why": "FWP 等价、容量界、delta 指令。",
        "url": "../deltanet/index.html",
        "ext": "https://arxiv.org/abs/2102.11174",
    },
    {
        "level": "前驱",
        "title": "并行 DeltaNet 训练（2024）",
        "why": "同一 delta rule 的 WY 分块并行。",
        "url": "../deltanet-parallel/index.html",
        "ext": "https://arxiv.org/abs/2406.06484",
    },
    {
        "level": "下游",
        "title": "Kimi Linear / KDA",
        "why": "通道级 Diag(α) + MLA 混合。",
        "url": "../kda/index.html",
        "ext": "https://arxiv.org/abs/2510.26692",
    },
    {
        "level": "对照",
        "title": "Mamba2",
        "why": "标量衰减加性更新的强基线。",
        "url": "https://arxiv.org/abs/2405.21060",
        "ext": "",
    },
    {
        "level": "代码",
        "title": "NVlabs/GatedDeltaNet",
        "why": "官方实现与实验入口。",
        "url": "https://github.com/NVlabs/GatedDeltaNet",
        "ext": "",
    },
]
