"""Fine-grained Watts–Strogatz (Nature 1998) paragraphs: original + zh + summary.

Source: Watts & Strogatz, Collective dynamics of 'small-world' networks,
Nature 393, 440–442 (1998). DOI: 10.1038/30918.

English follows the published letter closely (ligatures/line breaks normalized).
Figure captions and Table 1 are included as readable paragraphs.
A final bridge section connects the model to BigBird-style sparse attention.
"""

SECTIONS = [
    {
        "id": "opening",
        "title": "开篇动机：介于规则与随机之间",
        "paras": [
            {
                "en": "Networks of coupled dynamical systems have been used to model biological oscillators, Josephson junction arrays, excitable media, neural networks, spatial games, genetic control networks and many other self-organizing systems.",
                "zh": "耦合动力系统网络已被用来建模生物振荡器、约瑟夫森结阵列、可激发介质、神经网络、空间博弈、基因调控网络，以及许多其他自组织系统。",
                "summary": "开场：网络耦合动力学早已是各领域的标准建模语言。",
                "terms": ["coupled dynamical systems"],
            },
            {
                "en": "Ordinarily, the connection topology is assumed to be either completely regular or completely random. But many biological, technological and social networks lie somewhere between these two extremes.",
                "zh": "通常，连接拓扑被假定为要么完全规则，要么完全随机。但许多生物、技术与社会网络其实落在这两极之间。",
                "summary": "痛点：真实世界既不是纯格子，也不是纯随机图。",
                "terms": ["regular lattice", "random graph"],
            },
            {
                "en": "Here we explore simple models of networks that can be tuned through this middle ground: regular networks ‘rewired’ to introduce increasing amounts of disorder.",
                "zh": "本文探索可在这一中间地带连续调节的简单网络模型：对规则网络做「重连（rewire）」，以引入越来越多的无序。",
                "summary": "方法预告：从规则环出发，用概率 p 随机重连。",
                "terms": ["rewiring", "p"],
            },
            {
                "en": "We find that these systems can be highly clustered, like regular lattices, yet have small characteristic path lengths, like random graphs. We call them ‘small-world’ networks, by analogy with the small-world phenomenon (popularly known as six degrees of separation).",
                "zh": "我们发现：这些系统可以像规则格子一样高度聚类，同时又像随机图一样具有很短的特征路径长度。我们称之为「小世界」网络，类比于小世界现象（通俗说法即六度分隔）。",
                "summary": "定义一句话：高聚类 C + 短平均路径 L = small-world。",
                "terms": ["small-world networks", "clustering coefficient", "characteristic path length"],
            },
            {
                "en": "The neural network of the worm Caenorhabditis elegans, the power grid of the western United States, and the collaboration graph of film actors are shown to be small-world networks.",
                "zh": "秀丽隐杆线虫（C. elegans）的神经网络、美国西部电网，以及电影演员合作图，都被证明是小世界网络。",
                "summary": "三个实证例子：脑网络、电网、演员合作网。",
                "terms": ["C. elegans", "power grid", "film actors"],
            },
            {
                "en": "Models of dynamical systems with small-world coupling display enhanced signal-propagation speed, computational power, and synchronizability. In particular, infectious diseases spread more easily in small-world networks than in regular lattices.",
                "zh": "具有小世界耦合的动力系统模型表现出更快的信号传播、更强的计算能力与更好的同步性。尤其是，传染病在小世界网络中比在规则格子上更容易传播。",
                "summary": "动力学后果：传播更快、更易同步；疾病传播是主测试用例。",
                "terms": ["synchronizability"],
            },
        ],
    },
    {
        "id": "construction",
        "title": "模型构造：随机重连程序（Fig. 1）",
        "paras": [
            {
                "en": "To interpolate between regular and random networks, we consider the following random rewiring procedure (Fig. 1). Starting from a ring lattice with n vertices and k edges per vertex, we rewire each edge at random with probability p.",
                "zh": "为在规则网络与随机网络之间插值，我们考虑如下随机重连程序（图 1）。从具有 n 个顶点、每个顶点 k 条边的环格子出发，以概率 p 把每条边随机重连。",
                "summary": "三参数：n（点数）、k（度数）、p（重连概率）。",
                "terms": ["ring lattice", "n", "k", "p"],
                "figure": "rewire",
            },
            {
                "en": "This construction allows us to ‘tune’ the graph between regularity (p = 0) and disorder (p = 1), and thereby to probe the intermediate region 0 < p < 1, about which little is known.",
                "zh": "该构造使我们能在规则（p=0）与无序（p=1）之间「调谐」图，从而探测此前知之甚少的中间区域 0<p<1。",
                "summary": "关键：p 是连续旋钮，重点在中间态，不在两极。",
                "terms": ["p"],
            },
            {
                "en": "Figure 1 procedure (caption, condensed): Start with a ring of n vertices, each connected to its k nearest neighbours by undirected edges. Choose a vertex and the edge that connects it to its nearest neighbour in a clockwise sense. With probability p, reconnect this edge to a vertex chosen uniformly at random over the entire ring (duplicate edges forbidden); otherwise leave the edge in place. Repeat clockwise around the ring; then proceed to second-nearest neighbours, and so on, until each original edge has been considered once (nk/2 edges ⇒ k/2 laps).",
                "zh": "图 1 程序（题注精炼）：从 n 点环开始，每点连到 k 个最近邻（无向边）。取一点及其顺时针最近邻边：以概率 p 把它重连到环上均匀随机的另一点（禁止重边），否则保持。沿环顺时针重复；再处理次近邻……直到原格子每条边都被考虑一次（共 nk/2 条边，即转 k/2 圈）。",
                "summary": "算法细节：按「邻域半径」一圈圈扫，每条边最多被尝试重连一次。",
                "terms": ["rewiring"],
            },
            {
                "en": "For p = 0 the original ring is unchanged; as p increases the graph becomes increasingly disordered until for p = 1 all edges are rewired randomly. For intermediate p the graph is a small-world network: highly clustered like a regular graph, yet with small characteristic path length, like a random graph.",
                "zh": "p=0 时原环不变；随 p 增大图越来越无序，直到 p=1 时所有边都被随机重连。对中间的 p，图即为小世界网络：像规则图一样高度聚类，又像随机图一样特征路径短。",
                "summary": "三种相：规则大世界 → 小世界 → 随机小世界（但聚类崩掉）。",
                "terms": ["small-world networks"],
            },
        ],
    },
    {
        "id": "metrics",
        "title": "两个度量：L(p) 与 C(p)",
        "paras": [
            {
                "en": "We quantify the structural properties of these graphs by their characteristic path length L(p) and clustering coefficient C(p), as defined in Fig. 2 legend. Here L(p) measures the typical separation between two vertices in the graph (a global property), whereas C(p) measures the cliquishness of a typical neighbourhood (a local property).",
                "zh": "我们用特征路径长度 L(p) 与聚类系数 C(p)（定义见图 2 题注）量化这些图的结构性质。L(p) 度量图中两顶点之间的典型分隔（全局性质）；C(p) 度量典型邻域的抱团程度（局部性质）。",
                "summary": "记住分工：L 看全局远近，C 看局部抱团。",
                "terms": ["characteristic path length", "clustering coefficient"],
            },
            {
                "en": "Definition of L: the number of edges in the shortest path between two vertices, averaged over all pairs of vertices.",
                "zh": "L 的定义：两顶点最短路径上的边数，再对所有顶点对取平均。",
                "summary": "L = 平均最短路径长度。",
                "terms": ["characteristic path length"],
            },
            {
                "en": "Definition of C: Suppose that a vertex v has k_v neighbours; then at most k_v(k_v − 1)/2 edges can exist between them (when every neighbour of v is connected to every other neighbour of v). Let C_v denote the fraction of these allowable edges that actually exist. Define C as the average of C_v over all v.",
                "zh": "C 的定义：设顶点 v 有 k_v 个邻居，则邻居之间最多可有 k_v(k_v−1)/2 条边（当邻居两两相连时）。令 C_v 为这些「允许边」中实际存在的比例；再对所有 v 平均得到 C。",
                "summary": "C_v = 实际三角形边数 / 可能三角形边数；C 是平均局部密度。",
                "terms": ["clustering coefficient"],
            },
            {
                "en": "For friendship networks, these statistics have intuitive meanings: L is the average number of friendships in the shortest chain connecting two people; C_v reflects the extent to which friends of v are also friends of each other; and thus C measures the cliquishness of a typical friendship circle.",
                "zh": "对朋友网络，这两个统计量有直观含义：L 是连接两人的最短朋友链上的平均友情步数；C_v 反映「v 的朋友彼此也是朋友」的程度；因而 C 度量典型朋友圈的抱团性。",
                "summary": "社交直觉：L≈几度分隔，C≈朋友圈有多封闭。",
                "terms": [],
            },
            {
                "en": "The networks of interest to us have many vertices with sparse connections, but not so sparse that the graph is in danger of becoming disconnected. Specifically, we require n ≫ k ≫ ln(n) ≫ 1, where k ≫ ln(n) guarantees that a random graph will be connected.",
                "zh": "我们关心的网络顶点很多、连接稀疏，但又不至于稀疏到容易不连通。具体要求 n ≫ k ≫ ln(n) ≫ 1，其中 k ≫ ln(n) 保证随机图连通。",
                "summary": "参数制度：大而稀疏但仍连通——后面渐近公式都在这套假设下。",
                "terms": ["n", "k"],
            },
            {
                "en": "In this regime, we find that L ∼ n/(2k) ≫ 1 and C ∼ 3/4 as p → 0, while L ≈ L_random ∼ ln(n)/ln(k) and C ≈ C_random ∼ k/n ≪ 1 as p → 1.",
                "zh": "在此制度下：当 p→0 时 L∼n/(2k)≫1 且 C∼3/4；当 p→1 时 L≈L_random∼ln(n)/ln(k)，且 C≈C_random∼k/n≪1。",
                "summary": "两极公式：规则世界 L 随 n 线性；随机世界 L 只随 n 对数、C 崩到 ~k/n。",
                "terms": ["L_random", "C_random"],
            },
            {
                "en": "Thus the regular lattice at p = 0 is a highly clustered, large world where L grows linearly with n, whereas the random network at p = 1 is a poorly clustered, small world where L grows only logarithmically with n. These limiting cases might lead one to suspect that large C is always associated with large L, and small C with small L.",
                "zh": "因此 p=0 的规则格子是高度聚类的「大世界」（L 随 n 线性增长）；而 p=1 的随机网络是低聚类的「小世界」（L 仅对数增长）。这两极容易让人误以为：大 C 总伴随大 L，小 C 总伴随小 L。",
                "summary": "作者先立靶子：人们会以为 C 与 L 必须同涨同跌。",
                "terms": [],
            },
        ],
    },
    {
        "id": "smallworld",
        "title": "小世界区间：捷径如何压低 L（Fig. 2）",
        "paras": [
            {
                "en": "On the contrary, Fig. 2 reveals that there is a broad interval of p over which L(p) is almost as small as L_random yet C(p) ≫ C_random.",
                "zh": "恰恰相反，图 2 显示存在相当宽的 p 区间：其中 L(p) 几乎已小到接近 L_random，但 C(p) 仍远大于 C_random。",
                "summary": "核心发现：存在「又短路径、又高聚类」的宽平台。",
                "terms": ["small-world networks"],
                "figure": "lc_curve",
            },
            {
                "en": "These small-world networks result from the immediate drop in L(p) caused by the introduction of a few long-range edges. Such ‘short cuts’ connect vertices that would otherwise be much farther apart than L_random.",
                "zh": "这类小世界网络源于：引入少数长程边后 L(p) 立刻下降。这些「捷径（short cuts）」连接的是原本会远比 L_random 更远的顶点对。",
                "summary": "机制：少量长程捷径就够把全局距离打穿。",
                "terms": ["short cuts"],
            },
            {
                "en": "For small p, each short cut has a highly nonlinear effect on L, contracting the distance not just between the pair of vertices that it connects, but between their immediate neighbourhoods, neighbourhoods of neighbourhoods and so on.",
                "zh": "当 p 很小时，每条捷径对 L 有高度非线性的影响：它不仅缩短所连两点的距离，还压缩它们的直接邻域、邻域的邻域……之间的距离。",
                "summary": "非线性杠杆：一条捷径改写整片「邻域球」的距离。",
                "terms": ["short cuts"],
            },
            {
                "en": "By contrast, an edge removed from a clustered neighbourhood to make a short cut has, at most, a linear effect on C; hence C(p) remains practically unchanged for small p even though L(p) drops rapidly.",
                "zh": "相比之下，为制造捷径而从聚类邻域中移走的一条边，对 C 至多只有线性影响；因此在小 p 下，尽管 L(p) 迅速下降，C(p) 几乎不变。",
                "summary": "不对称：捷径狠砍 L，却几乎不伤 C。",
                "terms": ["clustering coefficient"],
            },
            {
                "en": "The important implication here is that at the local level (as reflected by C(p)), the transition to a small world is almost undetectable.",
                "zh": "重要含义：在局部层面（由 C(p) 反映），向小世界的转变几乎不可察觉。",
                "summary": "读图要点：局部看起来还像格子，全局已经「六度」了。",
                "terms": [],
            },
            {
                "en": "Fig. 2 note: data are averages over 20 random realizations, normalized by L(0), C(0) for a regular lattice; n = 1,000 vertices, average degree k = 10. A logarithmic horizontal scale resolves the rapid drop in L(p). During this drop, C(p) remains almost constant at its regular-lattice value.",
                "zh": "图 2 说明：数据为 20 次随机重连实现的平均，并用规则格子的 L(0)、C(0) 归一化；n=1000，平均度数 k=10。横轴对数刻度用以分辨 L(p) 的急速下降；下降期间 C(p) 几乎保持规则格子的取值。",
                "summary": "实验设定备忘：n=1000, k=10；先盯 L 的陡降区间。",
                "terms": [],
            },
            {
                "en": "To check the robustness of these results, we have tested many different types of initial regular graphs, as well as different algorithms for random rewiring, and all give qualitatively similar results. The only requirement is that the rewired edges must typically connect vertices that would otherwise be much farther apart than L_random.",
                "zh": "为检验稳健性，作者测试了许多不同的初始规则图以及不同的随机重连算法，结果定性相似。唯一要求是：被重连的边通常应连接那些原本远比 L_random 更远的顶点。",
                "summary": "稳健条件：重连必须真的变成「长程」捷径，而不是挪到近处。",
                "terms": ["rewiring"],
            },
        ],
    },
    {
        "id": "empirical",
        "title": "实证：演员网 / 电网 / C. elegans（Table 1）",
        "paras": [
            {
                "en": "The idealized construction above reveals the key role of short cuts. It suggests that the small-world phenomenon might be common in sparse networks with many vertices, as even a tiny fraction of short cuts would suffice.",
                "zh": "上述理想化构造揭示了捷径的关键作用。它暗示：小世界现象在顶点很多的稀疏网络中可能很常见——因为哪怕极少数捷径也足够。",
                "summary": "从模型推现实：稀疏大网「天然容易」变小世界。",
                "terms": ["short cuts"],
            },
            {
                "en": "To test this idea, we have computed L and C for the collaboration graph of actors in feature films, the electrical power grid of the western United States, and the neural network of the nematode worm C. elegans. All three graphs are of scientific interest.",
                "zh": "为检验这一想法，我们计算了故事片演员合作图、美国西部电网，以及线虫 C. elegans 神经网络的 L 与 C。这三张图都具有科学兴趣。",
                "summary": "选例原则：有完整接线数据 + 本身重要，不是挑好看的。",
                "terms": ["film actors", "power grid", "C. elegans"],
            },
            {
                "en": "The graph of film actors is a surrogate for a social network, with the advantage of being much more easily specified. It is also akin to the graph of mathematical collaborations centred, traditionally, on P. Erdős. The graph of the power grid is relevant to the efficiency and robustness of power networks. And C. elegans is the sole example of a completely mapped neural network.",
                "zh": "演员合作图可作社会网络的替代，优点是更容易明确指定；也类似于以 Erdős 为中心的数学合作图。电网图关系到电力网络的效率与稳健性。而 C. elegans 是当时唯一被完全测绘的神经网络。",
                "summary": "三个例子各自代表：社交、基础设施、生物神经。",
                "terms": [],
            },
            {
                "en": "Table 1 (Film actors): n = 225,226, k = 61; L_actual = 3.65 vs L_random = 2.99; C_actual = 0.79 vs C_random = 0.00027. Two actors are joined by an edge if they have acted in a film together (giant connected component, ~90% of IMDb actors as of April 1997).",
                "zh": "表 1（电影演员）：n=225,226，k=61；L_actual=3.65 vs L_random=2.99；C_actual=0.79 vs C_random=0.00027。若两人同演一部电影则连边（取巨连通分量，约占 1997 年 4 月 IMDb 演员的 90%）。",
                "summary": "演员网：L 已接近随机，C 却比随机高三个数量级。",
                "terms": ["Table 1", "film actors"],
            },
            {
                "en": "Table 1 (Power grid): n = 4,941, k = 2.67; L_actual = 18.7 vs L_random = 12.4; C_actual = 0.080 vs C_random = 0.005. Vertices represent generators, transformers and substations; edges are high-voltage transmission lines.",
                "zh": "表 1（电网）：n=4,941，k=2.67；L_actual=18.7 vs L_random=12.4；C_actual=0.080 vs C_random=0.005。顶点为发电机、变压器与变电站；边为高压输电线路。",
                "summary": "电网：路径略长于随机，但聚类仍明显高于随机。",
                "terms": ["Table 1", "power grid"],
            },
            {
                "en": "Table 1 (C. elegans): n = 282, k = 14; L_actual = 2.65 vs L_random = 2.25; C_actual = 0.28 vs C_random = 0.05. An edge joins two neurons if they are connected by either a synapse or a gap junction. Edges treated as undirected and unweighted.",
                "zh": "表 1（C. elegans）：n=282，k=14；L_actual=2.65 vs L_random=2.25；C_actual=0.28 vs C_random=0.05。若两神经元以突触或间隙连接相连则连边；边视为无向无权。",
                "summary": "线虫脑：短路径 + 明显高于随机的聚类。",
                "terms": ["Table 1", "C. elegans"],
            },
            {
                "en": "All three networks show the small-world phenomenon: L ≳ L_random but C ≫ C_random. These examples were not hand-picked; they were chosen because of their inherent interest and because complete wiring diagrams were available. Thus the small-world phenomenon is not merely a curiosity of social networks nor an artefact of an idealized model—it is probably generic for many large, sparse networks found in nature.",
                "zh": "三张网络都呈现小世界现象：L ≳ L_random 但 C ≫ C_random。这些例子并非刻意挑选，而是因其固有重要性且有完整接线数据。因此小世界现象不只是社交网络的奇闻，也不是理想模型的假象——对自然界许多大型稀疏网络很可能具有普适性。",
                "summary": "结论性判断：小世界很可能是大自然的默认架构之一。",
                "terms": ["small-world networks"],
            },
        ],
    },
    {
        "id": "dynamics",
        "title": "动力学：疾病传播与其他系统（Fig. 3）",
        "paras": [
            {
                "en": "We now investigate the functional significance of small-world connectivity for dynamical systems. Our test case is a deliberately simplified model for the spread of an infectious disease. The population structure is modelled by the family of graphs described in Fig. 1.",
                "zh": "接下来考察小世界连通性对动力系统的功能意义。测试用例是一个刻意简化的传染病传播模型；人群结构由图 1 那一族图给出。",
                "summary": "从结构转到功能：先拿传染病当显微镜。",
                "terms": [],
            },
            {
                "en": "At time t = 0, a single infective individual is introduced into an otherwise healthy population. Infective individuals are removed permanently (by immunity or death) after a period of sickness that lasts one unit of dimensionless time. During this time, each infective individual can infect each of its healthy neighbours with probability r.",
                "zh": "在 t=0 时，向原本健康的人群引入单个感染者。感染者在持续一个无量纲时间单位的病程后被永久移除（免疫或死亡）。在此期间，每个感染者可以以概率 r 感染其每个健康邻居。",
                "summary": "SIR 味道的简化：病程=1，传染概率=r，沿边传播。",
                "terms": ["r"],
            },
            {
                "en": "On subsequent time steps, the disease spreads along the edges of the graph until it either infects the entire population, or it dies out, having infected some fraction of the population in the process.",
                "zh": "在后续时间步，疾病沿图的边传播，直到感染整个人群，或在感染一部分人后灭绝。",
                "summary": "观测终点：全感染 / 自行熄灭，以及过程中的感染规模与时间。",
                "terms": [],
            },
            {
                "en": "Two results emerge. First, the critical infectiousness r_half, at which the disease infects half the population, decreases rapidly for small p (Fig. 3a). Second, for a disease that is sufficiently infectious to infect the entire population regardless of its structure, the time T(p) required for global infection resembles the L(p) curve (Fig. 3b).",
                "zh": "出现两个结果。第一，使疾病感染半数人口的临界传染性 r_half，在小 p 时迅速下降（图 3a）。第二，对足以无论结构如何都能感染全人群的疾病，全球感染所需时间 T(p) 的曲线形态与 L(p) 相似（图 3b）。",
                "summary": "捷径一加：阈值更低、传遍更快；T(p) 几乎跟着 L(p) 走。",
                "terms": ["r_half", "T(p)"],
            },
            {
                "en": "Thus, infectious diseases are predicted to spread much more easily and quickly in a small world; the alarming and less obvious point is how few short cuts are needed to make the world small.",
                "zh": "因此预测：传染病在小世界中传播更容易、更快；更令人警惕且不那么显然的一点是——让世界变「小」只需要极少的捷径。",
                "summary": "警句：很少的长程边，就能把传播动力学改写掉。",
                "terms": ["short cuts"],
            },
            {
                "en": "Our model differs from other network epidemic models in illuminating dynamics as an explicit function of structure, rather than for a few particular topologies. Compared with Kretschmar & Morris (who vary concurrency on disconnected graphs with k = 1), all our graphs remain connected; hence changes come from subtler structural features than connectedness. Moreover, transitions to a smaller world are not obvious to an individual, unlike increases in concurrent partners.",
                "zh": "与其他网络流行病模型不同，本模型把动力学显式写成结构的函数，而不是只看少数特定拓扑。与 Kretschmar & Morris（在 k=1 的不连通图上改变并发性）相比，本文图始终连通，故变化来自比连通性更细的结构特征；而且「世界变小」对个体并不显而易见，不像并发伴侣数增加那样可被直接察觉。",
                "summary": "对照文献：强调「保持连通 + 结构细变化」才是小世界动力学的来源。",
                "terms": [],
            },
            {
                "en": "Three other dynamical systems on the same graph family: (1) Cellular automata for density classification — a simple majority-rule on a small-world graph can outperform known human and GA-generated rules on a ring lattice. (2) Iterated multi-player Prisoner's dilemma — as short cuts increase, cooperation (generalized tit-for-tat) becomes less likely to emerge. (3) Coupled phase oscillators — small-world networks synchronize almost as readily as mean-field models despite orders of magnitude fewer edges; possibly relevant to visual-cortex synchronization if the brain is small-world.",
                "zh": "同一图族上的另外三个动力系统：（1）密度分类元胞自动机——小世界上的简单多数规则可超过环格子上已知的人工/遗传算法规则；（2）迭代多人囚徒困境——捷径增多时，广义针锋相对策略更难涌现合作；（3）耦合相位振荡器——小世界几乎像平均场一样容易同步，尽管边少几个数量级；若脑具有小世界结构，或与视皮层远距同步相关。",
                "summary": "功能图谱：计算↑、合作↓、同步≈平均场——结构同时改写多种动力学。",
                "terms": ["synchronizability"],
            },
        ],
    },
    {
        "id": "closing",
        "title": "结语",
        "paras": [
            {
                "en": "We hope that our work will stimulate further studies of small-world networks. Their distinctive combination of high clustering with short characteristic path length cannot be captured by traditional approximations such as those based on regular lattices or random graphs.",
                "zh": "我们希望这项工作能激发对小世界网络的进一步研究。其「高聚类 + 短特征路径」的独特组合，无法被基于规则格子或随机图的传统近似所刻画。",
                "summary": "学术定位：逼出第三类拓扑近似，两极模型都不够。",
                "terms": ["small-world networks"],
            },
            {
                "en": "Although small-world architecture has not received much attention, we suggest that it will probably turn out to be widespread in biological, social and man-made systems, often with important dynamical consequences.",
                "zh": "尽管小世界架构当时尚未受到太多关注，但我们推测它很可能广泛存在于生物、社会与人造系统中，并常常带来重要的动力学后果。",
                "summary": "预言式收束：小世界会是默认架构，而不只是数学玩具。",
                "terms": [],
            },
        ],
    },
    {
        "id": "bigbird",
        "title": "桥接到 BigBird：注意力里的小世界",
        "paras": [
            {
                "en": "Bridge (study note, not from the 1998 letter): BigBird cites the Watts–Strogatz intuition when designing sparse attention. Window attention plays the role of the ring-lattice local edges (high clustering / locality of reference). Random attention plays the role of short cuts that shrink average path length on the attention graph. Global tokens further add a star-like hub that theory needs for universal approximation.",
                "zh": "桥接（学习笔记，非 1998 原文）：BigBird 设计稀疏注意力时引用了 Watts–Strogatz 直觉。窗口注意力对应环格子局部边（高聚类 / 引用局部性）；随机注意力对应缩短注意力图平均路径的捷径；全局 token 再叠加理论所需的星形枢纽。",
                "summary": "对照表：WS 的局部边→窗口；捷径→随机边；BigBird 额外加全局星形。",
                "terms": ["window attention", "random attention", "global tokens", "short cuts"],
            },
            {
                "en": "Important engineering divergence: classic Watts–Strogatz rewires by deleting a local edge and replacing it with a random long-range edge. BigBird keeps all local (window) edges and adds extra random edges, because deleting structured local edges is hardware-unfriendly, while adding random (block) edges preserves locality and still shortens paths.",
                "zh": "关键工程分歧：经典 Watts–Strogatz 通过「删除一条局部边并换成随机长程边」来重连。BigBird 保留全部局部（窗口）边，再额外添加随机边——因为删掉结构化局部边对硬件不友好，而追加随机（块）边既保留局部性，又能缩短路径。",
                "summary": "和 BigBird example 页同一句话：不删窗，只加随机捷径。",
                "terms": ["rewiring", "BigBird"],
            },
            {
                "en": "Reading checklist for attention design: (1) Does your sparse pattern keep high local clustering (window / band)? (2) Do you have enough long-range short cuts so information need not hop across O(n/w) layers? (3) If you need BERT-like expressivity proofs, do you also have O(1) global hubs? Watts–Strogatz answers (1)+(2); BigBird adds (3) and block-sparse kernels.",
                "zh": "注意力设计核对清单：（1）稀疏图案是否保持高局部聚类（窗口/带状）？（2）是否有足够长程捷径，使信息不必跨 O(n/w) 层接力？（3）若需要类 BERT 表达力证明，是否还有 O(1) 全局枢纽？Watts–Strogatz 回答 (1)+(2)；BigBird 补上 (3) 与块稀疏核。",
                "summary": "把 1998 的结构洞见，翻译成 2020 注意力三问。",
                "terms": ["BigBird", "block sparse"],
            },
        ],
    },
]

