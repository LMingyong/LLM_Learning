#!/usr/bin/env python3
"""Build fine-grained BigBird study page: original + zh + paragraph summary."""

from __future__ import annotations

import html
import json
from pathlib import Path

from bigbird_paragraphs import GLOSSARY, REFS, SECTIONS

OUT = Path(__file__).resolve().parents[1] / "papers/bigbird/index.html"


def esc(s: str) -> str:
    return html.escape(s)


def pattern_cells(kind: str, n: int = 14, cell: int = 11) -> tuple[str, int]:
    gap = 1
    size = n * (cell + gap)
    rects = []
    rnd = set()
    for i in range(n):
        for k in range(2):
            j = (i * 5 + k * 7 + 3) % n
            if j != i:
                rnd.add((i, j))
                rnd.add((j, i))
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
        '<svg viewBox="0 0 760 230" xmlns="http://www.w3.org/2000/svg" role="img" '
        'aria-label="BigBird Figure 1 building blocks">'
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
    messy = "".join(
        f'<rect x="{(j % 12) * 14}" y="{(j // 12) * 14}" width="12" height="12" rx="2" '
        f'fill="{"#1f4e79" if (j * 3 + 1) % 5 == 0 else "#e7e1d4"}"/>'
        for j in range(48)
    )
    blocks = []
    for bi in range(4):
        for bj in range(4):
            on = bi == bj or bi == 0 or bj == 0 or (bi + bj) % 3 == 0
            color = "#0f6e56" if bi == bj else ("#b85c38" if bi == 0 or bj == 0 else "#1f4e79")
            if not on:
                color = "#e7e1d4"
            blocks.append(
                f'<rect x="{bj * 42}" y="{bi * 42}" width="38" height="38" rx="4" '
                f'fill="{color}" opacity="{"0.9" if on else "0.45"}"/>'
            )
    return f"""
<svg viewBox="0 0 720 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="block sparse">
  <rect width="720" height="250" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="360" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">块稀疏：按 block 决定整块是否参与（利于 GPU 块矩阵核）</text>
    <text x="170" y="55" text-anchor="middle" font-size="12" fill="#5a6a62">token 级稀疏（散点，难加速）</text>
    <g transform="translate(60,70)">{messy}</g>
    <text x="520" y="55" text-anchor="middle" font-size="12" fill="#5a6a62">block 级稀疏（整块 GEMM）</text>
    <g transform="translate(430,70)">{"".join(blocks)}</g>
    <text x="360" y="235" text-anchor="middle" font-size="12" fill="#7d8c84">BigBird 工程实现：随机 / 窗口 / 全局都落在块掩码上</text>
  </g>
</svg>
"""


FIGURES = {
    "pattern": (
        "教学重绘 · 对应论文 Fig. 1（白色=不算注意力）",
        fig_four(),
    ),
    "block": (
        "教学示意 · 块稀疏 vs token 级散点",
        fig_block(),
    ),
}


