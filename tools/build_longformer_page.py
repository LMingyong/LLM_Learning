#!/usr/bin/env python3
"""Build a detailed Longformer study page (light, diagram-rich)."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "papers/longformer/index.html"


def pattern_cells(kind: str, n: int = 14, cell: int = 11) -> tuple[str, int]:
    gap = 1
    size = n * (cell + gap)
    rects = []
    for i in range(n):
        for j in range(n):
            x = j * (cell + gap)
            y = i * (cell + gap)
            # bidirectional for encoder-style Longformer diagrams
            dist = abs(i - j)
            color = "#ebe6db"
            on = False
            if kind == "full":
                on = True
                color = "#0f6e56"
            elif kind == "window":
                w = 2
                on = dist <= w
                color = "#0f6e56" if on else "#e7e1d4"
            elif kind == "dilated":
                # window with gaps: attend every other within span
                span = 5
                on = dist <= span and (dist % 2 == 0 or dist <= 1)
                color = "#1f4e79" if on and dist > 1 else ("#0f6e56" if on else "#e7e1d4")
            elif kind == "global":
                w = 2
                globals_ = {1, 2}  # a few global positions
                on = dist <= w or i in globals_ or j in globals_
                if i in globals_ or j in globals_:
                    color = "#b85c38"
                elif dist <= w:
                    color = "#0f6e56"
                else:
                    color = "#e7e1d4"
            op = "0.92" if on else "0.5"
            rects.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{color}" opacity="{op}"/>'
            )
    return "".join(rects), size


def fig_four_patterns() -> str:
    items = [
        ("full", "(a) Full n² attention"),
        ("window", "(b) Sliding window"),
        ("dilated", "(c) Dilated window"),
        ("global", "(d) Global + window"),
    ]
    parts = [
        '<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Longformer 四种注意力图案">'
    ]
    parts.append('<rect width="760" height="230" fill="#fffcf5"/>')
    x = 22
    for kind, title in items:
        g, size = pattern_cells(kind)
        parts.append(f'<g transform="translate({x},40)">{g}</g>')
        parts.append(
            f'<text x="{x + size/2}" y="28" text-anchor="middle" font-family="Manrope,sans-serif" '
            f'font-size="12" font-weight="700" fill="#1c2420">{title}</text>'
        )
        x += size + 30
    parts.append(
        '<g transform="translate(80,210)" font-family="Manrope,sans-serif" font-size="11" fill="#5a6a62">'
        '<rect width="10" height="10" rx="2" fill="#0f6e56"/><text x="14" y="9">局部窗口</text>'
        '<rect x="90" width="10" height="10" rx="2" fill="#1f4e79"/><text x="104" y="9">空洞/扩张</text>'
        '<rect x="190" width="10" height="10" rx="2" fill="#b85c38"/><text x="204" y="9">全局 token 相关边</text>'
        '<rect x="330" width="10" height="10" rx="2" fill="#e7e1d4"/><text x="344" y="9">不计算</text>'
        "</g></svg>"
    )
    return "\n".join(parts)


def fig_hub() -> str:
    circles = []
    for i in range(13):
        r = 14 if i in (1, 2) else 9
        fill = "#b85c38" if i in (1, 2) else "#0f6e56"
        circles.append(f'<circle cx="{60 + i * 50}" cy="120" r="{r}" fill="{fill}"/>')
    circles_svg = "".join(circles)
    return f"""
<svg viewBox="0 0 720 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="枢纽车站类比">
  <rect width="720" height="220" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="360" y="24" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">把文档想成一条铁路：普通站只连邻居，枢纽站连全线</text>
    <path d="M60 120 H660" stroke="#0f6e56" stroke-width="2.5" fill="none"/>
    {circles_svg}
    <path d="M110 120 Q360 40 610 120" fill="none" stroke="#b85c38" stroke-width="1.8" stroke-dasharray="4 3" opacity="0.85"/>
    <path d="M160 120 Q360 200 560 120" fill="none" stroke="#b85c38" stroke-width="1.8" stroke-dasharray="4 3" opacity="0.7"/>
    <text x="110" y="158" text-anchor="middle" font-size="11" fill="#b85c38" font-weight="700">全局枢纽 [CLS] / 问题词</text>
    <text x="360" y="190" text-anchor="middle" font-size="12" fill="#5a6a62">绿色：滑动窗口局部边 · 橙色虚线：全局枢纽与全序列互通</text>
  </g>
