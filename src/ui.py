"""Theme, CSS and small HTML components for the Streamlit app."""
from __future__ import annotations

import html
import streamlit as st

TEAL, CORAL, AMBER, VIOLET, INK, MUTED = "#2DE2C5", "#FF5C6C", "#FFB547", "#8B7CFF", "#070B14", "#8FA0BF"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
  --ink:#070B14; --panel:rgba(16,24,42,.58); --panel-2:rgba(22,32,56,.72);
  --line:rgba(143,160,191,.16); --line-2:rgba(143,160,191,.30);
  --text:#E6ECF8; --muted:#8FA0BF; --teal:#2DE2C5; --coral:#FF5C6C; --amber:#FFB547; --violet:#8B7CFF;
}
html, body, [class*="css"], .stApp { font-family:'IBM Plex Sans',system-ui,sans-serif; color:var(--text); }
h1,h2,h3,h4 { font-family:'Sora',sans-serif !important; letter-spacing:-.02em; color:var(--text); }
.stApp { background: var(--ink); }
[data-testid="stAppViewContainer"], [data-testid="stHeader"] { background:transparent !important; }
[data-testid="stHeader"] { height:2.5rem; }
.block-container { padding-top:2rem; padding-bottom:4rem; max-width:1280px; position:relative; z-index:2; }

