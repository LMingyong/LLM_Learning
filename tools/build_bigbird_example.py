#!/usr/bin/env python3
"""Build BigBird end-to-end pipeline page: design → algorithm → hardware → engineering."""

from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "papers/bigbird/example.html"


def fig_pipeline() -> str:
    return """
<svg viewBox="0 0 820 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="全流程四阶段">
  <rect width="820" height="170" fill="#fffcf5"/>
  <defs>
    <marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="#0f6e56"/>
    </marker>
  </defs>
  <g font-family="Manrope,sans-serif">
    <rect x="20" y="40" width="160" height="70" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="100" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">1. 注意力设计</text>
    <text x="100" y="92" text-anchor="middle" font-size="11" fill="#5a6a62">图结构 · 三积木</text>
    <line x1="185" y1="75" x2="215" y2="75" stroke="#0f6e56" stroke-width="2" marker-end="url(#a)"/>
    <rect x="220" y="40" width="160" height="70" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="300" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">2. 具体算法</text>
    <text x="300" y="92" text-anchor="middle" font-size="11" fill="#5a6a62">掩码 · Softmax · ITC/ETC</text>
    <line x1="385" y1="75" x2="415" y2="75" stroke="#0f6e56" stroke-width="2" marker-end="url(#a)"/>
    <rect x="420" y="40" width="160" height="70" rx="12" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="500" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#b85c38">3. 硬件优化</text>
    <text x="500" y="92" text-anchor="middle" font-size="11" fill="#5a6a62">块稀疏 · GEMM · 访存</text>
    <line x1="585" y1="75" x2="615" y2="75" stroke="#0f6e56" stroke-width="2" marker-end="url(#a)"/>
    <rect x="620" y="40" width="180" height="70" rx="12" fill="#1c2420"/>
    <text x="710" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4. 工程落地</text>
    <text x="710" y="92" text-anchor="middle" font-size="11" fill="#cfd8d3">数据布局 · 训练推理</text>
    <text x="410" y="145" text-anchor="middle" font-size="12" fill="#7d8c84">从「允许哪些 Q·K」一路落到「GPU 上真能跑到 O(n)」</text>
  </g>
</svg>
"""


def fig_smallworld() -> str:
    return """
<svg viewBox="0 0 760 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="小世界随机捷径">
  <rect width="760" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="380" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">为什么要随机边：缩短注意力图上的平均路径长度</text>
    <text x="190" y="55" text-anchor="middle" font-size="12" fill="#0f6e56" font-weight="700">仅窗口 / 局部</text>
    <circle cx="70" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="70" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">A</text>
    <circle cx="130" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="130" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">B</text>
    <circle cx="190" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="190" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">C</text>
    <circle cx="250" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="250" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">D</text>
    <circle cx="310" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="310" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">E</text>
    <path d="M84 110 H116 M144 110 H176 M204 110 H236 M264 110 H296" stroke="#0f6e56" stroke-width="2"/>
    <text x="190" y="155" text-anchor="middle" font-size="11" fill="#5a6a62">A→…→E 路径很长（多层接力）</text>
    <text x="560" y="55" text-anchor="middle" font-size="12" fill="#1f4e79" font-weight="700">加上随机捷径 · 小世界</text>
    <circle cx="440" cy="110" r="14" fill="#dce8f3" stroke="#1f4e79"/><text x="440" y="114" text-anchor="middle" font-size="12" fill="#1f4e79">A</text>
    <circle cx="500" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="500" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">B</text>
    <circle cx="560" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="560" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">C</text>
    <circle cx="620" cy="110" r="14" fill="#d8efe6" stroke="#0f6e56"/><text x="620" y="114" text-anchor="middle" font-size="12" fill="#0f6e56">D</text>
    <circle cx="680" cy="110" r="14" fill="#dce8f3" stroke="#1f4e79"/><text x="680" y="114" text-anchor="middle" font-size="12" fill="#1f4e79">E</text>
    <path d="M454 110 H486 M514 110 H546 M574 110 H606 M634 110 H666" stroke="#0f6e56" stroke-width="2"/>
    <path d="M440 96 C520 40, 600 40, 680 96" fill="none" stroke="#1f4e79" stroke-width="2" stroke-dasharray="5 4"/>
    <text x="560" y="155" text-anchor="middle" font-size="11" fill="#5a6a62">A 一跳接近 E（随机边）</text>
    <text x="380" y="185" text-anchor="middle" font-size="12" fill="#7d8c84">随机边负责远距一跳；再配全局枢纽，理论表达力才能站稳</text>
  </g>
</svg>
"""


