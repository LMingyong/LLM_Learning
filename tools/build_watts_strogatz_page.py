#!/usr/bin/env python3
"""Build fine-grained Watts–Strogatz study page: original + zh + paragraph summary."""

from __future__ import annotations

import html
import json
from pathlib import Path

from watts_strogatz_paragraphs import GLOSSARY, REFS, SECTIONS

OUT = Path(__file__).resolve().parents[1] / "papers/watts-strogatz/index.html"


def esc(s: str) -> str:
    return html.escape(s)


def fig_rewire() -> str:
    return """
<svg viewBox="0 0 780 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Watts-Strogatz rewiring">
  <rect width="780" height="220" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="390" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">Fig.1 教学重绘：环格子随机重连（p 从小到大）</text>
    <!-- p=0 -->
    <text x="130" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#0f6e56">p = 0 规则</text>
    <circle cx="130" cy="120" r="48" fill="none" stroke="#d8d0c0" stroke-width="2"/>
    <g fill="#0f6e56">
      <circle cx="130" cy="72" r="7"/><circle cx="178" cy="100" r="7"/><circle cx="162" cy="155" r="7"/>
      <circle cx="98" cy="155" r="7"/><circle cx="82" cy="100" r="7"/><circle cx="130" cy="168" r="0"/>
    </g>
    <path d="M130 79 L178 100 L162 148 L98 148 L82 100 Z" fill="none" stroke="#0f6e56" stroke-width="2"/>
    <path d="M130 79 L162 148 M178 100 L98 148 M82 100 L130 79" fill="none" stroke="#0f6e56" stroke-width="1.2" opacity=".55"/>
    <!-- p mid -->
    <text x="390" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">0 &lt; p &lt; 1 小世界</text>
    <circle cx="390" cy="120" r="48" fill="none" stroke="#d8d0c0" stroke-width="2"/>
    <g fill="#0f6e56">
      <circle cx="390" cy="72" r="7"/><circle cx="438" cy="100" r="7"/><circle cx="422" cy="155" r="7"/>
      <circle cx="358" cy="155" r="7"/><circle cx="342" cy="100" r="7"/>
    </g>
    <path d="M390 79 L438 100 L422 148 L358 148 L342 100 Z" fill="none" stroke="#0f6e56" stroke-width="2"/>
    <path d="M390 79 Q430 40 438 100" fill="none" stroke="#1f4e79" stroke-width="2.5" stroke-dasharray="5 3"/>
    <path d="M342 100 Q300 160 422 148" fill="none" stroke="#1f4e79" stroke-width="2" stroke-dasharray="5 3"/>
    <!-- p=1 -->
    <text x="650" y="52" text-anchor="middle" font-size="12" font-weight="700" fill="#b85c38">p = 1 随机</text>
    <circle cx="650" cy="120" r="48" fill="none" stroke="#d8d0c0" stroke-width="2"/>
    <g fill="#b85c38">
      <circle cx="650" cy="72" r="7"/><circle cx="698" cy="100" r="7"/><circle cx="682" cy="155" r="7"/>
      <circle cx="618" cy="155" r="7"/><circle cx="602" cy="100" r="7"/>
    </g>
    <path d="M650 79 L682 155 M698 100 L618 155 M602 100 L682 155 M650 79 L618 155 M698 100 L602 100"
          fill="none" stroke="#b85c38" stroke-width="2"/>
    <text x="390" y="205" text-anchor="middle" font-size="12" fill="#7d8c84">绿=局部边 · 蓝虚线=捷径 · 橙=高度随机化后的长程连接</text>
  </g>
</svg>
"""