/* ---------- animated backdrop ---------- */
.bg-wrap{ position:fixed; inset:0; z-index:0; overflow:hidden; pointer-events:none; }
.bg-orb{ position:absolute; border-radius:50%; filter:blur(90px); opacity:.42; will-change:transform; }
.bg-orb.a{ width:46vw; height:46vw; left:-12vw; top:-14vw; background:radial-gradient(circle,#0f8f84 0%,transparent 68%); animation:driftA 26s ease-in-out infinite alternate; }
.bg-orb.b{ width:40vw; height:40vw; right:-10vw; top:8vh; background:radial-gradient(circle,#4b3fd1 0%,transparent 68%); animation:driftB 32s ease-in-out infinite alternate; }
.bg-orb.c{ width:34vw; height:34vw; left:30vw; bottom:-16vw; background:radial-gradient(circle,#b8344b 0%,transparent 68%); opacity:.30; animation:driftC 38s ease-in-out infinite alternate; }
.bg-grid{ position:absolute; inset:0; background-image:linear-gradient(var(--line) 1px,transparent 1px),linear-gradient(90deg,var(--line) 1px,transparent 1px); background-size:56px 56px; opacity:.22;
  -webkit-mask-image:radial-gradient(ellipse at 50% 30%,#000 0%,transparent 72%); mask-image:radial-gradient(ellipse at 50% 30%,#000 0%,transparent 72%); }
@keyframes driftA{ to{ transform:translate(14vw,10vh) scale(1.15);} }
@keyframes driftB{ to{ transform:translate(-12vw,16vh) scale(.9);} }
@keyframes driftC{ to{ transform:translate(-18vw,-10vh) scale(1.2);} }
@media (prefers-reduced-motion:reduce){ .bg-orb{ animation:none !important; } .ring-arc{ transition:none !important; } }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{ background:linear-gradient(180deg,rgba(10,16,30,.92),rgba(8,12,24,.96)); border-right:1px solid var(--line); }
[data-testid="stSidebar"] > div:first-child{ padding-top:1rem; }
.brand{ display:flex; align-items:center; gap:.7rem; padding:.2rem .4rem 1.1rem; }
.brand-mark{ width:38px; height:38px; border-radius:11px; display:grid; place-items:center; font-size:1.2rem;
  background:linear-gradient(135deg,rgba(45,226,197,.25),rgba(139,124,255,.25)); border:1px solid var(--line-2); box-shadow:0 0 22px rgba(45,226,197,.18); }
.brand-name{ font-family:'Sora'; font-weight:700; font-size:1.02rem; line-height:1.1; }
.brand-sub{ color:var(--muted); font-size:.74rem; }
[data-testid="stSidebar"] [role="radiogroup"]{ gap:.25rem; }
[data-testid="stSidebar"] [role="radiogroup"] label{ padding:.55rem .75rem; border-radius:12px; border:1px solid transparent; transition:all .18s ease; width:100%; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover{ background:rgba(143,160,191,.08); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){ background:linear-gradient(90deg,rgba(45,226,197,.16),rgba(45,226,197,.03)); border-color:rgba(45,226,197,.38); }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child{ display:none; }
[data-testid="stSidebar"] [role="radiogroup"] p{ font-weight:500; font-size:.95rem; }

/* ---------- glass cards ---------- */
.glass{ background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:1.25rem 1.4rem;
  backdrop-filter:blur(16px); -webkit-backdrop-filter:blur(16px); box-shadow:0 18px 50px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04); }
.glass.tight{ padding:1rem 1.15rem; }
.kpi{ background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:1.05rem 1.2rem; backdrop-filter:blur(14px); position:relative; overflow:hidden; height:100%; }
.kpi::before{ content:""; position:absolute; left:0; top:0; bottom:0; width:3px; background:var(--accent,var(--teal)); }
.kpi-label{ color:var(--muted); font-size:.82rem; margin-bottom:.35rem; }
.kpi-value{ font-family:'IBM Plex Mono',monospace; font-weight:600; font-size:1.95rem; letter-spacing:-.03em; line-height:1.1; }
.kpi-sub{ color:var(--muted); font-size:.78rem; margin-top:.4rem; }

/* ---------- hero ---------- */
.hero{ padding:2.4rem 2.2rem 2.1rem; border-radius:26px; border:1px solid var(--line-2); position:relative; overflow:hidden;
  background:linear-gradient(135deg,rgba(16,26,48,.78),rgba(12,18,34,.62)); backdrop-filter:blur(18px); }
.hero::after{ content:""; position:absolute; right:-80px; top:-80px; width:340px; height:340px; border-radius:50%;
  background:radial-gradient(circle,rgba(45,226,197,.22),transparent 65%); }
.hero h1{ font-size:2.75rem; line-height:1.06; font-weight:800; margin:0 0 .8rem; max-width:20ch; }
.hero p{ color:#b7c4dc; font-size:1.06rem; max-width:62ch; line-height:1.6; margin:0 0 1.2rem; }
.chip{ display:inline-flex; align-items:center; gap:.4rem; padding:.34rem .8rem; border-radius:999px; border:1px solid var(--line-2);
  background:rgba(143,160,191,.08); color:#cfd9ec; font-size:.82rem; margin:0 .45rem .45rem 0; }
.chip.teal{ border-color:rgba(45,226,197,.45); color:var(--teal); background:rgba(45,226,197,.08); }
.chip.coral{ border-color:rgba(255,92,108,.45); color:var(--coral); background:rgba(255,92,108,.08); }
.chip.amber{ border-color:rgba(255,181,71,.45); color:var(--amber); background:rgba(255,181,71,.08); }

.section-title{ font-family:'Sora'; font-weight:700; font-size:1.45rem; margin:2.1rem 0 .25rem; }
.section-sub{ color:var(--muted); margin:0 0 1rem; max-width:75ch; line-height:1.55; }
.page-title{ font-family:'Sora'; font-weight:800; font-size:2.1rem; margin:.1rem 0 .2rem; }

/* ---------- pipeline (a real sequence) ---------- */
.step{ position:relative; background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:1rem 1.05rem 1.05rem; height:100%; }
.step-n{ width:28px; height:28px; border-radius:9px; display:grid; place-items:center; font-family:'IBM Plex Mono'; font-weight:600; font-size:.85rem;
  background:rgba(45,226,197,.14); color:var(--teal); border:1px solid rgba(45,226,197,.4); margin-bottom:.6rem; }
.step h4{ font-size:1rem; margin:0 0 .3rem; }
.step p{ color:var(--muted); font-size:.86rem; margin:0; line-height:1.5; }

/* ---------- risk ring ---------- */
.ring-wrap{ display:flex; flex-direction:column; align-items:center; padding:.4rem 0 .2rem; }
.ring{ position:relative; width:250px; height:250px; }
.ring svg{ transform:rotate(-90deg); }
.ring-bg{ stroke:rgba(143,160,191,.16); }
.ring-arc{ transition:stroke-dashoffset 1.1s cubic-bezier(.2,.8,.2,1); filter:drop-shadow(0 0 10px var(--glow)); }
.ring-center{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; }
.ring-score{ font-family:'IBM Plex Mono'; font-weight:600; font-size:3.1rem; letter-spacing:-.04em; line-height:1; }
.ring-label{ color:var(--muted); font-size:.85rem; margin-top:.3rem; }
.verdict{ margin-top:.7rem; padding:.55rem 1.1rem; border-radius:14px; font-family:'Sora'; font-weight:700; font-size:1.02rem; border:1px solid; }
.verdict.low{ color:var(--teal); border-color:rgba(45,226,197,.5); background:rgba(45,226,197,.1); }
.verdict.elevated{ color:var(--amber); border-color:rgba(255,181,71,.5); background:rgba(255,181,71,.1); }
.verdict.high{ color:var(--coral); border-color:rgba(255,92,108,.55); background:rgba(255,92,108,.12); }

.callout{ border-radius:16px; padding:.95rem 1.1rem; border:1px solid var(--line-2); background:rgba(143,160,191,.06); color:#c5d0e4; line-height:1.55; font-size:.93rem; }
.callout b{ color:var(--text); }
.callout.warn{ border-color:rgba(255,181,71,.4); background:rgba(255,181,71,.07); }
.callout.good{ border-color:rgba(45,226,197,.4); background:rgba(45,226,197,.06); }
.callout.bad{ border-color:rgba(255,92,108,.45); background:rgba(255,92,108,.07); }
.reason{ display:flex; justify-content:space-between; gap:1rem; padding:.55rem 0; border-bottom:1px solid var(--line); font-size:.92rem; }
.reason:last-child{ border-bottom:none; }
.reason .f{ font-family:'IBM Plex Mono'; font-weight:600; }
.reason .up{ color:var(--coral); } .reason .down{ color:var(--teal); }
.reason .d{ color:var(--muted); }

/* ---------- widgets ---------- */
.stButton > button, .stDownloadButton > button{ border-radius:12px; border:1px solid rgba(45,226,197,.5); background:linear-gradient(135deg,rgba(45,226,197,.22),rgba(139,124,255,.18));
  color:var(--text); font-weight:600; padding:.55rem 1.1rem; transition:transform .15s ease, box-shadow .15s ease; }
.stButton > button:hover, .stDownloadButton > button:hover{ transform:translateY(-1px); box-shadow:0 8px 26px rgba(45,226,197,.22); border-color:var(--teal); color:#fff; }
.stButton > button[kind="primary"]{ background:linear-gradient(135deg,#2DE2C5,#22b8d6); color:#04121a; border:none; }
[data-baseweb="input"], [data-baseweb="select"] > div, .stNumberInput input, .stTextInput input{ background:rgba(10,16,30,.7) !important; border-radius:11px !important; }
[data-testid="stTabs"] [role="tablist"]{ gap:.3rem; border-bottom:1px solid var(--line); }
[data-testid="stTabs"] button[role="tab"]{ border-radius:10px 10px 0 0; padding:.55rem 1rem; }
[data-testid="stExpander"]{ border:1px solid var(--line) !important; border-radius:16px !important; background:var(--panel); }
[data-testid="stFileUploaderDropzone"]{ border:1.5px dashed var(--line-2); border-radius:18px; background:rgba(10,16,30,.5); }
[data-testid="stDataFrame"]{ border:1px solid var(--line); border-radius:14px; overflow:hidden; }
[data-testid="stImage"] img{ border-radius:14px; border:1px solid var(--line); }
hr{ border-color:var(--line) !important; }
footer{ visibility:hidden; }
.foot{ color:var(--muted); font-size:.8rem; text-align:center; margin-top:3rem; }

@media (max-width:760px){ .hero h1{ font-size:2rem; } .hero{ padding:1.5rem 1.2rem; } .ring{ width:210px; height:210px; } .ring-score{ font-size:2.5rem; } }
</style>
"""

BACKDROP = '<div class="bg-wrap"><div class="bg-grid"></div><div class="bg-orb a"></div><div class="bg-orb b"></div><div class="bg-orb c"></div></div>'


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
    r, c = 104, 2 * 3.14159265 * 104
    off = c * (1 - max(0.0, min(1.0, score)))
    label = {"low": "Looks normal", "elevated": "Needs a review", "high": "Likely fraud"}[band]
    return f"""
    <div class="ring-wrap"><div class="ring" style="--glow:{color}55">
      <svg width="250" height="250" viewBox="0 0 250 250">
        <circle class="ring-bg" cx="125" cy="125" r="{r}" fill="none" stroke-width="16"/>
        <circle class="ring-arc" cx="125" cy="125" r="{r}" fill="none" stroke="{color}" stroke-width="16" stroke-linecap="round"
                stroke-dasharray="{c:.1f}" stroke-dashoffset="{off:.1f}"/>
      </svg>
      <div class="ring-center"><div class="ring-score" style="color:{color}">{score:.3f}</div><div class="ring-label">risk score</div></div>
    </div><div class="verdict {band}">{label}</div></div>"""
