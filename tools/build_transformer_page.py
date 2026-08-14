#!/usr/bin/env python3
"""Build fine-grained Attention Is All You Need study page."""

from __future__ import annotations

import html
import json
from pathlib import Path

from reader_math import KATEX_HEAD, MATH_CSS, render_formulas
from transformer_paragraphs import FORMULA_WALL, GLOSSARY, REFS, SECTIONS

OUT = Path(__file__).resolve().parents[1] / "papers/transformer/index.html"


def esc(s: str) -> str:
    return html.escape(s)


def fig_qkv() -> str:
    return """
<svg viewBox="0 0 820 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="QKV">
  <rect width="820" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">查字典类比：Query 提问 · Key 标签 · Value 内容</text>
    <rect x="40" y="50" width="220" height="100" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="150" y="88" text-anchor="middle" font-size="16" font-weight="700" fill="#1f4e79">Query</text>
    <text x="150" y="114" text-anchor="middle" font-size="12" fill="#5a6a62">此刻要读什么？</text>
    <text x="150" y="134" text-anchor="middle" font-size="11" fill="#7d8c84">当前 token 的问题</text>
    <rect x="300" y="50" width="220" height="100" rx="12" fill="#fff3d6" stroke="#8a6a20"/>
    <text x="410" y="88" text-anchor="middle" font-size="16" font-weight="700" fill="#8a6a20">Key</text>
    <text x="410" y="114" text-anchor="middle" font-size="12" fill="#5a6a62">这条记录关于什么？</text>
    <text x="410" y="134" text-anchor="middle" font-size="11" fill="#7d8c84">用来被匹配</text>
    <rect x="560" y="50" width="220" height="100" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="670" y="88" text-anchor="middle" font-size="16" font-weight="700" fill="#0f6e56">Value</text>
    <text x="670" y="114" text-anchor="middle" font-size="12" fill="#5a6a62">真正取走的内容</text>
    <text x="670" y="134" text-anchor="middle" font-size="11" fill="#7d8c84">按权重混合</text>
    <text x="410" y="178" text-anchor="middle" font-size="12" fill="#7d8c84">分数 = 问与标签有多齐；输出 = 内容的加权和</text>
  </g>
</svg>
"""


def fig_cost() -> str:
    return """
<svg viewBox="0 0 820 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="cost">
  <rect width="820" height="210" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">N×N 分数表：本仓库两条分叉都从这里出发</text>
    <rect x="40" y="48" width="230" height="110" rx="12" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="155" y="80" text-anchor="middle" font-size="14" font-weight="700" fill="#b85c38">稠密 Transformer</text>
    <text x="155" y="106" text-anchor="middle" font-size="12" fill="#5a6a62">每个 query 看所有 key</text>
    <text x="155" y="128" text-anchor="middle" font-size="12" fill="#5a6a62">O(N² d) · 本页</text>
    <rect x="295" y="48" width="230" height="110" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="410" y="80" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">稀疏注意力</text>
    <text x="410" y="106" text-anchor="middle" font-size="12" fill="#5a6a62">同一公式，删掉多数边</text>
    <text x="410" y="128" text-anchor="middle" font-size="12" fill="#5a6a62">O(N·r) · 下一站</text>
    <rect x="550" y="48" width="230" height="110" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="665" y="80" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">线性注意力</text>
    <text x="665" y="106" text-anchor="middle" font-size="12" fill="#5a6a62">改核，不造 N×N</text>
    <text x="665" y="128" text-anchor="middle" font-size="12" fill="#5a6a62">O(N) · 另一条线</text>
    <text x="410" y="188" text-anchor="middle" font-size="12" fill="#7d8c84">建议第一遍先走稀疏（改掩码），再走线性（改公式）</text>
  </g>
</svg>
"""


