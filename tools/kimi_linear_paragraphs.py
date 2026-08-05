"""Fine-grained Kimi Linear / KDA paragraphs: original + zh + summary.

Paper: Kimi Linear: An Expressive, Efficient Attention Architecture
arXiv:2510.26692 (Kimi Team / Moonshot).

Focus: Abstract, Intro, §2 lineage, §3 KDA, §4 architecture, key experiments,
plus a code-bridge section aligned with ./kda/.
"""

FORMULA_WALL = [
    {
        "tag": "Linear · 只加不改",
        "latex": r"S_t = S_{t-1} + k_t v_t^\top,\quad o_t = S_t^\top q_t",
        "note": "固定大小状态；旧关联永不擦除。",
    },
    {
        "tag": "DeltaNet · delta rule",
        "latex": r"S_t=(I-\beta_t k_t k_t^\top)S_{t-1}+\beta_t k_t v_t^\top",
        "note": "先按 key 擦旧，再写入新 value。",
    },
    {
        "tag": "GDN · 标量遗忘",
        "latex": r"S_t=\alpha_t\,(I-\beta_t k_t k_t^\top)S_{t-1}+\beta_t k_t v_t^\top",
        "note": "整头共用一个 α。",
    },
    {
        "tag": "式 (1) · KDA",
        "latex": r"S_t=\bigl(I-\beta_t k_t k_t^\top\bigr)\,\mathrm{Diag}(\alpha_t)\,S_{t-1}+\beta_t k_t v_t^\top",
        "note": "通道级对角门；本页必背。",
        "wide": True,
    },
]

