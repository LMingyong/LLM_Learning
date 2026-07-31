#!/usr/bin/env python3
"""Build BigBird deep-dive study page."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "papers/bigbird/index.html"


def pattern_cells(kind: str, n: int = 14, cell: int = 11) -> tuple[str, int]:
    gap = 1
    size = n * (cell + gap)
    rects = []
    # deterministic "random" edges for teaching figure
    rnd = set()
    for i in range(n):
        for k in range(2):
            j = (i * 5 + k * 7 + 3) % n
            if j != i:
                rnd.add((i, j))
                rnd.add((j, i))  # often implemented symmetrically in encoder
    globals_ = {0, 1}
    for i in range(n):
        for j in range(n):
            x = j * (cell + gap)
            y = i * (cell + gap)
            dist = abs(i - j)
            color = "#e7e1d4"
            on = False
            if kind == "random":
                on = (i, j) in rnd
                color = "#1f4e79" if on else color
            elif kind == "window":
                on = dist <= 2
                color = "#0f6e56" if on else color
            elif kind == "global":
                on = i in globals_ or j in globals_
                color = "#b85c38" if on else color
            elif kind == "bigbird":
                on = dist <= 2 or i in globals_ or j in globals_ or (i, j) in rnd
                if i in globals_ or j in globals_:
                    color = "#b85c38"
                elif (i, j) in rnd and dist > 2:
                    color = "#1f4e79"
                elif dist <= 2:
                    color = "#0f6e56"
            op = "0.92" if on else "0.5"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
                f'fill="{color}" opacity="{op}"/>'
            )
    return "".join(rects), size


def fig_four() -> str:
    items = [
        ("random", "(a) Random"),
        ("window", "(b) Window"),
        ("global", "(c) Global"),
        ("bigbird", "(d) BIGBIRD"),
    ]
    parts = [
        '<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img">'
        '<rect width="760" height="230" fill="#fffcf5"/>'
    ]
    x = 22
    for kind, title in items:
        g, size = pattern_cells(kind)
        parts.append(f'<g transform="translate({x},40)">{g}</g>')
        parts.append(
            f'<text x="{x + size/2}" y="28" text-anchor="middle" '
            f'font-family="Manrope,sans-serif" font-size="12" font-weight="700" '
            f'fill="#1c2420">{title}</text>'
        )
        x += size + 30
    parts.append(
        '<g transform="translate(70,210)" font-family="Manrope,sans-serif" font-size="11" fill="#5a6a62">'
        '<rect width="10" height="10" rx="2" fill="#0f6e56"/><text x="14" y="9">局部窗口</text>'
        '<rect x="90" width="10" height="10" rx="2" fill="#b85c38"/><text x="104" y="9">全局</text>'
        '<rect x="160" width="10" height="10" rx="2" fill="#1f4e79"/><text x="174" y="9">随机边</text>'
        '<rect x="250" width="10" height="10" rx="2" fill="#e7e1d4"/><text x="264" y="9">不计算</text>'
        "</g></svg>"
    )
    return "\n".join(parts)


def fig_block() -> str:
    return """
<svg viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect width="720" height="250" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="360" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">块稀疏：按 block 决定整块是否参与（利于 GPU 块矩阵核）</text>
    <!-- token-level sparse messy -->
    <text x="170" y="55" text-anchor="middle" font-size="12" fill="#5a6a62">token 级稀疏（散点，难加速）</text>
    <g transform="translate(60,70)">
""" + "".join(
        f'<rect x="{(j%12)*14}" y="{(j//12)*14}" width="12" height="12" rx="2" fill="{"#1f4e79" if (i*j+i)%5==0 else "#e7e1d4"}"/>'
        for i in range(1) for j in range(48)
    ) + """
    </g>
    <!-- block sparse clean -->
    <text x="520" y="55" text-anchor="middle" font-size="12" fill="#5a6a62">block 级稀疏（整块 dense GEMM）</text>
    <g transform="translate(390,70)">