def fig_arch() -> str:
    return """
<svg viewBox="0 0 820 250" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="architecture">
  <rect width="820" height="250" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">图 1 教学重绘：左边编码器 · 右边解码器 · 各 6 层</text>
    <rect x="70" y="44" width="280" height="168" rx="14" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="210" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">Encoder ×6</text>
    <text x="210" y="98" text-anchor="middle" font-size="13" fill="#1c2420">① 多头自注意力</text>
    <text x="210" y="120" text-anchor="middle" font-size="12" fill="#5a6a62">看整句源语言</text>
    <text x="210" y="148" text-anchor="middle" font-size="13" fill="#1c2420">② 逐位置 FFN</text>
    <text x="210" y="170" text-anchor="middle" font-size="12" fill="#5a6a62">每词各自 MLP</text>
    <text x="210" y="196" text-anchor="middle" font-size="11" fill="#7d8c84">每子层：残差 + LayerNorm</text>
    <rect x="470" y="44" width="280" height="168" rx="14" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="610" y="70" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">Decoder ×6</text>
    <text x="610" y="96" text-anchor="middle" font-size="13" fill="#1c2420">① 掩码自注意力</text>
    <text x="610" y="118" text-anchor="middle" font-size="13" fill="#1c2420">② 交叉注意力</text>
    <text x="610" y="140" text-anchor="middle" font-size="12" fill="#5a6a62">Q 来自解码器 · KV 来自编码器</text>
    <text x="610" y="166" text-anchor="middle" font-size="13" fill="#1c2420">③ 逐位置 FFN</text>
    <text x="610" y="196" text-anchor="middle" font-size="11" fill="#7d8c84">同样残差 + LayerNorm</text>
    <text x="410" y="234" text-anchor="middle" font-size="12" fill="#7d8c84">输入两端都是：token 嵌入 + 位置编码</text>
  </g>
</svg>
"""


def fig_scaled() -> str:
    return """
<svg viewBox="0 0 820 210" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="scaled steps">
  <rect width="820" height="210" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">缩放点积四步（对应原文图 2 左 / 式 1）</text>
    <rect x="20" y="50" width="180" height="100" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="110" y="84" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">A. 点积</text>
    <text x="110" y="110" text-anchor="middle" font-size="12" fill="#5a6a62">S = Q Kᵀ</text>
    <text x="110" y="132" text-anchor="middle" font-size="11" fill="#7d8c84">形状 N×N</text>
    <rect x="220" y="50" width="180" height="100" rx="12" fill="#fff3d6" stroke="#8a6a20"/>
    <text x="310" y="84" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6a20">B. 缩放</text>
    <text x="310" y="110" text-anchor="middle" font-size="12" fill="#5a6a62">÷ √d_k</text>
    <text x="310" y="132" text-anchor="middle" font-size="11" fill="#7d8c84">防 softmax 饱和</text>
    <rect x="420" y="50" width="180" height="100" rx="12" fill="#f3e0d6" stroke="#b85c38"/>
    <text x="510" y="84" text-anchor="middle" font-size="14" font-weight="700" fill="#b85c38">C. softmax</text>
    <text x="510" y="110" text-anchor="middle" font-size="12" fill="#5a6a62">按行变权重</text>
    <text x="510" y="132" text-anchor="middle" font-size="11" fill="#7d8c84">可加 −∞ 掩码</text>
    <rect x="620" y="50" width="180" height="100" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="710" y="84" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">D. ×V</text>
    <text x="710" y="110" text-anchor="middle" font-size="12" fill="#5a6a62">加权求和</text>
    <text x="710" y="132" text-anchor="middle" font-size="11" fill="#7d8c84">输出 N×d_v</text>
    <text x="410" y="178" text-anchor="middle" font-size="12" fill="#5a6a62">O(N²) 发生在 A：那张分数表被造出来了</text>
    <text x="410" y="198" text-anchor="middle" font-size="12" fill="#7d8c84">稀疏注意力 = 在 A/C 之前就不允许多数 (i,j)</text>
  </g>
</svg>
"""