SECTIONS = [
    {
        "id": "abstract",
        "title": "Abstract 摘要",
        "paras": [
            {
                "en": "We introduce Kimi Linear, a hybrid linear attention architecture that, for the first time, outperforms full attention under fair comparisons across various scenarios—including short-context, long-context, and reinforcement learning (RL) scaling regimes.",
                "zh": "我们提出 Kimi Linear：一种混合线性注意力架构；在公平对比下，它在短上下文、长上下文与强化学习（RL）扩展等多种场景中首次整体优于全注意力。",
                "summary": "开场主张：混合线性注意力可以在公平设置下全面打赢全注意力。",
                "terms": ["Kimi Linear", "hybrid linear attention"],
            },
            {
                "en": "At its core lies Kimi Delta Attention (KDA), an expressive linear attention module that extends Gated DeltaNet with a finer-grained gating mechanism, enabling more effective use of limited finite-state RNN memory.",
                "zh": "其核心是 Kimi Delta Attention（KDA）：一种富表达力的线性注意力模块，在 Gated DeltaNet 之上引入更细粒度的门控，从而更有效地利用有限状态的 RNN 记忆。",
                "summary": "核心模块：KDA = GDN + 通道级细粒度遗忘门。",
                "terms": ["KDA", "Gated DeltaNet", "finite-state RNN memory"],
            },
            {
                "en": "Our bespoke chunkwise algorithm achieves high hardware efficiency through a specialized variant of the Diagonal-Plus-Low-Rank (DPLR) transition matrices, which substantially reduces computation compared to the general DPLR formulation while remaining more consistent with the classical delta rule.",
                "zh": "我们定制的分块算法借助 Diagonal-Plus-Low-Rank（DPLR）转移矩阵的一种特化变体获得高硬件效率：相对通用 DPLR 大幅降算，同时更贴近经典 delta rule。",
                "summary": "训练侧卖点：特化 DPLR 分块核，又快又贴 delta rule。",
                "terms": ["DPLR", "chunkwise algorithm", "delta rule"],
            },
            {
                "en": "We pretrain a Kimi Linear model with 3B activated parameters and 48B total parameters, based on a layerwise hybrid of KDA and Multi-Head Latent Attention (MLA). Our experiments show that with an identical training recipe, Kimi Linear outperforms full MLA with a sizeable margin across all evaluated tasks, while reducing KV cache usage by up to 75% and achieving up to 6× decoding throughput for a 1M context.",
                "zh": "我们预训练了激活 3B、总参 48B 的 Kimi Linear，层间混合 KDA 与 Multi-Head Latent Attention（MLA）。实验表明：相同训练配方下，它在所有评测任务上以明显优势超过全 MLA，同时 KV cache 最高可降约 75%，在 1M 上下文解码吞吐最高约 6×。",
                "summary": "规模数字：48B/3B；同配方赢 MLA；cache −75%；1M 解码最高约 6×。",
                "terms": ["MLA", "KV cache"],
            },
            {
                "en": "These results demonstrate that Kimi Linear can be a drop-in replacement for full attention architectures with superior performance and efficiency, including tasks with longer input and output lengths.",
                "zh": "结果表明：Kimi Linear 可作为全注意力架构的即插即用替代，在更长输入/输出任务上也兼具更优性能与效率。",
                "summary": "产品结论：不是「差不多」，而是可替换且更强。",
                "terms": [],
            },
        ],
    },
    {
        "id": "intro",
        "title": "1 Introduction 引言（关键段落）",
        "paras": [
            {
                "en": "As large language models (LLMs) evolve into increasingly capable agents, the computational demands of inference—particularly in long-horizon and reinforcement learning (RL) settings—are becoming a central bottleneck.",
                "zh": "随着大语言模型日益成为更强的智能体，推理算力需求——尤其在长时程与强化学习设定下——正成为核心瓶颈。",
                "summary": "场景位移：瓶颈从「训练」转向「长解码 / RL test-time」。",
                "terms": ["RL test-time scaling"],
            },
            {
                "en": "In particular, the quadratic time complexity and the linearly growing key–value (KV) cache of softmax attention introduce substantial computational and memory overheads, hindering throughput, context-length scaling, and real-time interactivity.",
                "zh": "尤其是，softmax 注意力的二次时间复杂度以及线性增长的 KV cache，带来显著的计算与内存开销，阻碍吞吐、上下文扩展与实时交互。",
                "summary": "敌人画像：O(L²) 计算 + O(L) KV cache。",
                "terms": ["softmax attention", "KV cache"],
            },
            {
                "en": "Linear attention offers a principled approach to reducing computational complexity but has historically underperformed softmax attention in language modeling—even for short sequences—due to limited expressivity. Recent advances have significantly narrowed this gap, primarily through two innovations: gating or decay mechanisms and the delta rule.",
                "zh": "线性注意力原则上可降复杂度，但历史上因表达力不足，即便短序列也常弱于 softmax。近期进展显著缩小差距，主要靠两类创新：门控/衰减机制，以及 delta rule。",
                "summary": "线性注意力两件宝：遗忘门 + delta 纠错写入。",
                "terms": ["linear attention", "delta rule", "gating"],
            },
            {
                "en": "Nevertheless, purely linear structures remain fundamentally constrained by the finite-state capacity, making long-sequence modeling and in-context retrieval theoretically challenging. Hybrid architectures that combine softmax and linear attention—using a few global-attention layers alongside predominantly faster linear layers—have thus emerged as a practical compromise.",
                "zh": "然而纯线性结构仍受有限状态容量根本制约，长序列建模与上下文检索在理论上困难。于是出现折中：少数全局 softmax 层 + 大量更快的线性层，构成混合架构。",
                "summary": "为何必须混合：有限状态 RNN 记不住一切；留几层全注意力补检索。",
                "terms": ["hybrid linear attention", "finite-state RNN memory"],
            },
            {
                "en": "While GDN, similar to Mamba2, employs a coarse head-wise forget gate, KDA introduces a channel-wise variant in which each feature dimension maintains an independent forgetting rate, akin to Gated Linear Attention (GLA). This fine-grained design enables more precise regulation of the finite-state RNN memory.",
                "zh": "GDN 类似 Mamba2，使用粗糙的 head 级遗忘门；KDA 则引入通道级变体——每个特征维各自有独立遗忘率，类似 GLA。这种细粒度设计能更精确地调控有限状态 RNN 记忆。",
                "summary": "相对 GDN 的一刀：遗忘从「一头一个 α」升级为「一通道一个 α」。",
                "terms": ["KDA", "Gated DeltaNet", "GLA", "Mamba2"],
            },
            {
                "en": "Kimi Linear interleaves KDA with periodic full attention layers in a uniform 3:1 ratio. This hybrid structure reduces memory and KV-cache usage by up to 75% during long-sequence generation while preserving global information flow via the full attention layers.",
                "zh": "Kimi Linear 以均匀 3:1 比例交织 KDA 与周期性全注意力层。该混合在长序列生成时最高可减少约 75% 的内存与 KV cache，同时靠全注意力层保留全局信息流。",
                "summary": "架构超参背下来：KDA:MLA = 3:1 ⇒ cache 约剩 1/4。",
                "terms": ["3:1 hybrid", "MLA"],
            },
        ],
    },
    {
        "id": "lineage",
        "title": "2.2 谱系：Linear → DeltaNet → GDN",
        "paras": [
            {
                "en": "Linear Attention as Online Learning. Linear attention maintains a matrix-valued recurrent state that accumulates key–value associations (see formula panel).",
                "zh": "线性注意力作为在线学习：用矩阵值递推状态累积 key–value 关联（见下方公式卡）。",
                "summary": "朴素线性：只加不改；S 是固定大小的联想记忆。",
                "terms": ["linear attention", "associative memory"],
                "figure": "pipeline",
                "formulas": [
                    {
                        "tag": "Linear · 状态更新",
                        "latex": r"S_t = S_{t-1} + k_t v_t^\top",
                        "note": "只加不改：旧关联永不擦除。",
                    },
                    {
                        "tag": "Linear · 读出",
                        "latex": r"o_t = S_t^\top q_t",
                        "note": "用当前 query 从固定大小状态读出。",
                    },
                ],
            },
            {
                "en": "From the fast-weight perspective, S_t serves as an associative memory storing transient mappings from keys to values. This update can be viewed as performing gradient descent on an unbounded correlation objective, which continually reinforces recent key–value pairs without any forgetting.",
                "zh": "从快权重视角，S_t 是存储 key→value 短暂映射的联想记忆。该更新可视为对无界相关目标做梯度下降：不断强化近期 KV，却没有任何遗忘。",
                "summary": "问题种子：没有「擦除标准」，状态只会越堆越脏。",
                "terms": ["fast weights"],
                "formulas": [
                    {
                        "tag": "目标 · 无界相关",
                        "latex": r"\mathcal{L}_t(S) = -\langle S^\top k_t,\, v_t\rangle",
                        "note": "梯度下降只会「越加越多」，没有遗忘项。",
                    },
                ],
            },
            {
                "en": "DeltaNet: Online Gradient Descent on Reconstruction Loss. DeltaNet reinterprets this recurrence as online gradient descent on a reconstruction objective. Taking a gradient step with learning rate β_t yields the classical delta rule (see formula panel).",
                "zh": "DeltaNet：对重构损失做在线梯度下降。以学习率 β_t 走一步，得到经典 delta rule（见下方公式卡）。",
                "summary": "delta rule：先按当前 key 擦旧，再写入新 value（秩一 Householder 型）。",
                "terms": ["DeltaNet", "delta rule", "β"],
                "formulas": [
                    {
                        "tag": "目标 · 重构损失",
                        "latex": r"\mathcal{L}_t(S)=\tfrac12\bigl\|S^\top k_t - v_t\bigr\|^2",
                        "note": "希望当前 key 读出的内容接近目标 value。",
                    },
                    {
                        "tag": "DeltaNet · 更新",
                        "latex": r"S_t=(I-\beta_t k_t k_t^\top)S_{t-1}+\beta_t k_t v_t^\top",
                        "note": "先按 key 擦旧，再写入新 value。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "This rule—the classical delta rule—treats S as a learnable associative memory that continually corrects itself toward the mapping k_t ↦ v_t. The rank-1 update structure, equivalent to a generalized Householder transformation, supports hardware-efficient chunkwise parallelization.",
                "zh": "这一经典 delta rule 把 S 当作可学习联想记忆，不断向映射 k_t↦v_t 自我纠正。秩一更新等价于广义 Householder 变换，支持硬件高效的分块并行。",
                "summary": "既有学习语义，又有可并行的代数结构。",
                "terms": ["Householder", "chunkwise algorithm"],
                "formulas": [
                    {
                        "tag": "等价展开 · 预测误差",
                        "latex": r"\hat v_t=k_t^\top S_{t-1},\quad e_t=v_t-\hat v_t,\quad S_t=S_{t-1}+\beta_t k_t e_t^\top",
                        "note": "误差接近 0 时几乎不再写入——避免重复叠同一关联。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Gated DeltaNet as Weight Decay. Although DeltaNet stabilizes learning, it still retains outdated associations indefinitely. Gated DeltaNet (GDN) introduces a scalar forget gate α_t ∈ [0,1] before the delta update.",
                "zh": "Gated DeltaNet 作为权重衰减：尽管 DeltaNet 稳定了学习，过时关联仍无限保留。GDN 在 delta 更新前引入标量遗忘门 α_t∈[0,1]。",
                "summary": "GDN：整头共用一个 α，给快权重加数据相关的「体重衰减」。",
                "terms": ["Gated DeltaNet", "α"],
                "formulas": [
                    {
                        "tag": "GDN · 标量门",
                        "latex": r"S_t=\alpha_t\,(I-\beta_t k_t k_t^\top)S_{t-1}+\beta_t k_t v_t^\top",
                        "note": "整头共用一个遗忘速度。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Here, α_t acts as a form of weight decay on the fast weights, implementing a forgetting mechanism analogous to data-dependent L2 regularization. This simple yet effective modification provides a principled way to control memory lifespan and mitigate interference.",
                "zh": "此处 α_t 相当于快权重上的权重衰减，实现类似数据相关 L2 正则的遗忘机制。这一简单有效的改动给出控制记忆寿命、减轻干扰的原则性手段。",
                "summary": "标量门已经很强，但仍「一头一速」，精细度不够。",
                "terms": ["gating"],
            },
        ],
    },
    {
        "id": "kda",
        "title": "3 Kimi Delta Attention（核心公式）",
        "paras": [
            {
                "en": "We propose Kimi Delta Attention (KDA), a new gated linear attention variant that refines GDN’s scalar decay by introducing a fine-grained diagonalized gate Diag(α_t) that enables fine-grained control over memory decay and positional awareness.",
                "zh": "我们提出 Kimi Delta Attention（KDA）：一种新的门控线性注意力变体，用细粒度对角门 Diag(α_t) 改进 GDN 的标量衰减，从而精细控制记忆衰减与位置感知。",
                "summary": "KDA 一句话：把 α 从标量升级成对角向量。",
                "terms": ["KDA", "Diag(α_t)"],
            },
            {
                "en": "Equation (1) is the core KDA recurrence: channel-wise forget via Diag(α_t), then a delta-rule write, then a query readout. Shapes: S ∈ R^{d_k×d_v}, o ∈ R^{d_v}.",
                "zh": "式 (1) 是 KDA 核心递推：用 Diag(α_t) 做通道遗忘，再做 delta 写入，最后用 query 读出。形状：S∈R^{d_k×d_v}，o∈R^{d_v}。",
                "summary": "必背公式：先通道遗忘，再 delta 擦写，最后用 q 读出。",
                "terms": ["Eq.1", "β", "α"],
                "figure": "kda_steps",
                "formulas": [
                    {
                        "tag": "式 (1) · KDA 状态更新",
                        "latex": r"S_t=\bigl(I-\beta_t k_t k_t^\top\bigr)\,\mathrm{Diag}(\alpha_t)\,S_{t-1}+\beta_t k_t v_t^\top",
                        "note": "相对 GDN：α 从标量变成对角向量。",
                        "wide": True,
                    },
                    {
                        "tag": "式 (1) · 读出",
                        "latex": r"o_t = S_t^\top q_t",
                        "note": "状态大小固定，不随序列长度增长。",
                    },
                ],
            },
            {
                "en": "Teaching expansion (aligned with this repo’s recurrent_kda): four explicit steps—forget, predict, correct, read—matching the formula panels below.",
                "zh": "教学展开（与本仓库 recurrent_kda 对齐）：四步——遗忘、预测、纠错、读取——见下方公式卡。",
                "summary": "四步口诀：忘 → 读预测 → 写误差 → 用 q 查。",
                "terms": ["recurrent_kda", "log_decay"],
                "formulas": [
                    {
                        "tag": "步骤 1 · 遗忘",
                        "latex": r"S \leftarrow \mathrm{Diag}\bigl(\exp(g_t)\bigr)\,S,\quad g_t\le 0",
                        "note": "逐通道 α=exp(g)；g≤0 ⇒ α∈(0,1]。",
                    },
                    {
                        "tag": "步骤 2 · 预测",
                        "latex": r"\hat v \leftarrow k_t^\top S",
                        "note": "用当前 key 当地址，读出旧内容。",
                    },
                    {
                        "tag": "步骤 3 · 纠错写入",
                        "latex": r"S \leftarrow S + \beta_t\, k_t\,(v_t-\hat v)^\top",
                        "note": "只写预测误差（delta）。",
                    },
                    {
                        "tag": "步骤 4 · 查询",
                        "latex": r"o_t \leftarrow \Bigl(\frac{q_t}{\sqrt{d}}\Bigr)^\top S",
                        "note": "教学代码里带 1/√d 缩放。",
                    },
                ],
            },
            {
                "en": "Intuition: k_t is the address that selects which memory “row” to edit/query; v_t is the content to store; q_t reads from the updated S; exp(g_t) is the per-channel forget rate; β_t is the write strength of this correction step.",
                "zh": "直觉：k_t 是地址，决定改写/查询哪条「记忆行」；v_t 是要写入的内容；q_t 从更新后的 S 读取；exp(g_t) 是各地址通道的遗忘率；β_t 是本次纠错写入强度。",
                "summary": "符号角色表：地址 / 内容 / 查询 / 遗忘 / 写入强度。",
                "terms": ["associative memory"],
            },
            {
                "en": "State shape is fixed at [heads, d_k, d_v] (this repo’s teaching code uses d_k = d_v = d) and does not grow with sequence length—this is the core gain versus a KV cache of size O(t · d).",
                "zh": "状态形状固定为 [heads, d_k, d_v]（本仓库教学代码取 d_k=d_v=d），不随序列变长——相对大小为 O(t·d) 的 KV cache，这是核心收益。",
                "summary": "复杂度收益：每步 O(d²)/head，与长度无关；cache 换成固定 S。",
                "terms": ["KV cache"],
            },
        ],
    },
    {
        "id": "chunk",
        "title": "3.1–3.2 分块算法与相对 DPLR 的效率",
        "paras": [
            {
                "en": "By partially expanding the recurrence for Eq. 1 into a chunk-wise formulation, a series of rank-1 matrix transformations can be compressed into dense WY / UT representations while maintaining stability under diagonal gating.",
                "zh": "把式 (1) 的递推部分展开为分块形式后，可将一串秩一矩阵变换压缩成稠密的 WY / UT 表示，并在对角门控下保持稳定。",
                "summary": "训练并行：chunk 内把多次秩一更新打包成可 matmul 的块。",
                "terms": ["chunkwise algorithm", "WY representation", "UT transform"],
            },
            {
                "en": "During the output stage, we adopt an inter-block recurrent and intra-block parallel strategy to maximize matrix multiplication throughput, thereby fully utilizing Tensor Cores.",
                "zh": "输出阶段采用块间递推、块内并行策略，以最大化矩阵乘吞吐，从而吃满 Tensor Core。",
                "summary": "硬件口令：块间串行传 S，块内尽量 GEMM。",
                "terms": ["Tensor Core"],
            },
            {
                "en": "In representational capacity, KDA aligns with the generalized DPLR family (fine-grained decay). By binding both low-rank factors to k, KDA cuts second-level chunk matmuls and stays closer to the classical delta rule.",
                "zh": "表达能力上，KDA 对齐广义 DPLR 族（同样细粒度衰减）。通过把两个低秩因子都绑定到 k，KDA 减少二级分块 matmul，同时更贴近经典 delta rule。",
                "summary": "特化诀窍：a=b=k → 少做 matmul，还更贴经典 delta rule。",
                "terms": ["DPLR"],
                "formulas": [
                    {
                        "tag": "广义 DPLR",
                        "latex": r"S_t=\bigl(D-a_t b_t^\top\bigr)S_{t-1}+k_t v_t^\top",
                        "note": "KDA 特化：把 a、b 都绑到 k，算子约快 1×（相对通用 DPLR）。",
                        "wide": True,
                    },
                ],
            },
        ],
    },
    {
        "id": "arch",
        "title": "4 Kimi Linear 模型架构",
        "paras": [
            {
                "en": "Neural parameterization (per head): short-conv + Swish for q/k/v; L2Norm on q/k; low-rank channel gate α; sigmoid write strength β. See formula panels.",
                "zh": "神经参数化（每头）：q/k/v 走短卷积 + Swish；q/k 再 L2Norm；α 低秩通道门；β 为 sigmoid 写入强度。见公式卡。",
                "summary": "实现清单：短卷积 + Swish；q/k 再 L2Norm；α 低秩投影；β sigmoid。",
                "terms": ["ShortConv", "L2Norm", "α", "β"],
                "figure": "hybrid",
                "formulas": [
                    {
                        "tag": "q / k",
                        "latex": r"q_t,k_t=\mathrm{L2Norm}\bigl(\mathrm{Swish}(\mathrm{ShortConv}(W_{q/k}x_t))\bigr)",
                        "note": "L2Norm 稳住特征值。",
                        "wide": True,
                    },
                    {
                        "tag": "v / α / β",
                        "latex": r"v_t=\mathrm{Swish}(\mathrm{ShortConv}(W_v x_t)),\quad \alpha_t=f(W^\uparrow_\alpha W^\downarrow_\alpha x_t),\quad \beta_t=\sigma(W_\beta x_t)",
                        "note": "α∈[0,1]^{d_k}（逐通道）；β∈[0,1]（标量写入强度）。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "For q, k, v we apply a ShortConv followed by a Swish activation, following GDN. The q and k representations are further L2-normalized to ensure eigenvalue stability. The per-channel decay α is parameterized via a low-rank projection with rank equal to the head dimension.",
                "zh": "对 q、k、v 先做 ShortConv 再接 Swish（沿用 GDN）。q、k 再经 L2Norm 以保证特征值稳定。逐通道衰减 α 用秩=头维的低秩投影参数化。",
                "summary": "稳定技巧：L2Norm(q/k) + 低秩 α，参数量可控。",
                "terms": ["ShortConv"],
            },
            {
                "en": "Before the output projection, we use a head-wise RMSNorm and a data-dependent gating mechanism. The output gate uses low-rank parameterization similar to the forget gate, alleviating Attention Sink while keeping parameters fair.",
                "zh": "输出投影前使用 head 级 RMSNorm 与数据相关门控。输出门同样低秩，在参数公平的同时缓解 Attention Sink。",
                "summary": "输出门默认 Sigmoid（消融显示优于 Swish / 无门）。",
                "terms": ["output gate", "Attention Sink", "RMSNorm"],
                "formulas": [
                    {
                        "tag": "输出门",
                        "latex": r"o_t=W_o\Bigl(\sigma(W^\uparrow_g W^\downarrow_g x_t)\,\odot\,\mathrm{RMSNorm}(\mathrm{KDA}(\cdot))\Bigr)",
                        "note": "默认 Sigmoid 门；消融显示优于 Swish / 无门。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Hybrid model architecture. Long-context retrieval remains the primary bottleneck for pure linear attention; we therefore hybridize KDA with a small number of full global-attention (Full MLA) layers. Empirically, a uniform 3:1 ratio (3 KDA layers to 1 MLA layer) provided the best quality–throughput trade-off.",
                "zh": "混合架构：长上下文检索仍是纯线性注意力的主瓶颈，故将 KDA 与少量全全局注意力（Full MLA）层混合。经验上，均匀 3:1（3 层 KDA : 1 层 MLA）给出最佳质量–吞吐折中。",
                "summary": "层间混合（非头间）：3 KDA + 1 MLA 循环堆叠。",
                "terms": ["3:1 hybrid", "MLA"],
            },
            {
                "en": "No Position Encoding (NoPE) for MLA Layers. In Kimi Linear, we apply NoPE to all full attention (MLA) layers. This design delegates the entire responsibility for encoding positional information and recency bias to the KDA layers. KDA is thus established as the primary position-aware operator.",
                "zh": "MLA 层采用 NoPE（无显式位置编码）。该设计把位置信息与近因偏差的编码责任全部交给 KDA 层，从而使 KDA 成为主要的位置感知算子。",
                "summary": "分工：KDA 管位置/近因；MLA 专心做全局检索。",
                "terms": ["NoPE", "RoPE"],
            },
            {
                "en": "NoPE also offers practical advantages for MLA: it enables conversion to highly efficient pure Multi-Query Attention (MQA) at inference, and simplifies long-context training by removing RoPE base / YaRN tuning.",
                "zh": "NoPE 对 MLA 还有工程好处：推理时可转为高效纯 MQA；长上下文训练也省去 RoPE 频率基 / YaRN 调参。",
                "summary": "工程红利：更简单的长文扩展与推理形态。",
                "terms": ["MQA", "NoPE"],
            },
        ],
    },
    {
        "id": "expts",
        "title": "5 实验要点（合成 / 消融 / 主结果）",
        "paras": [
            {
                "en": "Synthetic tests (palindrome, MQAR, stack): across sequence lengths 256→2048, KDA consistently achieves the highest accuracy versus GDN and Mamba2. On palindrome and recall-intensive MQAR, KDA also converges significantly faster than GDN. Mamba2 (multiplicative decay only, no delta rule) fails on all tasks in these settings.",
                "zh": "合成任务（回文、MQAR、栈）：序列长度 256→2048 时，KDA 相对 GDN 与 Mamba2 始终最高精度；在回文与检索密集的 MQAR 上收敛也明显更快。仅有乘性衰减、无 delta rule 的 Mamba2 在这些设定下全部失败。",
                "summary": "细粒度门 + delta rule 在「记/取/状态追踪」上都被测到了。",
                "terms": ["MQAR", "delta rule"],
            },
            {
                "en": "Hybrid-ratio ablation (Table 1): 3:1 yields best train/val PPL (9.23 / 5.65). Higher ratios (7:1, 15:1) hurt validation; 1:1 keeps similar val but raises inference cost; pure MLA (0:1) is worse. Removing the output gate or convolution, or using Swish output gate, all degrade validation.",
                "zh": "混合比消融（表 1）：3:1 训练/验证 PPL 最佳（9.23 / 5.65）。更高比例伤验证；1:1 验证相近但推理更贵；纯 MLA（0:1）更差。去掉输出门或卷积、改用 Swish 输出门，验证都会变差。",
                "summary": "超参结论：3:1 + Sigmoid 输出门 + ShortConv，一套不要拆。",
                "terms": ["3:1 hybrid", "output gate"],
            },
            {
                "en": "Main 1.4T pretrain (48B/3B): with identical recipe, Kimi Linear beats full MLA and hybrid GDN-H on short-context general/math/code/Chinese suites (e.g., MMLU-Pro 51.0 vs MLA 47.2 / GDN-H 47.9).",
                "zh": "主实验 1.4T 预训练（48B/3B）：相同配方下，短上下文通用/数学/代码/中文套件上 Kimi Linear 超过全 MLA 与混合 GDN-H（如 MMLU-Pro 51.0 vs MLA 47.2 / GDN-H 47.9）。",
                "summary": "短文也赢：不是「牺牲短文换长文」。",
                "terms": ["Kimi Linear", "MLA"],
            },
            {
                "en": "Long-context @128k (Table 5): Kimi Linear leads average (54.5) with strong RULER 84.3 and RepoQA 68.5; GDN-H drops behind MLA on several long tasks, while Kimi Linear stays on top. NoPE variant beats the RoPE variant on long-context average.",
                "zh": "128k 长上下文（表 5）：Kimi Linear 平均分领先（54.5），RULER 84.3、RepoQA 68.5 突出；GDN-H 在多项长任务落后于 MLA，而 Kimi Linear 仍居首。NoPE 变体的长文平均优于 RoPE 变体。",
                "summary": "长文：细粒度 KDA + NoPE-MLA 的组合最稳。",
                "terms": ["NoPE", "RULER"],
            },
            {
                "en": "RL math training: with identical algorithm/hparams, Kimi Linear shows faster rising train accuracy and better MATH500 / AIME2025 test curves than MLA—suggesting benefits under reasoning-intensive long-form generation.",
                "zh": "数学 RL：算法与超参相同下，Kimi Linear 训练准确率爬升更快，MATH500 / AIME2025 测试曲线也好于 MLA——显示在推理密集的长生成中更有利。",
                "summary": "RL test-time 场景也受益，呼应摘要主张。",
                "terms": ["RL test-time scaling"],
            },
            {
                "en": "Efficiency: up to ~75% KV-cache reduction from 3:1 hybridization; up to ~6× decoding throughput at 1M context versus MLA. Chunkwise KDA kernel is ~2× faster than general DPLR at long inputs (Figure 2).",
                "zh": "效率：3:1 混合最高约减 75% KV cache；1M 上下文相对 MLA 解码吞吐最高约 6×。分块 KDA 核在长输入上约比通用 DPLR 快 2×（图 2）。",
                "summary": "记住三个数：−75% cache、~6× 解码、~2× 相对 DPLR。",
                "terms": ["KV cache", "DPLR"],
            },
        ],
    },
    {
        "id": "code",
        "title": "对照本仓库代码（学习桥接）",
        "paras": [
            {
                "en": "Code bridge (study note): kda/recurrent.py (same folder as this HTML) implements the token-wise gold recurrence—channel forget, predict, delta write, query—matching Eq.1’s teaching expansion. Prefer this file when checking numerical correctness.",
                "zh": "代码桥接（学习笔记）：与本页同夹的 kda/recurrent.py 实现逐步金标准递推——通道遗忘、预测、delta 写入、查询——对应式 (1) 的教学展开。核对数值正确性时优先看此文件。",
                "summary": "正确性锚点：先读 recurrent_kda，再谈 chunk / 融合核。",
                "terms": ["recurrent_kda"],
            },
            {
                "en": "kda/layer.py wraps projections, short convolution, gate parameterization, and output gating around the recurrence—mirroring §4 neural parameterization at teaching scale.",
                "zh": "kda/layer.py 在递推外包投影、短卷积、门控参数化与输出门，对应 §4 神经参数化的教学尺度实现。",
                "summary": "层包装：公式之外的「工程零件」都在 layer.py。",
                "terms": ["ShortConv", "output gate"],
            },
            {
                "en": "demo.py shows shapes and stateful cache continuation; test_kda.py checks chunk equivalence, β=0 decay-only behavior, causality, and cache consistency. Production should use official FlashKDA / FLA kernels.",
                "zh": "同夹 demo.py 演示形状与带状态 cache 续写；test_kda.py 检查 chunk 等价、β=0 仅衰减、因果性与 cache 一致性。生产请用官方 FlashKDA / FLA 核。",
                "summary": "学习路径：公式墙 → recurrent → layer → demo → tests → 官方 kernel。",
                "terms": ["FlashKDA"],
            },
            {
                "en": "Reading order suggestion: (1) this HTML’s formula wall + lineage; (2) notes.md for a compact card; (3) step through recurrent_kda with a tiny [B,T,H,D]; (4) compare to GDN by collapsing α to a scalar; (5) return to paper §3.1 only when you need chunk/WY details.",
                "zh": "建议阅读顺序：(1) 本页公式墙 + 谱系；(2) notes.md 短卡片；(3) 用很小的 [B,T,H,D] 单步跟 recurrent_kda；(4) 把 α 塌成标量对比 GDN；(5) 需要 chunk/WY 细节时再回论文 §3.1。",
                "summary": "别一上来啃分块推导；先把递推四步跑通。",
                "terms": [],
            },
        ],
    },
]

GLOSSARY = [
    ("Kimi Linear", "Moonshot 混合线性注意力架构：层间 KDA:MLA≈3:1，可替换全注意力。"),
    ("KDA", "Kimi Delta Attention：带通道级对角遗忘门的 delta-rule 线性注意力。"),
    ("Gated DeltaNet", "在 DeltaNet 上加标量遗忘门 α 的线性注意力（GDN）。"),
    ("DeltaNet", "用重构损失的在线梯度（delta rule）更新联想记忆 S 的模型。"),
    ("delta rule", "S ← (I−βkkᵀ)S + βkvᵀ：按 key 擦旧再写新。"),
    ("linear attention", "用固定大小状态压缩历史，使每步复杂度与长度解耦的注意力族。"),
    ("hybrid linear attention", "少量全注意力层 + 大量线性注意力层的混合堆叠。"),
    ("finite-state RNN memory", "状态维度不随序列增长的有限记忆；表达力有理论上界。"),
    ("Diag(α_t)", "以向量 α_t 为对角元的对角阵；实现逐通道遗忘。"),
    ("α", "遗忘/衰减因子；GDN 为标量，KDA 为每通道向量。"),
    ("β", "delta 写入步长 / 学习率，控制本次纠错强度。"),
    ("MLA", "Multi-Head Latent Attention，本架构中的全注意力层选择。"),
    ("3:1 hybrid", "每 3 层 KDA 插 1 层 MLA 的均匀层间混合比。"),
    ("KV cache", "softmax 注意力推理时缓存的历史 key/value，随长度线性涨。"),
    ("DPLR", "Diagonal-Plus-Low-Rank 转移矩阵族；KDA 用其特化形态加速。"),
    ("chunkwise algorithm", "把序列切块，块内并行、块间递推状态的训练算法。"),
    ("WY representation", "把一串秩一更新打包成紧凑矩阵表示的技术。"),
    ("UT transform", "用于降低非 matmul FLOPs、更好吃硬件的三角变换技巧。"),
    ("ShortConv", "小核深度卷积，捕捉局部 token 依赖。"),
    ("L2Norm", "对 q/k 做 L2 归一化以稳定特征值。"),
    ("output gate", "KDA 输出后的数据相关门；默认 Sigmoid 低秩门。"),
    ("Attention Sink", "注意力过度黏在初始 token 等位置的现象；输出门可缓解。"),
    ("RMSNorm", "均方根归一化，用于 KDA 输出侧。"),
    ("NoPE", "No Position Encoding：MLA 层不加 RoPE，位置交给 KDA。"),
    ("RoPE", "旋转位置编码；本文长文对比中 NoPE 更优。"),
    ("MQA", "Multi-Query Attention；NoPE 便于推理时走高效 MQA。"),
    ("GLA", "Gated Linear Attention，通道级门控线性注意力前驱之一。"),
    ("Mamba2", "以乘性衰减为主的状态空间/线性注意力变体；无 delta rule。"),
    ("associative memory", "把 key 映射到 value 的可写可读记忆（此处即 S）。"),
    ("fast weights", "把注意力状态视为快速适应的临时权重的视角。"),
    ("Householder", "与秩一投影更新相关的正交/反射变换结构。"),
    ("softmax attention", "标准 QK softmax 注意力，KV cache 随 L 增长。"),
    ("RL test-time scaling", "推理期用 RL/长轨迹扩展算力与能力的范式。"),
    ("MQAR", "Multi-Query Associative Recall，多查询联想回忆合成任务。"),
    ("RULER", "长上下文评测套件之一。"),
    ("FlashKDA", "生产级 KDA 融合核（见 fla-org/flash-linear-attention）。"),
    ("recurrent_kda", "本仓库逐步递推实现，数值正确性金标准。"),
    ("log_decay", "通道遗忘的对数域参数 g≤0，exp(g)∈(0,1]。"),
    ("Eq.1", "KDA 主更新公式。"),
    ("Tensor Core", "GPU 上适合规则 GEMM 的张量计算单元。"),
    ("gating", "数据相关的遗忘或输出控制机制。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "Kimi Linear / KDA",
        "why": "逐段精读对象；公式以 PDF 为准。",
        "url": "./paper.pdf",
        "ext": "https://arxiv.org/abs/2510.26692",
    },
    {
        "level": "笔记",
        "title": "本夹 notes.md",
        "why": "更短的公式卡片与读码顺序。",
        "url": "./notes.md",
        "ext": "",
    },
    {
        "level": "代码",
        "title": "本夹 kda/",
        "why": "教学向 PyTorch：recurrent / layer；同夹还有 demo.py 与 test_kda.py。",
        "url": "./kda/",
        "ext": "",
    },
    {
        "level": "前驱",
        "title": "DeltaNet 原点（2021）",
        "why": "delta rule 理论：FWP / 容量 / β 写入。",
        "url": "../deltanet/index.html",
        "ext": "https://arxiv.org/abs/2102.11174",
    },
    {
        "level": "前驱",
        "title": "并行 DeltaNet 训练（2024）",
        "why": "可扩展 delta rule 训练基线；KDA 在其上加通道门。",
        "url": "../deltanet-parallel/index.html",
        "ext": "https://arxiv.org/abs/2406.06484",
    },
    {
        "level": "前驱",
        "title": "Linear Attention（Transformers are RNNs）",
        "why": "固定大小状态 S / 因果 RNN 形式的经典源头。",
        "url": "../linear-attention/index.html",
        "ext": "https://arxiv.org/abs/2006.16236",
    },
    {
        "level": "前驱",
        "title": "Gated DeltaNet",
        "why": "标量门 + delta rule 的直接前驱。",
        "url": "https://arxiv.org/abs/2412.06464",
        "ext": "",
    },
    {
        "level": "内核",
        "title": "Flash Linear Attention · KDA ops",
        "why": "官方分块/融合核与 vLLM 集成入口。",
        "url": "https://github.com/fla-org/flash-linear-attention/tree/main/fla/ops/kda",
        "ext": "",
    },
    {
        "level": "相关",
        "title": "Attention Residuals",
        "why": "同家族实验载体（Kimi Linear 48B）上的残差改法。",
        "url": "../attention-residuals/index.html",
        "ext": "",
    },
]