CSS = r"""
:root{
  --bg:#f6f3ec; --bg2:#efe9dc; --paper:#fffcf5; --ink:#1c2420; --muted:#5a6a62;
  --faint:#7d8c84; --line:#d8d0c0; --accent:#0f6e56; --accent-soft:#d8efe6;
  --warm:#b85c38; --warm-soft:#f3e0d6; --blue:#1f4e79; --blue-soft:#dce8f3;
  --shadow:0 12px 40px rgba(40,50,40,.08);
  --serif:"Literata",Georgia,"Noto Serif SC",serif;
  --sans:"Manrope",system-ui,"Noto Sans SC",sans-serif;
  --mono:ui-monospace,Menlo,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;color:var(--ink);font-family:var(--serif);font-size:17px;line-height:1.75;
background:radial-gradient(900px 500px at 0% 0%,rgba(15,110,86,.07),transparent 55%),
radial-gradient(700px 400px at 100% 8%,rgba(184,92,56,.06),transparent 50%),
linear-gradient(180deg,var(--bg),var(--bg2));min-height:100vh}
a{color:var(--accent);text-underline-offset:3px}
a:hover{color:var(--warm)}
.app{display:grid;grid-template-columns:260px minmax(0,1fr);min-height:100vh}
.side{position:sticky;top:0;height:100vh;overflow:auto;padding:22px 16px 28px;
border-right:1px solid var(--line);background:rgba(255,252,245,.85);backdrop-filter:blur(10px)}
.brand{font-family:var(--sans);font-weight:700;font-size:12px;color:var(--accent);letter-spacing:.04em;margin:0 0 8px}
.side h1{font-family:var(--sans);font-size:20px;line-height:1.25;margin:0 0 8px}
.side .meta{font-family:var(--sans);font-size:12px;color:var(--muted);line-height:1.55;margin-bottom:16px}
.side nav a{display:block;padding:8px 10px;border-radius:10px;color:var(--muted);
font-family:var(--sans);font-size:13px;text-decoration:none;margin-bottom:2px}
.side nav a:hover,.side nav a.active{background:var(--accent-soft);color:var(--ink)}
.side .hint{margin-top:18px;padding:12px;border:1px solid var(--line);border-radius:12px;
font-family:var(--sans);font-size:12px;color:var(--faint);line-height:1.55;background:var(--paper)}
.main{padding:22px 28px 80px;max-width:1080px}
.topbar{position:sticky;top:0;z-index:20;margin:0 -28px 22px;padding:14px 28px;
display:flex;flex-wrap:wrap;gap:10px;align-items:center;
background:rgba(246,243,236,.9);border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}
.seg{display:inline-flex;padding:4px;border-radius:999px;background:var(--paper);border:1px solid var(--line)}
.seg button{appearance:none;border:0;background:transparent;color:var(--muted);cursor:pointer;
font-family:var(--sans);font-size:12px;padding:8px 12px;border-radius:999px}
.seg button.on{background:var(--accent-soft);color:var(--ink);font-weight:600}
.btn{font-family:var(--sans);font-size:12px;border:1px solid var(--line);background:var(--paper);
color:var(--ink);border-radius:999px;padding:8px 12px;cursor:pointer;text-decoration:none;display:inline-flex;align-items:center}
.btn:hover{border-color:var(--accent)}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.search{flex:1;min-width:180px}
.search input{width:100%;border-radius:999px;border:1px solid var(--line);background:var(--paper);
color:var(--ink);padding:9px 14px;font-family:var(--sans);font-size:13px;outline:none}
.search input:focus{border-color:var(--accent)}
.hero{border:1px solid var(--line);border-radius:18px;padding:22px 24px;margin-bottom:22px;
background:linear-gradient(135deg,rgba(15,110,86,.08),transparent 45%),var(--paper);
box-shadow:var(--shadow)}
.hero h2{font-family:var(--sans);margin:0 0 8px;font-size:28px}
.hero p{margin:0;color:var(--muted);font-family:var(--sans);font-size:14px;line-height:1.65}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chip{font-family:var(--sans);font-size:11px;padding:6px 10px;border-radius:999px;border:1px solid var(--line);color:var(--muted);background:#fff}
.chip em{color:var(--warm);font-style:normal;font-weight:600}
.section{margin:28px 0 10px;scroll-margin-top:78px}
.section h3{font-family:var(--sans);font-size:18px;margin:0 0 12px;padding-bottom:8px;
border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:10px}
.section h3 span{font-size:12px;color:var(--faint);font-weight:500}
.card{border:1px solid var(--line);background:var(--paper);border-radius:16px;padding:14px 16px;margin:0 0 12px;
box-shadow:0 1px 0 rgba(255,255,255,.6) inset;transition:border-color .2s,transform .2s,box-shadow .2s}
.card:hover{border-color:rgba(15,110,86,.35);transform:translateY(-1px);box-shadow:var(--shadow)}
.card.active{border-color:var(--accent);box-shadow:0 0 0 1px rgba(15,110,86,.2),var(--shadow)}
.pidx{font-family:var(--sans);font-size:11px;color:var(--faint);float:right;margin-left:8px}
.summary{font-family:var(--sans);font-size:13px;color:#0b3d30;background:var(--accent-soft);
border-left:3px solid var(--accent);padding:8px 10px;border-radius:0 10px 10px 0;margin:0 0 12px;line-height:1.55}
.summary b{font-weight:700}
.lang{font-size:15.5px;line-height:1.8}
.lang .en{color:#24312c}
.lang .zh{color:#1c2420}
.lang .label{font-family:var(--sans);font-size:11px;color:var(--faint);letter-spacing:.08em;text-transform:uppercase;margin:0 0 4px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}
body.mode-zh .en-block,body.mode-en .zh-block{display:none}
body.mode-zh .pair,body.mode-en .pair{grid-template-columns:1fr}
.terms{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;clear:both}
.term{font-family:var(--sans);font-size:11px;padding:4px 8px;border-radius:999px;cursor:pointer;
background:var(--warm-soft);color:#6a2f18;border:1px solid rgba(184,92,56,.25)}
.term:hover{background:#efd2c2}
.figure{margin:12px 0 4px;border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fffcf5}
.figure .cap{font-family:var(--sans);font-size:12px;color:var(--faint);padding:8px 12px;border-top:1px solid var(--line)}
.figure svg{display:block;width:100%;height:auto}
.hidden-by-search{display:none !important}
.drawer{position:fixed;top:0;right:0;width:min(420px,100%);height:100vh;overflow:auto;z-index:40;
background:var(--paper);border-left:1px solid var(--line);
transform:translateX(100%);transition:transform .28s ease;padding:18px 16px 40px;box-shadow:var(--shadow)}
.drawer.open{transform:none}
.drawer h2{font-family:var(--sans);margin:8px 0 6px;font-size:18px}
.gitem{border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0;background:#fff}
.gitem b{font-family:var(--sans);color:var(--warm)}
.gitem p{margin:6px 0 0;color:var(--muted);font-size:14px;line-height:1.55}
.refgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.ref{border:1px solid var(--line);border-radius:16px;padding:14px;background:var(--paper);
display:flex;flex-direction:column;gap:8px;min-height:140px}
.ref .lv{font-family:var(--sans);font-size:11px;align-self:start;padding:4px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.ref .lv.must{color:#fff;background:var(--accent);border-color:transparent;font-weight:700}
.ref .lv.imp{color:#fff;background:var(--warm);border-color:transparent;font-weight:700}
.ref h4{margin:0;font-family:var(--sans);font-size:15px;line-height:1.35}
.ref p{margin:0;color:var(--muted);font-size:13px;line-height:1.5;flex:1}
.kbd{font-family:var(--mono);font-size:11px;border:1px solid var(--line);border-bottom-width:2px;border-radius:6px;padding:1px 5px;color:var(--faint);background:#fff}
.note{font-family:var(--sans);font-size:13px;color:var(--muted);line-height:1.6;margin:0 0 16px}
@media (max-width:960px){
  .app{grid-template-columns:1fr}
  .side{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}
  .pair{grid-template-columns:1fr}
  .main{padding:16px 14px 70px}
  .topbar{margin:0 -14px 16px;padding:12px 14px}
}
"""