""" + "".join(
        f'<rect x="{c*52}" y="{r*52}" width="48" height="48" rx="6" fill="{"#0f6e56" if (r==c or r==0 or c==0 or (r+c)==3) else "#e7e1d4"}" opacity="0.9"/>'
        for r in range(4) for c in range(4)
    ) + """
    </g>
    <text x="360" y="235" text-anchor="middle" font-size="12" fill="#7d8c84">BigBird 工程实现常把随机/窗口/全局都落在「块」上，而不是每个 token 各选邻居</text>
  </g>
</svg>
"""


def fig_path() -> str:
    return """
<svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect width="720" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="360" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">为什么要随机边：缩短注意力图上的平均路径长度</text>
    <!-- only window: long path -->
    <text x="180" y="55" text-anchor="middle" font-size="12" fill="#0f6e56" font-weight="700">只有窗口：远距要多跳</text>
    <circle cx="80" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="130" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="180" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="230" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="280" cy="110" r="10" fill="#0f6e56"/>
    <path d="M90 110 H120 M140 110 H170 M190 110 H220 M240 110 H270" stroke="#0f6e56" stroke-width="2"/>
    <text x="180" y="150" text-anchor="middle" font-size="11" fill="#5a6a62">A → … → E 路径很长</text>

    <!-- with random shortcut -->
    <text x="520" y="55" text-anchor="middle" font-size="12" fill="#1f4e79" font-weight="700">加上随机捷径：小世界</text>
    <circle cx="420" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="470" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="520" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="570" cy="110" r="10" fill="#0f6e56"/>
    <circle cx="620" cy="110" r="10" fill="#0f6e56"/>
    <path d="M430 110 H460 M480 110 H510 M530 110 H560 M580 110 H610" stroke="#0f6e56" stroke-width="2"/>
    <path d="M420 100 Q520 40 620 100" fill="none" stroke="#1f4e79" stroke-width="2.2" stroke-dasharray="5 3"/>
    <text x="520" y="150" text-anchor="middle" font-size="11" fill="#5a6a62">A 一跳接近 E（随机边）</text>
    <text x="360" y="185" text-anchor="middle" font-size="12" fill="#7d8c84">再配合全局枢纽，理论可证明仍能逼近全注意力的表达能力</text>
  </g>