def fig_mask() -> str:
    return """
<svg viewBox="0 0 820 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="causal mask">
  <rect width="820" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">解码器因果掩码：只能看自己及左边</text>
    <text x="80" y="58" font-size="12" fill="#7d8c84">key →</text>
    <text x="28" y="120" font-size="12" fill="#7d8c84">q</text>
    <g font-size="13" font-weight="700">
      <rect x="90" y="70" width="36" height="36" fill="#d8efe6" stroke="#0f6e56"/><text x="108" y="93" text-anchor="middle" fill="#0f6e56">✓</text>
      <rect x="130" y="70" width="36" height="36" fill="#f3e0d6" stroke="#b85c38"/><text x="148" y="93" text-anchor="middle" fill="#b85c38">−∞</text>
      <rect x="170" y="70" width="36" height="36" fill="#f3e0d6" stroke="#b85c38"/><text x="188" y="93" text-anchor="middle" fill="#b85c38">−∞</text>
      <rect x="210" y="70" width="36" height="36" fill="#f3e0d6" stroke="#b85c38"/><text x="228" y="93" text-anchor="middle" fill="#b85c38">−∞</text>
      <rect x="90" y="110" width="36" height="36" fill="#d8efe6" stroke="#0f6e56"/><text x="108" y="133" text-anchor="middle" fill="#0f6e56">✓</text>
      <rect x="130" y="110" width="36" height="36" fill="#d8efe6" stroke="#0f6e56"/><text x="148" y="133" text-anchor="middle" fill="#0f6e56">✓</text>
      <rect x="170" y="110" width="36" height="36" fill="#f3e0d6" stroke="#b85c38"/><text x="188" y="133" text-anchor="middle" fill="#b85c38">−∞</text>
      <rect x="210" y="110" width="36" height="36" fill="#f3e0d6" stroke="#b85c38"/><text x="228" y="133" text-anchor="middle" fill="#b85c38">−∞</text>
      <rect x="90" y="150" width="36" height="36" fill="#d8efe6" stroke="#0f6e56"/><text x="108" y="173" text-anchor="middle" fill="#0f6e56">✓</text>
      <rect x="130" y="150" width="36" height="36" fill="#d8efe6" stroke="#0f6e56"/><text x="148" y="173" text-anchor="middle" fill="#0f6e56">✓</text>
      <rect x="170" y="150" width="36" height="36" fill="#d8efe6" stroke="#0f6e56"/><text x="188" y="173" text-anchor="middle" fill="#0f6e56">✓</text>
      <rect x="210" y="150" width="36" height="36" fill="#f3e0d6" stroke="#b85c38"/><text x="228" y="173" text-anchor="middle" fill="#b85c38">−∞</text>
    </g>
    <text x="480" y="100" font-size="14" fill="#1c2420">绿色：允许（j ≤ i）</text>
    <text x="480" y="128" font-size="14" fill="#1c2420">红色：非法未来，softmax 前设 −∞</text>
    <text x="480" y="156" font-size="13" fill="#7d8c84">稀疏注意力 = 在这张下三角里再挖更多洞</text>
  </g>
</svg>
"""


def fig_mha() -> str:
    return """
<svg viewBox="0 0 820 230" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="multi-head">
  <rect width="820" height="230" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">多头：8 套投影各算缩放点积，再拼回去（图 2 右）</text>
    <rect x="30" y="48" width="120" height="70" rx="10" fill="#efe9dc" stroke="#5a6a62"/>
    <text x="90" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">Q K V</text>
    <text x="90" y="98" text-anchor="middle" font-size="11" fill="#5a6a62">N×512</text>
    <rect x="180" y="42" width="90" height="48" rx="8" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="225" y="71" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">head 1</text>
    <rect x="280" y="42" width="90" height="48" rx="8" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="325" y="71" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">head 2</text>
    <rect x="380" y="42" width="90" height="48" rx="8" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="425" y="71" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">…</text>
    <rect x="480" y="42" width="90" height="48" rx="8" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="525" y="71" text-anchor="middle" font-size="12" font-weight="700" fill="#1f4e79">head 8</text>
    <text x="355" y="110" text-anchor="middle" font-size="11" fill="#7d8c84">每头 d_k=64 · 各自一张 N×N 分数图</text>
    <rect x="250" y="128" width="220" height="48" rx="10" fill="#fff3d6" stroke="#8a6a20"/>
    <text x="360" y="157" text-anchor="middle" font-size="13" font-weight="700" fill="#8a6a20">Concat → N×512</text>
    <rect x="500" y="128" width="200" height="48" rx="10" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="600" y="157" text-anchor="middle" font-size="13" font-weight="700" fill="#0f6e56">× W^O</text>
    <text x="410" y="202" text-anchor="middle" font-size="12" fill="#5a6a62">总计算量 ≈ 单头用满 512 维：变窄换来多套读法</text>
  </g>
</svg>
"""