GLOSSARY = [
    ("small-world networks", "同时具备高聚类系数与短特征路径长度的网络；介于规则格子与随机图之间。"),
    ("rewiring", "以概率 p 把原有边的一端改接到随机顶点，用于从规则图过渡到随机图。"),
    ("ring lattice", "把顶点排成环，每个点连接左右各 k/2 个最近邻的规则图。"),
    ("characteristic path length", "所有顶点对最短路径长度的平均值，记 L；度量全局分隔。"),
    ("clustering coefficient", "度量局部抱团：邻居之间实际边数占可能边数的比例，再对点平均，记 C。"),
    ("short cuts", "连接原本很远顶点的长程边；少量即可非线性地压缩 L。"),
    ("p", "每条边被随机重连的概率；p=0 规则，p=1 全随机，中间出现小世界。"),
    ("n", "顶点数。"),
    ("k", "每个顶点的边数（度数）。"),
    ("L_random", "同 n、k 的随机图上的特征路径长度，约 ln(n)/ln(k)。"),
    ("C_random", "同 n、k 的随机图聚类系数，约 k/n。"),
    ("regular lattice", "高度规则、局部连接占主导的格子网络。"),
    ("random graph", "边随机放置的图（如 Erdős–Rényi）；短路径但低聚类。"),
    ("coupled dynamical systems", "单元按网络边相互作用的动力学系统族。"),
    ("synchronizability", "耦合系统达成同步的难易程度。"),
    ("C. elegans", "秀丽隐杆线虫；其神经网络被完整测绘，是本文实证之一。"),
    ("power grid", "美国西部电网图：电站/变电站为点，高压线为边。"),
    ("film actors", "电影演员合作图：同片合作则连边。"),
    ("Table 1", "三个真实网络的 L、C 与对应随机基线对照表。"),
    ("r", "疾病模型中，感染者在一个病程内传染每个健康邻居的概率。"),
    ("r_half", "使最终感染人数达到人口一半的临界传染性。"),
    ("T(p)", "在足够强传染下，疾病传遍全图所需时间；形态接近 L(p)。"),
    ("BigBird", "稀疏 Transformer：窗口+随机+全局；随机边灵感来自小世界捷径。"),
    ("window attention", "注意力中的局部窗口连接，对应 WS 的环格子局部边。"),
    ("random attention", "注意力中的随机连接，对应 WS 的短程/长程捷径。"),
    ("global tokens", "与全序列相连的枢纽 token；BigBird 在 WS 直觉之外追加的星形结构。"),
    ("block sparse", "以块为单位的稀疏实现，使 GPU 能对选中块做稠密 GEMM。"),
]

REFS = [
    {
        "level": "本篇",
        "title": "Collective dynamics of ‘small-world’ networks",
        "why": "Watts & Strogatz, Nature 1998；逐段精读对象。",
        "url": "./paper.pdf",
        "ext": "https://doi.org/10.1038/30918",
    },
    {
        "level": "对照",
        "title": "BigBird 逐段精读",
        "why": "把 WS 的窗口+捷径直觉写进稀疏注意力。",
        "url": "../bigbird/index.html",
        "ext": "https://arxiv.org/abs/2007.14062",
    },
    {
        "level": "对照",
        "title": "BigBird 全流程（设计→硬件）",
        "why": "工程上为何「不删窗口、只加随机边」。",
        "url": "../bigbird/example.html",
        "ext": "",
    },
    {
        "level": "前驱",
        "title": "Milgram — The small world problem",
        "why": "社会小世界 / 六度分隔实验传统。",
        "url": "https://doi.org/10.1037/e400002009-005",
        "ext": "",
    },
    {
        "level": "专题",
        "title": "稀疏注意力专题",
        "why": "把小世界图直觉放回现代注意力谱系。",
        "url": "../../topics/sparse-attention/index.html",
        "ext": "",
    },
]