def fig_lc() -> str:
    return """
<svg viewBox="0 0 760 260" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="L and C vs p">
  <rect width="760" height="260" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="380" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">Fig.2 示意：L(p) 先陡降，C(p) 后下降 → 中间小世界带</text>
    <!-- axes -->
    <line x1="80" y1="210" x2="700" y2="210" stroke="#5a6a62" stroke-width="1.5"/>
    <line x1="80" y1="210" x2="80" y2="50" stroke="#5a6a62" stroke-width="1.5"/>
    <text x="390" y="245" text-anchor="middle" font-size="12" fill="#5a6a62">p（对数轴示意）→</text>
    <text x="40" y="130" text-anchor="middle" font-size="12" fill="#5a6a62" transform="rotate(-90 40 130)">归一化 L,C</text>
    <!-- L curve -->
    <path d="M90 70 C140 72, 180 75, 220 140 S320 195, 420 200 S600 205, 680 206"
          fill="none" stroke="#1f4e79" stroke-width="3"/>
    <!-- C curve -->
    <path d="M90 78 C200 78, 280 80, 360 95 S520 150, 620 190 S680 200, 690 202"
          fill="none" stroke="#0f6e56" stroke-width="3"/>
    <!-- small-world band -->
    <rect x="210" y="55" width="220" height="145" fill="#1f4e79" opacity="0.06" rx="8"/>
    <text x="320" y="48" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">小世界区间</text>
    <text x="320" y="175" text-anchor="middle" font-size="11" fill="#5a6a62">L≈L_random · C≫C_random</text>
    <g font-size="12">
      <rect x="560" y="60" width="14" height="4" fill="#1f4e79"/><text x="580" y="65" fill="#1f4e79">L(p)/L(0)</text>
      <rect x="560" y="82" width="14" height="4" fill="#0f6e56"/><text x="580" y="87" fill="#0f6e56">C(p)/C(0)</text>
    </g>
    <text x="100" y="225" font-size="11" fill="#7d8c84">p→0</text>
    <text x="660" y="225" font-size="11" fill="#7d8c84">p→1</text>
  </g>
</svg>
"""


FIGURES = {
    "rewire": ("教学重绘 · 对应论文 Fig. 1 随机重连程序", fig_rewire()),
    "lc_curve": ("教学示意 · 对应论文 Fig. 2：L 先降、C 后降", fig_lc()),
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
<title>Watts–Strogatz 逐段精读 · 小世界网络</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@400;500;700&amp;family=Noto+Serif+SC:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
<style>{CSS}</style></head>
<body class="mode-both"><div class="app">
<aside class="side">
<div class="brand">LLM Learning · Paper Reader</div>
<h1>Watts–Strogatz 逐段精读</h1>
<div class="meta">Nature 393, 440–442 (1998)<br/>每段 = 小结 + Original + 译文<br/>BigBird 随机边的图论前驱</div>
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
<a class="btn" href="../bigbird/example.html">BigBird 全流程 →</a>
<a class="btn" href="../bigbird/index.html">BigBird 精读 →</a>
<div class="search"><input id="q" type="search" placeholder="搜索段落 / 名词 / 引用…" /></div>
</div>
<section class="hero">
<h2>Collective dynamics of ‘small-world’ networks</h2>
<p>浅色逐段精读 Watts &amp; Strogatz（1998）。抓住两件事：<strong>L 因少量捷径陡降</strong>，而<strong>C 在小 p 下几乎不动</strong>——于是出现「高聚类 + 短路径」的小世界带。末节桥接到 BigBird：窗口≈局部边，随机注意力≈捷径，但工程上选择「不删窗、只加边」。</p>
<div class="chips">
<span class="chip">旋钮：<em>p 重连概率</em></span>
<span class="chip">全局：<em>L(p)</em></span>
<span class="chip">局部：<em>C(p)</em></span>
<span class="chip">机制：<em>short cuts</em></span>
<span class="chip">下游：<em>BigBird 随机边</em></span>
</div>
</section>
<p class="note">英文贴近 Nature 原文；图注/表 1 做了可读性整理。段末小结为学习导读。公式与表号以 <a href="./paper.pdf">paper.pdf</a> 为准。</p>
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
        lv = "must" if r["level"] == "本篇" else ("imp" if r["level"] in ("对照", "前驱") else "")
        links = f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">打开 →</a>'
        if r.get("ext"):
            links += f' · <a href="{esc(r["ext"])}" target="_blank" rel="noopener">外链</a>'
        parts.append(
            f'<div class="ref" data-blob="{esc((r["title"] + " " + r["why"]).lower())}">'
            f'<span class="lv {lv}">{esc(r["level"])}</span>'
            f"<h4>{esc(r['title'])}</h4><p>{esc(r['why'])}</p>{links}</div>\n"
        )
    parts.append(
        '</div><p class="note" style="margin-top:28px">本页为学习用逐段精读；数字与图以 PDF 为准。示意图为教学重绘。</p>'
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
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    n = sum(len(s["paras"]) for s in SECTIONS)
    print(f"Wrote {OUT} ({n} paragraphs, {OUT.stat().st_size} bytes)")