</svg>
"""


PAGE = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>BigBird 详解 · 局部 + 全局 + 随机</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;display=swap" rel="stylesheet"/>
<style>
:root{{
  --bg:#f6f3ec; --bg2:#efe9dc; --paper:#fffcf5; --ink:#1c2420; --muted:#5a6a62;
  --faint:#7d8c84; --line:#d8d0c0; --accent:#0f6e56; --accent-soft:#d8efe6;
  --warm:#b85c38; --warm-soft:#f3e0d6; --blue:#1f4e79; --blue-soft:#dce8f3;
  --shadow:0 12px 40px rgba(40,50,40,.08);
  --serif:"Literata",Georgia,"Noto Serif SC",serif;
  --sans:"Manrope",system-ui,"Noto Sans SC",sans-serif;
  --mono:ui-monospace,Menlo,monospace; --measure:44rem;
}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;color:var(--ink);font-family:var(--serif);font-size:18px;line-height:1.8;
background:radial-gradient(900px 500px at 0% 0%,rgba(15,110,86,.07),transparent 55%),
radial-gradient(700px 400px at 100% 8%,rgba(31,78,121,.06),transparent 50%),
linear-gradient(180deg,var(--bg),var(--bg2))}}
a{{color:var(--accent);text-underline-offset:3px}}
a:hover{{color:var(--warm)}}
.layout{{display:grid;grid-template-columns:250px minmax(0,1fr);min-height:100vh}}
.nav{{position:sticky;top:0;height:100vh;overflow:auto;padding:28px 18px 40px;border-right:1px solid var(--line);
background:rgba(255,252,245,.78);backdrop-filter:blur(10px);font-family:var(--sans)}}
.nav .brand{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);font-weight:700;margin:0 0 8px}}
.nav h1{{font-size:22px;margin:0 0 6px;line-height:1.25}}
.nav .sub{{font-size:12.5px;color:var(--muted);margin:0 0 18px;line-height:1.5}}
.nav a{{display:block;padding:8px 10px;border-radius:8px;color:var(--muted);text-decoration:none;font-size:13.5px;margin-bottom:2px}}
.nav a:hover,.nav a.active{{background:var(--accent-soft);color:var(--ink)}}
.nav .box{{margin-top:18px;padding:12px;border:1px solid var(--line);border-radius:12px;background:var(--paper);font-size:12px;color:var(--faint);line-height:1.55}}
.main{{padding:28px 40px 100px;max-width:880px}}
.toolbar{{position:sticky;top:0;z-index:10;margin:0 -40px 22px;padding:12px 40px;display:flex;flex-wrap:wrap;gap:8px;
background:rgba(246,243,236,.92);border-bottom:1px solid var(--line);backdrop-filter:blur(8px);font-family:var(--sans)}}
.btn{{border:1px solid var(--line);background:var(--paper);color:var(--ink);border-radius:999px;padding:8px 12px;font-size:12.5px;text-decoration:none}}
.btn:hover{{border-color:var(--accent);color:var(--accent)}}
.btn.primary{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.hero{{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:28px 30px;box-shadow:var(--shadow);margin-bottom:10px}}
.hero h2{{font-family:var(--sans);font-size:32px;margin:0 0 12px;letter-spacing:-.02em;line-height:1.25}}
.hero p{{margin:0;color:var(--muted);font-family:var(--sans);font-size:15.5px;line-height:1.7;max-width:48rem}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}}
.pill{{font-family:var(--sans);font-size:12px;padding:6px 11px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}}
.pill.warm{{background:var(--warm-soft);color:var(--warm)}}
.pill.blue{{background:var(--blue-soft);color:var(--blue)}}
h3.sec{{font-family:var(--sans);font-size:24px;margin:48px 0 16px;scroll-margin-top:76px;letter-spacing:-.02em}}
h3.sec .num{{color:var(--accent);margin-right:10px}}
h4{{font-family:var(--sans);font-size:17px;margin:26px 0 10px}}
.prose p{{margin:0 0 1.05em;max-width:var(--measure)}}
.prose ul,.prose ol{{max-width:var(--measure)}}
.prose li{{margin:0 0 .45em}}
.callout{{border-left:4px solid var(--accent);background:var(--accent-soft);padding:14px 16px;border-radius:0 12px 12px 0;
margin:16px 0 22px;font-family:var(--sans);font-size:15px;line-height:1.65;color:#163a30;max-width:48rem}}
.callout.warm{{border-color:var(--warm);background:var(--warm-soft);color:#5a2e1c}}
.callout.blue{{border-color:var(--blue);background:var(--blue-soft);color:#1a3550}}
.fig{{background:var(--paper);border:1px solid var(--line);border-radius:16px;padding:14px;margin:18px 0 6px;box-shadow:var(--shadow);overflow:auto}}
.fig svg{{display:block;width:100%;height:auto;max-width:760px;margin:0 auto}}
.caption{{font-family:var(--sans);font-size:13px;color:var(--faint);margin:0 0 22px;text-align:center}}
.formula{{font-family:var(--mono);font-size:13.5px;line-height:1.65;background:#1c2420;color:#e8f2ec;border-radius:14px;
padding:14px 16px;overflow:auto;margin:12px 0 20px;max-width:48rem;white-space:pre}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0 22px}}
.card{{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
.card h5{{font-family:var(--sans);margin:0 0 6px;font-size:14.5px}}
.card p{{margin:0;font-family:var(--sans);font-size:13.5px;color:var(--muted);line-height:1.55}}
.compare{{width:100%;border-collapse:collapse;font-family:var(--sans);font-size:14px;margin:12px 0 22px;max-width:48rem}}
.compare th,.compare td{{border:1px solid var(--line);padding:10px 12px;text-align:left;background:var(--paper);vertical-align:top}}
.compare th{{background:var(--accent-soft);color:#163a30}}
.term-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:10px;margin:12px 0}}
.term{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:12px 14px}}
.term b{{font-family:var(--sans);color:var(--warm);display:block;margin-bottom:4px;font-size:14px}}
.term p{{margin:0;font-family:var(--sans);font-size:13.5px;color:var(--muted);line-height:1.5}}
.refgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}}
.ref{{display:flex;flex-direction:column;gap:6px;background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:14px;min-height:120px}}
.ref .tag{{font-family:var(--sans);font-size:11px;align-self:start;padding:3px 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent)}}
.ref h5{{margin:0;font-family:var(--sans);font-size:14.5px}}
.ref p{{margin:0;font-family:var(--sans);font-size:13.5px;color:var(--muted);flex:1;line-height:1.5}}
@media (max-width:900px){{
  .layout{{grid-template-columns:1fr}}
  .nav{{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}}
  .main{{padding:18px 16px 80px}}
  .toolbar{{margin:0 -16px 16px;padding:10px 16px}}
  .grid2{{grid-template-columns:1fr}}
  .hero h2{{font-size:26px}}
}}
</style>
</head>
<body>
<div class="layout">
<aside class="nav">
  <div class="brand">LLM Learning · Paper</div>
  <h1>BigBird</h1>
  <p class="sub">Zaheer et al., 2020 · 局部 + 全局 + 随机稀疏注意力</p>
  <nav id="toc">
    <a href="#why">1. 要解决什么</a>
    <a href="#blocks">2. 三块积木一图看懂</a>
    <a href="#graph">3. 图稀疏化直觉</a>
    <a href="#random">4. 随机边为什么重要</a>
    <a href="#global">5. 全局 token（ITC/ETC）</a>
    <a href="#block">6. 块稀疏工程意义</a>
    <a href="#theory">7. 理论承诺</a>
    <a href="#vs">8. 和 Longformer 对比</a>
    <a href="#use">9. 任务与影响</a>
    <a href="#glossary">10. 名词</a>
    <a href="#refs">11. 原文</a>
  </nav>
  <div class="box">
    读完 Longformer 再读这篇最顺：BigBird = 窗口 + 全局，再加<strong>随机块</strong>，并给出更强理论。<br/><br/>
    <a href="../longformer/index.html">Longformer 专页</a> ·
    <a href="../../topics/sparse-attention/index.html">稀疏专题</a>
  </div>
</aside>

<main class="main">
  <div class="toolbar">
    <a class="btn primary" href="./paper.pdf" target="_blank">打开原文 PDF</a>
    <a class="btn" href="https://arxiv.org/abs/2007.14062" target="_blank">arXiv:2007.14062</a>
    <a class="btn" href="../longformer/index.html">Longformer →</a>
    <a class="btn" href="../../topics/sparse-attention/index.html">← 稀疏专题</a>
  </div>

  <header class="hero">
    <h2>BigBird：局部 + 全局 + 随机块</h2>
    <p>论文 <em>Big Bird: Transformers for Longer Sequences</em>（Zaheer et al., Google Research, 2020）。它在滑动窗口与全局 token 之外，再引入<strong>随机稀疏边</strong>（工程上常以块为单位），把全注意力的二次依赖降到线性，并证明这种稀疏注意力仍是序列函数的万能近似器、在标准假设下图灵完备——这正是你在稀疏专题 3.3 看到的那段话的出处。</p>
    <div class="pills">
      <span class="pill">三件套：R + W + G</span>
      <span class="pill warm">复杂度线性</span>
      <span class="pill blue">块稀疏 · 可上 8× 长度</span>
    </div>
  </header>

  <article class="prose">

  <h3 class="sec" id="why"><span class="num">01</span>要解决什么</h3>

  <p>和 Longformer 同一痛点：BERT 式全自注意力内存随长度平方涨，硬件上常见上限约 512。问答、摘要、文档分类、基因组序列等都需要更长上下文。</p>

  <p>BigBird 不只想「跑得动」，还想回答两个理论问题：</p>
  <ol>
    <li>能不能用<strong>更少的内积</strong>仍吃到全注意力的经验红利？</li>
    <li>稀疏之后，Transformer 的<strong>表达力</strong>（万能近似、图灵完备）还在不在？</li>
  </ol>
  <p>答案是：用「全局 + 窗口 + 随机」构图，复杂度线性，理论性质保留，经验上在 QA / 摘要等任务显著受益，上下文可到此前同类硬件的约 <strong>8×</strong>。</p>


  <h3 class="sec" id="blocks"><span class="num">02</span>三块积木一图看懂</h3>

  <p>论文 Figure 1 把注意力拆成积木再拼起来。白色表示不算注意力：</p>

  <div class="fig">{fig_four()}</div>
  <p class="caption">图 1 · 对齐论文 Fig.1：(a) 随机 (b) 滑动窗口 (c) 全局 (d) 三者合成的 BIGBIRD。</p>

  <div class="grid2">
    <div class="card"><h5>Random · 随机</h5><p>每个 token（或块）再连 r 个随机位置。缩短图上平均路径，形成「小世界」捷径。</p></div>
    <div class="card"><h5>Window · 局部</h5><p>宽度 w 的滑动窗口，捕捉邻近语言学结构；Clark 等发现邻近内积极重要。</p></div>
    <div class="card"><h5>Global · 全局</h5><p>g 个全局位与全序列互通。理论证明里关键；经验上 CLS 等也极有用。</p></div>
    <div class="card"><h5>合起来</h5><p>边数约 O(n·(w+r+g)) 量级，相对 n² 是线性。论文消融：单靠 R 或 W 都不够接近 BERT。</p></div>
  </div>

  <div class="callout">
    <strong>和你截图那段话的对应：</strong>「窗口与全局之外再加随机稀疏边」= (a)+(b)+(c)→(d)；「缩短平均路径长度」= 小世界直觉；「块稀疏」= 工程上把这些边落成 block mask，方便块矩阵核。
  </div>


  <h3 class="sec" id="graph"><span class="num">03</span>图稀疏化直觉</h3>

  <p>作者把自注意力看成有向图：节点是 token，边是「query i 是否看 key j」。全注意力 = 完全图，贵。问题变成：<strong>稀疏化这张图，还要近似完全图的好性质。</strong></p>

  <p>两个愿望：</p>
  <ul>
    <li><strong>短平均路径</strong>——信息别在图上绕太远（随机图 / 扩展图擅长这个）；</li>
    <li><strong>局部性</strong>——语言和生物序列高度依赖邻居（高聚类系数；Watts–Strogatz 小世界模型：先做环上的窗口邻居，再rewire/加随机边）。</li>
  </ul>

  <p>于是自然得到：先保留窗口（局部），再加随机边（短路径），最后由理论补上全局星形结构。</p>

  <div class="formula">广义注意力（论文式 AT）：
对每个头 h，位置 i 只对邻居集 N(i) 做
  σ( Qh(xi) Kh(X_N(i))ᵀ ) · Vh(X_N(i))
N(i) 由稀疏图 D 的出边决定；D 完全图时退回标准 Transformer。</div>


  <h3 class="sec" id="random"><span class="num">04</span>随机边为什么重要</h3>

  <div class="fig">{fig_path()}</div>
  <p class="caption">图 2 · 仅窗口时远距多跳；随机捷径让平均路径变短（小世界）。</p>

  <p>论文表格消融（512 设定下的直观对比）说明：只用 Random 或只用 Window，MLM/SQuAD/MNLI 都明显弱于 BERT；<strong>R+W</strong> 会好很多，但仍需全局才能真正站稳。随机边不是装饰——它负责「远距一跳可达」，补窗口多层扩散太慢的问题。</p>

  <div class="callout warm">
    <strong>实现细节：</strong>经典 Watts–Strogatz 会「删掉一些局部边再随机重连」。硬件上删边不划算，BigBird 选择<strong>保留局部边并额外加随机边</strong>，性质不受损，kernel 更好写。
  </div>


  <h3 class="sec" id="global"><span class="num">05</span>全局 token：ITC 与 ETC</h3>

  <p>全局位有两种构造（名称来自 Extended Transformer Construction 一脉）：</p>

  <table class="compare">
    <tr><th>变体</th><th>怎么做</th><th>直觉</th></tr>
    <tr><td><strong>BIGBIRD-ITC</strong></td><td>把输入里已有的某些位置标成 global（行列全 1）</td><td>类似 Longformer：问题词 / CLS 当枢纽</td></tr>
    <tr><td><strong>BIGBIRD-ETC</strong></td><td>额外插入 g 个新的全局 token，与所有原 token 互连</td><td>多一块「外部记忆」存全局上下文</td></tr>
  </table>

  <p>理论部分甚至用「星形图」（中心点连所有人）证明：只要稀疏图<strong>包含</strong>这种星形，就能在 O(n) 内积下逼近连续序列函数。这为「必须有全局位」提供了证明动机，而不只是工程启发式。</p>


  <h3 class="sec" id="block"><span class="num">06</span>块稀疏：工程上真正能加速的关键</h3>

  <div class="fig">{fig_block()}</div>
  <p class="caption">图 3 · token 级散点稀疏难吃满 GPU；block 级稀疏让每个允许块内部仍是 dense GEMM。</p>

  <p>若每个 query 各自 gather 一串不规则 key，内存访问碎片化，Tensor Core 不高兴。BigBird 把随机/窗口/全局都落成<strong>块级掩码</strong>：</p>
  <ul>
    <li>序列切成大小为 B 的块；</li>
    <li>「随机连 r 个」变成「随机连 r 个块」；</li>
    <li>窗口也按块邻域定义；</li>
    <li>允许的 (query块, key块) 内部跑普通密集乘加。</li>
  </ul>

  <div class="callout blue">
    <strong>记住这句话：</strong>稀疏图案决定「哪些块存在」；块内仍 dense。这与后来 Flash Attention 的 tiling 哲学相容——先决定加载哪些块，再在片上高效算。
  </div>


  <h3 class="sec" id="theory"><span class="num">07</span>理论承诺（读论文时抓住的点）</h3>

  <ul>
    <li><strong>万能近似：</strong>对包含星形全局结构的稀疏注意力，Transformer 编码器仍能以任意精度逼近紧集上的连续序列到序列函数（扩展了 Yun et al. 对全注意力的结果）。</li>
    <li><strong>图灵完备：</strong>在有限精度等标准假设下，BigBird 稀疏 Transformer 仍可模拟图灵机（对照 Pérez et al. 对全 Transformer 的结果）。</li>
    <li><strong>没有免费午餐：</strong>论文也给出下界——某些任务上，足够稀疏的机制可能需要多项式更多层。稀疏省的是每层边数，不是魔法无限表达。</li>
  </ul>


  <h3 class="sec" id="vs"><span class="num">08</span>和 Longformer 怎么对照读</h3>

  <table class="compare">
    <tr><th></th><th>Longformer</th><th>BigBird</th></tr>
    <tr><td>局部</td><td>滑动窗口（LM 可用扩张）</td><td>滑动窗口</td></tr>
    <tr><td>全局</td><td>任务选位，对称 attend</td><td>ITC / ETC 两种全局</td></tr>
    <tr><td>额外</td><td>—</td><td><strong>随机边 / 随机块</strong></td></tr>
    <tr><td>理论</td><td>偏工程与任务实证</td><td>万能近似 + 图灵完备证明</td></tr>
    <tr><td>工程关键词</td><td>banded / chunk 实现</td><td><strong>块稀疏</strong>矩阵核</td></tr>
  </table>

  <p>可以记：<strong>Longformer = 窗口 + 全局</strong>；<strong>BigBird = 窗口 + 全局 + 随机</strong>，并系统讨论「为什么这样稀疏仍然够强」。</p>


  <h3 class="sec" id="use"><span class="num">09</span>任务表现与后续影响</h3>

  <p>更长上下文带来：多项 QA、文档摘要刷新当时结果；还把注意力模型应用到 DNA 等基因组序列的上下文表示（启动子区域、染色质谱预测等）。</p>

  <p>谱系上：它巩固了「局部 + 全局」工业骨架，并把<strong>随机块 / 块稀疏</strong>写成可复述的标准零件。今天读 NSA、Flash 窗口核、各种 block-sparse kernel，都能在 BigBird 这里找到工程与理论的接合点。</p>


  <h3 class="sec" id="glossary"><span class="num">10</span>名词速查</h3>
  <div class="term-grid">
    <div class="term"><b>random attention</b><p>每个位置额外连接 r 个随机 key（常按块）。</p></div>
    <div class="term"><b>window attention</b><p>只连接左右各 w/2 邻域。</p></div>
    <div class="term"><b>global tokens</b><p>与全序列互连的枢纽；理论星形结构的来源。</p></div>
    <div class="term"><b>ITC / ETC</b><p>用现有位置当全局，或额外插入全局 token。</p></div>
    <div class="term"><b>block sparse</b><p>以块为单位的稀疏掩码；块内 dense。</p></div>
    <div class="term"><b>small-world graph</b><p>高局部聚类 + 短平均路径的随机图模型。</p></div>
    <div class="term"><b>universal approximator</b><p>能任意逼近某类连续序列函数。</p></div>
    <div class="term"><b>Turing complete</b><p>在假设下可模拟任意计算（图灵机）。</p></div>
  </div>


  <h3 class="sec" id="refs"><span class="num">11</span>原文与延伸</h3>
  <div class="refgrid">
    <div class="ref"><span class="tag">本篇</span><h5>Big Bird: Transformers for Longer Sequences</h5><p>局部+全局+随机；块稀疏与理论证明的主文献。</p><a href="./paper.pdf">本地 PDF</a> · <a href="https://arxiv.org/abs/2007.14062">arXiv</a></div>
    <div class="ref"><span class="tag">必读对照</span><h5>Longformer</h5><p>窗口+全局的任务向经典；建议与本篇对照读。</p><a href="../longformer/index.html">专页</a></div>
    <div class="ref"><span class="tag">谱系</span><h5>稀疏注意力专题</h5><p>把 BigBird 放回 Sparse Transformer → Longformer → NSA 时间线。</p><a href="../../topics/sparse-attention/index.html">打开</a></div>
    <div class="ref"><span class="tag">实现</span><h5>Flash Attention</h5><p>块被选中之后，如何在 GPU 上高效算。</p><a href="../../topics/flash-attention/index.html">打开</a></div>
  </div>

  <p style="margin-top:36px;font-family:var(--sans);font-size:13px;color:var(--faint)">示意图为教学重绘，对应论文 Fig.1 结构。证明细节与实验数字以 <a href="./paper.pdf">paper.pdf</a> 为准。</p>
  </article>
</main>
</div>
<script>
const links=[...document.querySelectorAll('#toc a')];
const secs=links.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
const io=new IntersectionObserver(es=>{{
  es.forEach(en=>{{
    if(!en.isIntersecting) return;
    const id='#'+en.target.id;
    links.forEach(a=>a.classList.toggle('active', a.getAttribute('href')===id));
  }});
}}, {{rootMargin:'-20% 0px -65% 0px', threshold:0.01}});
secs.forEach(s=>io.observe(s));
</script>
</body>
</html>
"""

# Fix fig_block - the nested string concat in f-string for PAGE uses fig_block() which has its own concat - need to fix fig_block to not break
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(PAGE, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
