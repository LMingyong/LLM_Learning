#!/usr/bin/env python3
"""Build interactive topic study pages (sparse / flash attention)."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CSS = r"""
:root{
  --bg0:#071316; --bg1:#0d1f24; --line:rgba(180,220,210,.14);
  --text:#e7f2ef; --muted:#9bb4ae; --faint:#6f8b84;
  --accent:#3dceb0; --accent2:#f0b35a; --card:#0f2429cc;
  --shadow:0 18px 50px rgba(0,0,0,.35); --radius:18px;
  --serif:"Source Serif 4","Noto Serif SC",Georgia,serif;
  --sans:"Sora","Noto Sans SC",system-ui,sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,monospace;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;color:var(--text);font-family:var(--serif);
  background:radial-gradient(1200px 700px at 10% -10%,rgba(61,206,176,.18),transparent 55%),
    radial-gradient(900px 600px at 100% 0%,rgba(240,179,90,.12),transparent 50%),
    linear-gradient(180deg,var(--bg0),var(--bg1) 40%,#08181c);min-height:100vh}
body::before{content:"";position:fixed;inset:0;pointer-events:none;opacity:.35;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.45'/%3E%3C/svg%3E");
  mix-blend-mode:soft-light}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.app{display:grid;grid-template-columns:280px minmax(0,1fr);min-height:100vh}
.side{position:sticky;top:0;height:100vh;overflow:auto;padding:22px 16px 28px;
  border-right:1px solid var(--line);background:linear-gradient(180deg,rgba(8,24,28,.92),rgba(8,24,28,.75));backdrop-filter:blur(10px)}
.brand{font-family:var(--sans);font-weight:600;font-size:13px;color:var(--accent);margin:0 0 6px}
.side h1{font-family:var(--sans);font-size:20px;line-height:1.25;margin:0 0 8px}
.side .meta{font-family:var(--sans);font-size:12px;color:var(--muted);line-height:1.5;margin-bottom:16px}
.side nav a{display:block;padding:8px 10px;border-radius:10px;color:var(--muted);
  font-family:var(--sans);font-size:13px;text-decoration:none;margin-bottom:2px}
.side nav a:hover,.side nav a.active{background:rgba(61,206,176,.1);color:var(--text)}
.side .hint{margin-top:18px;padding:12px;border:1px solid var(--line);border-radius:12px;
  font-family:var(--sans);font-size:12px;color:var(--faint);line-height:1.55}
.main{padding:22px 28px 80px;max-width:1100px}
.topbar{position:sticky;top:0;z-index:20;margin:0 -28px 22px;padding:14px 28px;
  display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  background:rgba(7,19,22,.82);border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}
.seg{display:inline-flex;padding:4px;border-radius:999px;background:rgba(255,255,255,.04);border:1px solid var(--line)}
.seg button{appearance:none;border:0;background:transparent;color:var(--muted);cursor:pointer;
  font-family:var(--sans);font-size:12px;padding:8px 12px;border-radius:999px}
.seg button.on{background:rgba(61,206,176,.18);color:var(--text)}
.btn{font-family:var(--sans);font-size:12px;border:1px solid var(--line);background:rgba(255,255,255,.04);
  color:var(--text);border-radius:999px;padding:8px 12px;cursor:pointer}
.btn:hover{border-color:rgba(61,206,176,.45)}
.search{flex:1;min-width:180px}
.search input{width:100%;border-radius:999px;border:1px solid var(--line);background:rgba(0,0,0,.25);
  color:var(--text);padding:9px 14px;font-family:var(--sans);font-size:13px;outline:none}
.search input:focus{border-color:rgba(61,206,176,.55)}
.hero{border:1px solid var(--line);border-radius:var(--radius);padding:22px 24px;margin-bottom:22px;
  background:linear-gradient(135deg,rgba(61,206,176,.12),transparent 40%),linear-gradient(180deg,rgba(20,48,57,.9),rgba(15,36,41,.75));
  box-shadow:var(--shadow)}
.hero h2{font-family:var(--sans);margin:0 0 8px;font-size:28px}
.hero p{margin:0;color:var(--muted);font-family:var(--sans);font-size:14px;line-height:1.6}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.chip{font-family:var(--sans);font-size:11px;padding:6px 10px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.chip em{color:var(--accent2);font-style:normal}
.section{margin:28px 0 10px;scroll-margin-top:78px}
.section h3{font-family:var(--sans);font-size:18px;margin:0 0 12px;padding-bottom:8px;
  border-bottom:1px solid var(--line);display:flex;align-items:baseline;gap:10px}
.section h3 span{font-size:12px;color:var(--faint);font-weight:500}
.card{border:1px solid var(--line);background:var(--card);border-radius:16px;padding:14px 16px;margin:0 0 12px;
  transition:border-color .2s,transform .2s,box-shadow .2s}
.card:hover{border-color:rgba(61,206,176,.35);transform:translateY(-1px);box-shadow:0 10px 30px rgba(0,0,0,.22)}
.card.active{border-color:rgba(61,206,176,.55);box-shadow:0 0 0 1px rgba(61,206,176,.2)}
.summary{font-family:var(--sans);font-size:13px;color:#d8fff4;background:rgba(61,206,176,.1);
  border-left:3px solid var(--accent);padding:8px 10px;border-radius:0 10px 10px 0;margin:0 0 10px;line-height:1.5}
.lang{font-size:15.5px;line-height:1.75}
.lang .en{color:#d7e7e2}.lang .zh{color:#f3faf7}
.lang .label{font-family:var(--sans);font-size:11px;color:var(--faint);letter-spacing:.08em;text-transform:uppercase;margin:0 0 4px}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}
body.mode-zh .en-block,body.mode-en .zh-block{display:none}
body.mode-zh .pair,body.mode-en .pair{grid-template-columns:1fr}
.terms{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.term{font-family:var(--sans);font-size:11px;padding:4px 8px;border-radius:999px;cursor:pointer;
  background:rgba(240,179,90,.1);color:#ffd89a;border:1px solid rgba(240,179,90,.25)}
.term:hover{background:rgba(240,179,90,.2)}
.pre{font-family:var(--mono);font-size:12.5px;line-height:1.55;background:rgba(0,0,0,.35);
  border:1px solid var(--line);border-radius:12px;padding:12px 14px;margin:8px 0;overflow:auto;color:#cde8e0}
.hidden-by-search{display:none !important}
.drawer{position:fixed;top:0;right:0;width:min(420px,100%);height:100vh;overflow:auto;z-index:40;
  background:linear-gradient(180deg,#0c2026,#09171b);border-left:1px solid var(--line);
  transform:translateX(100%);transition:transform .28s ease;padding:18px 16px 40px;box-shadow:var(--shadow)}
.drawer.open{transform:none}
.drawer h2{font-family:var(--sans);margin:0 0 6px;font-size:18px}
.gitem{border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0}
.gitem b{font-family:var(--sans);color:var(--accent2)}
.gitem p{margin:6px 0 0;color:var(--muted);font-size:14px;line-height:1.55}
.refgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}
.ref{border:1px solid var(--line);border-radius:16px;padding:14px;background:rgba(15,36,41,.85);
  display:flex;flex-direction:column;gap:8px;min-height:140px}
.ref .lv{font-family:var(--sans);font-size:11px;align-self:start;padding:4px 8px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.ref .lv.must{color:#08201b;background:var(--accent);border-color:transparent;font-weight:700}
.ref .lv.imp{color:#2a1c05;background:var(--accent2);border-color:transparent;font-weight:700}
.ref h4{margin:0;font-family:var(--sans);font-size:15px;line-height:1.35}
.ref p{margin:0;color:var(--muted);font-size:13px;line-height:1.5;flex:1}
.kbd{font-family:var(--mono);font-size:11px;border:1px solid var(--line);border-bottom-width:2px;border-radius:6px;padding:1px 5px;color:var(--faint)}
.flow{border:1px solid var(--line);border-radius:14px;padding:14px;margin:10px 0;background:rgba(0,0,0,.2)}
.flow ol{margin:0;padding-left:20px;font-family:var(--sans);font-size:13px;line-height:1.7;color:var(--muted)}
@media (max-width:960px){
  .app{grid-template-columns:1fr}
  .side{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}
  .pair{grid-template-columns:1fr}
  .main{padding:16px 14px 70px}
  .topbar{margin:0 -14px 16px;padding:12px 14px}
}
"""


def esc(s: str) -> str:
    return html.escape(s)


def build_page(meta: dict[str, Any]) -> str:
    sections = meta["sections"]
    glossary = meta["glossary"]
    refs = meta["refs"]
    title = meta["title"]
    subtitle = meta["subtitle"]
    hero = meta["hero"]
    chips = meta["chips"]
    formula = meta.get("formula", "")

    parts: list[str] = []
    parts.append(
        f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{esc(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&family=Sora:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap" rel="stylesheet"/>
<style>{CSS}</style></head>
<body class="mode-both"><div class="app">
<aside class="side">
<div class="brand">LLM Learning · Topic Reader</div>
<h1>{esc(meta["nav_title"])}</h1>
<div class="meta">{esc(subtitle)}</div>
<nav id="toc">"""
    )
    for sec in sections:
        parts.append(f'<a href="#{sec["id"]}">{esc(sec["title"])}</a>\n')
    parts.append('<a href="#glossary">名词重点解释</a>\n<a href="#refs">重点引用论文</a>\n')
    parts.append(
        """</nav>
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
"""
    )
    rel = meta.get("related")
    if rel:
        rel_href = esc(rel["href"])
        rel_label = esc(rel["label"])
        parts.append(f'<a class="btn" href="{rel_href}">{rel_label} →</a>\n')
    parts.append(
        """<div class="search"><input id="q" type="search" placeholder="搜索段落 / 名词 / 引用…" /></div>
</div>
"""
    )
    parts.append(
        """<section class="hero"><h2>"""
        + esc(hero)
        + """</h2><p>"""
        + esc(meta["hero_desc"])
        + """</p><div class="chips">"""
    )
    for c in chips:
        parts.append(f'<span class="chip">{esc(c["label"])}：<em>{esc(c["value"])}</em></span>')
    parts.append("</div></section>\n")

    if formula:
        parts.append(
            f'<section class="section" id="formula"><h3>核心公式 / 流程 <span>先建立直觉</span></h3>'
            f'<div class="card"><div class="pre">{formula}</div></div></section>\n'
        )

    card_i = 0
    for sec in sections:
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
            extra = p.get("extra", "")
            p_en, p_zh, p_sum = esc(p["en"]), esc(p["zh"]), esc(p["summary"])
            parts.append(
                f'<article class="card para" data-idx="{card_i}" data-blob="{esc(blob)}">\n'
                f'<div class="summary"><b>小结</b> · {p_sum}</div>\n'
                f'<div class="pair lang">\n'
                f'<div class="en-block"><div class="label">Original</div><div class="en">{p_en}</div></div>\n'
                f'<div class="zh-block"><div class="label">译文</div><div class="zh">{p_zh}</div></div>\n'
                f'</div>{extra}\n<div class="terms">{terms}</div></article>\n'
            )
        parts.append("</section>\n")

    parts.append('<section class="section" id="glossary"><h3>名词重点解释</h3><div class="refgrid">\n')
    for name, desc in glossary:
        parts.append(
            f'<div class="gitem" id="term-{esc(name)}" data-blob="{esc((name+" "+desc).lower())}">'
            f"<b>{esc(name)}</b><p>{esc(desc)}</p></div>\n"
        )
    parts.append("</div></section>\n")

    parts.append('<section class="section" id="refs"><h3>重点引用论文</h3><div class="refgrid">\n')
    for r in refs:
        lv = "must" if r["level"] == "必读" else ("imp" if r["level"] == "重点" else "")
        parts.append(
            f'<div class="ref" data-blob="{esc((r["title"]+" "+r["why"]).lower())}">'
            f'<span class="lv {lv}">{esc(r["level"])}</span>'
            f"<h4>{esc(r['title'])}</h4><p>{esc(r['why'])}</p>"
            f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">打开 →</a></div>\n'
        )
    parts.append("</div></section></main></div>\n")

    gjs = ",\n".join(f"{json.dumps(k)}:{json.dumps(v)}" for k, v in glossary)
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
new IntersectionObserver(es=>{{es.forEach(en=>{{if(!en.isIntersecting)return;const id='#'+en.target.id;
tocLinks.forEach(a=>a.classList.toggle('active',a.getAttribute('href')===id));}});}},
{{rootMargin:'-20% 0px -65% 0px',threshold:0.01}}).observe?sections.forEach(s=>new IntersectionObserver(es=>{{es.forEach(en=>{{if(!en.isIntersecting)return;const id='#'+en.target.id;
tocLinks.forEach(a=>a.classList.toggle('active',a.getAttribute('href')===id));}});}},
{{rootMargin:'-20% 0px -65% 0px',threshold:0.01}}).observe(s)):null;
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
    from topic_content import FLASH_ATTENTION, SPARSE_ATTENTION

    out_sparse = ROOT / "topics/sparse-attention/index.html"
    out_flash = ROOT / "topics/flash-attention/index.html"
    out_sparse.write_text(build_page(SPARSE_ATTENTION), encoding="utf-8")
    out_flash.write_text(build_page(FLASH_ATTENTION), encoding="utf-8")
    print(f"Wrote {out_sparse} ({out_sparse.stat().st_size} bytes)")
    print(f"Wrote {out_flash} ({out_flash.stat().st_size} bytes)")
