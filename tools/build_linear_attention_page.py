#!/usr/bin/env python3
"""Build fine-grained Linear Attention (Katharopoulos et al.) study page."""

from __future__ import annotations

import html
import json
from pathlib import Path

from linear_attention_paragraphs import GLOSSARY, REFS, SECTIONS
from reader_math import KATEX_HEAD, MATH_CSS, render_formulas

OUT = Path(__file__).resolve().parents[1] / "papers/linear-attention/index.html"


def esc(s: str) -> str:
    return html.escape(s)


def fig_assoc() -> str:
    return """
<svg viewBox="0 0 820 220" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="associativity">
  <rect width="820" height="220" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">结合律重排：从 O(N²) 注意力矩阵到 O(N) 状态聚合</text>
    <rect x="40" y="55" width="320" height="110" rx="14" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="200" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#b85c38">Softmax / 朴素核</text>
    <text x="200" y="112" text-anchor="middle" font-size="13" fill="#5a6a62">(φ(Q) φ(K)ᵀ) V</text>
    <text x="200" y="138" text-anchor="middle" font-size="12" fill="#7d8c84">先造 N×N，再乘 V → O(N²)</text>
    <path d="M375 110 H445" stroke="#0f6e56" stroke-width="2"/>
    <text x="410" y="100" text-anchor="middle" font-size="11" fill="#0f6e56">结合律</text>
    <rect x="460" y="55" width="320" height="110" rx="14" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="620" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">Linear Attention</text>
    <text x="620" y="112" text-anchor="middle" font-size="13" fill="#5a6a62">φ(Q) (φ(K)ᵀ V)</text>
    <text x="620" y="138" text-anchor="middle" font-size="12" fill="#7d8c84">先聚 S=Σφ(k)vᵀ，再读 → O(N)</text>
    <text x="410" y="195" text-anchor="middle" font-size="12" fill="#7d8c84">前提：sim(q,k)=φ(q)ᵀφ(k) ≥ 0</text>
  </g>
</svg>
"""


def fig_rnn() -> str:
    return """
<svg viewBox="0 0 820 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="RNN form">
  <rect width="820" height="210" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">因果线性注意力 = 双状态 RNN</text>
    <rect x="40" y="60" width="120" height="70" rx="12" fill="#efe9dc" stroke="#5a6a62"/>
    <text x="100" y="90" text-anchor="middle" font-size="14" font-weight="700" fill="#1c2420">x_i</text>
    <text x="100" y="112" text-anchor="middle" font-size="11" fill="#5a6a62">当前输入</text>
    <path d="M165 95 H200" stroke="#0f6e56" stroke-width="2"/>
    <rect x="205" y="50" width="200" height="90" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="305" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="#1f4e79">更新状态</text>
    <text x="305" y="100" text-anchor="middle" font-size="12" fill="#5a6a62">S ← S + φ(k)vᵀ</text>
    <text x="305" y="120" text-anchor="middle" font-size="12" fill="#5a6a62">Z ← Z + φ(k)</text>
    <path d="M410 95 H445" stroke="#0f6e56" stroke-width="2"/>
    <rect x="450" y="50" width="200" height="90" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="550" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="#0f6e56">读出</text>
    <text x="550" y="100" text-anchor="middle" font-size="12" fill="#5a6a62">o ∝ φ(q)ᵀ S</text>
    <text x="550" y="120" text-anchor="middle" font-size="12" fill="#5a6a62">/ φ(q)ᵀ Z</text>
    <path d="M655 95 H690" stroke="#0f6e56" stroke-width="2"/>
    <rect x="695" y="60" width="90" height="70" rx="12" fill="#1c2420"/>
    <text x="740" y="100" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">y_i</text>
    <text x="410" y="175" text-anchor="middle" font-size="12" fill="#5a6a62">每步常数时间；状态大小与序列长度无关</text>
    <text x="410" y="195" text-anchor="middle" font-size="12" fill="#7d8c84">标题含义：Transformers are RNNs（时间维递推）</text>
  </g>
</svg>
"""


