#!/usr/bin/env python3
"""Build fine-grained Kimi Linear / KDA study page."""

from __future__ import annotations

import html
import json
from pathlib import Path

from kimi_linear_paragraphs import FORMULA_WALL, GLOSSARY, REFS, SECTIONS
from reader_math import KATEX_HEAD, MATH_CSS, render_formulas

OUT = Path(__file__).resolve().parents[1] / "papers/kda/index.html"


def esc(s: str) -> str:
    return html.escape(s)


def fig_pipeline() -> str:
    return """
<svg viewBox="0 0 820 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="lineage">
  <rect width="820" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">谱系：Linear → DeltaNet → GDN → KDA</text>
    <rect x="30" y="60" width="160" height="70" rx="12" fill="#efe9dc" stroke="#5a6a62"/>
    <text x="110" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">Linear Attn</text>
    <text x="110" y="110" text-anchor="middle" font-size="11" fill="#5a6a62">S+=kvᵀ · 只加不改</text>
    <path d="M195 95 H225" stroke="#0f6e56" stroke-width="2"/>
    <rect x="230" y="60" width="160" height="70" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="310" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#1f4e79">DeltaNet</text>
    <text x="310" y="110" text-anchor="middle" font-size="11" fill="#5a6a62">delta 擦写纠错</text>
    <path d="M395 95 H425" stroke="#0f6e56" stroke-width="2"/>
    <rect x="430" y="60" width="160" height="70" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="510" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#0f6e56">GDN</text>
    <text x="510" y="110" text-anchor="middle" font-size="11" fill="#5a6a62">标量门 α</text>
    <path d="M595 95 H625" stroke="#0f6e56" stroke-width="2"/>
    <rect x="630" y="60" width="160" height="70" rx="12" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="710" y="90" text-anchor="middle" font-size="13" font-weight="700" fill="#b85c38">KDA</text>
    <text x="710" y="110" text-anchor="middle" font-size="11" fill="#5a6a62">Diag(α) 通道门</text>
    <text x="410" y="170" text-anchor="middle" font-size="12" fill="#7d8c84">每一步都保留前一步能力，只把「遗忘」做得更细</text>
  </g>
</svg>
"""


def fig_kda_steps() -> str:
    return """
<svg viewBox="0 0 820 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="KDA four steps">
  <rect width="820" height="210" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">KDA 逐步递推（与 recurrent_kda 对齐）</text>
    <rect x="20" y="55" width="170" height="90" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="105" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">1. 遗忘</text>
    <text x="105" y="108" text-anchor="middle" font-size="12" fill="#5a6a62">S ← Diag(e^{g}) S</text>
    <text x="105" y="128" text-anchor="middle" font-size="11" fill="#7d8c84">逐通道 α</text>
    <rect x="220" y="55" width="170" height="90" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="305" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">2. 预测</text>
    <text x="305" y="108" text-anchor="middle" font-size="12" fill="#5a6a62">v̂ ← kᵀ S</text>
    <text x="305" y="128" text-anchor="middle" font-size="11" fill="#7d8c84">按地址读出</text>
    <rect x="420" y="55" width="180" height="90" rx="12" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="510" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#b85c38">3. 纠错写入</text>
    <text x="510" y="108" text-anchor="middle" font-size="12" fill="#5a6a62">S += β k (v−v̂)ᵀ</text>
    <text x="510" y="128" text-anchor="middle" font-size="11" fill="#7d8c84">delta rule</text>
    <rect x="630" y="55" width="170" height="90" rx="12" fill="#1c2420"/>
    <text x="715" y="85" text-anchor="middle" font-size="14" font-weight="700" fill="#fff">4. 查询</text>
    <text x="715" y="108" text-anchor="middle" font-size="12" fill="#cfd8d3">o ← (q/√d)ᵀ S</text>
    <text x="715" y="128" text-anchor="middle" font-size="11" fill="#9bb4ae">固定大小状态</text>
    <text x="410" y="185" text-anchor="middle" font-size="12" fill="#7d8c84">状态 S ∈ R^{d×d}/head，不随序列长度增长</text>
  </g>
</svg>
"""