def fig_hw() -> str:
    return """
<svg viewBox="0 0 820 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="硬件数据流">
  <rect width="820" height="280" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">硬件数据流：从 HBM 到 Tensor Core</text>

    <rect x="30" y="55" width="150" height="56" rx="10" fill="#efe9dc" stroke="#5a6a62"/>
    <text x="105" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#1c2420">HBM / DRAM</text>
    <text x="105" y="96" text-anchor="middle" font-size="11" fill="#5a6a62">Q,K,V 分块驻留</text>

    <path d="M185 83 H220" stroke="#0f6e56" stroke-width="2"/>
    <rect x="220" y="55" width="160" height="56" rx="10" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="300" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#0f6e56">块索引表</text>
    <text x="300" y="96" text-anchor="middle" font-size="11" fill="#5a6a62">全局/窗/随机 block</text>

    <path d="M385 83 H420" stroke="#0f6e56" stroke-width="2"/>
    <rect x="420" y="55" width="170" height="56" rx="10" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="505" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">连续 Gather</text>
    <text x="505" y="96" text-anchor="middle" font-size="11" fill="#5a6a62">整块装入 SRAM</text>

    <path d="M595 83 H630" stroke="#0f6e56" stroke-width="2"/>
    <rect x="630" y="55" width="160" height="56" rx="10" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="710" y="78" text-anchor="middle" font-size="12" font-weight="700" fill="#b85c38">Tensor Core</text>
    <text x="710" y="96" text-anchor="middle" font-size="11" fill="#5a6a62">块内 dense GEMM</text>

    <rect x="30" y="150" width="760" height="100" rx="12" fill="#fff" stroke="#d8d0c0"/>
    <text x="50" y="178" font-size="12" font-weight="700" fill="#b85c38">关键对照</text>
    <text x="50" y="200" font-size="12" fill="#5a6a62">✗ token 级散点 gather：破坏合并访存，Tensor Core 吃不满，带宽浪费大</text>
    <text x="50" y="222" font-size="12" fill="#5a6a62">✓ block 级掩码：每个允许的 (query-block, key-block) 做一次规则矩阵乘，稀疏在「块之间」</text>
    <text x="50" y="244" font-size="12" fill="#0f6e56">代价记账：度数 ≈ g + w + r（常数）→ 总 FLOPs / 内存 ≈ O(n)</text>
  </g>
</svg>
"""


def fig_block() -> str:
    messy = "".join(
        f'<rect x="{(j % 12) * 14}" y="{(j // 12) * 14}" width="12" height="12" rx="2" '
        f'fill="{"#1f4e79" if (j * 3 + 1) % 5 == 0 else "#e7e1d4"}"/>'
        for j in range(48)
    )
    blocks = []
    for bi in range(4):
        for bj in range(4):
            on = bi == bj or bi == 0 or bj == 0 or (bi + bj) % 3 == 0
            if bi == bj:
                color = "#0f6e56"
            elif bi == 0 or bj == 0:
                color = "#b85c38"
            elif on:
                color = "#1f4e79"
            else:
                color = "#e7e1d4"
            blocks.append(
                f'<rect x="{bj * 42}" y="{bi * 42}" width="38" height="38" rx="4" '
                f'fill="{color}" opacity="{"0.9" if on else "0.4"}"/>'
            )
    return f"""
<svg viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect width="720" height="250" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="360" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">块稀疏：按 block 决定整块是否参与</text>
    <text x="170" y="55" text-anchor="middle" font-size="12" fill="#5a6a62">token 级散点（难加速）</text>
    <g transform="translate(60,70)">{messy}</g>
    <text x="520" y="55" text-anchor="middle" font-size="12" fill="#5a6a62">block 级掩码（可 GEMM）</text>
    <g transform="translate(430,70)">{"".join(blocks)}</g>
    <g transform="translate(80,220)" font-size="11" fill="#5a6a62">
      <rect width="10" height="10" rx="2" fill="#0f6e56"/><text x="14" y="9">窗口块</text>
      <rect x="90" width="10" height="10" rx="2" fill="#b85c38"/><text x="104" y="9">全局块</text>
      <rect x="170" width="10" height="10" rx="2" fill="#1f4e79"/><text x="184" y="9">随机块</text>
      <rect x="250" width="10" height="10" rx="2" fill="#e7e1d4"/><text x="264" y="9">跳过</text>
    </g>
  </g>
</svg>
"""


