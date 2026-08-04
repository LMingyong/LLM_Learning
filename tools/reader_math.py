"""Shared KaTeX formula panels for paper study HTML pages."""

from __future__ import annotations

import html
from typing import Any


def esc(s: str) -> str:
    return html.escape(s)


KATEX_HEAD = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[{left:'\\\\[',right:'\\\\]',display:true},{left:'$',right:'$',display:false}],throwOnError:false});"></script>
"""

MATH_CSS = r"""
.math-stack{display:flex;flex-direction:column;gap:10px;margin:12px 0 4px}
.math-panel{border:1px solid var(--line);border-radius:14px;background:linear-gradient(180deg,#fff,#fffcf5);
padding:12px 14px;box-shadow:0 8px 24px rgba(40,50,40,.04)}
.math-panel .math-tag{font-family:var(--sans);font-size:11px;font-weight:700;letter-spacing:.04em;
color:var(--accent);margin:0 0 8px;display:flex;align-items:center;gap:8px}
.math-panel .math-tag::before{content:"";width:8px;height:8px;border-radius:2px;background:var(--accent);flex:0 0 auto}
.math-panel .math-eq{overflow-x:auto;padding:4px 0 2px;font-size:1.05em;line-height:1.6;color:var(--ink)}
.math-panel .math-eq .katex-display{margin:0.4em 0}
.math-panel .math-note{font-family:var(--sans);font-size:12px;color:var(--muted);margin-top:8px;
padding-top:8px;border-top:1px dashed var(--line);line-height:1.5}
.formula-wall{display:grid;grid-template-columns:1fr;gap:12px;margin:0 0 18px}
@media (min-width:820px){.formula-wall{grid-template-columns:1fr 1fr}}
.formula-wall .math-panel{min-height:100%}
.formula-wall .math-panel.span2{grid-column:1 / -1}
.inline-math-hint{font-family:var(--sans);font-size:12px;color:var(--faint);margin:0 0 10px}
"""


def render_formulas(formulas: list[dict[str, Any]] | None, *, wall: bool = False) -> str:
    if not formulas:
        return ""
    panels: list[str] = []
    for f in formulas:
        tag = esc(f.get("tag", "公式"))
        latex = f.get("latex", "").strip()
        note = f.get("note", "")
        span = " span2" if f.get("wide") else ""
        note_html = f'<div class="math-note">{esc(note)}</div>' if note else ""
        # Keep raw LaTeX inside \[ \]; do not HTML-escape backslashes needed by KaTeX,
        # but escape <>& that could break HTML.
        safe_latex = (
            latex.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        panels.append(
            f'<div class="math-panel{span}" data-blob="{esc((tag + " " + note + " " + latex).lower())}">'
            f'<div class="math-tag">{tag}</div>'
            f'<div class="math-eq">\\[{safe_latex}\\]</div>'
            f"{note_html}</div>"
        )
    cls = "formula-wall" if wall else "math-stack"
    return f'<div class="{cls}">{"".join(panels)}</div>'