</svg>
"""


def fig_receptive() -> str:
    return """
<svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect width="720" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="360" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">多层窗口如何扩大感受野（论文：顶层 ≈ ℓ × w）</text>
    <!-- layer boxes -->
    <rect x="40" y="50" width="640" height="36" rx="8" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="60" y="73" font-size="12" fill="#0f6e56" font-weight="700">第 1 层</text>
    <text x="200" y="73" font-size="12" fill="#5a6a62">每个 token 只看窗口 w → 局部搭配、邻近语法</text>

    <rect x="40" y="96" width="640" height="36" rx="8" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="60" y="119" font-size="12" fill="#1f4e79" font-weight="700">第 2 层</text>
    <text x="200" y="119" font-size="12" fill="#5a6a62">邻居的邻居也被间接看见 → 感受野变宽</text>

    <rect x="40" y="142" width="640" height="36" rx="8" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="60" y="165" font-size="12" fill="#b85c38" font-weight="700">第 ℓ 层</text>
    <text x="200" y="165" font-size="12" fill="#5a6a62">理论可达 ℓ×w（再加扩张 d 可达 ℓ×d×w）· 类似 CNN 堆叠</text>
  </g>
</svg>
"""


PAGE = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Longformer 详解 · 局部 + 全局注意力</title>
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
radial-gradient(700px 400px at 100% 8%,rgba(184,92,56,.06),transparent 50%),
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
.prose ul,.prose ol{{max-width:var(--measure);color:var(--ink)}}
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
  <h1>Longformer</h1>
  <p class="sub">Beltagy et al., 2020 · 局部窗口 + 任务驱动全局注意力</p>
  <nav id="toc">
    <a href="#why">1. 为什么需要它</a>
    <a href="#idea">2. 核心想法一图看懂</a>
    <a href="#window">3. 滑动窗口详解</a>
    <a href="#dilated">4. 扩张窗口</a>
    <a href="#global">5. 全局注意力</a>
    <a href="#proj">6. 两套投影 QK V</a>
    <a href="#impl">7. 实现与复杂度</a>
    <a href="#tasks">8. 任务里怎么设全局位</a>
    <a href="#led">9. LED 与后续影响</a>
    <a href="#glossary">10. 名词</a>
    <a href="#refs">11. 原文</a>
  </nav>
  <div class="box">
    这篇是稀疏注意力里「局部 + 全局」范式的经典源头。<br/><br/>
    相关：<a href="../../topics/sparse-attention/index.html">稀疏注意力专题</a>
  </div>
</aside>

<main class="main">
  <div class="toolbar">
    <a class="btn primary" href="./paper.pdf" target="_blank">打开原文 PDF</a>
    <a class="btn" href="https://arxiv.org/abs/2004.05150" target="_blank">arXiv:2004.05150</a>
    <a class="btn" href="https://github.com/allenai/longformer" target="_blank">官方代码</a>
    <a class="btn" href="../../topics/sparse-attention/index.html">← 稀疏专题</a>
  </div>

  <header class="hero">
    <h2>Longformer：局部窗口 + 全局 token</h2>
    <p>论文全名 <em>Longformer: The Long-Document Transformer</em>（Beltagy, Peters, Cohan, AllenAI, 2020）。它把标准自注意力的 O(n²) 换成<strong>近似线性</strong>的稀疏图案：用滑动窗口建局部上下文，再用少量「任务驱动」的全局位置打通整篇文档——正是你截图里那段「90% 局部 + 少量全局」工业骨架的出处。</p>
    <div class="pills">
      <span class="pill">复杂度 ≈ O(n·w)</span>
      <span class="pill warm">对称全局注意力</span>
      <span class="pill blue">可替换 RoBERTa 注意力</span>
    </div>
  </header>

  <article class="prose">

  <h3 class="sec" id="why"><span class="num">01</span>为什么需要它</h3>

  <p>Transformer 的自注意力让每个位置看全序列，表达力强，但时间和显存都随长度 <strong>平方</strong>增长。BERT/RoBERTa 时代常见上限是 512 tokens。处理长文档时，人们只好：</p>
  <ul>
    <li><strong>截断</strong>——丢掉后半篇；</li>
    <li><strong>切块分别编码再拼</strong>——块与块之间信息难交互；</li>
    <li><strong>两阶段检索</strong>——先找相关段落再读，误差会级联。</li>
  </ul>
  <p>Longformer 的目标很明确：做一个<strong>可直接替换</strong>标准自注意力的模块，复杂度随长度近似线性，从而在<strong>单次前向</strong>里吃完整篇长文，而不是为每个任务发明复杂拼接架构。</p>

  <div class="callout">
    <strong>论文主张：</strong>注意力图案 = 窗口局部注意力 + 任务动机的全局注意力；二者缺一不可——局部负责建上下文表示，全局负责为下游预测聚合全序列信息。
  </div>


  <h3 class="sec" id="idea"><span class="num">02</span>核心想法一图看懂</h3>

  <p>论文 Figure 2 对比了四种图案。下面用教学重绘对齐原意（行/列都是 token 位置，着色表示「这一对要算注意力」）：</p>

  <div class="fig">{fig_four_patterns()}</div>
  <p class="caption">图 1 · 对应论文 Fig.2：(a) 全连接 (b) 滑动窗口 (c) 扩张窗口 (d) 全局 + 窗口。Longformer 下游任务主要用 (d)。</p>

  <div class="fig">{fig_hub()}</div>
  <p class="caption">图 2 · 枢纽车站类比：普通 token 只连邻居；[CLS]/问题词等少数枢纽与全线互通，网络仍连通，边数近线性。</p>


  <h3 class="sec" id="window"><span class="num">03</span>滑动窗口详解</h3>

  <p>给定窗口宽度 w，每个 token 关注左右各约 w/2 个位置（编码器设定下是双向的）。单层复杂度 O(n×w)，对长度 n 线性。</p>

  <div class="formula">对位置 i：
  S(i) = {{ i − w/2 , … , i + w/2 }}   （再按任务做因果裁剪）
只对 j ∈ S(i) 计算 softmax(q_i · k_j)</div>

  <p>只有一层时，模型「看不见」窗口外。但 Longformer 强调：<strong>堆叠多层</strong>后，信息可以像 CNN 一样逐层扩散——第 2 层能间接用到第 1 层邻居的邻居。若每层窗口同为 w、共 ℓ 层，顶层理论感受野约 <strong>ℓ × w</strong>。</p>

  <div class="fig">{fig_receptive()}</div>
  <p class="caption">图 3 · 多层窗口扩大感受野；字符级 LM 实验里还会让高层用更大窗口。</p>

  <div class="callout warm">
    <strong>消融结论（论文精神）：</strong>光有局部窗口，模型擅长「读懂附近的话」，但不擅长把整篇压成一个分类向量或对齐问答——所以必须加全局注意力，而不是把 w 开到整个 n（那又变回平方）。
  </div>


  <h3 class="sec" id="dilated"><span class="num">04</span>扩张（Dilated）滑动窗口</h3>

  <p>为了在不增加太多计算的前提下看得更远，可以把窗口「打洞」：在跨度内每隔 dilation d 取一个位置（类比扩张卷积）。固定 d、w 时，ℓ 层感受野可到约 <strong>ℓ × d × w</strong>，轻松到数万字符量级。</p>

  <p>多头时可以<strong>每头不同扩张</strong>：有的头 d=1 死盯局部，有的头 d&gt;1 跳着看远处。论文在<strong>字符级自回归 LM</strong>里大量使用扩张窗口；在 RoBERTa 继续预训练 + 下游微调设定里，更常用「普通窗口 + 全局」，实现也更简单（chunk 实现不支持 dilation）。</p>


  <h3 class="sec" id="global"><span class="num">05</span>全局注意力：任务驱动的枢纽</h3>

  <p>这是 Longformer 相对「纯窗口模型」最关键的设计，也是你截图段落的重点。</p>

  <h4>5.1 对称全局</h4>
  <p>选定少量位置 G（与 n 无关、数量很小）。对任意 g ∈ G：</p>
  <ul>
    <li>g 可以 attend 序列中<strong>所有</strong> token；</li>
    <li>序列中<strong>所有</strong> token 也可以 attend g。</li>
  </ul>
  <p>也就是说全局边是<strong>对称</strong>的：枢纽既读全篇，也被全篇读。这样分类头看 [CLS]、或文档里每个词对齐问题词，都有一条短路径，而不必指望信息只靠多层窗口慢慢渗过去。</p>

  <h4>5.2 为什么说「任务动机」</h4>
  <p>全局位置不是随机撒的，而是按任务先验指定：</p>
  <table class="compare">
    <tr><th>任务</th><th>典型全局位</th><th>意图</th></tr>
    <tr><td>文本分类</td><td>[CLS]</td><td>把全篇聚到一个向量</td></tr>
    <tr><td>问答 QA</td><td>问题里所有 token</td><td>文档每个位置都能直接对问题</td></tr>
    <tr><td>核心指代等</td><td>任务相关特殊位置</td><td>注入归纳偏置</td></tr>
  </table>

  <p>因为 |G| ≪ n 且与 n 无关，局部 O(n·w) 加上全局 O(n·|G|)，整体仍是 <strong>O(n)</strong>。</p>

  <div class="callout blue">
    <strong>和「只加一个可学习记忆向量」的差别：</strong>Longformer 的全局位通常是<strong>输入里真实存在的 token</strong>（问题词、[CLS]），带有内容；对称 attend 让文档侧每个位置都能直接写/读这些枢纽，而不是只在顶层池化一次。
  </div>


  <h3 class="sec" id="proj"><span class="num">06</span>两套线性投影（容易忽略但很重要）</h3>

  <p>标准注意力用一套 Q,K,V。Longformer 发现：局部窗口与全局枢纽的「比较方式」不同，最好分开参数化：</p>
  <div class="formula">滑动窗口：用 Qs, Ks, Vs
全局注意力：用 Qg, Kg, Vg
（初始化时让 g 套与 s 套相同，再微调）</div>
  <p>论文明确写：额外投影带来的灵活性对下游最佳性能<strong>至关重要</strong>。直觉上，[CLS] 聚合全篇时需要的 query 方向，和局部词预测邻居时的 query 方向，不必绑死在同一组矩阵上。</p>


  <h3 class="sec" id="impl"><span class="num">07</span>实现与复杂度</h3>

  <div class="grid2">
    <div class="card"><h5>复杂度</h5><p>窗口 O(n·w)；加少量全局仍 O(n)。相对 full O(n²)，长序列省显存是第一卖点（论文 Fig.1）。</p></div>
    <div class="card"><h5>实现难点</h5><p>要算 QKᵀ 的「带状对角线」而非常规 GEMM。作者对比 loop / chunk / 自定义 CUDA：chunk 最快但无 dilation；CUDA 内核用于 LM。</p></div>
    <div class="card"><h5>预训练策略</h5><p>从 RoBERTa checkpoint 继续 MLM 预训练，再微调——证明稀疏注意力可作 drop-in replacement。</p></div>
    <div class="card"><h5>LM 训练技巧</h5><p>分阶段加长序列与窗口：先让模型学会局部，再扩大上下文（否则一上来超长窗口难训）。</p></div>
  </div>


  <h3 class="sec" id="tasks"><span class="num">08</span>放到具体任务里怎么操作</h3>

  <h4>分类</h4>
  <p>输入仍是 <code>[CLS] + 文档</code>。只把 [CLS] 标成 global。每个文档 token 做窗口注意力，并都能看到 [CLS]；[CLS] 看到全文档。分类头只读 [CLS] 最终向量——与 BERT 用法一致，但文档可以远长于 512。</p>

  <h4>问答</h4>
  <p>拼接 <code>问题 + 文档</code>。把<strong>问题侧所有 token</strong>标成 global。于是文档每个位置都能直接对问题做注意力（对称地，问题也读全文档）。这比「先检索段落再 BERT」更干脆：单次编码整段上下文。</p>

  <h4>和切块法对比</h4>
  <p>切块法在块边界切断注意力；Longformer 用窗口多层扩散 + 全局枢纽，保留跨段交互，任务头可以保持简单。</p>


  <h3 class="sec" id="led"><span class="num">09</span>LED、结果与后续影响</h3>

  <p>论文还提出 <strong>Longformer-Encoder-Decoder (LED)</strong>：编码器用 Longformer 稀疏注意力，解码器侧处理生成，用于长文档摘要等 seq2seq（如 arXiv summarization）。</p>

  <p>实证上：字符级 LM 在 text8/enwik8 刷新或追平同期；继续预训练后在多个长文档任务上稳定强于 RoBERTa，WikiHop、TriviaQA 等达到当时 SOTA。</p>

  <p>后续脉络：ETC、BigBird（局部+全局+随机，并给理论）、以及今天 LLM 里常见的 sliding window / attention sink，都能看作这一思想的延伸。你在稀疏专题里看到的「工业骨架：90% 局部 + 少量全局」，正是 Longformer 这一设计被工程化以后的口头总结。</p>


  <h3 class="sec" id="glossary"><span class="num">10</span>名词速查</h3>
  <div class="term-grid">
    <div class="term"><b>sliding window attention</b><p>每个位置只与固定宽度邻域做注意力。</p></div>
    <div class="term"><b>dilated sliding window</b><p>窗口内按步长跳着取位置，扩大感受野。</p></div>
    <div class="term"><b>global attention</b><p>少数位置与全序列对称互连的枢纽注意力。</p></div>
    <div class="term"><b>task-motivated</b><p>全局位按任务先验选取（[CLS]、问题词等）。</p></div>
    <div class="term"><b>receptive field</b><p>多层堆叠后，顶层能间接聚合到的输入跨度。</p></div>
    <div class="term"><b>drop-in replacement</b><p>可替换标准自注意力而不改整体预训练范式。</p></div>
    <div class="term"><b>LED</b><p>Longformer Encoder-Decoder，用于长文本生成。</p></div>
    <div class="term"><b>Qg,Kg,Vg</b><p>专供全局注意力的另一套投影参数。</p></div>
  </div>


  <h3 class="sec" id="refs"><span class="num">11</span>原文与延伸</h3>
  <div class="refgrid">
    <div class="ref"><span class="tag">本篇</span><h5>Longformer: The Long-Document Transformer</h5><p>局部 + 全局稀疏注意力经典论文；请以 PDF 公式与 Fig.2 为准。</p><a href="./paper.pdf">本地 PDF</a> · <a href="https://arxiv.org/abs/2004.05150">arXiv</a></div>
    <div class="ref"><span class="tag">相关</span><h5>稀疏注意力专题</h5><p>把 Longformer 放回窗口 / BigBird / NSA 谱系里对照读。</p><a href="../../topics/sparse-attention/index.html">打开专题</a></div>
    <div class="ref"><span class="tag">相关</span><h5>BigBird</h5><p>在局部+全局上加随机块，并讨论万能近似。</p><a href="../../topics/sparse-attention/papers/BigBird_2007.14062.pdf">PDF</a></div>
    <div class="ref"><span class="tag">相关</span><h5>Flash Attention</h5><p>窗口图案可与 Flash 的 window_size 结合做高效实现。</p><a href="../../topics/flash-attention/index.html">打开专题</a></div>
  </div>

  <p style="margin-top:36px;font-family:var(--sans);font-size:13px;color:var(--faint)">教学重绘示意图，非论文扫描件。实验数字与实现细节以 <a href="./paper.pdf">paper.pdf</a> 为准。</p>
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

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(PAGE, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