def fig_three() -> str:
    return """
<svg viewBox="0 0 820 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="three uses">
  <rect width="820" height="200" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="26" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">同一套 MultiHead，三处 Q/K/V 来源不同</text>
    <rect x="30" y="48" width="240" height="110" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="150" y="78" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">编码器自注意</text>
    <text x="150" y="104" text-anchor="middle" font-size="12" fill="#5a6a62">Q=K=V=源句</text>
    <text x="150" y="126" text-anchor="middle" font-size="11" fill="#7d8c84">双向 · 无因果掩码</text>
    <rect x="290" y="48" width="240" height="110" rx="12" fill="#fff3d6" stroke="#8a6a20"/>
    <text x="410" y="78" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6a20">解码器掩码自注意</text>
    <text x="410" y="104" text-anchor="middle" font-size="12" fill="#5a6a62">Q=K=V=目标句</text>
    <text x="410" y="126" text-anchor="middle" font-size="11" fill="#7d8c84">下三角掩码</text>
    <rect x="550" y="48" width="240" height="110" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="670" y="78" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">交叉注意</text>
    <text x="670" y="104" text-anchor="middle" font-size="12" fill="#5a6a62">Q=解码器 · KV=编码器</text>
    <text x="670" y="126" text-anchor="middle" font-size="11" fill="#7d8c84">对齐源与目标</text>
    <text x="410" y="180" text-anchor="middle" font-size="12" fill="#7d8c84">GPT 只用中间这种（解码器堆）；BERT 只用左边这种（编码器堆）</text>
  </g>
</svg>
"""


def fig_pos() -> str:
    return """
<svg viewBox="0 0 820 180" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="positional encoding">
  <rect width="820" height="180" fill="#fffcf5"/>
  <g font-family="Manrope,sans-serif">
    <text x="410" y="28" text-anchor="middle" font-size="13" font-weight="700" fill="#1c2420">位置编码：注意力本身不知道词序，必须加进去</text>
    <rect x="80" y="55" width="200" height="70" rx="12" fill="#dce8f3" stroke="#1f4e79"/>
    <text x="180" y="96" text-anchor="middle" font-size="14" font-weight="700" fill="#1f4e79">token 嵌入</text>
    <text x="300" y="96" font-size="22" fill="#0f6e56">+</text>
    <rect x="340" y="55" width="200" height="70" rx="12" fill="#fff3d6" stroke="#8a6a20"/>
    <text x="440" y="88" text-anchor="middle" font-size="14" font-weight="700" fill="#8a6a20">正弦 PE</text>
    <text x="440" y="108" text-anchor="middle" font-size="11" fill="#5a6a62">sin / cos · 不同频率</text>
    <text x="555" y="96" font-size="22" fill="#0f6e56">=</text>
    <rect x="590" y="55" width="150" height="70" rx="12" fill="#d8efe6" stroke="#0f6e56"/>
    <text x="665" y="96" text-anchor="middle" font-size="14" font-weight="700" fill="#0f6e56">送进第 1 层</text>
    <text x="410" y="155" text-anchor="middle" font-size="12" fill="#7d8c84">相对偏移 k 时，PE(pos+k) 是 PE(pos) 的线性函数</text>
  </g>
</svg>
"""


