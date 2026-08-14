"""Fine-grained study notes for Attention Is All You Need.

Paper: Vaswani et al., NIPS 2017. arXiv:1706.03762.

Core methods (§3) are split near sentence-level, with extra teaching
paragraphs that unpack shapes, steps, and why each trick exists.
"""

FORMULA_WALL = [
    {
        "tag": "缩放点积注意力（式 1）",
        "latex": r"\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V",
        "note": "先算 N×N 分数，缩放，softmax 成权重，再加权 V。这就是 O(N²) 的源头。",
        "wide": True,
    },
    {
        "tag": "多头（式 2–3）",
        "latex": r"\mathrm{MultiHead}(Q,K,V)=\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)W^O",
        "note": r"每个 head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V)。",
        "wide": True,
    },
    {
        "tag": "残差 + LayerNorm",
        "latex": r"x \leftarrow \mathrm{LayerNorm}\bigl(x + \mathrm{Sublayer}(x)\bigr)",
        "note": "每个子层（注意力或 FFN）外包这一层。",
        "wide": True,
    },
    {
        "tag": "逐位置 FFN（式 2）",
        "latex": r"\mathrm{FFN}(x)=\max(0,xW_1+b_1)W_2+b_2",
        "note": "位置之间不混合；混合只发生在注意力里。",
        "wide": True,
    },
    {
        "tag": "正弦位置编码",
        "latex": r"PE_{(pos,2i)}=\sin\!\bigl(pos/10000^{2i/d_{\mathrm{model}}}\bigr),\quad PE_{(pos,2i+1)}=\cos\!\bigl(pos/10000^{2i/d_{\mathrm{model}}}\bigr)",
        "note": "没有 RNN，位置信息必须另加。",
        "wide": True,
    },
]