def build() -> str:
    parts: list[str] = []
    parts.append(
        f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>BigBird 逐段精读 · 原文 / 译文 / 段末小结</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@400;500;700&amp;family=Noto+Serif+SC:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<style>{CSS}</style></head>
<body class="mode-both"><div class="app">
<aside class="side">
<div class="brand">LLM Learning · Paper Reader</div>
<h1>BigBird 逐段精读</h1>
<div class="meta">Zaheer et al. · arXiv:2007.14062<br/>每段 = 小结 + Original + 译文<br/>Longformer 专页未改动</div>
<nav id="toc">"""
    )
    for sec in SECTIONS:
        parts.append(f'<a href="#{sec["id"]}">{esc(sec["title"])}</a>\n')
    parts.append(
        """<a href="#glossary">名词重点解释</a>
<a href="#refs">重点引用</a>
</nav>
<div class="hint">
<div><span class="kbd">1</span>对照 <span class="kbd">2</span>译文 <span class="kbd">3</span>原文</div>
<div style="margin-top:6px"><span class="kbd">J</span>/<span class="kbd">K</span>跳段 <span class="kbd">G</span>名词 <span class="kbd">/</span>搜索</div>
</div></aside>
<main class="main">
<div class="topbar">
<div class="seg" id="modeSeg">
<button data-mode="both" class="on">对照</button>
<button data-mode="zh">仅译文</button>
<button data-mode="en">仅原文</button>
</div>
<button class="btn" id="btnGlossary">名词表</button>
<a class="btn primary" href="./paper.pdf" target="_blank" rel="noopener">打开原文 PDF</a>
<a class="btn" href="./example.html">全流程：设计→硬件 →</a>
<a class="btn" href="../longformer/index.html">Longformer →</a>
<a class="btn" href="../../topics/sparse-attention/index.html">稀疏专题 →</a>
<div class="search"><input id="q" type="search" placeholder="搜索段落 / 名词 / 引用…" /></div>
</div>
<section class="hero">
<h2>Big Bird: Transformers for Longer Sequences</h2>
<p>浅色逐段精读：严格按论文脉络拆段，段首给中文小结，段内左右对照 Original / 译文。核心记住三件套——全局 g、窗口 w、随机 r——以及「含星形全局结构 ⇒ 万能近似」。</p>
<div class="chips">
<span class="chip">图案：<em>global + window + random</em></span>
<span class="chip">复杂度：<em>O(n)</em></span>
<span class="chip">理论：<em>万能近似 + 图灵完备</em></span>
<span class="chip">工程：<em>块稀疏</em></span>
<span class="chip">长度：<em>~8×</em></span>
</div>
</section>
<p class="note">英文尽量贴近原文；PDF 断行/连字处做了可读性规范化。Table / Figure 数字以 <a href="./paper.pdf">paper.pdf</a> 为准。段末小结是学习用导读，不是论文原文。</p>
"""
    )

    card_i = 0
    for sec in SECTIONS:
        parts.append(
            f'<section class="section" id="{sec["id"]}"><h3>{esc(sec["title"])} '
            f'<span>{len(sec["paras"])} 段</span></h3>\n'
        )
        for p in sec["paras"]:
            card_i += 1
            terms = "".join(
                f'<span class="term" data-term="{esc(t)}">{esc(t)}</span>'
                for t in p.get("terms", [])
            )
            blob = " ".join(
                [p["en"], p["zh"], p["summary"], " ".join(p.get("terms", []))]
            ).lower()
            fig_html = ""
            fig_key = p.get("figure")
            if fig_key in FIGURES:
                cap, svg = FIGURES[fig_key]
                fig_html = (
                    f'<div class="figure">{svg}'
                    f'<div class="cap">{esc(cap)}</div></div>'
                )
            p_en, p_zh, p_sum = esc(p["en"]), esc(p["zh"]), esc(p["summary"])
            parts.append(
                f'<article class="card para" data-idx="{card_i}" data-blob="{esc(blob)}">\n'
                f'<span class="pidx">§{card_i}</span>\n'
                f'<div class="summary"><b>小结</b> · {p_sum}</div>\n'
                f'<div class="pair lang">\n'
                f'<div class="en-block"><div class="label">Original</div><div class="en">{p_en}</div></div>\n'
                f'<div class="zh-block"><div class="label">译文</div><div class="zh">{p_zh}</div></div>\n'
                f"</div>{fig_html}\n"
                f'<div class="terms">{terms}</div></article>\n'
            )
        parts.append("</section>\n")

    parts.append(
        '<section class="section" id="glossary"><h3>名词重点解释 '
        f'<span>{len(GLOSSARY)} 条</span></h3><div class="refgrid">\n'
    )
    for name, desc in GLOSSARY:
        parts.append(
            f'<div class="gitem" id="term-{esc(name)}" data-blob="{esc((name + " " + desc).lower())}">'
            f"<b>{esc(name)}</b><p>{esc(desc)}</p></div>\n"
        )
    parts.append("</div></section>\n")

    parts.append('<section class="section" id="refs"><h3>重点引用</h3><div class="refgrid">\n')
    for r in REFS:
        lv = "must" if r["level"] == "本篇" else ("imp" if r["level"] in ("对照", "近亲") else "")
        links = f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">打开 →</a>'
        if r.get("ext"):
            links += f' · <a href="{esc(r["ext"])}" target="_blank" rel="noopener">arXiv</a>'
        parts.append(
            f'<div class="ref" data-blob="{esc((r["title"] + " " + r["why"]).lower())}">'
            f'<span class="lv {lv}">{esc(r["level"])}</span>'
            f"<h4>{esc(r['title'])}</h4><p>{esc(r['why'])}</p>{links}</div>\n"
        )
    parts.append(
        '</div><p class="note" style="margin-top:28px">本页为学习用逐段精读整理；公式、表号与实验数字以 PDF 原文为准。示意图为教学重绘。</p>'
        "</section></main></div>\n"
    )

    gjs = ",\n".join(f"{json.dumps(k)}:{json.dumps(v)}" for k, v in GLOSSARY)
    parts.append(
        f"""
<aside class="drawer" id="drawer"><button class="btn" id="closeDrawer">关闭</button>
<h2>名词速查</h2><div id="drawerBody"></div></aside>
<script>
const body=document.body;const cards=[...document.querySelectorAll('.para')];let idx=0;
const glossary={{{gjs}}};
function setMode(m){{body.classList.remove('mode-both','mode-zh','mode-en');body.classList.add('mode-'+m);
document.querySelectorAll('#modeSeg button').forEach(b=>b.classList.toggle('on',b.dataset.mode===m));}}
document.getElementById('modeSeg').onclick=e=>{{const b=e.target.closest('button');if(b)setMode(b.dataset.mode);}};
function focusCard(i){{if(!cards.length)return;idx=(i+cards.length)%cards.length;cards.forEach(c=>c.classList.remove('active'));
const c=cards[idx];c.classList.add('active');c.scrollIntoView({{behavior:'smooth',block:'center'}});}}
const q=document.getElementById('q');q.oninput=()=>{{const s=q.value.trim().toLowerCase();
document.querySelectorAll('[data-blob]').forEach(el=>{{el.classList.toggle('hidden-by-search',s&&!(el.dataset.blob||'').includes(s));}});}};
const drawer=document.getElementById('drawer');const drawerBody=document.getElementById('drawerBody');
document.getElementById('btnGlossary').onclick=()=>{{drawerBody.innerHTML=Object.entries(glossary).map(([k,v])=>`<div class="gitem"><b>${{k}}</b><p>${{v}}</p></div>`).join('');drawer.classList.add('open');}};
document.getElementById('closeDrawer').onclick=()=>drawer.classList.remove('open');
document.body.onclick=e=>{{const t=e.target.closest('.term');if(!t)return;
drawerBody.innerHTML=`<div class="gitem"><b>${{t.dataset.term}}</b><p>${{glossary[t.dataset.term]||'暂无'}}</p></div>`;drawer.classList.add('open');}};
const tocLinks=[...document.querySelectorAll('#toc a')];
const sections=tocLinks.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
const io=new IntersectionObserver(es=>{{es.forEach(en=>{{if(!en.isIntersecting)return;const id='#'+en.target.id;
tocLinks.forEach(a=>a.classList.toggle('active',a.getAttribute('href')===id));}});}},
{{rootMargin:'-20% 0px -65% 0px',threshold:0.01}});
sections.forEach(s=>io.observe(s));
document.onkeydown=e=>{{if(e.target.matches('input,textarea'))return;
if(e.key==='1')setMode('both');if(e.key==='2')setMode('zh');if(e.key==='3')setMode('en');
if(e.key==='j'||e.key==='J'){{e.preventDefault();focusCard(idx+1);}}
if(e.key==='k'||e.key==='K'){{e.preventDefault();focusCard(idx-1);}}
if(e.key==='g'||e.key==='G')document.getElementById('btnGlossary').click();
if(e.key==='/'){{e.preventDefault();q.focus();}};}};
</script></body></html>"""
    )
    return "".join(parts)


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    n = sum(len(s["paras"]) for s in SECTIONS)
    print(f"Wrote {OUT} ({n} paragraphs, {OUT.stat().st_size} bytes)")