FIGURES = {
    "qkv": ("教学示意 · 先分清 Q / K / V 三个角色", fig_qkv()),
    "cost": ("教学示意 · 稠密 / 稀疏 / 线性 三条路", fig_cost()),
    "arch": ("教学示意 · 对应原文 Figure 1", fig_arch()),
    "scaled": ("教学示意 · 对应原文 Figure 2 左、式 (1)", fig_scaled()),
    "mask": ("教学示意 · 解码器因果掩码", fig_mask()),
    "mha": ("教学示意 · 对应原文 Figure 2 右、式 (2)(3)", fig_mha()),
    "three": ("教学示意 · 对应原文 §3.2.3 三种用法", fig_three()),
    "pos": ("教学示意 · 对应原文 §3.5", fig_pos()),
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
.bridge-callout{border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:0 14px 14px 0;
background:var(--paper);padding:14px 16px;margin:0 0 18px;font-family:var(--sans);font-size:14px;color:var(--muted);line-height:1.65}
.bridge-callout strong{color:var(--ink)}
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
<title>原始 Transformer · 逐段精读（Vaswani 2017）</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Literata:opsz,wght@7..72,400;7..72,600;7..72,700&amp;family=Manrope:wght@400;500;600;700&amp;family=Noto+Sans+SC:wght@400;500;700&amp;family=Noto+Serif+SC:wght@400;600;700&amp;display=swap" rel="stylesheet"/>
{KATEX_HEAD}
<style>{CSS}</style></head>
<body class="mode-both"><div class="app">
<aside class="side">
<div class="brand">LLM Learning · Paper Reader</div>
<h1>原始 Transformer</h1>
<div class="meta">arXiv:1706.03762 · NIPS 2017<br/>Attention Is All You Need<br/>从零：QKV · 缩放点积 · 多头</div>
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
<a class="btn" href="../sparse-attention/index.html">稀疏注意力 →</a>
<a class="btn" href="../linear-attention/index.html">线性注意力 →</a>
<div class="search"><input id="q" type="search" placeholder="搜索段落 / 名词 / 引用…" /></div>
</div>
<section class="hero">
<h2>Attention Is All You Need</h2>
<p>本夹对应 <strong>arXiv:1706.03762</strong>：原始 Transformer。从零讲清 Q / K / V、缩放点积四步、多头拼接，以及 <em>O(N²)</em> 从哪来。
核心方法（§3.2）按计算步骤拆开；标了「导读」的段落是教学补充，不是论文原句。</p>
<div class="chips">
<span class="chip">核心：<em>softmax(QKᵀ/√d_k) V</em></span>
<span class="chip">多头：<em>h=8 · d_k=64</em></span>
<span class="chip">下一站：<em>稀疏注意力</em></span>
</div>
</section>
<div class="bridge-callout">
<strong>怎么读本页：</strong>先读「从零」导读（QKV 与形状），再逐段走 §3.2.1 四步和 §3.2.2 多头，不要跳。
§4 表 1 最后一行已经在谈「只看 r 个邻居」——那就是稀疏注意力的入口。
读完打开 <a href="../sparse-attention/">稀疏专题</a>。
</div>
<p class="note">英文贴近 NIPS 2017 论文；导读段为学习笔记。仓库总阅读顺序见根目录 README。</p>
<section class="section" id="formulas"><h3>公式墙（速查） <span>先记住这五式</span></h3>
<p class="inline-math-hint">段内还有逐步展开卡；核心方法请按卡片顺序读，不要只扫这一墙。</p>
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
            teach = p["en"].startswith("Teaching note")
            en_lab = "Teaching" if teach else "Original"
            zh_lab = "导读" if teach else "译文"
            parts.append(
                f'<article class="card para" data-idx="{card_i}" data-blob="{esc(blob)}">\n'
                f'<span class="pidx">§{card_i}</span>\n'
                f'<div class="summary"><b>小结</b> · {p_sum}</div>\n'
                f"{math_html}"
                f'<div class="pair lang">\n'
                f'<div class="en-block"><div class="label">{en_lab}</div><div class="en">{p_en}</div></div>\n'
                f'<div class="zh-block"><div class="label">{zh_lab}</div><div class="zh">{p_zh}</div></div>\n'
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
        lv = "must" if r["level"] == "本篇" else ("imp" if r["level"] in ("下一站", "对照") else "")
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