SECTIONS = [
    {
        "id": "zero",
        "title": "从零：注意力在干什么（导读，请先读）",
        "paras": [
            {
                "en": "Teaching note. Sequence transduction (e.g. translation) maps a source sequence of tokens to a target sequence. Before 2017 the default was RNN/CNN encoder–decoder: the encoder compressed the source, the decoder generated the target one step at a time.",
                "zh": "导读。序列转导（如翻译）要把一串源词变成一串目标词。2017 年前默认是 RNN/CNN 编码器–解码器：编码器把源句压成状态，解码器逐步吐出目标词。",
                "summary": "任务先立住：源序列 → 目标序列。",
                "terms": ["sequence transduction", "encoder-decoder"],
            },
            {
                "en": "Teaching note. RNNs mix information over time by hidden-state recurrence. That mixing is sequential: token 5 cannot be processed until tokens 1–4 are done. Training therefore cannot fully parallelize over the length axis. The Transformer’s bet: replace recurrence with a mixing operator that looks at the whole sequence at once.",
                "zh": "导读。RNN 靠隐状态沿时间混信息，所以必须按顺序算：第 5 个词要等前 4 个算完。训练没法在长度维上完全并行。Transformer 的赌注：换一个能一眼看完整句的混合算子。",
                "summary": "RNN 的痛：算得对，但算不并行。",
                "terms": ["RNN", "parallelization"],
            },
            {
                "en": "Teaching note. Name the three roles after a dictionary. Query = the question you are asking now. Key = the label on each stored item. Value = the content of that item. Attention: compare the current query with every key, turn similarities into weights, return a weighted mix of values.",
                "zh": "导读。三个角色按「查字典」来记。Query = 此刻要问的问题。Key = 每条记录上的标签。Value = 记录里的内容。注意力：用当前 query 去对所有 key 打分，分数变成权重，再按权重混合 value。",
                "summary": "Q 提问，K 当标签，V 给内容。",
                "terms": ["Q", "K", "V", "attention"],
                "figure": "qkv",
            },
            {
                "en": "Teaching note. Concrete shapes for one sentence of N tokens, model width d_model. Input X ∈ R^{N×d_model}. Three learned matrices make Q=X W^Q, K=X W^K, V=X W^V. Then the score matrix is Q Kᵀ ∈ R^{N×N}: entry (i,j) is “how much token i wants to read token j”.",
                "zh": "导读。N 个词、模型宽度 d_model。输入 X∈R^{N×d_model}。三个可学矩阵做出 Q、K、V。分数矩阵 QKᵀ∈R^{N×N}：第 (i,j) 格是「第 i 个词想读第 j 个词有多想」。",
                "summary": "形状锚点：X 是 N×d；QKᵀ 是 N×N。",
                "terms": ["d_model", "attention matrix"],
                "formulas": [
                    {
                        "tag": "投影成 Q/K/V",
                        "latex": r"Q=XW^Q,\quad K=XW^K,\quad V=XW^V",
                        "note": "自注意力里三者都来自同一段 X；编码器–解码器注意力里 Q 来自解码器，K/V 来自编码器。",
                        "wide": True,
                    },
                    {
                        "tag": "形状",
                        "latex": r"X\in\mathbb{R}^{N\times d_{\mathrm{model}}},\; QK^\top\in\mathbb{R}^{N\times N},\; \mathrm{softmax}(\cdot)V\in\mathbb{R}^{N\times d_v}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Teaching note. Softmax turns a row of raw scores into non-negative weights that sum to 1. So each query reads a convex combination of values—never “all of one token and none of the others” unless one score dominates. That is why attention can softly copy, average, or ignore.",
                "zh": "导读。Softmax 把一行原始分数变成非负、和为 1 的权重。于是每个 query 读到的是 value 的凸组合——除非某一格特别大，否则不会「只看一个词」。所以注意力能软拷贝、软平均、软忽略。",
                "summary": "softmax = 把打分成「读多少」。",
                "terms": ["softmax"],
                "formulas": [
                    {
                        "tag": "按行归一化",
                        "latex": r"\alpha_{ij}=\frac{e^{s_{ij}}}{\sum_{j'}e^{s_{ij'}}},\quad y_i=\sum_j \alpha_{ij} v_j",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Teaching note. Self-attention means Q, K, V are all produced from the same sequence. Encoder–decoder attention means Q comes from the target side while K,V come from the source side. Causal (masked) self-attention further forbids looking at future target tokens, so generation stays left-to-right.",
                "zh": "导读。自注意力：Q、K、V 都来自同一段序列。编码器–解码器注意力：Q 来自目标侧，K/V 来自源侧。因果（掩码）自注意力再禁止看未来的目标词，生成才能从左到右。",
                "summary": "三种用法：自注意 / 交叉注意 / 因果自注意。后文 §3.2.3 会再讲。",
                "terms": ["self-attention", "encoder-decoder attention", "causal masking"],
            },
            {
                "en": "Teaching note. The N×N score matrix is the cost. Time and memory both scale as O(N²) if you materialize it. Every later paper in this repo is a reaction to that square: sparse attention deletes most (i,j) edges; linear attention never builds the matrix; FlashAttention still computes full attention but tiles it to spare HBM.",
                "zh": "导读。代价就在这张 N×N 分数表。若把它完整造出来，时间与内存都是 O(N²)。本仓库后面的论文全是在对这个平方作出反应：稀疏注意力删掉大多数 (i,j) 边；线性注意力根本不造这张表；FlashAttention 仍算全注意力，但分块算以省显存。",
                "summary": "读完本页你该能指着 QKᵀ 说：稀疏 = 不让多数格参与 softmax。",
                "terms": ["quadratic complexity", "sparse attention", "linear attention"],
                "figure": "cost",
            },
        ],
    },
    {
        "id": "abstract",
        "title": "Abstract 摘要",
        "paras": [
            {
                "en": "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism.",
                "zh": "当时主流的序列转导模型基于复杂的循环或卷积网络，并包含编码器与解码器。表现最好的模型还会用注意力把编码器和解码器连起来。",
                "summary": "2017 年的默认配方：RNN/CNN + 一点注意力。",
                "terms": ["sequence transduction", "attention"],
            },
            {
                "en": "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely.",
                "zh": "我们提出一种新的简单网络结构——Transformer，完全基于注意力机制，彻底去掉循环与卷积。",
                "summary": "标题落地：Attention is all you need。",
                "terms": ["Transformer"],
            },
            {
                "en": "Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.",
                "zh": "在两项机器翻译任务上的实验表明：质量更好，更可并行，训练时间显著更少。",
                "summary": "卖点不只是 BLEU，还有「训得快」。",
                "terms": ["parallelization"],
            },
            {
                "en": "Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On WMT 2014 English-to-French it establishes a new single-model SOTA of 41.8 BLEU after 3.5 days on eight GPUs.",
                "zh": "WMT14 英德达到 28.4 BLEU，比当时最佳（含集成）高 2 分以上。英法在 8 块 GPU 上训 3.5 天达到单模型 41.8 BLEU。",
                "summary": "数字锚：28.4 / 41.8；硬件锚：8 GPU × 3.5 天。",
                "terms": ["BLEU"],
            },
        ],
    },
    {
        "id": "intro",
        "title": "1 Introduction 引言",
        "paras": [
            {
                "en": "Recurrent neural networks, long short-term memory and gated recurrent neural networks in particular, have been firmly established as state of the art in sequence modeling and transduction.",
                "zh": "循环网络，尤其是 LSTM 与门控 RNN，当时已被视为序列建模与转导的主流。",
                "summary": "先承认：RNN 家族是当时的 SOTA。",
                "terms": ["RNN", "LSTM"],
            },
            {
                "en": "The number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions, linearly for ConvS2S and logarithmically for ByteNet. This makes it more difficult to learn dependencies between distant positions.",
                "zh": "要让任意两个位置的信号发生关系，所需运算次数随距离增长：ConvS2S 线性、ByteNet 对数。这让远距离依赖更难学。",
                "summary": "卷积路径：位置离得越远，信息要走的步数越多。",
                "terms": ["long-range dependency"],
            },
            {
                "en": "In this work we propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new SOTA in translation after being trained for as little as twelve hours on eight P100 GPUs.",
                "zh": "本文提出 Transformer：抛弃循环，完全靠注意力抽取输入与输出之间的全局依赖。它可大幅并行；在 8 块 P100 上最短约 12 小时即可达到翻译新 SOTA。",
                "summary": "全局一步到位 + 训练可并行。",
                "terms": ["Transformer", "self-attention"],
            },
        ],
    },
    {
        "id": "background",
        "title": "2 Background 背景（精要）",
        "paras": [
            {
                "en": "The goal of reducing sequential computation also forms the foundation of the Extended Neural GPU, ByteNet and ConvS2S, all of which use convolutional neural networks as basic building block, computing hidden representations in parallel for all input and output positions.",
                "zh": "减少顺序计算这一目标，也是 Extended Neural GPU、ByteNet 与 ConvS2S 的基础——它们用卷积做积木，可对所有输入/输出位置并行算隐表示。",
                "summary": "前人已经在「去循环」；本文换注意力来去。",
                "terms": [],
            },
            {
                "en": "Self-attention, sometimes called intra-attention, is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence. End-to-end memory networks are based on a recurrent attention mechanism instead of sequence-aligned recurrence.",
                "zh": "自注意力（也称内部注意力）让同一序列的不同位置互相发生关系，从而算出该序列的表示。端到端记忆网络则用循环注意力，而不是与序列对齐的循环。",
                "summary": "自注意力不是本文发明的词，但本文把它做成整座楼的承重墙。",
                "terms": ["self-attention"],
            },
        ],
    },
    {
        "id": "arch",
        "title": "3 总览：编码器–解码器栈",
        "paras": [
            {
                "en": "The Transformer follows this overall architecture using stacked self-attention and point-wise, fully connected layers for both the encoder and decoder, shown in the left and right halves of Figure 1.",
                "zh": "Transformer 沿用编码器–解码器总结构：两侧都是堆叠的自注意力与逐位置全连接层，见图 1 左右两半。",
                "summary": "整张图只干两件事：注意（混位置）+ FFN（混通道）。",
                "terms": ["encoder-decoder", "Transformer"],
                "figure": "arch",
            },
            {
                "en": "Encoder: The encoder is composed of a stack of N=6 identical layers. Each layer has two sub-layers: a multi-head self-attention mechanism, and a simple, position-wise fully connected feed-forward network.",
                "zh": "编码器：N=6 层相同的栈。每层两个子层：多头自注意力，以及简单的逐位置全连接前馈网络。",
                "summary": "编码器一层 = 多头自注意 + FFN。",
                "terms": ["encoder", "N=6"],
            },
            {
                "en": "We employ a residual connection around each of the two sub-layers, followed by layer normalization. That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself.",
                "zh": "每个子层外包残差连接，再接层归一化。即输出为 LayerNorm(x + Sublayer(x))，其中 Sublayer(x) 是该子层本身。",
                "summary": "记这一句：先加回去，再 LayerNorm。",
                "terms": ["residual", "LayerNorm"],
                "formulas": [
                    {
                        "tag": "子层包装",
                        "latex": r"\mathrm{LayerNorm}\bigl(x+\mathrm{Sublayer}(x)\bigr)",
                        "note": "Sublayer 是 MultiHead 或 FFN。训练时对 Sublayer 输出做 dropout。",
                    },
                ],
            },
            {
                "en": "To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension d_model = 512.",
                "zh": "为了残差能直接相加，模型中所有子层以及嵌入层的输出维都是 d_model=512。",
                "summary": "宽度约定：全程 512 维对齐。",
                "terms": ["d_model"],
            },
            {
                "en": "Decoder: The decoder is also composed of a stack of N=6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack.",
                "zh": "解码器同样 N=6 层。在编码器那两个子层之外，再插入第三个子层：对编码器栈的输出做多头注意力。",
                "summary": "解码器一层 = 掩码自注意 + 交叉注意 + FFN。",
                "terms": ["decoder", "encoder-decoder attention"],
            },
            {
                "en": "Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization. We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions. This masking, combined with the fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.",
                "zh": "解码器同样残差 + LayerNorm。另外把解码器自注意力改成：禁止位置去看后面的位置。该掩码再加上输出嵌入右移一位，保证预测位置 i 只依赖已经知道的 <i 输出。",
                "summary": "因果掩码 = 生成时不能偷看未来。",
                "terms": ["causal masking", "auto-regressive"],
                "figure": "mask",
            },
        ],
    },
    {
        "id": "attn-def",
        "title": "3.2 注意力在定义上是什么",
        "paras": [
            {
                "en": "An attention function can be described as mapping a query and a set of key-value pairs to an output, where the query, keys, values, and output are all vectors.",
                "zh": "注意力函数可以描述为：把一个 query 和一组 key–value 对映射成一个输出；query、key、value 与输出都是向量。",
                "summary": "接口： (query, {(key,value)}) → output。",
                "terms": ["attention", "Q", "K", "V"],
            },
            {
                "en": "The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.",
                "zh": "输出是 value 的加权和；每个 value 的权重，由 query 与对应 key 的相容性函数算出。",
                "summary": "两步：相容性打分 → 用分数加权 V。",
                "terms": ["compatibility function"],
                "formulas": [
                    {
                        "tag": "定义（尚未指定打分）",
                        "latex": r"y=\sum_j \alpha(q,k_j)\, v_j",
                        "note": "α 由相容性函数再归一化得到。下一节把相容性定成缩放点积。",
                    },
                ],
            },
        ],
    },
    {
        "id": "scaled",
        "title": "3.2.1 缩放点积注意力（核心，请逐步读）",
        "paras": [
            {
                "en": "We call our particular attention “Scaled Dot-Product Attention” (Figure 2). The input consists of queries and keys of dimension d_k, and values of dimension d_v.",
                "zh": "我们把所用的注意力叫做「缩放点积注意力」（图 2）。输入是维度为 d_k 的 query/key，以及维度为 d_v 的 value。",
                "summary": "名字拆开：点积打分 + 除以 √d_k。",
                "terms": ["scaled dot-product attention", "d_k", "d_v"],
                "figure": "scaled",
            },
            {
                "en": "We compute the dot products of the query with all keys, divide each by √d_k, and apply a softmax function to obtain the weights on the values.",
                "zh": "用 query 与所有 key 做点积，每个再除以 √d_k，然后 softmax，得到加在 value 上的权重。",
                "summary": "四个动作：点积 → 缩放 → softmax → 加权 V。",
                "terms": ["softmax"],
            },
            {
                "en": "Teaching note. Step A — scores. For one query q ∈ R^{d_k} and keys stacked as K ∈ R^{N×d_k}, the vector of raw scores is K q (or q Kᵀ in row convention). Entry j is q·k_j: alignment of “what I ask” with “what this position is about”.",
                "zh": "导读。步骤 A — 打分。一个 query q∈R^{d_k}，key 排成 K∈R^{N×d_k}，原始分数是各 q·k_j：问的内容与该位置「关于什么」有多齐。",
                "summary": "点积大 = 方向像 = 更该读这个 value。",
                "terms": ["Q", "K"],
                "formulas": [
                    {
                        "tag": "步骤 A · 分数",
                        "latex": r"s_j = q^\top k_j \quad (j=1,\ldots,N)",
                        "note": "批量写法：S = Q Kᵀ，形状 N_q × N_k。",
                    },
                ],
            },
            {
                "en": "Teaching note. Step B — scale. Divide every score by √d_k before softmax. This is not a normalization of the vectors themselves; it only shrinks the logits. Why: if q and k have roughly independent coordinates of variance 1, then q·k has variance d_k, so typical scores grow like √d_k. Large logits make softmax peaky and gradients tiny.",
                "zh": "导读。步骤 B — 缩放。softmax 之前把每个分数除以 √d_k。这不是把向量本身单位化，只是把 logit 缩小。原因：若 q、k 各维近似独立且方差为 1，则 q·k 的方差是 d_k，典型分数按 √d_k 变大。logit 太大时 softmax 又尖、梯度又小。",
                "summary": "√d_k 是为了 softmax 别饱和，不是为了「除个常数好看」。",
                "terms": ["scaled dot-product attention", "d_k"],
                "formulas": [
                    {
                        "tag": "步骤 B · 缩放",
                        "latex": r"\tilde s_j=\frac{q^\top k_j}{\sqrt{d_k}}",
                        "note": "原文：无缩放时，大 d_k 下加性注意力更稳；加上 1/√d_k 后点积可用。",
                    },
                    {
                        "tag": "方差直觉",
                        "latex": r"q,k\sim\text{坐标方差 }1 \;\Rightarrow\; \mathrm{Var}(q^\top k)\approx d_k",
                    },
                ],
            },
            {
                "en": "Teaching note. Step C — softmax. Apply softmax over keys for this query. Weights α_j ≥ 0 and sum to 1. Optional causal mask: set illegal scores to −∞ before softmax so their α becomes 0 (decoder self-attention).",
                "zh": "导读。步骤 C — softmax。对这个 query 在 key 维上做 softmax。权重 α_j≥0 且和为 1。可选因果掩码：非法分数在 softmax 前设为 −∞，对应 α 变成 0（解码器自注意力）。",
                "summary": "掩码不是另做一层，是改 softmax 的输入。",
                "terms": ["softmax", "causal masking"],
                "formulas": [
                    {
                        "tag": "步骤 C · 权重",
                        "latex": r"\alpha_j=\mathrm{softmax}_j(\tilde s)=\frac{e^{\tilde s_j}}{\sum_{j'}e^{\tilde s_{j'}}}",
                    },
                ],
            },
            {
                "en": "Teaching note. Step D — mix values. Output y = Σ_j α_j v_j ∈ R^{d_v}. If one α is ~1, you almost copy that value; if α is spread out, you average. That is the entire attention: a data-dependent pooling over the sequence.",
                "zh": "导读。步骤 D — 混合 value。输出 y=Σ_j α_j v_j ∈ R^{d_v}。某个 α≈1 就几乎拷贝那个 value；α 摊开就是平均。注意力的全部：按数据决定怎么池化整段序列。",
                "summary": "输出仍是 d_v 维向量，不是那张 N×N 表。",
                "terms": ["V"],
                "formulas": [
                    {
                        "tag": "步骤 D · 加权",
                        "latex": r"y=\sum_j \alpha_j v_j",
                    },
                ],
            },
            {
                "en": "In practice, we compute the attention function on a set of queries simultaneously, packed together into a matrix Q. The keys and values are also packed together into matrices K and V. We compute the matrix of outputs as: Attention(Q, K, V) = softmax(Q Kᵀ / √d_k) V.",
                "zh": "实践中把一组 query 打成矩阵 Q，key、value 打成 K、V，一次算完：Attention(Q,K,V)=softmax(QKᵀ/√d_k) V。",
                "summary": "式 (1)：四个步骤的矩阵版。请对着形状读。",
                "terms": ["scaled dot-product attention"],
                "formulas": [
                    {
                        "tag": "原文式 (1)",
                        "latex": r"\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V",
                        "note": "Q: N_q×d_k；K: N_k×d_k；V: N_k×d_v；输出: N_q×d_v。中间 QKᵀ 是 N_q×N_k。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "The two most commonly used attention functions are additive attention (Bahdanau et al., 2015) and dot-product (multiplicative) attention. Dot-product attention is identical to our algorithm, except for the scaling factor of 1/√d_k. Additive attention computes the compatibility function using a feed-forward network with a single hidden layer.",
                "zh": "当时最常用的两种注意力是加性注意力（Bahdanau 2015）与点积（乘性）注意力。点积注意力与本算法相同，只是没有 1/√d_k 这个缩放。加性注意力用带单隐层的前馈网做相容性。",
                "summary": "对照：Bahdanau 用小网络打分；这里用点积，能吃矩阵乘。",
                "terms": ["additive attention"],
            },
            {
                "en": "While the two are similar in theoretical complexity, dot-product attention is much faster and more space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code.",
                "zh": "二者理论复杂度相近，但点积注意力实践中更快、更省空间，因为它能用高度优化的矩阵乘法实现。",
                "summary": "选点积的工程理由：matmul 是现成最快原语。",
                "terms": ["scaled dot-product attention"],
            },
            {
                "en": "While for small values of d_k the two mechanisms perform similarly, additive attention outperforms dot product attention without scaling for larger values of d_k. We suspect that for large values of d_k, the dot products grow large in magnitude, pushing the softmax function into regions where it has extremely small gradients. To counteract this effect, we scale the dot products by 1/√d_k.",
                "zh": "d_k 小时两者差不多；d_k 大且不缩放时，加性注意力更好。我们怀疑大 d_k 下点积幅值变大，把 softmax 推到梯度极小的区域。因此把点积除以 √d_k。",
                "summary": "缩放的论文原话：对抗 softmax 饱和。",
                "terms": ["d_k", "softmax"],
            },
        ],
    },
    {
        "id": "mha",
        "title": "3.2.2 多头注意力（核心，请逐步读）",
        "paras": [
            {
                "en": "Instead of performing a single attention function with d_model-dimensional keys, values and queries, we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections to d_k, d_v and d_k dimensions, respectively.",
                "zh": "不是只用一组 d_model 维的 Q/K/V 做一次注意力，我们发现：用 h 组不同的、可学习的线性投影，分别把 Q/K/V 投到 d_k、d_v、d_k 维，会更好。",
                "summary": "多头的「头」= 一套独立的投影矩阵。",
                "terms": ["multi-head attention", "h"],
                "figure": "mha",
            },
            {
                "en": "On each of these projected versions of queries, keys and values we then perform the attention function in parallel, yielding d_v-dimensional output values. These are concatenated and once again projected, resulting in the final values, as depicted in Figure 2.",
                "zh": "在每组投影后的 Q/K/V 上并行做注意力，得到 d_v 维输出；再拼接，再投影一次，得到最终值，见图 2。",
                "summary": "流程：分头投影 → 各头注意力 → 拼接 → W^O 混回去。",
                "terms": ["W^O"],
            },
            {
                "en": "Teaching note. Why not one fat head? A single softmax is a single distribution over keys. It tends to average. Multiple heads let the layer keep several different distributions at once—e.g. one head on syntax, one on the previous mention of an entity, one on positional neighbors—then W^O mixes those views.",
                "zh": "导读。为什么不做成一个很宽的单头？一次 softmax 只是对 key 的一个分布，容易平均掉。多头让一层同时保留好几套分布——例如一头看句法、一头看实体的上次提及、一头看位置邻居——再由 W^O 把这些视角混起来。",
                "summary": "多头 = 并行的多种「读法」，不是把维度切着好玩。",
                "terms": ["multi-head attention", "representation subspaces"],
            },
            {
                "en": "MultiHead(Q, K, V) = Concat(head_1, …, head_h) W^O where head_i = Attention(Q W_i^Q, K W_i^K, V W_i^V).",
                "zh": "MultiHead(Q,K,V)=Concat(head_1,…,head_h) W^O，其中 head_i=Attention(Q W_i^Q, K W_i^K, V W_i^V)。",
                "summary": "式 (2)(3)：先各头缩放点积，再拼接投影。",
                "terms": ["multi-head attention"],
                "formulas": [
                    {
                        "tag": "原文式 (2)",
                        "latex": r"\mathrm{MultiHead}(Q,K,V)=\mathrm{Concat}(\mathrm{head}_1,\ldots,\mathrm{head}_h)\,W^O",
                        "wide": True,
                    },
                    {
                        "tag": "原文式 (3)",
                        "latex": r"\mathrm{head}_i=\mathrm{Attention}(QW_i^Q,\,KW_i^K,\,VW_i^V)",
                        "note": "这里的 Attention 就是上一节的缩放点积。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "Where the projections are parameter matrices W_i^Q ∈ R^{d_model × d_k}, W_i^K ∈ R^{d_model × d_k}, W_i^V ∈ R^{d_model × d_v} and W^O ∈ R^{h d_v × d_model}.",
                "zh": "投影参数：W_i^Q、W_i^K ∈ R^{d_model×d_k}，W_i^V ∈ R^{d_model×d_v}，W^O ∈ R^{h d_v × d_model}。",
                "summary": "参数形状：每头三块小矩阵 + 一块拼回去的 W^O。",
                "terms": ["W^Q", "W^K", "W^V", "W^O"],
                "formulas": [
                    {
                        "tag": "参数形状",
                        "latex": r"W_i^Q,W_i^K\in\mathbb{R}^{d_{\mathrm{model}}\times d_k},\; W_i^V\in\mathbb{R}^{d_{\mathrm{model}}\times d_v},\; W^O\in\mathbb{R}^{hd_v\times d_{\mathrm{model}}}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "In this work we employ h = 8 parallel attention layers, or heads. For each of these we use d_k = d_v = d_model / h = 64. Due to the reduced dimension of each head, the total computational cost is similar to that of single-head attention with full dimensionality.",
                "zh": "本文用 h=8 个并行注意力头。每头 d_k=d_v=d_model/h=64。由于每头维度缩小，总计算量与「用满宽度做单头」相近。",
                "summary": "数字：512 维切成 8×64；多头几乎不额外加价。",
                "terms": ["h", "d_k", "d_model"],
                "formulas": [
                    {
                        "tag": "本文设定",
                        "latex": r"h=8,\quad d_{\mathrm{model}}=512,\quad d_k=d_v=64",
                        "note": "实现上常把 h 个头的投影做成一块大矩阵再 reshape，数值等价。",
                    },
                ],
            },
            {
                "en": "Teaching note. Shape walk-through. Start with X ∈ R^{N×512}. After the Q projection you have Q ∈ R^{N×512}, then view it as R^{N×8×64}. Each of the 8 slices is one head’s queries. Attention is run independently per head (8 different N×N score maps). Concatenate the 8 outputs of size N×64 back to N×512, then multiply W^O.",
                "zh": "导读。形状走一遍。X∈R^{N×512}。Q 投影后仍是 N×512，再看成 N×8×64；8 片就是 8 头的 query。每头独立做注意力（8 张不同的 N×N 分数图）。8 个 N×64 输出拼回 N×512，再乘 W^O。",
                "summary": "实现口诀：reshape 成分头 → 各算各的 → concat → 线性混。",
                "terms": ["multi-head attention"],
            },
            {
                "en": "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions. With a single attention head, averaging inhibits this.",
                "zh": "多头注意力让模型能联合关注不同位置、不同表示子空间里的信息。单头时，平均会抑制这种能力。",
                "summary": "原文动机句：单头会平均掉子空间。",
                "terms": ["representation subspaces"],
            },
        ],
    },
    {
        "id": "apps",
        "title": "3.2.3 三种用法：自注意 / 交叉注意 / 掩码",
        "paras": [
            {
                "en": "The Transformer uses multi-head attention in three different ways.",
                "zh": "Transformer 在三处使用多头注意力，用法不同。",
                "summary": "同一套 MultiHead 公式，Q/K/V 来源不同。",
                "terms": ["multi-head attention"],
                "figure": "three",
            },
            {
                "en": "In “encoder-decoder attention” layers, the queries come from the previous decoder layer, and the memory keys and values come from the output of the encoder stack. This allows every position in the decoder to attend over all positions in the input sequence. This mimics the typical encoder-decoder attention mechanisms in sequence-to-sequence models.",
                "zh": "编码器–解码器注意力层：query 来自上一层解码器，key/value 来自编码器栈输出。于是解码器每个位置都能看完整句输入。这模仿了 seq2seq 里典型的编解码注意力。",
                "summary": "交叉注意：目标侧提问，源侧提供档案。",
                "terms": ["encoder-decoder attention"],
                "formulas": [
                    {
                        "tag": "交叉注意的来源",
                        "latex": r"Q\leftarrow \text{decoder},\quad K,V\leftarrow \text{encoder}",
                    },
                ],
            },
            {
                "en": "The encoder contains self-attention layers. In a self-attention layer all of the keys, values and queries come from the same place, in this case, the output of the previous layer in the encoder. Each position in the encoder can attend to all positions in the previous layer of the encoder.",
                "zh": "编码器里是自注意力层：Q/K/V 都来自编码器上一层输出。编码器每个位置都能看到上一层的所有位置。",
                "summary": "编码侧：每个词可以看全句（无因果掩码）。",
                "terms": ["self-attention", "encoder"],
            },
            {
                "en": "Similarly, self-attention layers in the decoder allow each position in the decoder to attend to all positions in the decoder up to and including that position. We need to prevent leftward information flow in the decoder to preserve the auto-regressive property. We implement this inside of scaled dot-product attention by masking out (setting to −∞) all values in the input of the softmax which correspond to illegal connections.",
                "zh": "解码器自注意力：每个位置只能看自己及之前的位置。为保持自回归，要阻止信息从右往左流。实现方式：在缩放点积内部，把非法连接对应的 softmax 输入设为 −∞。",
                "summary": "解码侧：下三角掩码；非法格进 −∞ 再 softmax。",
                "terms": ["causal masking", "auto-regressive", "decoder"],
                "formulas": [
                    {
                        "tag": "因果掩码",
                        "latex": r"s_{ij}\leftarrow -\infty \quad\text{if } j>i",
                        "note": "softmax(−∞)=0，等价于不读未来。",
                    },
                ],
            },
        ],
    },
    {
        "id": "ffn",
        "title": "3.3 逐位置前馈网络",
        "paras": [
            {
                "en": "In addition to attention sub-layers, each of the layers in our encoder and decoder contains a fully connected feed-forward network, which is applied to each position separately and identically. This consists of two linear transformations with a ReLU activation in between.",
                "zh": "除注意力子层外，编码器与解码器每层还有一个全连接前馈网：对每个位置单独、相同地作用。它是两层线性变换，中间夹 ReLU。",
                "summary": "FFN 不看邻居；邻居混合只发生在注意力里。",
                "terms": ["FFN", "ReLU"],
                "formulas": [
                    {
                        "tag": "原文 FFN",
                        "latex": r"\mathrm{FFN}(x)=\max(0,xW_1+b_1)W_2+b_2",
                        "note": "输入输出维 d_model=512；内层 d_ff=2048。可看成核大小 1 的卷积。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "While the linear transformations are the same across different positions, they use different parameters from layer to layer. Another way of describing this is as two convolutions with kernel size 1. The dimensionality of input and output is d_model = 512, and the inner-layer has dimensionality d_ff = 2048.",
                "zh": "不同位置共用同一套线性变换，但层与层参数不同。也可看成两层核大小为 1 的卷积。输入输出 512 维，内层 2048 维。",
                "summary": "扩到 2048 再压回 512：通道上的非线性。",
                "terms": ["d_ff", "d_model"],
            },
        ],
    },
    {
        "id": "embed",
        "title": "3.4 嵌入与 Softmax",
        "paras": [
            {
                "en": "Similarly to other sequence transduction models, we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model. We also use the usual learned linear transformation and softmax function to convert the decoder output to predicted next-token probabilities.",
                "zh": "与其他序列转导模型一样：用可学习嵌入把输入/输出 token 变成 d_model 维向量；解码器输出再经线性层 + softmax 变成下一个 token 的概率。",
                "summary": "两端仍是标准词嵌入与词表 softmax。",
                "terms": ["embedding", "softmax"],
            },
            {
                "en": "In our model, we share the same weight matrix between the two embedding layers and the pre-softmax linear transformation. In the embedding layers, we multiply those weights by √d_model.",
                "zh": "两个嵌入层与 softmax 前的线性层共享同一权重矩阵。嵌入时把这些权重乘以 √d_model。",
                "summary": "词表矩阵共用；嵌入再乘 √d_model 做尺度匹配。",
                "terms": ["d_model"],
            },
        ],
    },
    {
        "id": "posenc",
        "title": "3.5 位置编码（没有 RNN 之后必须补的）",
        "paras": [
            {
                "en": "Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence. To this end, we add “positional encodings” to the input embeddings at the bottoms of the encoder and decoder stacks. The positional encodings have the same dimension d_model as the embeddings, so that the two can be summed.",
                "zh": "模型既无循环也无卷积，要利用词序，就必须注入相对或绝对位置信息。因此在编码器与解码器栈底部，把「位置编码」加到输入嵌入上。位置编码维数与嵌入相同，以便相加。",
                "summary": "注意力本身对置换不敏感；位置靠加 PE 告诉模型。",
                "terms": ["positional encoding"],
                "figure": "pos",
            },
            {
                "en": "In this work, we use sine and cosine functions of different frequencies: PE(pos, 2i) = sin(pos / 10000^{2i/d_model}), PE(pos, 2i+1) = cos(pos / 10000^{2i/d_model}), where pos is the position and i is the dimension. Each dimension of the positional encoding corresponds to a sinusoid. The wavelengths form a geometric progression from 2π to 10000·2π.",
                "zh": "本文用不同频率的正弦与余弦：偶维 sin、奇维 cos，pos 是位置、i 是维度。位置编码的每个维度对应一条正弦波，波长从 2π 到 10000·2π 成等比。",
                "summary": "正弦 PE：每个维度一条波，频率按维递减。",
                "terms": ["sinusoidal PE"],
                "formulas": [
                    {
                        "tag": "正弦位置编码",
                        "latex": r"PE_{(pos,2i)}=\sin\!\frac{pos}{10000^{2i/d_{\mathrm{model}}}},\quad PE_{(pos,2i+1)}=\cos\!\frac{pos}{10000^{2i/d_{\mathrm{model}}}}",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "We chose this function because we hypothesized it would allow the model to easily learn to attend by relative position, since for any fixed offset k, PE(pos+k) can be represented as a linear function of PE(pos). We also experimented with using learned positional embeddings instead, and found that the two versions produced nearly identical results. We chose the sinusoidal version because it may allow the model to extrapolate to sequence lengths longer than the ones encountered during training.",
                "zh": "选它是因为：对任意固定偏移 k，PE(pos+k) 可写成 PE(pos) 的线性函数，便于学相对位置。我们也试过可学习位置嵌入，结果几乎相同。选正弦版是因为它可能外推到训练时未见过的长度。",
                "summary": "相对位置可线性读出；正弦版还可能外推更长句。",
                "terms": ["positional encoding"],
            },
        ],
    },
    {
        "id": "why",
        "title": "4 为什么用自注意力（接到稀疏的关键表）",
        "paras": [
            {
                "en": "In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations (x_1, …, x_n) to another sequence of equal length (z_1, …, z_n), with x_i, z_i ∈ R^{d}.",
                "zh": "本节把自注意力层与常用的循环层、卷积层比较：都是把变长符号表示序列 (x_1,…,x_n) 映到等长的 (z_1,…,z_n)。",
                "summary": "比较轴：复杂度、并行、路径长度。",
                "terms": ["self-attention"],
            },
            {
                "en": "One is the total computational complexity per layer. Another is the amount of computation that can be parallelized, as measured by the minimum number of sequential operations required. The third is the path length between long-range dependencies in the network. The shorter these paths, the easier it is to learn long-range dependencies.",
                "zh": "一是每层总计算复杂度。二是可并行的计算量（用所需最少顺序步数衡量）。三是网络中长程依赖的路径长度——路径越短，长程依赖越好学。",
                "summary": "三指标：算多少、能否并行、远依赖要走几步。",
                "terms": ["long-range dependency", "parallelization"],
            },
            {
                "en": "A self-attention layer connects all positions with a constant number of sequentially executed operations, whereas a recurrent layer requires O(n) sequential operations. In terms of computational complexity, self-attention layers are faster than recurrent layers when the sequence length n is smaller than the representation dimensionality d, which is most often the case with sentence representations used by state-of-the-art models in machine translations, such as word-piece and byte-pair representations.",
                "zh": "自注意力用常数步顺序运算连接所有位置，循环层则需要 O(n) 步。当序列长度 n 小于表示维 d 时，自注意力比循环层更快——机器翻译里用 word-piece / BPE 时常常如此。",
                "summary": "句长不长时，O(n² d) 仍可能比 RNN 的 O(n d²) 更香。",
                "terms": ["quadratic complexity"],
                "formulas": [
                    {
                        "tag": "原文表 1（复杂度）",
                        "latex": r"\begin{aligned}\text{Self-Attention}&:\; O(n^2 d),\ \text{顺序步 }O(1),\ \text{最大路径 }O(1)\\ \text{Recurrent}&:\; O(n d^2),\ \text{顺序步 }O(n),\ \text{最大路径 }O(n)\\ \text{Convolutional}&:\; O(k n d^2),\ \text{顺序步 }O(1),\ \text{最大路径 }O(\log_k n)\\ \text{Restricted self-attn}&:\; O(r n d),\ \text{顺序步 }O(1),\ \text{最大路径 }O(n/r)\end{aligned}",
                        "note": "最后一行已经在谈「限制每位置只看 r 个邻居」——这就是稀疏注意力的原型。",
                        "wide": True,
                    },
                ],
            },
            {
                "en": "To improve computational performance for tasks involving very long sequences, self-attention could be restricted to considering only a neighborhood of size r in the input sequence centered around the respective output position. This would increase the maximum path length to O(n/r). We plan to investigate this approach in future work.",
                "zh": "对很长序列，可以把自注意力限制为：每个输出位置只看输入里以它为中心、大小为 r 的邻域。这会把最大路径长度变成 O(n/r)。我们计划在未来工作中研究这一方法。",
                "summary": "原文已经点名「局部窗口」——Sparse Transformer / Longformer 就是来做这件事的。",
                "terms": ["restricted self-attention", "sparse attention"],
            },
            {
                "en": "Teaching note. Read Table 1’s last row as the on-ramp to this repo’s sparse track. Full self-attention: every query sees every key, path length 1, cost n². Restricted / sparse: each query sees r keys, cost ~ n r, but information may need several layers to travel. Later Longformer (sliding window + global tokens) and BigBird (window + global + random) are concrete designs of that r-neighborhood plus extra “hub” tokens so path length stays small.",
                "zh": "导读。把表 1 最后一行当成通往本仓库稀疏路线的匝道。全自注意：每个 query 看所有 key，路径长度 1，代价 n²。限制/稀疏：每个 query 看 r 个 key，代价约 n r，但信息可能要走若干层。后来的 Longformer（滑窗+全局 token）与 BigBird（窗口+全局+随机）就是把这个 r 邻域设计具体化，并加「枢纽」token 以保持短路径。",
                "summary": "稀疏不是否定本文，而是接过本文自己写下的未来工作。",
                "terms": ["Longformer", "BigBird", "Sparse Transformer"],
            },
        ],
    },
    {
        "id": "train",
        "title": "5 训练要点（极简）",
        "paras": [
            {
                "en": "We trained on the standard WMT 2014 English-German dataset (~4.5M sentence pairs, 37k byte-pair tokens) and English-French (~36M sentences, 32k word-piece tokens). Base model: d_model=512, d_ff=2048, h=8, P_drop=0.1, N=6. Big model: d_model=1024, d_ff=4096, h=16.",
                "zh": "数据：WMT14 英德约 450 万句对（37k BPE），英法约 3600 万句（32k word-piece）。Base：512/2048/8 头/dropout 0.1/6 层。Big：1024/4096/16 头。",
                "summary": "记住 Base 数字，后面读论文常拿它当单位。",
                "terms": ["d_model", "h", "N=6"],
            },
            {
                "en": "Adam optimizer with β1=0.9, β2=0.98, ε=10^{-9}. Learning rate warmup for 4000 steps then inverse-sqrt decay. Residual dropout P_drop=0.1 on embeddings and after each sub-layer. Label smoothing ε_ls=0.1.",
                "zh": "Adam：β1=0.9，β2=0.98，ε=10^{-9}。学习率 4000 步 warmup 再按步数平方根反比衰减。残差 dropout 0.1。标签平滑 0.1。",
                "summary": "训练配方：warmup + dropout + label smoothing。",
                "terms": ["dropout", "warmup"],
                "formulas": [
                    {
                        "tag": "学习率",
                        "latex": r"lrate = d_{\mathrm{model}}^{-0.5}\cdot \min\!\bigl(step^{-0.5},\; step\cdot warmup^{-1.5}\bigr)",
                        "wide": True,
                    },
                ],
            },
        ],
    },
    {
        "id": "results",
        "title": "6 结果与变体（极简）",
        "paras": [
            {
                "en": "On WMT 2014 English-to-German, Transformer (big) achieves 28.4 BLEU, a new SOTA exceeding ensembles at a fraction of the training cost. English-to-French: 41.8 BLEU single-model SOTA.",
                "zh": "WMT14 英德：Transformer (big) 28.4 BLEU，新 SOTA，训练成本远低于当时的集成系统。英法：41.8 BLEU 单模型 SOTA。",
                "summary": "质量与训练成本同时打赢。",
                "terms": ["BLEU"],
            },
            {
                "en": "Table 3 variations: reducing heads from 8 to 1 drops BLEU by 0.9; too many heads (32) also hurts slightly. Removing positional encoding is catastrophic. Replacing residual dropout or label smoothing also hurts. These ablations justify the default recipe you just learned.",
                "zh": "表 3 变体：头从 8 减到 1，BLEU 掉 0.9；头太多（32）也略伤。去掉位置编码是灾难。去掉残差 dropout 或标签平滑也会伤。这些消融就是在给你刚学的默认配方作证。",
                "summary": "消融印象：单头不行；没 PE 更不行。",
                "terms": ["multi-head attention", "positional encoding"],
            },
        ],
    },
    {
        "id": "next",
        "title": "读完之后：接到稀疏注意力",
        "paras": [
            {
                "en": "You now have the full dense Transformer: QKV projections, scaled softmax, multi-head, residual+LN, FFN, sinusoidal PE, and the O(n² d) cost. Sparse attention keeps this formula and changes only who is allowed in the softmax—mask extra (i,j) pairs besides the causal ones.",
                "zh": "到这里，稠密 Transformer 已经齐了：QKV 投影、缩放 softmax、多头、残差+LN、FFN、正弦 PE，以及 O(n² d) 代价。稀疏注意力保留这套公式，只改 softmax 里允许谁——在因果掩码之外再禁掉更多 (i,j)。",
                "summary": "稀疏 = 同一套 Attention(Q,K,V)，换一张更稀的掩码。",
                "terms": ["sparse attention", "attention mask"],
            },
            {
                "en": "In this repo, next on the sparse track: papers/sparse-attention (map of patterns) → papers/sparse-transformer (fixed factorized patterns) → papers/longformer (window + global) → papers/watts-strogatz (random-graph intuition) → papers/bigbird (window + global + random) → papers/nsa (trainable hierarchical sparse). FlashAttention is orthogonal: still full softmax, but IO-aware.",
                "zh": "本仓库稀疏路线：papers/sparse-attention（图案总览）→ papers/sparse-transformer（固定分解图案）→ papers/longformer（窗口+全局）→ papers/watts-strogatz（随机图直觉）→ papers/bigbird（窗口+全局+随机）→ papers/nsa（可训练层次稀疏）。FlashAttention 是另一轴：仍是全 softmax，只是更会走 IO。",
                "summary": "下一站打开稀疏专题即可，不必先跳到线性注意力。",
                "terms": ["Sparse Transformer", "Longformer", "BigBird", "NSA"],
            },
            {
                "en": "A second track changes the formula rather than the mask: linear attention replaces softmax(QKᵀ)V by φ(Q)(φ(K)ᵀ V) so the N×N matrix never appears. That starts at papers/linear-attention, then DeltaNet / Gated DeltaNet / KDA. Do not mix the two stories on the first pass.",
                "zh": "第二条路线改公式而不是改掩码：线性注意力用 φ(Q)(φ(K)ᵀ V) 替换 softmax(QKᵀ)V，N×N 矩阵不再出现。从 papers/linear-attention 起，再到 DeltaNet / Gated DeltaNet / KDA。第一遍不要把两条故事拧在一起。",
                "summary": "先走稀疏（改连边），再走线性（改核），两条都从本页的式 (1) 分叉。",
                "terms": ["linear attention", "DeltaNet", "KDA"],
            },
        ],
    },
]

GLOSSARY = [
    ("Transformer", "本文提出的编码器–解码器：只用注意力与逐位置 FFN，不用 RNN/CNN。"),
    ("sequence transduction", "把源序列映射成目标序列的任务，如翻译。"),
    ("encoder-decoder", "编码器读源句，解码器写目标句；中间用交叉注意力对齐。"),
    ("encoder", "N=6 层：每层多头自注意 + FFN。源句双向可见。"),
    ("decoder", "N=6 层：掩码自注意 + 交叉注意 + FFN。目标句因果可见。"),
    ("attention", "用 query 对 key 打分，softmax 成权重，再加权 value。"),
    ("self-attention", "Q/K/V 来自同一序列的注意力。"),
    ("encoder-decoder attention", "Q 来自解码器，K/V 来自编码器的交叉注意力。"),
    ("Q", "Query：当前要读什么。"),
    ("K", "Key：每个位置的标签，用来被 query 匹配。"),
    ("V", "Value：匹配上之后真正混合的内容。"),
    ("compatibility function", "query 与 key 有多配；本文用缩放点积。"),
    ("scaled dot-product attention", "softmax(QKᵀ/√d_k) V。"),
    ("softmax", "把一行分数变成非负且和为 1 的权重。"),
    ("d_k", "每个头里 query/key 的维度；本文 64。"),
    ("d_v", "每个头里 value 的维度；本文 64。"),
    ("d_model", "模型主宽度；Base 为 512。"),
    ("d_ff", "FFN 隐层宽度；Base 为 2048。"),
    ("multi-head attention", "h 组不同投影各做一次注意力，再拼接投影。"),
    ("h", "头数；Base 为 8。"),
    ("W^Q", "把输入投成 query 的矩阵（每头一块，或拼成大矩阵）。"),
    ("W^K", "key 投影矩阵。"),
    ("W^V", "value 投影矩阵。"),
    ("W^O", "多头拼接后的输出投影。"),
    ("representation subspaces", "不同头可以读不同的表示方向/关系类型。"),
    ("causal masking", "把未来位置的分数设为 −∞，保证自回归。"),
    ("auto-regressive", "生成位置 i 只依赖已经生成的 <i。"),
    ("attention mask", "允许/禁止 (i,j) 配对的 0/1 或 −∞ 掩码。"),
    ("attention matrix", "N×N 的分数或权重表；稠密时这就是 O(N²)。"),
    ("residual", "x + Sublayer(x)，让梯度与身份映射好走。"),
    ("LayerNorm", "在残差之后做的层归一化。"),
    ("FFN", "逐位置两层 MLP，中间 ReLU；不混合不同位置。"),
    ("ReLU", "max(0,·)，本文 FFN 的激活。"),
    ("embedding", "token → d_model 向量。"),
    ("positional encoding", "加到嵌入上的位置信息；本文用正弦。"),
    ("sinusoidal PE", "不同频率的 sin/cos 位置编码。"),
    ("N=6", "编码器/解码器层数。"),
    ("RNN", "沿时间递推的网络；本文要丢掉它以便并行。"),
    ("LSTM", "带门控的 RNN 变体，2017 年前的序列主流。"),
    ("parallelization", "长度维上可同时算；自注意力顺序步为 O(1)。"),
    ("long-range dependency", "相距很远的 token 之间的依赖；自注意力路径长度为 1。"),
    ("quadratic complexity", "全注意力相对长度的 O(n² d) 代价。"),
    ("restricted self-attention", "原文表 1：每位置只看 r 个邻居；稀疏注意力的种子。"),
    ("sparse attention", "softmax 只在允许的 (i,j) 上做；本仓库稀疏路线。"),
    ("linear attention", "用核特征避开 N×N 矩阵；本仓库线性路线。"),
    ("additive attention", "Bahdanau：用小网络打分而不是点积。"),
    ("BLEU", "机器翻译自动指标；本文英德 28.4。"),
    ("dropout", "残差分支上的随机丢弃；P_drop=0.1。"),
    ("warmup", "前 4000 步拉高学习率再衰减。"),
    ("Sparse Transformer", "Child et al.：固定稀疏分解图案。"),
    ("Longformer", "滑窗局部 + 任务全局 token。"),
    ("BigBird", "窗口 + 全局 + 随机块。"),
    ("NSA", "可训练的层次稀疏注意力。"),
    ("DeltaNet", "在线性注意力状态上用 delta 规则改写。"),
    ("KDA", "通道级门控的 delta 线性注意力。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "Attention Is All You Need",
        "why": "原始 Transformer；QKV / 多头 / 位置编码的定义页。",
        "url": "./paper.pdf",
        "ext": "https://arxiv.org/abs/1706.03762",
    },
    {
        "level": "下一站",
        "title": "稀疏注意力专题",
        "why": "同一套公式，改连边；从零走稀疏的地图。",
        "url": "../sparse-attention/index.html",
        "ext": "",
    },
    {
        "level": "下一站",
        "title": "Sparse Transformer",
        "why": "原文表 1「restricted self-attention」的早期落地。",
        "url": "../sparse-transformer/",
        "ext": "https://arxiv.org/abs/1904.10509",
    },
    {
        "level": "下一站",
        "title": "Longformer",
        "why": "滑窗 + 全局 token，长文档近线性。",
        "url": "../longformer/index.html",
        "ext": "https://arxiv.org/abs/2004.05150",
    },
    {
        "level": "对照",
        "title": "Linear Attention",
        "why": "另一分叉：不造 N×N，改核函数。先读完本页再去。",
        "url": "../linear-attention/index.html",
        "ext": "https://arxiv.org/abs/2006.16236",
    },
    {
        "level": "背景",
        "title": "Bahdanau attention (2015)",
        "why": "加性注意力；本文点积注意力的对照。",
        "url": "https://arxiv.org/abs/1409.0473",
        "ext": "",
    },
]