def fig_hybrid() -> str:
    boxes = []
    labels = ["KDA", "KDA", "KDA", "MLA", "KDA", "KDA", "KDA", "MLA"]
    x = 40
    for i, lab in enumerate(labels):
        if lab == "KDA":
            fill, stroke, tc = "#d8efe6", "#0f6e56", "#0f6e56"
        else:
            fill, stroke, tc = "#f3e0d6", "#b85c38", "#b85c38"
        boxes.append(
            f'<rect x="{x}" y="70" width="80" height="56" rx="10" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x+40}" y="103" text-anchor="middle" font-size="13" font-weight="700" fill="{tc}">{lab}</text>'
        )
        if i < len(labels) - 1:
            boxes.append(
                f'<path d="M{x+82} 98 H{x+95}" stroke="#5a6a62" stroke-width="2"/>'
            )
        x += 95
    return f"""
<svg viewBox="0 0 820 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="hybrid 3:1">
  <rect width="820" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">层间混合 3:1 · 每层后接 MoE FFN（示意）</text>
    {''.join(boxes)}
    <text x="410" y="165" text-anchor="middle" font-size="12" fill="#5a6a62">绿 = KDA 线性层（压 cache） · 橙 = MLA 全注意力（补检索） · MLA 用 NoPE</text>
    <text x="410" y="188" text-anchor="middle" font-size="12" fill="#7d8c84">长生成时 KV cache 约只剩全注意力层的 1/4</text>
  </g>
</svg>
"""


FIGURES = {
    "pipeline": ("教学示意 · 从线性注意力到 KDA", fig_pipeline()),
    "kda_steps": ("教学示意 · 与本夹 kda/recurrent.py 对齐", fig_kda_steps()),
    "hybrid": ("教学示意 · 对应论文 Fig.3 的 3:1 交织", fig_hybrid()),
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
.hero h2{font-family:var(--sans);margin:0 0 8px;font-size:26px}
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
<title>Kimi Linear / KDA 逐段精读 · Delta Attention</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@400;500;700&amp;family=Noto+Serif+SC:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
{KATEX_HEAD}
<style>{CSS}</style></head>
<body class="mode-both"><div class="app">
<aside class="side">
<div class="brand">LLM Learning · Paper Reader</div>
<h1>Kimi Linear / KDA</h1>
<div class="meta">arXiv:2510.26692<br/>每段 = 小结 + Original + 译文<br/>公式独立成卡 · 教学代码在本夹 kda/</div>
<nav id="toc">
<a href="#formulas">公式墙（速查）</a>
"""
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
<a class="btn" href="#formulas">公式墙</a>
<a class="btn" href="./notes.md">公式笔记 →</a>
<a class="btn" href="./kda/recurrent.py">recurrent.py →</a>
<a class="btn" href="./demo.py">demo.py →</a>
<a class="btn" href="../deltanet/index.html">DeltaNet 原点 →</a>
<a class="btn" href="../deltanet-parallel/index.html">并行训练 →</a>
<a class="btn" href="../gated-deltanet/index.html">Gated DeltaNet →</a>
<a class="btn" href="../linear-attention/index.html">Linear Attention →</a>
<div class="search"><input id="q" type="search" placeholder="搜索段落 / 名词 / 引用…" /></div>
</div>
<section class="hero">
<h2>Kimi Linear · Kimi Delta Attention（KDA）</h2>
<p>本夹对应 <strong>arXiv:2510.26692</strong>。与 DeltaNet 分开放：理论见 <a href="../deltanet/">deltanet</a>，可扩展训练见 <a href="../deltanet-parallel/">deltanet-parallel</a>；本夹是通道级门控 + 混合架构。精读含独立公式卡（KaTeX）。</p>
<div class="chips">
<span class="chip">核心：<em>KDA = GDN + Diag(α)</em></span>
<span class="chip">架构：<em>KDA:MLA = 3:1</em></span>
<span class="chip">收益：<em>−75% cache · ~6× 解码</em></span>
<span class="chip">代码：<em>./kda/</em></span>
</div>
</section>
<p class="note">建议：<a href="../deltanet/">原点</a> → <a href="../deltanet-parallel/">并行</a> → <a href="../gated-deltanet/index.html">GDN</a> → 本页，再扫本页 <a href="#formulas">公式墙</a>，最后打开 <a href="./kda/recurrent.py">recurrent.py</a>。</p>
<section class="section" id="formulas"><h3>公式墙（速查） <span>谱系一览</span></h3>
<p class="inline-math-hint">以下公式从正文抽出，便于对照；段内还有更细的展开卡。</p>
"""
        + render_formulas(FORMULA_WALL, wall=True)
        + "</section>\n"
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
        lv = "must" if r["level"] == "本篇" else ("imp" if r["level"] in ("代码", "前驱", "笔记") else "")
        links = f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">打开 →</a>'
        if r.get("ext"):
            links += f' · <a href="{esc(r["ext"])}" target="_blank" rel="noopener">外链</a>'
        parts.append(
            f'<div class="ref" data-blob="{esc((r["title"] + " " + r["why"]).lower())}">'
            f'<span class="lv {lv}">{esc(r["level"])}</span>'
            f"<h4>{esc(r['title'])}</h4><p>{esc(r['why'])}</p>{links}</div>\n"
        )
    parts.append(
        '</div><p class="note" style="margin-top:28px">本页为学习用逐段精读；数字与公式以 PDF 为准。示意图为教学重绘。</p>'
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
