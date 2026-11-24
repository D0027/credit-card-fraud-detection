"""Theme, CSS and small HTML components for the Streamlit app."""
from __future__ import annotations

import html
import streamlit as st

TEAL, CORAL, AMBER, VIOLET, INK, MUTED = "#2DE2C5", "#FF5C6C", "#FFB547", "#8B7CFF", "#070B14", "#8FA0BF"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

@property --ang { syntax:'<angle>'; inherits:false; initial-value:0deg; }

:root{
  --ink:#070B14; --panel:rgba(16,24,42,.58); --panel-2:rgba(22,32,56,.72);
  --line:rgba(143,160,191,.16); --line-2:rgba(143,160,191,.30);
  --text:#E6ECF8; --muted:#8FA0BF; --teal:#2DE2C5; --coral:#FF5C6C; --amber:#FFB547; --violet:#8B7CFF;
  --head:'Sora','Segoe UI',system-ui,-apple-system,sans-serif; --body:'IBM Plex Sans','Segoe UI',system-ui,sans-serif; --mono:'IBM Plex Mono',ui-monospace,Consolas,monospace;
}
html, body, [class*="css"], .stApp { font-family:var(--body); color:var(--text); }
h1,h2,h3,h4 { font-family:var(--head) !important; letter-spacing:-.02em; color:var(--text); }
html, body { background:var(--ink); }
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stHeader"] { background:transparent !important; }
[data-testid="stHeader"] { height:2.5rem; }
.block-container { padding-top:2rem; padding-bottom:4rem; max-width:1280px; position:relative; z-index:2; }

