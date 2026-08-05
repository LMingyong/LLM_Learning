"""Original DeltaNet theory paper (Schlag et al., ICML 2021).

Paper: Linear Transformers Are Secretly Fast Weight Programmers
arXiv:2102.11174

Emphasis: pedagogical bridge from Linear Attention → FWP view →
capacity limit → delta-rule programming instruction.
"""

FORMULA_WALL = [
    {
        "tag": "Linear Attn = 加性快权重",
        "latex": r"W_i = W_{i-1} + v_i\otimes\phi(k_i),\quad y_i = W_i\,\phi(q_i)",
        "note": "只加不改：每来一对 (k,v) 就叠一层外积。",
        "wide": True,
    },
    {
        "tag": "容量直觉",
        "latex": r"\#\{\text{可互不干扰的 key}\} \le d_{\mathrm{dot}}=\dim\phi(k)",
        "note": "L > d_dot 时必然串扰；这就是「超容量」体制。",
        "wide": True,
    },
    {
        "tag": "DeltaNet · 纠错写入",
        "latex": r"W_i = W_{i-1} + \beta_i\,(v_i-\bar v_i)\otimes\phi(k_i),\quad \bar v_i=W_{i-1}\phi(k_i)",
        "note": "先读出旧绑定，再按误差改写——经典 delta rule。",
        "wide": True,
    },
    {
        "tag": "写入强度",
        "latex": r"\beta_i=\sigma(W_\beta x_i)\in(0,1)",
        "note": "模型自己学「这次要改多狠」。",
    },
]