FIGURES = {
    "assoc": ("教学示意 · 对应论文 §3.2 结合律重排", fig_assoc()),
    "rnn": ("教学示意 · 对应论文 §3.3–3.4 因果递推 / RNN 形式", fig_rnn()),
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
.hero h2{font-family:var(--sans);margin:0 0 8px;font-size:24px}
.hero p{margin:0;color:var(--muted);font-family:var(--sans);font-size:14px;line-height:1.65}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chip{font-family:var(--sans);font-size:11px;padding:6px 10px;border-radius:999px;border:1px solid var(--line);color:var(--muted);background:#fff}
.chip em{color:var(--warm);font-style:normal;font-weight:600}
.section{margin:28px 0 10px;scroll-margin-top:78px}
.section h3{font-family:var(--sans);font-size:18px;margin:0 0 12px;padding-bottom:8px;
border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:10px}
.section h3 span{font-size:12px;color:var(--faint);font-weight:500}
.card{border:1px solid var(--line);background:var(--paper);border-radius:16px;padding:14px 16px;margin:0 0 12px;
transition:border-color .2s,transform .2s,box-shadow .2s}
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
""" + MATH_CSS + r"""
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
<title>Linear Attention 逐段精读 · Transformers are RNNs</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@400;500;700&amp;family=Noto+Serif+SC:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
{KATEX_HEAD}
<style>{CSS}</style></head>
<body class="mode-both"><div class="app">
<aside class="side">
<div class="brand">LLM Learning · Paper Reader</div>
<h1>Linear Attention</h1>
<div class="meta">Katharopoulos et al. · ICML 2020<br/>arXiv:2006.16236<br/>每段 = 小结 + Original + 译文</div>
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
<a class="btn" href="../delta-attention/index.html">DeltaNet →</a>
<a class="btn" href="../kda/index.html">KDA →</a>
<a class="btn" href="https://linear-transformers.com/" target="_blank" rel="noopener">官网 →</a>
<div class="search"><input id="q" type="search" placeholder="搜索段落 / 名词 / 引用…" /></div>
</div>
<section class="hero">
<h2>Transformers are RNNs · Linear Attention</h2>
<p>线性注意力经典源头：用核特征把 softmax 换成 φ(q)ᵀφ(k)，再用结合律把计算从「N×N 矩阵」重排成「固定大小状态聚合」。因果形式下，Transformer 就是带双状态 (S,Z) 的 RNN——这也是后来 DeltaNet / GDN / KDA 的起点。</p>
<div class="chips">
<span class="chip">复杂度：<em>O(N²) → O(N)</em></span>
<span class="chip">特征：<em>φ = elu+1</em></span>
<span class="chip">推理：<em>常数内存 RNN</em></span>
<span class="chip">下游：<em>KDA / 混合架构</em></span>
</div>
</section>
<p class="note">英文贴近 ICML 2020 论文；段末小结为学习导读。学完建议接着读 <a href="../delta-attention/index.html">DeltaNet</a> 与 <a href="../kda/index.html">KDA</a>。</p>
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
            math_html = render_formulas(p.get("formulas"))
            p_en, p_zh, p_sum = esc(p["en"]), esc(p["zh"]), esc(p["summary"])
            parts.append(
                f'<article class="card para" data-idx="{card_i}" data-blob="{esc(blob)}">\n'
                f'<span class="pidx">§{card_i}</span>\n'
                f'<div class="summary"><b>小结</b> · {p_sum}</div>\n'
                f"{math_html}"
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
        lv = "must" if r["level"] == "本篇" else ("imp" if r["level"] in ("下游", "官网") else "")
        links = f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">打开 →</a>'
        if r.get("ext"):
            links += f' · <a href="{esc(r["ext"])}" target="_blank" rel="noopener">外链</a>'
        parts.append(
            f'<div class="ref" data-blob="{esc((r["title"] + " " + r["why"]).lower())}">'
            f'<span class="lv {lv}">{esc(r["level"])}</span>'
            f"<h4>{esc(r['title'])}</h4><p>{esc(r['why'])}</p>{links}</div>\n"
        )
    parts.append(
        '</div><p class="note" style="margin-top:28px">本页为学习用逐段精读；公式以 PDF 为准。示意图为教学重绘。</p>'
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