/* ================= animated backdrop ================= */
.bg-wrap{ position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none; }
.bg-orb{ position:absolute; border-radius:50%; filter:blur(70px); will-change:transform; }
.bg-orb.a{ width:52vw; height:52vw; left:-14vw; top:-18vw; opacity:.80; background:radial-gradient(circle,#13b9a8 0%,rgba(19,185,168,0) 66%); animation:driftA 15s ease-in-out infinite alternate; }
.bg-orb.b{ width:46vw; height:46vw; right:-12vw; top:4vh; opacity:.75; background:radial-gradient(circle,#5a4bff 0%,rgba(90,75,255,0) 66%); animation:driftB 19s ease-in-out infinite alternate; }
.bg-orb.c{ width:40vw; height:40vw; left:26vw; bottom:-18vw; opacity:.60; background:radial-gradient(circle,#e0405a 0%,rgba(224,64,90,0) 66%); animation:driftC 23s ease-in-out infinite alternate; }
.bg-orb.d{ width:26vw; height:26vw; left:48vw; top:20vh; opacity:.45; background:radial-gradient(circle,#ffb547 0%,rgba(255,181,71,0) 66%); animation:driftD 17s ease-in-out infinite alternate; }
.bg-grid{ position:absolute; inset:0; background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px); background-size:56px 56px; opacity:.30;
  -webkit-mask-image:radial-gradient(ellipse at 50% 30%,#000 0%,transparent 75%); mask-image:radial-gradient(ellipse at 50% 30%,#000 0%,transparent 75%); animation:gridpan 40s linear infinite; }
.bg-dots{ position:absolute; left:0; right:0; top:-160px; bottom:0; background-image:radial-gradient(circle,rgba(45,226,197,.85) 1.2px,transparent 1.8px); background-size:120px 160px; opacity:.38; animation:dotsrise 16s linear infinite;
  -webkit-mask-image:linear-gradient(to top,#000 0%,transparent 85%); mask-image:linear-gradient(to top,#000 0%,transparent 85%); }
.bg-dots.two{ background-image:radial-gradient(circle,rgba(139,124,255,.9) 1px,transparent 1.6px); background-size:190px 230px; background-position:60px 40px; opacity:.32; animation-duration:26s; }
.bg-scan{ position:absolute; left:0; right:0; height:2px; top:-4px; background:linear-gradient(90deg,transparent,rgba(45,226,197,.85),transparent); box-shadow:0 0 28px 6px rgba(45,226,197,.25); animation:scandown 11s ease-in-out infinite; opacity:.55; }
@keyframes driftA{ 0%{transform:translate(0,0) scale(1);} 100%{transform:translate(22vw,16vh) scale(1.25);} }
@keyframes driftB{ 0%{transform:translate(0,0) scale(1);} 100%{transform:translate(-20vw,22vh) scale(.85);} }
@keyframes driftC{ 0%{transform:translate(0,0) scale(1);} 100%{transform:translate(-26vw,-16vh) scale(1.25);} }
@keyframes driftD{ 0%{transform:translate(0,0) scale(.9);} 100%{transform:translate(-16vw,24vh) scale(1.3);} }
@keyframes gridpan{ to{ background-position:56px 56px; } }
@keyframes dotsrise{ to{ transform:translateY(-160px); } }
@keyframes scandown{ 0%{top:-4px;opacity:0;} 8%{opacity:.6;} 92%{opacity:.6;} 100%{top:100vh;opacity:0;} }

/* ================= entrance + hover motion ================= */
@keyframes rise{ from{ opacity:0; transform:translateY(22px) scale(.985); } to{ opacity:1; transform:none; } }
@keyframes grow{ from{ transform:scaleX(0);} to{ transform:scaleX(1);} }
@keyframes spin{ to{ transform:rotate(360deg);} }
@keyframes breathe{ 0%,100%{ box-shadow:0 0 14px rgba(45,226,197,.18);} 50%{ box-shadow:0 0 30px rgba(45,226,197,.50);} }
@keyframes ping{ 0%{ box-shadow:0 0 0 0 rgba(45,226,197,.65);} 80%,100%{ box-shadow:0 0 0 9px rgba(45,226,197,0);} }
@keyframes sheen{ 0%{ transform:translateX(-130%) skewX(-18deg);} 55%,100%{ transform:translateX(330%) skewX(-18deg);} }
@keyframes beam{ 0%{ left:-12%; opacity:0;} 10%{opacity:1;} 90%{opacity:1;} 100%{ left:108%; opacity:0;} }
@keyframes floaty{ 0%,100%{ transform:translate(0,0);} 50%{ transform:translate(-26px,22px);} }
@keyframes valueglow{ 0%{ background-position:200% 0;} 100%{ background-position:-100% 0;} }
@keyframes tick{ to{ transform:translateX(-50%);} }
@keyframes alarm{ 0%,100%{ filter:drop-shadow(0 0 6px rgba(255,92,108,.35)); } 50%{ filter:drop-shadow(0 0 26px rgba(255,92,108,.85)); } }
@keyframes blink{ 0%,100%{ opacity:1;} 50%{ opacity:.55;} }
@keyframes ringdraw{ from{ stroke-dashoffset:var(--circ); } }

.hero, .kpi, .step, .glass, .callout, [data-testid="stPlotlyChart"], [data-testid="stImage"], [data-testid="stDataFrame"], .ticker{ animation:rise .75s cubic-bezier(.2,.8,.2,1) both; }
[data-testid="stColumn"]:nth-child(2) .kpi, [data-testid="stColumn"]:nth-child(2) .step{ animation-delay:.08s; }
[data-testid="stColumn"]:nth-child(3) .kpi, [data-testid="stColumn"]:nth-child(3) .step{ animation-delay:.16s; }
[data-testid="stColumn"]:nth-child(4) .kpi, [data-testid="stColumn"]:nth-child(4) .step{ animation-delay:.24s; }
[data-testid="stColumn"]:nth-child(5) .kpi, [data-testid="stColumn"]:nth-child(5) .step{ animation-delay:.32s; }
.kpi, .step, .glass{ transition:transform .25s ease, border-color .25s ease, box-shadow .25s ease; }
.kpi:hover, .step:hover, .glass:hover{ transform:translateY(-5px); border-color:rgba(45,226,197,.45); box-shadow:0 18px 44px rgba(0,0,0,.35), 0 0 0 1px rgba(45,226,197,.10), 0 0 34px rgba(45,226,197,.12); }

/* ================= sidebar ================= */
[data-testid="stSidebar"]{ background:linear-gradient(180deg,rgba(10,16,30,.90),rgba(8,12,24,.95)); border-right:1px solid var(--line); backdrop-filter:blur(14px); }
[data-testid="stSidebar"] > div:first-child{ padding-top:1rem; }
.brand{ display:flex; align-items:center; gap:.7rem; padding:.2rem .4rem 1.1rem; }
.brand-mark{ width:38px; height:38px; border-radius:11px; display:grid; place-items:center; font-size:1.2rem;
  background:linear-gradient(135deg,rgba(45,226,197,.25),rgba(139,124,255,.25)); border:1px solid var(--line-2); animation:breathe 3.2s ease-in-out infinite; }
.brand-name{ font-family:var(--head); font-weight:700; font-size:1.02rem; line-height:1.1; }
.brand-sub{ color:var(--muted); font-size:.74rem; }
[data-testid="stSidebar"] [role="radiogroup"]{ gap:.25rem; }
[data-testid="stSidebar"] [role="radiogroup"] label{ padding:.55rem .75rem; border-radius:12px; border:1px solid transparent; transition:all .2s ease; width:100%; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover{ background:rgba(143,160,191,.10); transform:translateX(4px); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){ background:linear-gradient(90deg,rgba(45,226,197,.20),rgba(45,226,197,.03)); border-color:rgba(45,226,197,.45); animation:breathe 3.6s ease-in-out infinite; }
[data-testid="stSidebar"] [role="radiogroup"] p{ font-weight:500; font-size:.95rem; }

/* ================= cards ================= */
.glass{ background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:1.25rem 1.4rem;
  backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); box-shadow:0 18px 50px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04); }
.glass.tight{ padding:1rem 1.15rem; }
.kpi{ background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:1.05rem 1.2rem; backdrop-filter:blur(14px); position:relative; overflow:hidden; min-height:128px; height:100%; }
.kpi::before{ content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--accent,var(--teal)); box-shadow:0 0 14px var(--accent,var(--teal)); }
.kpi::after{ content:""; position:absolute; top:0; bottom:0; width:38%; left:0; background:linear-gradient(100deg,transparent,rgba(255,255,255,.07),transparent); animation:sheen 7s ease-in-out infinite; pointer-events:none; }
.kpi-label{ color:var(--muted); font-size:.82rem; margin-bottom:.35rem; }
.kpi-value{ font-family:var(--mono); font-weight:600; font-size:1.95rem; letter-spacing:-.03em; line-height:1.1;
  background:linear-gradient(100deg,var(--text) 0%,var(--text) 40%,var(--accent,#2DE2C5) 50%,var(--text) 60%,var(--text) 100%); background-size:300% 100%;
  -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent; animation:valueglow 3.2s ease-out .4s 1 both; }
.kpi-sub{ color:var(--muted); font-size:.78rem; margin-top:.4rem; }

/* ================= hero ================= */
.hero{ padding:2.4rem 2.2rem 2.1rem; border-radius:26px; position:relative; overflow:hidden;
  background:linear-gradient(135deg,rgba(16,26,48,.80),rgba(12,18,34,.66)); backdrop-filter:blur(18px); border:1px solid transparent; }
.hero::before{ content:""; position:absolute; inset:0; border-radius:inherit; padding:1.5px; pointer-events:none;
  background:conic-gradient(from var(--ang),rgba(45,226,197,.9),rgba(139,124,255,.15) 25%,rgba(255,92,108,.8) 50%,rgba(139,124,255,.15) 75%,rgba(45,226,197,.9));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0); -webkit-mask-composite:xor; mask:linear-gradient(#000 0 0) content-box exclude,linear-gradient(#000 0 0);
  animation:borderspin 6s linear infinite; }
@keyframes borderspin{ to{ --ang:360deg; } }
.hero::after{ content:""; position:absolute; right:-80px; top:-80px; width:340px; height:340px; border-radius:50%;
  background:radial-gradient(circle,rgba(45,226,197,.30),transparent 65%); animation:floaty 9s ease-in-out infinite; pointer-events:none; }
.hero-beam{ position:absolute; top:0; bottom:0; width:2px; left:-12%; background:linear-gradient(180deg,transparent,rgba(45,226,197,.95),transparent); box-shadow:0 0 30px 8px rgba(45,226,197,.22); animation:beam 7s ease-in-out infinite; pointer-events:none; }
.hero h1{ font-size:2.75rem; line-height:1.06; font-weight:800; margin:0 0 .8rem; max-width:20ch; position:relative; }
.hero p{ color:#b7c4dc; font-size:1.06rem; max-width:62ch; line-height:1.6; margin:0 0 1.2rem; position:relative; }
.hero .chip{ position:relative; }
.chip{ display:inline-flex; align-items:center; gap:.45rem; padding:.34rem .8rem; border-radius:999px; border:1px solid var(--line-2);
  background:rgba(143,160,191,.08); color:#cfd9ec; font-size:.82rem; margin:0 .45rem .45rem 0; }
.chip.teal{ border-color:rgba(45,226,197,.45); color:var(--teal); background:rgba(45,226,197,.08); }
.chip.coral{ border-color:rgba(255,92,108,.45); color:var(--coral); background:rgba(255,92,108,.08); }
.chip.amber{ border-color:rgba(255,181,71,.45); color:var(--amber); background:rgba(255,181,71,.08); }
.dot{ width:8px; height:8px; border-radius:50%; background:currentColor; display:inline-block; animation:ping 1.8s ease-out infinite; }
.chip.coral .dot{ animation-name:ping-red; } .chip.amber .dot{ animation-name:ping-amber; }
@keyframes ping-red{ 0%{ box-shadow:0 0 0 0 rgba(255,92,108,.7);} 80%,100%{ box-shadow:0 0 0 9px rgba(255,92,108,0);} }
@keyframes ping-amber{ 0%{ box-shadow:0 0 0 0 rgba(255,181,71,.7);} 80%,100%{ box-shadow:0 0 0 9px rgba(255,181,71,0);} }

.section-title{ font-family:var(--head); font-weight:700; font-size:1.45rem; margin:2.1rem 0 .25rem; position:relative; padding-left:.9rem; }
.section-title::before{ content:""; position:absolute; left:0; top:.2em; bottom:.2em; width:4px; border-radius:4px; background:linear-gradient(180deg,var(--teal),var(--violet)); transform-origin:top; animation:grow 1s cubic-bezier(.2,.8,.2,1) both; }
.section-sub{ color:var(--muted); margin:0 0 1rem; max-width:75ch; line-height:1.55; }
.page-title{ font-family:var(--head); font-weight:800; font-size:2.1rem; margin:.1rem 0 .2rem; }
.page-title::after{ content:""; display:block; height:3px; width:72px; margin-top:.55rem; border-radius:3px; background:linear-gradient(90deg,var(--teal),var(--violet),var(--coral)); transform-origin:left; animation:grow 1.1s .15s cubic-bezier(.2,.8,.2,1) both; }

/* ================= ticker ================= */
.ticker{ display:flex; align-items:center; gap:1rem; margin:1rem 0 .2rem; padding:.55rem .9rem; border-radius:16px; border:1px solid var(--line); background:var(--panel); backdrop-filter:blur(12px); overflow:hidden; }
.ticker-label{ flex:none; color:var(--muted); font-size:.78rem; padding-right:1rem; border-right:1px solid var(--line-2); line-height:1.25; }
.ticker-mask{ flex:1; overflow:hidden; -webkit-mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent); mask-image:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent); }
.ticker-track{ display:inline-flex; gap:2.2rem; white-space:nowrap; animation:tick 38s linear infinite; }
.ticker:hover .ticker-track{ animation-play-state:paused; }
.tk{ font-family:var(--mono); font-size:.84rem; display:inline-flex; align-items:center; gap:.5rem; color:#cfd9ec; }
.tk i{ width:7px; height:7px; border-radius:50%; background:var(--teal); box-shadow:0 0 10px var(--teal); }
.tk.bad{ color:#ffb0b8; } .tk.bad i{ background:var(--coral); box-shadow:0 0 10px var(--coral); animation:blink 1.1s ease-in-out infinite; }
.tk.mid{ color:#ffd9a0; } .tk.mid i{ background:var(--amber); box-shadow:0 0 10px var(--amber); }

/* ================= pipeline ================= */
.step{ position:relative; background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:1rem 1.05rem 1.05rem; height:100%; }
.step-n{ width:28px; height:28px; border-radius:9px; display:grid; place-items:center; font-family:var(--mono); font-weight:600; font-size:.85rem;
  background:rgba(45,226,197,.14); color:var(--teal); border:1px solid rgba(45,226,197,.4); margin-bottom:.6rem; }
.step h4{ font-size:1rem; margin:0 0 .3rem; }
.step p{ color:var(--muted); font-size:.86rem; margin:0; line-height:1.5; }

/* ================= risk ring ================= */
.ring-wrap{ display:flex; flex-direction:column; align-items:center; padding:.4rem 0 .2rem; }
.ring{ position:relative; width:250px; height:250px; }
.ring.high{ animation:alarm 1.5s ease-in-out infinite; }
.ring svg{ transform:rotate(-90deg); overflow:visible; }
.ring-bg{ stroke:rgba(143,160,191,.16); }
.ring-arc{ animation:ringdraw 1.6s cubic-bezier(.2,.8,.2,1) both; filter:drop-shadow(0 0 10px var(--glow)); }
.ring-orbit{ transform-origin:125px 125px; animation:spin 22s linear infinite; }
.ring-orbit.rev{ animation-duration:34s; animation-direction:reverse; }
.ring-center{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.ring-score{ font-family:var(--mono); font-weight:600; font-size:3.1rem; letter-spacing:-.04em; line-height:1; }
.ring-label{ color:var(--muted); font-size:.85rem; margin-top:.3rem; }
.verdict{ margin-top:.7rem; padding:.55rem 1.1rem; border-radius:14px; font-family:var(--head); font-weight:700; font-size:1.02rem; border:1px solid; }
.verdict.low{ color:var(--teal); border-color:rgba(45,226,197,.5); background:rgba(45,226,197,.1); }
.verdict.elevated{ color:var(--amber); border-color:rgba(255,181,71,.5); background:rgba(255,181,71,.1); }
.verdict.high{ color:var(--coral); border-color:rgba(255,92,108,.55); background:rgba(255,92,108,.12); animation:blink 1.3s ease-in-out infinite; }

.callout{ border-radius:16px; padding:.95rem 1.1rem; border:1px solid var(--line-2); background:rgba(143,160,191,.06); color:#c5d0e4; line-height:1.55; font-size:.93rem; }
.callout b{ color:var(--text); }
.callout.warn{ border-color:rgba(255,181,71,.4); background:rgba(255,181,71,.07); }
.callout.good{ border-color:rgba(45,226,197,.4); background:rgba(45,226,197,.06); }
.callout.bad{ border-color:rgba(255,92,108,.45); background:rgba(255,92,108,.07); }
.reason{ display:flex; justify-content:space-between; gap:1rem; padding:.55rem 0; border-bottom:1px solid var(--line); font-size:.92rem; }
.reason:last-child{ border-bottom:none; }
.reason .f{ font-family:var(--mono); font-weight:600; }
.reason .up{ color:var(--coral); } .reason .down{ color:var(--teal); }
.reason .d{ color:var(--muted); }

/* ================= widgets ================= */
.stButton > button, .stDownloadButton > button{ position:relative; overflow:hidden; border-radius:12px; border:1px solid rgba(45,226,197,.5); background:linear-gradient(135deg,rgba(45,226,197,.22),rgba(139,124,255,.18));
  color:var(--text); font-weight:600; padding:.55rem 1.1rem; transition:transform .15s ease, box-shadow .15s ease; }
.stButton > button::after, .stDownloadButton > button::after{ content:""; position:absolute; top:0; bottom:0; width:40%; left:0; background:linear-gradient(100deg,transparent,rgba(255,255,255,.22),transparent); transform:translateX(-130%) skewX(-18deg); pointer-events:none; }
.stButton > button:hover, .stDownloadButton > button:hover{ transform:translateY(-2px); box-shadow:0 10px 28px rgba(45,226,197,.30); border-color:var(--teal); color:#fff; }
.stButton > button:hover::after, .stDownloadButton > button:hover::after{ animation:sheen 1s ease; }
.stButton > button:active{ transform:translateY(0) scale(.98); }
.stButton > button[kind="primary"]{ background:linear-gradient(135deg,#2DE2C5,#22b8d6); color:#04121a; border:none; }
[data-baseweb="input"], [data-baseweb="select"] > div, .stNumberInput input, .stTextInput input{ background:rgba(10,16,30,.7) !important; border-radius:11px !important; }
[data-testid="stTabs"] [role="tablist"]{ gap:.3rem; border-bottom:1px solid var(--line); }
[data-testid="stTabs"] button[role="tab"]{ border-radius:10px 10px 0 0; padding:.55rem 1rem; transition:background .2s ease; }
[data-testid="stTabs"] button[role="tab"]:hover{ background:rgba(45,226,197,.08); }
[data-testid="stExpander"]{ border:1px solid var(--line) !important; border-radius:16px !important; background:var(--panel); }
[data-testid="stFileUploaderDropzone"]{ border:1.5px dashed var(--line-2); border-radius:18px; background:rgba(10,16,30,.5); transition:all .25s ease; }
[data-testid="stFileUploaderDropzone"]:hover{ border-color:var(--teal); background:rgba(45,226,197,.06); box-shadow:0 0 30px rgba(45,226,197,.12); }
[data-testid="stDataFrame"]{ border:1px solid var(--line); border-radius:14px; overflow:hidden; }
[data-testid="stImage"] img{ border-radius:14px; border:1px solid var(--line); transition:transform .3s ease, box-shadow .3s ease; }
[data-testid="stImage"] img:hover{ transform:scale(1.015); box-shadow:0 16px 40px rgba(0,0,0,.4); }
hr{ border-color:var(--line) !important; }
footer{ visibility:hidden; }
.foot{ color:var(--muted); font-size:.8rem; text-align:center; margin-top:3rem; }

@media (max-width:760px){ .hero h1{ font-size:2rem; } .hero{ padding:1.5rem 1.2rem; } .ring{ width:210px; height:210px; } .ring-score{ font-size:2.5rem; } .ticker-label{ display:none; } }
@media (prefers-reduced-motion:reduce){ *, *::before, *::after{ animation:none !important; transition:none !important; } .kpi-value{ -webkit-text-fill-color:currentColor; color:var(--text); background:none; } }
</style>
"""

BACKDROP = '<div class="bg-wrap"><div class="bg-grid"></div><div class="bg-orb a"></div><div class="bg-orb b"></div><div class="bg-orb c"></div><div class="bg-orb d"></div><div class="bg-dots"></div><div class="bg-dots two"></div><div class="bg-scan"></div></div>'


def inject_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(BACKDROP, unsafe_allow_html=True)


def brand() -> None:
    st.markdown(
        '<div class="brand"><div class="brand-mark">🛡️</div><div><div class="brand-name">FraudSense</div>'
        '<div class="brand-sub">Card fraud risk console</div></div></div>', unsafe_allow_html=True)


def page_header(title: str, sub: str = "") -> None:
    st.markdown(f'<div class="page-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<p class="section-sub">{html.escape(sub)}</p>', unsafe_allow_html=True)


def section(title: str, sub: str = "") -> None:
    st.markdown(f'<div class="section-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<p class="section-sub">{html.escape(sub)}</p>', unsafe_allow_html=True)


def kpi(label: str, value: str, sub: str = "", accent: str = TEAL) -> str:
    return (f'<div class="kpi" style="--accent:{accent}"><div class="kpi-label">{html.escape(label)}</div>'
            f'<div class="kpi-value">{html.escape(value)}</div><div class="kpi-sub">{html.escape(sub)}</div></div>')


def callout(text_html: str, kind: str = "") -> None:
    st.markdown(f'<div class="callout {kind}">{text_html}</div>', unsafe_allow_html=True)


def risk_ring(score: float, band: str) -> str:
    color = {"low": TEAL, "elevated": AMBER, "high": CORAL}[band]
    r = 104
    c = 2 * 3.14159265 * r
    off = c * (1 - max(0.0, min(1.0, score)))
    label = {"low": "Looks normal", "elevated": "Needs a review", "high": "Likely fraud"}[band]
    return f"""
    <div class="ring-wrap"><div class="ring {band}" style="--glow:{color}66">
      <svg width="250" height="250" viewBox="0 0 250 250">
        <circle class="ring-orbit" cx="125" cy="125" r="121" fill="none" stroke="{color}" stroke-opacity=".45" stroke-width="1.5" stroke-dasharray="2 9" stroke-linecap="round"/>
        <circle class="ring-orbit rev" cx="125" cy="125" r="90" fill="none" stroke="{color}" stroke-opacity=".28" stroke-width="1" stroke-dasharray="40 14"/>
        <circle class="ring-bg" cx="125" cy="125" r="{r}" fill="none" stroke-width="16"/>
        <circle class="ring-arc" cx="125" cy="125" r="{r}" fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round"
                stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}" style="--circ:{c:.1f}"/>
      </svg>
      <div class="ring-center"><div class="ring-score" style="color:{color}">{score:.3f}</div><div class="ring-label">risk score</div></div>
    </div><div class="verdict {band}">{label}</div></div>"""


def live_chip(text: str, kind: str = "teal") -> str:
    return f'<span class="chip {kind}"><span class="dot"></span>{html.escape(text)}</span>'


def ticker() -> str:
    items = [("ok", "€45.20", "cleared", "0.01"), ("ok", "€12.99", "cleared", "0.02"), ("bad", "€3.50", "flagged", "0.93"),
             ("ok", "€210.00", "cleared", "0.03"), ("mid", "€1,250.00", "review", "0.71"), ("ok", "€8.75", "cleared", "0.01"),
             ("ok", "€67.40", "cleared", "0.04"), ("bad", "€1.00", "flagged", "0.88"), ("ok", "€320.10", "cleared", "0.02"),
             ("ok", "€29.90", "cleared", "0.01")]
    one = "".join(f'<span class="tk {k}"><i></i>{a} {b} · score {s}</span>' for k, a, b, s in items)
    return (f'<div class="ticker"><div class="ticker-label">Simulated feed<br/>not real data</div>'
            f'<div class="ticker-mask"><div class="ticker-track">{one}{one}</div></div></div>')