SECTIONS = [
    {
        "id": "bridge",
        "title": "先补缺口：从 Linear Attention 到 DeltaNet（导读）",
        "paras": [
            {
                "en": "Teaching bridge (study note). Start from Katharopoulos linear attention: after feature map φ, causal attention becomes a fixed-size matrix state that accumulates outer products and reads with the query.",
                "zh": "导读（学习笔记）。从 Katharopoulos 线性注意力出发：加了特征映射 φ 之后，因果注意力变成一块固定大小的矩阵状态——不断累加外积，再用 query 去读。",
                "summary": "你已经会的：S/W 是固定大小「便签本」，每步往上贴一张 kv 外积。",
                "terms": ["linear attention", "φ"],
                "figure": "bridge",
                "formulas": [
                    {
                        "tag": "你熟悉的线性注意力",
                        "latex": r"W_i=W_{i-1}+v_i\otimes\phi(k_i),\quad y_i=\frac{W_i\phi(q_i)}{z_i\cdot\phi(q_i)},\quad z_i=z_{i-1}+\phi(k_i)",
                        "note": "分母 z 是归一化累加器；分子就是快权重矩阵 W。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "The missing intuition: that matrix W is exactly a Fast Weight Programmer memory—keys are addresses, values are contents. Additive updates never erase; when too many keys share a finite address space, retrieval mixes several values (crosstalk).",
                "zh": "缺的直觉：矩阵 W 就是一块快权重记忆——key 是地址，value 是内容。加性更新从不擦除；当地址空间有限、key 太多时，读出来会混进多个 value（串扰）。",
                "summary": "卡点不在公式符号，而在「有限便签本会被写爆」。",
                "terms": ["FWP", "associative memory", "crosstalk"],
                "formulas": [
                    {
                        "tag": "理想检索（正交 key）",
                        "latex": r"\phi(k_a)^\top\phi(k_b)=0\ (a\neq b)\;\Rightarrow\;\text{读 }k_a\text{ 只拿到 }v_a",
                        "wide": True,
                    },
                    {
                        "tag": "超容量",
                        "latex": r"L > d_{\mathrm{dot}}\;\Rightarrow\;\text{无法再保证全体正交}\;\Rightarrow\;\text{串扰不可避免}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "DeltaNet’s one idea: before writing, read what is already stored at the current key; write only the correction, scaled by a learned β. Same finite W, but now editable.",
                "zh": "DeltaNet 的一个点子：写入前，先读当前 key 上已经存了什么；只把「误差」按可学习的 β 写回去。还是同一块有限 W，但变成可编辑的了。",
                "summary": "一句话跨越缺口：从「只许粘贴」升级到「先读再改」。",
                "terms": ["delta rule", "β"],
                "formulas": [
                    {
                        "tag": "四步口诀",
                        "latex": r"\bar v\leftarrow W\phi(k);\; v_{\mathrm{new}}\leftarrow\beta v+(1-\beta)\bar v;\; W\leftarrow W+v_{\mathrm{new}}\otimes\phi(k)-\bar v\otimes\phi(k)",
                        "note": "合并后即 W ← W + β(v−v̄)⊗φ(k)。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Where later papers sit: this 2021 paper is the theory/origin. 2024 “parallel DeltaNet” makes training fast; Gated DeltaNet adds scalar forget α; KDA makes forget channel-wise.",
                "zh": "后文位置：2021 这篇是理论原点；2024「并行 DeltaNet」解决训练速度；Gated DeltaNet 加标量遗忘 α；KDA 再把遗忘做成逐通道。",
                "summary": "先把原点读懂，再看训练技巧与门控升级才不晕。",
                "terms": ["Gated DeltaNet", "KDA"],
            },
        ],
    },
    {
        "id": "abstract",
        "title": "Abstract 摘要",
        "paras": [
            {
                "en": "We show the formal equivalence of linearised self-attention and fast weight controllers from the early ’90s: a slow net programs fast weights via additive outer products of keys and values.",
                "zh": "我们证明：线性化自注意力与上世纪 90 年代初的快权重控制器形式等价——慢网络通过 key/value 的加性外积去编程快权重。",
                "summary": "第一主张：Linear Attention ≡ Fast Weight Programmer。",
                "terms": ["FWP", "linear attention"],
            },
            {
                "en": "We infer a memory capacity limit of additive linear attention, and replace pure addition by a delta-rule-like instruction so the model can correct key→value mappings, with learned dynamic learning rates β.",
                "zh": "我们推出加性线性注意力的记忆容量上限，并把纯加性指令换成类似 delta rule 的指令，使模型能纠正 key→value 映射，且学习率 β 动态可学。",
                "summary": "第二主张：容量有限 ⇒ 必须学会改写，不能只会叠加。",
                "terms": ["delta rule", "β", "capacity"],
            },
            {
                "en": "We also propose a new kernel φ (DPFP) balancing simplicity and effectiveness, and show gains on synthetic retrieval, WMT14 En–De, and WikiText-103.",
                "zh": "我们还提出平衡简洁与效果的新核 φ（DPFP），并在合成检索、WMT14 英德、WikiText-103 上展示收益。",
                "summary": "第三块：更好的 φ + 实验验证。",
                "terms": ["DPFP", "φ"],
            },
        ],
    },
    {
        "id": "fwp",
        "title": "2–3 快权重视角：Linear Attn 到底在干什么",
        "paras": [
            {
                "en": "Classic FWP (Schmidhuber ’91/’92): slow weights invent patterns a,b; fast weight matrix W is updated by outer products and then multiplies the input—associative memory with write=sum, read=matvec.",
                "zh": "经典 FWP（Schmidhuber 91/92）：慢权重发明模式 a,b；快权重矩阵 W 靠外积更新，再乘输入——写=求和、读=矩阵向量乘的联想记忆。",
                "summary": "老故事：慢网写程序，快网当内存。",
                "terms": ["FWP", "outer product"],
                "formulas": [
                    {
                        "tag": "经典 FWP（示意）",
                        "latex": r"W_i=\sigma\!\bigl(W_{i-1}+a_i\otimes b_i\bigr),\quad y_i=W_i x_i",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Drop softmax from autoregressive self-attention and rearrange: y = (Σ v⊗k) q. That sum is exactly the fast weight matrix W built additively—same as linear attention without φ.",
                "zh": "自回归自注意力去掉 softmax 再重排：y=(Σ v⊗k) q。这个求和正是加性构造的快权重矩阵 W——也就是不加 φ 的线性注意力。",
                "summary": "等价证明的起点：无 softmax 注意力 = 加性 FWP。",
                "terms": ["self-attention"],
                "formulas": [
                    {
                        "tag": "无 Softmax 自注意力",
                        "latex": r"y_i=\Bigl(\sum_{j\le i}v_j\otimes k_j\Bigr)q_i",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Put φ back for softmax linearisation: W accumulates v⊗φ(k), z accumulates φ(k), readout divides by z·φ(q). This is linear Transformer = FWP + normalisation.",
                "zh": "为线性化 softmax 再引入 φ：W 累加 v⊗φ(k)，z 累加 φ(k)，读出时除以 z·φ(q)。这就是线性 Transformer = FWP + 归一化。",
                "summary": "和你在 papers/linear-attention 读到的，是同一套东西。",
                "terms": ["φ", "linear attention"],
                "figure": "equiv",
                "formulas": [
                    {
                        "tag": "线性 Transformer 递推",
                        "latex": r"W_i=W_{i-1}+v_i\otimes\phi(k_i),\quad z_i=z_{i-1}+\phi(k_i),\quad y_i=\frac{W_i\phi(q_i)}{z_i\cdot\phi(q_i)}",
                        "wide": True,
                    },
                ],
            },
        ],
    },
    {
        "id": "capacity",
        "title": "4.1 理论核心①：容量上限为什么要命",
        "paras": [
            {
                "en": "Endlessly adding associations into a finite matrix hits a wall. Retrieval is a matvec; to avoid interference, keys in φ-space should be orthogonal. In dimension d_dot you get at most d_dot orthogonal keys.",
                "zh": "往有限矩阵里无尽叠加关联必然撞墙。检索是矩阵向量乘；要避免干扰，φ 空间里的 key 应尽量正交。d_dot 维最多只有 d_dot 个正交 key。",
                "summary": "容量 ≈ 特征维数；不是「无限便签」。",
                "terms": ["capacity", "d_dot", "crosstalk"],
                "formulas": [
                    {
                        "tag": "容量界（直觉）",
                        "latex": r"\#\text{互不干扰绑定} \le d_{\mathrm{dot}}",
                        "note": "L>d_dot ⇒ 进入 overcapacity，串扰成为常态。",
                    },
                ],
            },
            {
                "en": "This is the basic (order-2) tensor-product representation story: Smolensky’s TPR theorems on crosstalk transfer here. Difference: classic TPR assumes known roles/fillers; FWPs learn the vectors.",
                "zh": "这就是最基本的（二阶）张量积表示：Smolensky 关于串扰的 TPR 定理可迁移过来。差别在于：经典 TPR 假定角色/填充已知；FWP 的向量是学出来的。",
                "summary": "理论血统：联想记忆 / TPR，不是拍脑袋调参。",
                "terms": ["TPR", "associative memory"],
            },
            {
                "en": "Softmax attention sidesteps this by growing storage (concatenate all KV). Linear models keep |W| fixed—so they must learn to delete/replace, not only append.",
                "zh": "Softmax 注意力靠「拼接全部 KV」让存储随长度涨，从而躲开这个问题。线性模型坚持 |W| 固定——所以必须学会删除/替换，而不能只会追加。",
                "summary": "和全注意力的本质分工：固定内存 vs 无限档案柜。",
                "terms": ["KV cache"],
            },
        ],
    },
    {
        "id": "delta",
        "title": "4.2 理论核心②：Delta 编程指令",
        "paras": [
            {
                "en": "In overcapacity, the model must selectively keep or forget associations. Pure addition (Eq. 17) is the wrong instruction set. We need an editable write.",
                "zh": "超容量下，模型必须有选择地保留或遗忘关联。纯加性（式 17）是错误的指令集。我们需要可编辑的写入。",
                "summary": "动机句：不会改写的内存，写爆了就废了。",
                "terms": ["delta rule"],
                "figure": "delta_steps",
            },
            {
                "en": "Delta update: retrieve \bar v = W φ(k); set write-strength β=σ(W_β x); form v_new = β v + (1−β)\bar v; then remove old and write new—equivalent to W ← W + β(v−\bar v)⊗φ(k).",
                "zh": "Delta 更新：读出 v̄=W φ(k)；写入强度 β=σ(W_β x)；混合 v_new=βv+(1−β)v̄；再擦旧写新——等价于 W←W+β(v−v̄)⊗φ(k)。",
                "summary": "这就是后来所有 DeltaNet / GDN / KDA 的共同祖先公式。",
                "terms": ["β", "delta rule"],
                "formulas": [
                    {
                        "tag": "读旧 / 混合",
                        "latex": r"\bar v_i=W_{i-1}\phi(k_i),\quad \beta_i=\sigma(W_\beta x_i),\quad v^{\mathrm{new}}_i=\beta_i v_i+(1-\beta_i)\bar v_i",
                        "wide": True,
                    },
                    {
                        "tag": "擦写（式 23–24）",
                        "latex": r"W_i=W_{i-1}+v^{\mathrm{new}}_i\otimes\phi(k_i)-\bar v_i\otimes\phi(k_i)=W_{i-1}+\beta_i(v_i-\bar v_i)\otimes\phi(k_i)",
                        "note": "β=1 完全覆盖该地址；β=0 完全不改。",
                        "wide": True,
                    },
                    {
                        "tag": "读出",
                        "latex": r"y_i=W_i\phi(q_i)",
                    },
                ],
            },
            {
                "en": "β is a dynamic learning rate for the classical Widrow–Hoff delta rule, invented by the network itself. Later Gated DeltaNet multiplies a global α in front; KDA replaces α by Diag(α).",
                "zh": "β 就是经典 Widrow–Hoff delta rule 的动态学习率，由网络自己生成。后来的 Gated DeltaNet 再在前面乘全局 α；KDA 把 α 换成 Diag(α)。",
                "summary": "谱系锚点：本页只有 β；α / Diag(α) 是后话。",
                "terms": ["Widrow-Hoff", "Gated DeltaNet", "KDA"],
            },
            {
                "en": "Normalisation caveat: running-sum attention normalisation can blow up and imbalance write/remove. The paper prefers sum-normalising φ(k), φ(q) components (sum normalisation).",
                "zh": "归一化注意：累加式 attention 归一化可能爆炸，且让擦/写失衡。本文更倾向对 φ(k)、φ(q) 做分量求和归一化（sum normalisation）。",
                "summary": "实现细节：DeltaNet 早期对「怎么归一化」很敏感。",
                "terms": ["sum normalisation"],
            },
        ],
    },
    {
        "id": "phi",
        "title": "5 特征映射 φ（简述）",
        "paras": [
            {
                "en": "φ must be nonnegative for attention weights. Its output dim d_dot sets capacity. ELU+1 is simple but keeps d_dot=d_key; FAVOR+ can raise dim via random features but adds noise; DPFP raises dim deterministically without sampling.",
                "zh": "φ 需非负才能当注意力权重；其输出维 d_dot 决定容量。ELU+1 简单但 d_dot=d_key；FAVOR+ 可用随机特征抬维但有噪声；DPFP 确定性抬维、不采样。",
                "summary": "φ 不只是「激活」，它直接买容量。",
                "terms": ["φ", "ELU+1", "FAVOR+", "DPFP"],
            },
        ],
    },
    {
        "id": "expts",
        "title": "6 实验要点（极简）",
        "paras": [
            {
                "en": "Synthetic retrieval: under overcapacity, delta updates beat pure additive linear attention—exactly the regime Sec. 4.1 predicts.",
                "zh": "合成检索：在超容量体制下，delta 更新明显强于纯加性线性注意力——正是 §4.1 预言的场景。",
                "summary": "理论不是空话：写爆之后，会不会改写成了胜负手。",
                "terms": ["capacity"],
            },
            {
                "en": "Real tasks: gains on WMT14 En–De and WikiText-103 versus strong linear-attention baselines; setting details in the paper.",
                "zh": "真实任务：相对强线性注意力基线，在 WMT14 英德与 WikiText-103 有收益；细节见原文。",
                "summary": "原点论文已在 MT/LM 上站住脚，不只是玩具。",
                "terms": [],
            },
        ],
    },
    {
        "id": "next",
        "title": "读完之后去哪",
        "paras": [
            {
                "en": "Next in this repo: papers/deltanet-parallel (hardware-efficient chunkwise training of the same delta rule) → papers/gated-deltanet (add α) → papers/kda (Diag(α)+hybrid).",
                "zh": "本仓库下一步：papers/deltanet-parallel（同一 delta rule 的硬件高效分块训练）→ papers/gated-deltanet（加 α）→ papers/kda（Diag(α)+混合）。",
                "summary": "原点 → 练得动 → 忘得快 → 忘得细。",
                "terms": ["chunkwise", "Gated DeltaNet", "KDA"],
            },
        ],
    },
]

GLOSSARY = [
    ("FWP", "Fast Weight Programmer：慢网络通过指令改写另一套快权重/记忆。"),
    ("linear attention", "用 φ 线性化 softmax 后，注意力等价于固定大小状态递推。"),
    ("φ", "特征映射；其输出维 d_dot 决定联想记忆容量上界。"),
    ("d_dot", "φ(k) 的维度；正交 key 的最大个数。"),
    ("capacity", "有限状态可稳定存储、互不干扰的 KV 关联数量上界。"),
    ("crosstalk", "非正交 key 导致读出混叠多个 value。"),
    ("overcapacity", "序列长度超过 d_dot、必然出现串扰的工作区。"),
    ("associative memory", "按 key 写入/读出 value 的记忆（此处即 W）。"),
    ("outer product", "v⊗k：把一对 KV 写成秩一更新加到 W 上。"),
    ("delta rule", "W ← W + β(v−v̄)⊗φ(k)：按预测误差纠错。"),
    ("β", "写入强度 / 动态学习率，β∈(0,1)。"),
    ("Widrow-Hoff", "经典误差纠正学习规则；本文将其可微地嵌入 FWP。"),
    ("TPR", "Tensor Product Representation；容量/串扰理论来源之一。"),
    ("self-attention", "序列内部 QKV 注意力；去掉 softmax 后显出 FWP 结构。"),
    ("KV cache", "Softmax 注意力存下全部历史 KV；线性模型用固定 W 代替。"),
    ("ELU+1", "Katharopoulos 的简单 φ；不抬维。"),
    ("FAVOR+", "随机特征近似 softmax 的 φ；可抬维但有采样方差。"),
    ("DPFP", "本文提出的确定性无参投影 φ，用于抬维。"),
    ("sum normalisation", "对 φ(k)/φ(q) 分量求和归一化，稳定擦写。"),
    ("Gated DeltaNet", "在 delta 前乘标量 α 的后续工作。"),
    ("KDA", "把 α 换成 Diag(α) 的后续工作（Kimi）。"),
    ("chunkwise", "后文并行训练用的分块日程；原点论文仍偏顺序更新。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "Linear Transformers Are Secretly FWPs",
        "why": "DeltaNet 理论原点：等价性、容量、delta 指令。",
        "url": "./paper.pdf",
        "ext": "https://arxiv.org/abs/2102.11174",
    },
    {
        "level": "前驱",
        "title": "Linear Attention（Transformers are RNNs）",
        "why": "加性固定状态 S/W 的直接前作。",
        "url": "../linear-attention/index.html",
        "ext": "https://arxiv.org/abs/2006.16236",
    },
    {
        "level": "后续",
        "title": "并行 DeltaNet 训练",
        "why": "同一 delta rule 的 WY/分块并行（2024）。",
        "url": "../deltanet-parallel/index.html",
        "ext": "https://arxiv.org/abs/2406.06484",
    },
    {
        "level": "后续",
        "title": "Gated DeltaNet",
        "why": "再加标量遗忘门 α。",
        "url": "../gated-deltanet/index.html",
        "ext": "https://arxiv.org/abs/2412.06464",
    },
    {
        "level": "后续",
        "title": "Kimi Linear / KDA",
        "why": "通道级 Diag(α) + 混合架构。",
        "url": "../kda/index.html",
        "ext": "https://arxiv.org/abs/2510.26692",
    },
]