PAGE = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>BigBird 全流程：设计 → 算法 → 硬件 → 工程</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;family=Noto+Sans+SC:wght@400;500;700&amp;family=Noto+Serif+SC:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<style>
:root{{
  --bg:#f6f3ec; --bg2:#efe9dc; --paper:#fffcf5; --ink:#1c2420; --muted:#5a6a62;
  --faint:#7d8c84; --line:#d8d0c0; --accent:#0f6e56; --accent-soft:#d8efe6;
  --warm:#b85c38; --warm-soft:#f3e0d6; --blue:#1f4e79; --blue-soft:#dce8f3;
  --shadow:0 12px 40px rgba(40,50,40,.08);
  --serif:"Literata",Georgia,"Noto Serif SC",serif;
  --sans:"Manrope",system-ui,"Noto Sans SC",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  --measure:46rem;
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
.side{{position:sticky;top:0;height:100vh;overflow:auto;padding:22px 16px 28px;
border-right:1px solid var(--line);background:rgba(255,252,245,.88);backdrop-filter:blur(10px)}}
.brand{{font-family:var(--sans);font-weight:700;font-size:11px;letter-spacing:.06em;color:var(--accent);margin:0 0 8px}}
.side h1{{font-family:var(--sans);font-size:18px;line-height:1.3;margin:0 0 8px}}
.side .meta{{font-family:var(--sans);font-size:12px;color:var(--muted);line-height:1.55;margin-bottom:16px}}
.side nav a{{display:block;padding:8px 10px;border-radius:10px;color:var(--muted);
font-family:var(--sans);font-size:13px;text-decoration:none;margin-bottom:2px}}
.side nav a:hover,.side nav a.active{{background:var(--accent-soft);color:var(--ink)}}
.main{{padding:28px 36px 90px}}
.wrap{{max-width:var(--measure)}}
.top{{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}}
.btn{{font-family:var(--sans);font-size:12px;border:1px solid var(--line);background:var(--paper);
color:var(--ink);border-radius:999px;padding:8px 12px;text-decoration:none}}
.btn:hover{{border-color:var(--accent)}}
.btn.primary{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.hero{{border:1px solid var(--line);border-radius:18px;padding:24px;margin-bottom:28px;
background:linear-gradient(135deg,rgba(15,110,86,.08),transparent 50%),var(--paper);box-shadow:var(--shadow)}}
.hero h2{{font-family:var(--sans);font-size:30px;margin:0 0 10px;line-height:1.25}}
.hero p{{margin:0;font-family:var(--sans);font-size:15px;color:var(--muted);line-height:1.65}}
.pills{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}}
.pill{{font-family:var(--sans);font-size:11px;padding:6px 10px;border-radius:999px;border:1px solid var(--line);background:#fff;color:var(--muted)}}
.pill strong{{color:var(--warm);font-weight:700}}
h3.sec{{font-family:var(--sans);font-size:22px;margin:42px 0 14px;scroll-margin-top:20px;
padding-bottom:8px;border-bottom:1px solid var(--line);display:flex;gap:12px;align-items:baseline}}
h3.sec .num{{font-size:13px;color:var(--accent);font-weight:700}}
h4{{font-family:var(--sans);font-size:16px;margin:22px 0 8px;color:var(--ink)}}
p{{margin:0 0 14px}}
.lead{{font-size:19px}}
.fig{{margin:16px 0;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:var(--paper);box-shadow:var(--shadow)}}
.fig svg{{display:block;width:100%;height:auto}}
.caption{{font-family:var(--sans);font-size:12px;color:var(--faint);padding:8px 12px;border-top:1px solid var(--line);margin:0}}
.callout{{border-left:3px solid var(--accent);background:var(--accent-soft);padding:12px 14px;border-radius:0 12px 12px 0;
font-family:var(--sans);font-size:14px;line-height:1.65;margin:14px 0 18px;color:#0b3d30}}
.callout.warm{{border-left-color:var(--warm);background:var(--warm-soft);color:#5a2a16}}
.callout.blue{{border-left-color:var(--blue);background:var(--blue-soft);color:#16324f}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}}
.card{{border:1px solid var(--line);background:var(--paper);border-radius:14px;padding:14px 16px}}
.card h5{{font-family:var(--sans);margin:0 0 6px;font-size:14px}}
.card p{{margin:0;font-family:var(--sans);font-size:13px;color:var(--muted);line-height:1.55}}
pre,code{{font-family:var(--mono)}}
pre{{background:#1c2420;color:#e7f2ef;border-radius:14px;padding:16px 18px;overflow:auto;
font-size:12.5px;line-height:1.55;margin:12px 0 18px;box-shadow:var(--shadow)}}
pre .c{{color:#7d8c84}}
pre .k{{color:#7dcea0}}
pre .s{{color:#f0b35a}}
pre .n{{color:#9ec9ff}}
table{{width:100%;border-collapse:collapse;font-family:var(--sans);font-size:13px;margin:12px 0 18px;background:var(--paper);
border:1px solid var(--line);border-radius:12px;overflow:hidden}}
th,td{{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{background:var(--accent-soft);color:#0b3d30;font-weight:700}}
tr:last-child td{{border-bottom:0}}
ol.steps,ul.clean{{font-family:var(--sans);font-size:14px;color:var(--muted);line-height:1.7}}
ol.steps{{padding-left:22px}}
.flow{{border:1px solid var(--line);border-radius:14px;padding:14px 16px;background:var(--paper);margin:12px 0 18px}}
.flow ol{{margin:0;padding-left:20px;font-family:var(--sans);font-size:14px;color:var(--muted);line-height:1.75}}
.footer{{margin-top:48px;padding-top:16px;border-top:1px solid var(--line);font-family:var(--sans);font-size:13px;color:var(--faint)}}
@media (max-width:960px){{
  .layout{{grid-template-columns:1fr}}
  .side{{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}}
  .main{{padding:18px 16px 70px}}
  .grid2{{grid-template-columns:1fr}}
  .hero h2{{font-size:24px}}
}}
</style>
</head>
<body>
<div class="layout">
<aside class="side">
  <div class="brand">LLM LEARNING · PAPER</div>
  <h1>BigBird 全流程</h1>
  <div class="meta">注意力设计 → 算法 → 硬件 → 工程落地<br/>与逐段精读页同目录</div>
  <nav id="toc">
    <a href="#overview">0. 全流程总览</a>
    <a href="#design">1. 注意力设计</a>
    <a href="#pattern">2. 三积木如何构图</a>
    <a href="#algo">3. 具体算法</a>
    <a href="#code">4. 代码级前向</a>
    <a href="#itc">5. ITC / ETC</a>
    <a href="#hardware">6. 硬件优化</a>
    <a href="#block">7. 块稀疏落地</a>
    <a href="#eng">8. 工程清单</a>
    <a href="#checklist">9. 端到端对照表</a>
  </nav>
</aside>

<main class="main">
<div class="wrap">
  <div class="top">
    <a class="btn primary" href="./paper.pdf" target="_blank" rel="noopener">打开原文 PDF</a>
    <a class="btn" href="./index.html">逐段精读 →</a>
    <a class="btn" href="../watts-strogatz/index.html">Watts–Strogatz 精读 →</a>
    <a class="btn" href="https://arxiv.org/abs/2007.14062" target="_blank" rel="noopener">arXiv:2007.14062</a>
    <a class="btn" href="../longformer/index.html">Longformer →</a>
    <a class="btn" href="../../topics/sparse-attention/index.html">稀疏专题 →</a>
  </div>

  <section class="hero">
    <h2>从注意力设计到 GPU 上的 O(n)</h2>
    <p>这篇讲 BigBird 的<strong>完整落地链条</strong>：先决定「谁可以看谁」（图结构设计），再写成可计算的掩码与注意力公式，然后改成 GPU 友好的块稀疏，最后落到训练/推理工程。读完应能回答：为什么保留局部边、随机边干什么、块稀疏省在哪里。</p>
    <div class="pills">
      <span class="pill">设计：<strong>g + w + r</strong></span>
      <span class="pill">算法：<strong>ATTN_D / 邻接矩阵</strong></span>
      <span class="pill">硬件：<strong>block GEMM</strong></span>
      <span class="pill">工程：<strong>~8× 长度</strong></span>
    </div>
  </section>

  <h3 class="sec" id="overview"><span class="num">00</span>全流程总览</h3>
  <div class="fig">{fig_pipeline()}<p class="caption">图 0 · 四阶段：设计意图必须能穿过算法与硬件，否则只是纸面稀疏。</p></div>
  <p class="lead">BigBird 要解决的不是「换一个更花哨的注意力公式」，而是：在<strong>不丢表达力</strong>的前提下，把全注意力的二次边集稀疏成线性边集，并且让稀疏在加速器上真的快。</p>
  <div class="flow">
    <ol>
      <li><strong>设计</strong>：把自注意力看成有向图；目标图要「短路径 + 局部性 + 全局枢纽」。</li>
      <li><strong>算法</strong>：用邻接矩阵 A 规定允许的 (query, key)；只对邻居做 QKᵀ / softmax / 加权 V。</li>
      <li><strong>硬件</strong>：把 token 级边提升为 block 级边，块内 dense GEMM，吃满 Tensor Core。</li>
      <li><strong>工程</strong>：固定 block size、预生成随机块、ETC 全局位、编码器稀疏 + 解码器全注意力等落地选择。</li>
    </ol>
  </div>

  <h3 class="sec" id="design"><span class="num">01</span>注意力设计：问题从哪来</h3>
  <p>标准 Transformer 全自注意力让每个 token 看所有 token，注意力矩阵是 n×n。计算与激活内存都随长度二次涨。常见硬件 + 常见模型规模下，上下文往往卡在约 <strong>512</strong>。QA、长摘要、文档分类、DNA 等任务直接吃亏。</p>
  <p>设计问题可以精确表述为：</p>
  <div class="callout">
    找一张稀疏有向图 D（每点出度近常数），使基于 D 的注意力在经验上接近全注意力，并在理论上尽量保留「万能近似 / 图灵完备」；同时边的几何形状要适配 GPU 的块矩阵乘。
  </div>
  <div class="grid2">
    <div class="card"><h5>必须保留的性质</h5><p>局部搭配（语法/相邻碱基）、远距依赖（指代、多跳证据）、可汇聚的全局表示（CLS/任务位）。</p></div>
    <div class="card"><h5>必须砍掉的代价</h5><p>O(n²) 的成对内积与注意力矩阵物化；任意散点 gather 导致的带宽浪费。</p></div>
  </div>

  <h3 class="sec" id="pattern"><span class="num">02</span>三积木如何构图</h3>
  <p>论文把答案拆成三块，再并起来：</p>
  <table>
    <thead><tr><th>积木</th><th>图含义</th><th>直觉</th><th>复杂度贡献</th></tr></thead>
    <tbody>
      <tr><td><strong>Window w</strong></td><td>环上滑动邻域</td><td>语言/生物局部性；高聚类</td><td>每点 ~w</td></tr>
      <tr><td><strong>Random r</strong></td><td>随机捷径</td><td>小世界；缩短平均路径</td><td>每点 ~r</td></tr>
      <tr><td><strong>Global g</strong></td><td>星形枢纽</td><td>信息汇聚/广播；理论关键</td><td>每点经全局 ~g</td></tr>
    </tbody>
  </table>
  <p>合并后，每个 query 的度数约为 <code>O(g + w + r)</code>。当 g、w、r 视为常数（或缓慢增长）时，整层注意力是 <strong>O(n)</strong>。</p>
  <div class="fig">{fig_smallworld()}<p class="caption">图 1 · 仅窗口时远距要多层接力；随机捷径把平均路径压短（小世界）。</p></div>
  <div class="callout warm">
    <strong>实现细节（对应你截图那段）：</strong>经典 Watts–Strogatz 会「删掉一些局部边再随机重连」。硬件上按位置删边不划算，BigBird 选择<strong>保留全部局部边，再额外加随机边</strong>——图性质不受损，kernel 更好写，访存更规则。
  </div>
  <p>消融直觉（论文 Table 1，长度 512）：仅 Window 或仅 Random 都明显弱于 BERT；R+W 好转但仍不够；最终必须加上 Global 才能在理论与经验上站稳。</p>

  <h3 class="sec" id="algo"><span class="num">03</span>具体算法：广义注意力</h3>
  <p>把允许的内积写成有向图 D。令 <code>N(i)</code> 为节点 i 的出邻居，则：</p>
  <pre><span class="c"># 广义注意力（论文式 (AT)）</span>
ATTN_D(X)_i = x_i + Σ_h  σ( Q_h(x_i) · K_h(X_N(i))ᵀ ) · V_h(X_N(i))

<span class="c"># 若 D 是完全图 → 退回 Vaswani 全注意力</span>
<span class="c"># 若 D = window ∪ random ∪ global → BigBird</span></pre>
  <p>工程上更常用邻接矩阵视角：</p>
  <pre>A[i, j] = 1  ⇔  query i 允许 attend key j
A[i, j] = 0  ⇔  该内积不计算（等价 logits = −∞）</pre>
  <h4>构造 A 的规则（token 视角）</h4>
  <ol class="steps">
    <li><strong>窗口</strong>：对所有 i，令 <code>A[i, i−w/2 : i+w/2] = 1</code>（边界裁剪）。</li>
    <li><strong>随机</strong>：对所有 i，从 {{0…n−1}} 采 r 个下标 j，令 <code>A[i,j]=1</code>（实现里常升为随机块）。</li>
    <li><strong>全局 ITC</strong>：选集合 G，对 i∈G 令整行整列全 1。</li>
    <li><strong>全局 ETC</strong>：在序列前插入 g 个新 token，它们与所有位置双向连接，再把原 A 嵌进右下角。</li>
  </ol>

  <h3 class="sec" id="code"><span class="num">04</span>代码级前向（教学伪代码）</h3>
  <p>下面用 NumPy 风格伪代码把「设计」落成「可跑的算法」。真实实现会换成块索引 + 融合核，但数学等价。</p>
  <pre><span class="k">import</span> numpy <span class="k">as</span> np

<span class="k">def</span> <span class="n">build_bigbird_mask</span>(n, w, r, global_idx, seed=0):
    <span class="c"># A[i,j]=True 表示允许注意力</span>
    A = np.zeros((n, n), dtype=bool)
    half = w // 2
    rng = np.random.default_rng(seed)

    <span class="c"># 1) 滑动窗口（保留全部局部边）</span>
    <span class="k">for</span> i <span class="k">in</span> range(n):
        lo, hi = max(0, i - half), min(n, i + half + 1)
        A[i, lo:hi] = True

    <span class="c"># 2) 额外随机边（不删窗口边）</span>
    <span class="k">for</span> i <span class="k">in</span> range(n):
        js = rng.choice(n, size=r, replace=False)
        A[i, js] = True

    <span class="c"># 3) 全局星形（ITC：用已有位置）</span>
    <span class="k">for</span> g <span class="k">in</span> global_idx:
        A[g, :] = True
        A[:, g] = True
    <span class="k">return</span> A


<span class="k">def</span> <span class="n">sparse_attention</span>(X, Wq, Wk, Wv, A):
    <span class="c"># X: [n,d]  —— 教学版：仍物化 scores，但被掩码位置不参与</span>
    Q, K, V = X @ Wq, X @ Wk, X @ Wv          <span class="c"># [n,m], [n,m], [n,d]</span>
    scores = (Q @ K.T) / np.sqrt(Q.shape[-1]) <span class="c"># [n,n]</span>
    scores = np.where(A, scores, -1e9)
    alpha = softmax(scores, axis=-1)
    <span class="k">return</span> alpha @ V                          <span class="c"># [n,d]</span></pre>
  <div class="callout blue">
    <strong>教学版 vs 产品版：</strong>上面仍分配了 n×n 的 <code>scores</code>，只是用 −∞ 掩掉。这<strong>不能</strong>带来内存线性——它只用于理解语义。真正 O(n) 要靠下一节：永不物化完整矩阵，只对允许的 block-pair 做 GEMM。
  </div>
  <h4>线性复杂度前向（块索引版骨架）</h4>
  <pre><span class="k">def</span> <span class="n">block_sparse_attention</span>(Q, K, V, block_links, B):
    <span class="c"># Q,K,V: [n, m]；序列切成 n/B 个块</span>
    <span class="c"># block_links[b] = 该 query 块需要计算的 key 块 id 列表</span>
    <span class="c">#   通常包含：全局块 + 窗口邻近块 + r 个随机块</span>
    out = empty_like(Q)
    <span class="k">for</span> b, key_blocks <span class="k">in</span> enumerate(block_links):
        q = Q[b*B:(b+1)*B]                         <span class="c"># [B,m]</span>
        k = concat([K[j*B:(j+1)*B] <span class="k">for</span> j <span class="k">in</span> key_blocks])
        v = concat([V[j*B:(j+1)*B] <span class="k">for</span> j <span class="k">in</span> key_blocks])
        logits = q @ k.T / sqrt(m)                 <span class="c"># [B, B*|links|]</span>
        out[b*B:(b+1)*B] = softmax(logits) @ v     <span class="c"># 块内 dense</span>
    <span class="k">return</span> out</pre>
  <p>每个 query 块只连常数个 key 块 ⇒ 每块 FLOPs = O(B · (B·常数) · m) ⇒ 总 FLOPs = O(n · 常数 · m)。</p>

  <h3 class="sec" id="itc"><span class="num">05</span>ITC / ETC：两种全局落地</h3>
  <table>
    <thead><tr><th></th><th>ITC（Internal）</th><th>ETC（Extended）</th></tr></thead>
    <tbody>
      <tr><td>做法</td><td>把已有 token 标成 global</td><td>额外插入 g 个全局 token（如 CLS）</td></tr>
      <tr><td>矩阵</td><td>仍是 n×n，选中行列全 1</td><td>扩成 (n+g)×(n+g)</td></tr>
      <tr><td>信息槽</td><td>占用原位置表示</td><td>额外位置专门存全局上下文</td></tr>
      <tr><td>经验</td><td>接近 Longformer 用法</td><td>论文中 QA 等任务更稳、常取 ETC</td></tr>
    </tbody>
  </table>
  <pre><span class="c"># ETC：在序列前插入 g 个全局位</span>
<span class="k">def</span> <span class="n">etc_expand</span>(A, g):
    N = A.shape[0]
    B = np.zeros((N+g, N+g), dtype=bool)
    B[:g, :] = True
    B[:, :g] = True
    B[g:, g:] = A
    <span class="k">return</span> B</pre>
  <p>理论侧：只要图包含「以全局点为中心的星形」，万能近似证明就能走通——全局不是调参装饰，而是表达力补丁。</p>

  <h3 class="sec" id="hardware"><span class="num">06</span>硬件优化：稀疏如何变成加速</h3>
  <p>算法稀疏 ≠ 硬件快。GPU 喜欢：<strong>合并访存、规则地址、大块矩阵乘</strong>。token 级「每人看 8 个散落邻居」会触发大量不规则 gather，Tensor Core 闲置，带宽打满算力吃不满。</p>
  <div class="fig">{fig_hw()}<p class="caption">图 2 · 硬件路径：HBM → 块索引 → 连续装载 → Tensor Core 块 GEMM。</p></div>
  <h4>三条硬件原则</h4>
  <ol class="steps">
    <li><strong>稀疏在块间，密集在块内</strong>：允许的 (Q-block, K-block) 用 dense GEMM；不允许的整块跳过。</li>
    <li><strong>不删窗口边</strong>：窗口是规整 band/块对角，最好写核；删边只会破坏规则性。</li>
    <li><strong>随机边升格为随机块</strong>：一次随机决定「连哪个 key 块」，块内仍连续，避免散点。</li>
  </ol>
  <div class="callout">
    内存直觉：全注意力要存 ~n² 的注意力相关激活；块稀疏只为「被选中的块对」分配工作区，工作集随选中块数线性涨。这也是相近硬件上上下文能到约 8× 的直接原因。
  </div>

  <h3 class="sec" id="block"><span class="num">07</span>块稀疏落地细节</h3>
  <div class="fig">{fig_block()}<p class="caption">图 3 · 左：token 散点；右：块掩码（绿窗 / 橙全局 / 蓝随机）。</p></div>
  <h4>典型超参（教学量级）</h4>
  <table>
    <thead><tr><th>符号</th><th>含义</th><th>常见量级</th></tr></thead>
    <tbody>
      <tr><td>n</td><td>序列长度</td><td>4096（相对 512 ≈ 8×）</td></tr>
      <tr><td>B</td><td>block size</td><td>64 / 128</td></tr>
      <tr><td>w</td><td>窗口宽度（token 或换算块数）</td><td>数十～数百 token</td></tr>
      <tr><td>r</td><td>每行随机块数</td><td>很小的常数（如 3）</td></tr>
      <tr><td>g</td><td>全局 token / 全局块</td><td>O(1)</td></tr>
    </tbody>
  </table>
  <h4>块链接表怎么生成</h4>
  <pre><span class="k">def</span> <span class="n">build_block_links</span>(num_blocks, window_blocks, r, global_blocks, rng):
    links = []
    <span class="k">for</span> b <span class="k">in</span> range(num_blocks):
        s = set(global_blocks)
        <span class="c"># 窗口：自身 ± window_blocks</span>
        <span class="k">for</span> j <span class="k">in</span> range(max(0,b-window_blocks), min(num_blocks,b+window_blocks+1)):
            s.add(j)
        <span class="c"># 随机块：额外采样（可与窗口重叠，重叠无妨）</span>
        s.update(rng.choice(num_blocks, size=r, replace=False).tolist())
        links.append(sorted(s))
    <span class="k">return</span> links  <span class="c"># 长度 = num_blocks，每项度数 ≈ 常数</span></pre>
  <p>训练时随机块可每步重采或固定种子预生成；推理常固定图案以保证可复现。</p>

  <h3 class="sec" id="eng"><span class="num">08</span>工程落地清单</h3>
  <h4>A. 模型侧</h4>
  <ul class="clean">
    <li>Encoder 用 BigBird 稀疏自注意力；生成任务里 Decoder 自注意力可保持全连接（输出通常短）。</li>
    <li>优先试 <strong>ETC</strong>：额外全局位当可学习「笔记本」。</li>
    <li>从 RoBERTa 等检查点热启动 + MLM 长序列继续预训练，再进 QA/摘要/分类。</li>
  </ul>
  <h4>B. 内核 / 框架侧</h4>
  <ul class="clean">
    <li>不要实现「对每个 token gather 任意 index 再 matmul」的朴素核作为主路径。</li>
    <li>实现 block-sparse matmul：输入 CSR/列表式 block 索引 + 连续 QKV 分块。</li>
    <li>能融合的尽量融合：mask + softmax + 加权 V，减少中间张量写回 HBM。</li>
    <li>关注激活检查点：即便注意力线性，FFN / 层数仍占显存。</li>
  </ul>
  <h4>C. 一次前向的工程时序</h4>
  <div class="flow">
    <ol>
      <li>Tokenize / 截断到 n（如 4096）；ETC 则前置 g 个全局位。</li>
      <li>Embedding + 位置编码；按 B 切块。</li>
      <li>查或生成 <code>block_links</code>（全局 ∪ 窗口 ∪ 随机）。</li>
      <li>每层：Linear → QKV；按 links 做块稀疏注意力；残差 + LN；FFN。</li>
      <li>任务头：分类取 CLS/全局位；抽取式 QA 出 span logits；摘要走 decoder。</li>
    </ol>
  </div>
  <h4>D. 常见坑</h4>
  <div class="grid2">
    <div class="card"><h5>掩码语义错</h5><p>把「不算」写成 0 分而不是 −∞，softmax 仍会漏概率。</p></div>
    <div class="card"><h5>只稀疏不算块</h5><p>理论 O(n) 但实测比 dense 还慢——散点 gather 害的。</p></div>
    <div class="card"><h5>随机边当装饰</h5><p>消融显示 R/W 单独都弱；随机负责远距捷径，不配全局仍不稳。</p></div>
    <div class="card"><h5>全局位乱放</h5><p>ITC 选错位置或 ETC 全局数太少，长程汇聚会塌。</p></div>
  </div>

  <h3 class="sec" id="checklist"><span class="num">09</span>端到端对照表</h3>
  <table>
    <thead><tr><th>阶段</th><th>关键产物</th><th>你要验证的一句话</th></tr></thead>
    <tbody>
      <tr><td>设计</td><td>图 D = W ∪ R ∪ G</td><td>短路径 + 局部性 + 星形枢纽是否都在？</td></tr>
      <tr><td>算法</td><td>A 或 block_links</td><td>每个 query 是否只对邻居做 softmax？</td></tr>
      <tr><td>硬件</td><td>块 GEMM 核</td><td>是否避免了 token 级散点？Tensor Core 有没有吃上？</td></tr>
      <tr><td>工程</td><td>可训可推模型</td><td>同卡能否从 ~512 拉到 ~4096？任务是否吃到长上下文？</td></tr>
    </tbody>
  </table>
  <div class="callout">
    一句话串起来：BigBird 先用<strong>小世界 + 全局星形</strong>设计一张线性度数的注意力图，再把边<strong>升格成块掩码</strong>好让 GPU 用稠密块乘加速，最终在相近硬件上把可用上下文拉长约一个数量级。
  </div>

  <div class="footer">
    教学页 · 与 <a href="./index.html">逐段精读</a> 互补 · 公式与表号以 <a href="./paper.pdf">paper.pdf</a> 为准 ·
    重新生成：<code>python3 tools/build_bigbird_example.py</code>
  </div>
</div>
</main>
</div>
<script>
const tocLinks=[...document.querySelectorAll('#toc a')];
const sections=tocLinks.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
const io=new IntersectionObserver(es=>{{es.forEach(en=>{{if(!en.isIntersecting)return;const id='#'+en.target.id;
tocLinks.forEach(a=>a.classList.toggle('active',a.getAttribute('href')===id));}});}},
{{rootMargin:'-20% 0px -65% 0px',threshold:0.01}});
sections.forEach(s=>io.observe(s));
</script>
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(PAGE, encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
