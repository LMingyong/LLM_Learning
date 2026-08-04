"""Fine-grained Linear Attention paragraphs: original + zh + summary.

Paper: Katharopoulos et al., Transformers are RNNs: Fast Autoregressive
Transformers with Linear Attention, ICML 2020. arXiv:2006.16236.
"""

SECTIONS = [
    {
        "id": "abstract",
        "title": "Abstract 摘要",
        "paras": [
            {
                "en": "Transformers achieve remarkable performance in several tasks but due to their quadratic complexity, with respect to the input’s length, they are prohibitively slow for very long sequences.",
                "zh": "Transformer 在多项任务上表现卓越，但由于相对输入长度的二次复杂度，对很长序列而言慢得难以接受。",
                "summary": "痛点：全注意力 O(N²)，长序列吃不消。",
                "terms": ["quadratic complexity"],
            },
            {
                "en": "To address this limitation, we express the self-attention as a linear dot-product of kernel feature maps and make use of the associativity property of matrix products to reduce the complexity from O(N²) to O(N), where N is the sequence length.",
                "zh": "为此，我们把自注意力写成核特征映射的线性点积，并利用矩阵乘法结合律，把复杂度从 O(N²) 降到 O(N)，其中 N 为序列长度。",
                "summary": "核心手法：核特征 φ + 结合律重排 → 线性复杂度。",
                "terms": ["kernel feature maps", "associativity", "linear attention"],
            },
            {
                "en": "We show that this formulation permits an iterative implementation that dramatically accelerates autoregressive transformers and reveals their relationship to recurrent neural networks.",
                "zh": "该形式允许迭代实现，从而大幅加速自回归 Transformer，并揭示其与循环神经网络的关系。",
                "summary": "副产品：因果线性注意力 = 固定状态 RNN。",
                "terms": ["RNN", "autoregressive inference"],
            },
            {
                "en": "Our linear transformers achieve similar performance to vanilla transformers and they are up to 4000x faster on autoregressive prediction of very long sequences.",
                "zh": "我们的线性 Transformer 性能接近原版 Transformer，在很长序列的自回归预测上最高可快约 4000 倍。",
                "summary": "卖点数字：质量相近，长解码最高约 4000×。",
                "terms": ["Linear Transformers"],
            },
        ],
    },
    {
        "id": "intro",
        "title": "1 Introduction 引言",
        "paras": [
            {
                "en": "Transformer models were originally introduced by Vaswani et al. (2017) in the context of neural machine translation and have demonstrated impressive results on a variety of tasks dealing with natural language, audio, and images.",
                "zh": "Transformer 最初由 Vaswani 等（2017）在神经机器翻译中提出，并在自然语言、音频与图像等多种任务上取得亮眼结果。",
                "summary": "先立功：Transformer 已是多模态默认底座。",
                "terms": ["Transformer"],
            },
            {
                "en": "However, these benefits often come with a very high computational and memory cost. The bottleneck is mainly caused by the global receptive field of self-attention, which processes contexts of N inputs with a quadratic memory and time complexity O(N²).",
                "zh": "然而这些收益常伴随极高的计算与内存代价。瓶颈主要来自自注意力的全局感受野：处理长度为 N 的上下文时，内存与时间复杂度为二次的 O(N²)。",
                "summary": "瓶颈定位：全局自注意力的二次代价。",
                "terms": ["self-attention"],
            },
            {
                "en": "As a result, in practice transformers are slow to train and their context is limited. This disrupts temporal coherence and hinders the capturing of long-term dependencies.",
                "zh": "结果是：实践中 Transformer 训练慢、上下文受限，破坏时间连贯性，并阻碍长程依赖捕捉。",
                "summary": "后果：训不快、看不长、长依赖难。",
                "terms": [],
            },
            {
                "en": "Lately, researchers shifted their attention to approaches that increase the context length without sacrificing efficiency. Child et al. (2019) introduced sparse factorizations (O(N√N)); Kitaev et al. (2020) reduced complexity to O(N log N) using LSH. Even though these models can be efficiently trained on large sequences, they do not speed-up autoregressive inference.",
                "zh": "近期研究转向「加长上下文又不牺牲效率」：Child 等提出稀疏分解（O(N√N)）；Kitaev 等用 LSH 降到 O(N log N)。但这些模型虽能高效训练长序列，却不能加速自回归推理。",
                "summary": "前人缺口：训练可加速，解码逐步仍贵。",
                "terms": ["Sparse Transformer", "Reformer", "LSH"],
            },
            {
                "en": "In this paper, we introduce the linear transformer model that significantly reduces the memory footprint and scales linearly with respect to the context length. We achieve this by using a kernel-based formulation of self-attention and the associative property of matrix products (§3.2). Using our linear formulation, we also express causal masking with linear complexity and constant memory (§3.3).",
                "zh": "本文提出线性 Transformer：显著降低内存占用，并对上下文长度线性扩展。做法是核形式的自注意力 + 矩阵乘法结合律（§3.2）；并在线性复杂度与常数内存下表达因果掩码（§3.3）。",
                "summary": "本文贡献预告：线性训练 + 因果常数内存推理。",
                "terms": ["causal masking", "linear attention"],
            },
            {
                "en": "This reveals the relation between transformers and RNNs, which enables us to perform autoregressive inference orders of magnitude faster (§3.4). Evaluation on image generation and ASR shows linear transformer reaches transformer-level performance while being up to three orders of magnitude faster during inference.",
                "zh": "这揭示了 Transformer 与 RNN 的关系，使自回归推理快上几个数量级（§3.4）。在图像生成与语音识别上的评估显示：线性 Transformer 可达 Transformer 级性能，推理最高快约三个数量级。",
                "summary": "标题含义落地：Transformers are RNNs ⇒ 解码像 RNN 一样便宜。",
                "terms": ["RNN", "autoregressive inference"],
            },
        ],
    },
    {
        "id": "related",
        "title": "2 Related Work 相关工作（精要）",
        "paras": [
            {
                "en": "Pruning, factorization, quantization, and distillation can speed training/inference, but time complexity remains quadratic in sequence length. In contrast, we reduce both memory and time complexity of transformers theoretically and empirically.",
                "zh": "剪枝、分解、量化与蒸馏可加速训练/推理，但时间复杂度对序列长度仍是二次的。对比之下，我们在理论与经验上都降低了 Transformer 的内存与时间复杂度。",
                "summary": "批评压缩派：再压也还是 O(N²)。",
                "terms": [],
            },
            {
                "en": "More related are Child et al. (sparse attention, O(N√N)) and Kitaev et al. (Reformer, O(N log N) via LSH). Reformer constrains keys to equal queries, so it cannot be used for decoding tasks where keys must differ from queries. Linear transformers impose no such constraints and scale linearly; they can also perform autoregressive inference three orders of magnitude faster.",
                "zh": "更相关的是 Child 等（稀疏注意力，O(N√N)）与 Kitaev 等（Reformer，经 LSH 达 O(N log N)）。Reformer 强制 key=query，故无法用于 key 必须异于 query 的解码任务。线性 Transformer 无此约束、线性扩展，且自回归推理可快三个数量级。",
                "summary": "对 Reformer：训练友好 ≠ 解码友好；本文两者兼顾。",
                "terms": ["Reformer", "Sparse Transformer"],
            },
            {
                "en": "Tsai et al. proposed a kernel-based formulation of attention as a kernel smoother. We use the kernel formulation to speed up self-attention and lower complexity. Concurrently, Shen et al. explored linearized attention for object detection; we additionally develop an autoregressive transformer with linear complexity and constant memory for both inference and training.",
                "zh": "Tsai 等提出注意力的核平滑视角；我们用核形式加速自注意力并降复杂度。同期 Shen 等探索目标检测中的线性化注意力；我们进一步做出训练与推理皆线性复杂度、推理常数内存的自回归 Transformer。",
                "summary": "谱系：核注意力思想 → 本文把它变成可训可推的线性 RNN 形。",
                "terms": ["kernel feature maps"],
            },
        ],
    },
    {
        "id": "softmax",
        "title": "3.1 Softmax 注意力回顾",
        "paras": [
            {
                "en": "Let x ∈ R^{N×F} denote a sequence of N feature vectors of dimensions F. A transformer is T : R^{N×F} → R^{N×F} defined by composing L layers. Each layer is T_l(x) = f_l(A_l(x) + x), where f_l acts position-wise (FFN) and A_l is self-attention across the sequence.",
                "zh": "令 x∈R^{N×F} 为 N 个 F 维特征向量组成的序列。Transformer 由 L 层复合：T_l(x)=f_l(A_l(x)+x)，其中 f_l 逐位置作用（FFN），A_l 是跨序列的自注意力。",
                "summary": "层结构：残差 + 位置无关 FFN + 唯一跨位置算子 A。",
                "terms": ["Transformer"],
            },
            {
                "en": "The input is projected to Q = x W_Q, K = x W_K, V = x W_V. Softmax attention computes A_l(x) = softmax(Q Kᵀ / √D) V, with softmax applied row-wise.",
                "zh": "输入投影为 Q、K、V。Softmax 注意力对缩放点积按行 softmax，再加权 V。",
                "summary": "标准式：先物化 N×N 相似度，再加权 V。",
                "terms": ["softmax attention", "Q", "K", "V"],
                "formulas": [
                    {
                        "tag": "Softmax 注意力",
                        "latex": r"A_\ell(x)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{D}}\right)V",
                        "note": "完整注意力矩阵 → O(N²)。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Generalized attention for any similarity: V'_i = Σ_j sim(Q_i, K_j) V_j / Σ_j sim(Q_i, K_j). Softmax attention is the special case sim(q,k) = exp(qᵀ k / √D).",
                "zh": "对任意相似度的广义注意力见公式卡。Softmax 是指数点积相似度的特例。",
                "summary": "抽象接口：只要 sim≥0，就能定义注意力。",
                "terms": ["similarity function"],
                "formulas": [
                    {
                        "tag": "广义注意力",
                        "latex": r"V'_i=\frac{\sum_j \mathrm{sim}(Q_i,K_j)V_j}{\sum_j \mathrm{sim}(Q_i,K_j)}",
                        "wide": True,
                    },
                ],
            },
        ],
    },
    {
        "id": "linearize",
        "title": "3.2 线性化注意力（核心推导）",
        "paras": [
            {
                "en": "The only constraint on sim(·) for Eq.3 to define attention is non-negativity. This includes all kernels k(x,y): R^{2}→R₊. Given a kernel with feature map φ(x), similarity becomes an inner product in feature space.",
                "zh": "式 (3) 要成为注意力，对 sim(·) 的唯一约束是非负。给定特征映射 φ，相似度变成特征空间内积。",
                "summary": "第一步：用 φ(q)ᵀφ(k) 代替 softmax 相似度。",
                "terms": ["kernel feature maps", "φ"],
                "figure": "assoc",
                "formulas": [
                    {
                        "tag": "核特征形式",
                        "latex": r"V'_i=\frac{\sum_j \phi(Q_i)^\top\phi(K_j)\,V_j}{\sum_j \phi(Q_i)^\top\phi(K_j)}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Using associativity of matrix multiplication, we aggregate keys/values once and reuse them for every query—avoiding the N×N matrix.",
                "zh": "利用矩阵乘法结合律：先聚合 KV 状态，再对每个 query 读出——避免 N×N 矩阵。",
                "summary": "关键重排：先聚合成 KV 状态，再对每个 query 读出。",
                "terms": ["associativity", "linear attention"],
                "formulas": [
                    {
                        "tag": "结合律重排",
                        "latex": r"V'_i=\frac{\phi(Q_i)^\top\bigl(\sum_j \phi(K_j)V_j^\top\bigr)}{\phi(Q_i)^\top\bigl(\sum_j \phi(K_j)\bigr)}",
                        "wide": True,
                    },
                    {
                        "tag": "向量化对照",
                        "latex": r"\phi(Q)\,(\phi(K)^\top V)\;\;\text{vs}\;\;(\phi(Q)\phi(K)^\top)\,V",
                        "note": "左：O(N)；右：O(N²)。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Softmax attention costs O(N²) time and memory because the full attention matrix must be stored for gradients. Linear attention from Eq.5 is O(N) time and memory because Σ_j φ(K_j) V_jᵀ and Σ_j φ(K_j) can be computed once and reused for every query.",
                "zh": "Softmax 注意力因需存储完整注意力矩阵以算梯度，时空皆 O(N²)。式 (5) 的线性注意力为 O(N)：两个累加器只需算一次，供所有 query 复用。",
                "summary": "复杂度跳跃：共享两个累加器，不再物化 N×N。",
                "terms": ["O(N)"],
            },
            {
                "en": "Feature maps and cost: exact softmax corresponds to an infinite-dimensional feature map, so exact linearization is infeasible. For experiments they use φ(x) = elu(x) + 1, yielding positive similarities and O(N D M) cost.",
                "zh": "精确 softmax 对应无穷维特征，无法精确线性化。实验采用 φ(x)=elu(x)+1，保证相似度非负。",
                "summary": "实践选择：elu+1 既正定友好，又避免 ReLU 把负梯度打死。",
                "terms": ["elu+1", "feature map"],
                "formulas": [
                    {
                        "tag": "特征映射",
                        "latex": r"\phi(x)=\mathrm{elu}(x)+1",
                    },
                ],
            },
            {
                "en": "We prefer elu(·) over relu(·) to avoid setting gradients to 0 when x is negative. Empirically this feature map performs on par with the full transformer while significantly reducing compute and memory.",
                "zh": "相对 relu，更偏好 elu，以免 x 为负时梯度被置零。经验上该特征映射性能与全 Transformer 相当，同时显著降低计算与内存。",
                "summary": "消融动机：正值相似度 + 可训练梯度。",
                "terms": ["elu+1"],
            },
        ],
    },
    {
        "id": "causal",
        "title": "3.3 因果掩码：线性时间 + 常数内存",
        "paras": [
            {
                "en": "Causal masking ensures position i is influenced only by positions j ≤ i. Softmax form becomes a prefix sum over similarities.",
                "zh": "因果掩码保证位置 i 只受 j≤i 影响。",
                "summary": "自回归训练的标准掩码约束。",
                "terms": ["causal masking"],
                "formulas": [
                    {
                        "tag": "因果 Softmax",
                        "latex": r"V'_i=\frac{\sum_{j=1}^{i}\mathrm{sim}(Q_i,K_j)V_j}{\sum_{j=1}^{i}\mathrm{sim}(Q_i,K_j)}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Linearized causal attention maintains two recurrent states—content memory S and normalizer Z—updated in constant time per step.",
                "zh": "线性化因果注意力维护两个递推状态——内容记忆 S 与归一化记忆 Z——每步常数时间更新。",
                "summary": "两个状态：内容记忆 S + 归一化记忆 Z。",
                "terms": ["S", "Z"],
                "figure": "rnn",
                "formulas": [
                    {
                        "tag": "因果线性读出",
                        "latex": r"V'_i=\frac{\phi(Q_i)^\top S_i}{\phi(Q_i)^\top Z_i}",
                    },
                    {
                        "tag": "状态定义",
                        "latex": r"S_i=\sum_{j\le i}\phi(K_j)V_j^\top,\quad Z_i=\sum_{j\le i}\phi(K_j)",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "A naive implementation stores all intermediate S_i for gradients, multiplying memory by max(D,M). The authors derive gradients via cumulative sums so both forward and backward of causal linear attention run in linear time and constant memory w.r.t. sequence length.",
                "zh": "朴素实现为求梯度需存所有中间 S_i，内存乘上 max(D,M)。作者用累加和形式推导梯度，使因果线性注意力前向与反向都对序列长度线性时间、常数内存。",
                "summary": "训练可行关键：常数内存反传（Algorithm 1 / CUDA）。",
                "terms": ["constant memory"],
            },
            {
                "en": "Training vs inference: with full ground truth available, layerwise parallelism still works for training. At inference, transformers normally recompute attention over all past steps (cost grows with square of current length). Linear transformers keep φ(K)Vᵀ as an internal state and update it each step like an RNN—constant cost per token.",
                "zh": "训练 vs 推理：有完整真值时仍可层间并行训练。推理时普通 Transformer 需对全部历史重算注意力（代价随当前长度平方涨）；线性 Transformer 把 φ(K)Vᵀ 当内部状态逐步更新，像 RNN——每 token 常数代价。",
                "summary": "两全：训练可并行，推理像 RNN。",
                "terms": ["autoregressive inference", "RNN"],
            },
        ],
    },
    {
        "id": "rnn",
        "title": "3.4 Transformers are RNNs",
        "paras": [
            {
                "en": "Any causally masked transformer layer can be written as a model that, given an input, modifies an internal state and then predicts an output—namely an RNN (recurrence over time, not depth as in Universal Transformers).",
                "zh": "任何带因果掩码的 Transformer 层都可写成：给定输入、修改内部状态、再预测输出——即 RNN（时间维递推，而非 Universal Transformers 那种深度维递推）。",
                "summary": "标题命题：因果 Transformer ≡ 某种 RNN。",
                "terms": ["RNN"],
            },
            {
                "en": "RNN form with two hidden states (attention memory s and normalizer z). See formula panels for the exact recurrence.",
                "zh": "双隐状态 RNN 形式（注意力记忆 s 与归一化记忆 z）。精确递推见下方公式卡。",
                "summary": "必背递推：累加 KV 外积与 K 特征，再用 q 特征归一化读出。",
                "terms": ["s", "Z", "φ"],
                "formulas": [
                    {
                        "tag": "状态更新",
                        "latex": r"s_i=s_{i-1}+\phi(x_i W_K)(x_i W_V)^\top,\quad z_i=z_{i-1}+\phi(x_i W_K)",
                        "wide": True,
                    },
                    {
                        "tag": "输出",
                        "latex": r"y_i=f_\ell\!\left(\frac{\phi(x_i W_Q)^\top s_i}{\phi(x_i W_Q)^\top z_i}+x_i\right)",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "This formulation imposes no constraint on the feature function and can represent any transformer in theory—even softmax ones (though exact softmax needs infinite features). It is a step toward understanding how transformers store and retrieve information relative to LSTMs.",
                "zh": "该形式对特征函数无额外约束，理论上可表示任意 Transformer——甚至 softmax 版（尽管精确 softmax 需要无穷维特征）。这是理解 Transformer 相对 LSTM 如何存取信息的一步。",
                "summary": "理论视野：线性化不只是加速技巧，也是统一视角。",
                "terms": ["feature map"],
            },
        ],
    },
    {
        "id": "expts",
        "title": "4 Experiments 实验要点",
        "paras": [
            {
                "en": "Baselines: full softmax transformer and Reformer (lsh-X). Feature map for linear: φ(x)=elu(x)+1. Code/demos at https://linear-transformers.com/; constant-memory gradients implemented in ~200 lines of CUDA.",
                "zh": "基线：全 softmax Transformer 与 Reformer（lsh-X）。线性模型特征映射：φ(x)=elu(x)+1。代码/演示见 linear-transformers.com；常数内存梯度约 200 行 CUDA。",
                "summary": "复现入口：官网 + CUDA 反传核。",
                "terms": ["elu+1", "Reformer"],
            },
            {
                "en": "Synthetic copy/duplication: linear converges smoothly to the same final loss as softmax, and lower than noisy LSH. Memory/time per sample scale linearly with N for linear and Reformer, while softmax scales quadratically (Fig.1, N up to 2^16).",
                "zh": "合成拷贝/复制任务：线性模型平滑收敛到与 softmax 相同的最终 loss，且低于带噪声的 LSH。每样本内存/时间对 N 线性扩展（linear 与 Reformer），softmax 仍二次（图 1，N 直至 2^16）。",
                "summary": "合成验证：收敛不差 + 资源真线性。",
                "terms": ["O(N)"],
            },
            {
                "en": "Image generation and ASR: linear transformers reach competitive / transformer-level performance with substantially less GPU memory and computation; autoregressive prediction of very long sequences can be up to ~4000× faster than vanilla transformers.",
                "zh": "图像生成与语音识别：线性 Transformer 达到有竞争力 / Transformer 级性能，同时 GPU 内存与计算显著更少；很长序列自回归预测最高可比原版快约 4000 倍。",
                "summary": "真实任务：质量跟得上，长解码拉开数量级差距。",
                "terms": ["autoregressive inference"],
            },
        ],
    },
    {
        "id": "bridge",
        "title": "桥接到后续：Delta / KDA / 混合架构",
        "paras": [
            {
                "en": "Bridge (study note): Katharopoulos linear attention is the ancestor of the “fixed-size state S” view used throughout modern linear-attention LLMs. Their recurrence s_i ← s_{i−1} + φ(k_i) v_iᵀ is exactly the additive online update that later papers reinterpret as fast-weight associative memory.",
                "zh": "桥接（学习笔记）：Katharopoulos 线性注意力是现代线性注意力 LLM 中「固定大小状态 S」视角的源头。其递推 s_i←s_{i−1}+φ(k_i)v_iᵀ，正是后来被重释为快权重联想记忆的加性在线更新。",
                "summary": "家族起点：只加不改的 S 累加器。",
                "terms": ["linear attention", "associative memory"],
            },
            {
                "en": "Limitations that later work attacks: (1) no forgetting—old associations interfere; (2) additive updates cannot correct wrong key→value bindings (hence DeltaNet’s delta rule); (3) scalar/channel gates (GDN/GLA/KDA) add data-dependent decay; (4) pure finite-state memory still struggles at retrieval, motivating hybrids like Kimi Linear (KDA:MLA=3:1).",
                "zh": "后续工作攻击的局限：(1) 无遗忘——旧关联互相干扰；(2) 加性更新不能纠正错误的 key→value 绑定（故有 DeltaNet 的 delta rule）；(3) 标量/通道门（GDN/GLA/KDA）加入数据相关衰减；(4) 纯有限状态检索仍吃力，催生 Kimi Linear 这类混合（KDA:MLA=3:1）。",
                "summary": "阅读地图：本文 → DeltaNet → GDN → KDA → 混合。",
                "terms": ["delta rule", "KDA", "Gated DeltaNet"],
            },
            {
                "en": "Suggested path in this repo: read this page’s §3.2–3.4 carefully; then papers/kimi-linear-delta-attention/index.html for the gated-delta upgrade; step through papers/kimi-linear-delta-attention/delta_attention/recurrent.py to see channel-wise forget + delta write on top of the same S-state idea.",
                "zh": "本仓库建议路径：先精读本页 §3.2–3.4；再读 papers/kimi-linear-delta-attention/index.html 看门控-delta 升级；最后跟同夹 delta_attention/recurrent.py，看在同一 S 状态思想上的通道遗忘 + delta 写入。",
                "summary": "学完这篇，再学 KDA 不会懵「S 从哪来」。",
                "terms": ["KDA", "recurrent_kda"],
            },
        ],
    },
]

GLOSSARY = [
    ("linear attention", "用核特征把注意力写成可结合的点积，使复杂度对长度线性。"),
    ("Linear Transformers", "本文提出的线性注意力 Transformer 模型族。"),
    ("quadratic complexity", "标准自注意力对序列长度 N 的 O(N²) 时空代价。"),
    ("O(N)", "线性注意力相对序列长度的渐近复杂度。"),
    ("kernel feature maps", "把 query/key 映射到特征空间，使 sim(q,k)=φ(q)ᵀφ(k)。"),
    ("φ", "特征映射函数；本文实验用 elu(x)+1。"),
    ("associativity", "矩阵乘法结合律：(AB)C=A(BC)，用于重排注意力计算顺序。"),
    ("softmax attention", "sim=exp(qᵀk/√D) 的标准注意力。"),
    ("self-attention", "序列内部用 Q/K/V 计算的注意力。"),
    ("causal masking", "位置 i 只能看见 j≤i，用于自回归。"),
    ("S", "因果线性注意力中的内容状态 Σ φ(k)vᵀ。"),
    ("Z", "归一化状态 Σ φ(k)，用于分母。"),
    ("s", "RNN 写法中的注意力记忆（同 S 的递推形式）。"),
    ("RNN", "逐步更新隐状态并产出输出的循环模型；本文证明因果 Transformer 可写成 RNN。"),
    ("autoregressive inference", "逐步生成：每步输出作为下一步输入。"),
    ("elu+1", "φ(x)=elu(x)+1，保证非负相似度并保留负区梯度。"),
    ("feature map", "同 φ：核对应的显式特征函数。"),
    ("constant memory", "相对序列长度，激活/状态内存不随 N 增长（推理或特化反传）。"),
    ("Transformer", "以自注意力为核心的序列模型。"),
    ("Q", "查询矩阵/向量。"),
    ("K", "键矩阵/向量。"),
    ("V", "值矩阵/向量。"),
    ("similarity function", "广义注意力中的 sim(q,k)≥0。"),
    ("Sparse Transformer", "Child et al. 用稀疏因子分解降复杂度的模型。"),
    ("Reformer", "Kitaev et al. 用 LSH 近似注意力的模型。"),
    ("LSH", "Locality-Sensitive Hashing，局部敏感哈希。"),
    ("delta rule", "后续 DeltaNet：按 key 擦旧再写新的更新，改进纯加性 S。"),
    ("Gated DeltaNet", "在 delta rule 上加标量遗忘门的线性注意力。"),
    ("KDA", "Kimi Delta Attention：通道级门控的 delta 线性注意力。"),
    ("associative memory", "把 key 映射到 value 的可写可读记忆（状态 S）。"),
    ("recurrent_kda", "本仓库 KDA 逐步递推实现。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "Transformers are RNNs (Linear Attention)",
        "why": "逐段精读对象；线性注意力经典源头。",
        "url": "./paper.pdf",
        "ext": "https://arxiv.org/abs/2006.16236",
    },
    {
        "level": "官网",
        "title": "linear-transformers.com",
        "why": "作者页：公式演示与代码入口。",
        "url": "https://linear-transformers.com/",
        "ext": "",
    },
    {
        "level": "下游",
        "title": "Kimi Linear / KDA 逐段精读",
        "why": "在加性 S 上加入遗忘门与 delta rule 的现代升级。",
        "url": "../kimi-linear-delta-attention/index.html",
        "ext": "https://arxiv.org/abs/2510.26692",
    },
    {
        "level": "对照",
        "title": "Reformer",
        "why": "同期高效注意力；训练可扩但解码约束不同。",
        "url": "https://arxiv.org/abs/2001.04451",
        "ext": "",
    },
    {
        "level": "代码",
        "title": "KDA 教学代码（同夹于 Kimi Linear）",
        "why": "看清「同一 S 状态」如何演变成 KDA。",
        "url": "../kimi-linear-delta-attention/delta_attention/",
        "ext": "",
    },
]
