"""Plotly figures that share one dark, transparent look."""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from .ui import AMBER, CORAL, MUTED, TEAL, VIOLET

FONT = dict(family="IBM Plex Sans, sans-serif", color="#C9D4E8", size=13)


def _base(fig: go.Figure, height: int = 360, legend: bool = True) -> go.Figure:
    fig.update_layout(
        height=height, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=FONT,
        margin=dict(l=10, r=10, t=40, b=10), showlegend=legend,
        legend=dict(orientation="h", y=-0.18, x=0, bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor="#0E1526", font_size=13),
    )
    fig.update_xaxes(gridcolor="rgba(143,160,191,.12)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(143,160,191,.12)", zeroline=False)
    return fig


def model_bars(val: pd.DataFrame, test: pd.DataFrame) -> go.Figure:
    order = test.sort_values("PR-AUC")["Model"].tolist()
    v = val.set_index("Model").reindex(order)["PR-AUC"]
    t = test.set_index("Model").reindex(order)["PR-AUC"]
    fig = go.Figure()
    fig.add_bar(y=order, x=v.values, name="Validation", orientation="h", marker_color=VIOLET, text=[f"{x:.3f}" for x in v], textposition="outside")
    fig.add_bar(y=order, x=t.values, name="Test", orientation="h", marker_color=TEAL, text=[f"{x:.3f}" for x in t], textposition="outside")
    fig.update_layout(barmode="group", title="PR-AUC by model (higher is better)")
    fig.update_xaxes(range=[0, 1.08])
    return _base(fig, 380)


def tuning_scatter(trials: pd.DataFrame) -> go.Figure:
    t = trials.sort_values("trial")
    best = t["val_PR_AUC"].idxmax()
    fig = go.Figure()
    fig.add_scatter(x=t["trial"], y=t["val_PR_AUC"], mode="lines+markers", line=dict(color=VIOLET, width=2),
                    marker=dict(size=11, color=[TEAL if i == best else VIOLET for i in t.index], line=dict(width=1, color="#0b1020")),
                    customdata=t[["num_leaves", "learning_rate", "scale_pos_weight", "best_iter"]],
                    hovertemplate="trial %{x}<br>val PR-AUC %{y:.4f}<br>leaves %{customdata[0]} | lr %{customdata[1]}"
                                  "<br>pos weight %{customdata[2]:.1f} | rounds %{customdata[3]}<extra></extra>")
    fig.update_layout(title="Random search: validation PR-AUC per trial (best in teal)")
    fig.update_xaxes(dtick=1, title="trial")
    fig.update_yaxes(title="val PR-AUC")
    return _base(fig, 340, legend=False)


def cost_bars(ops: pd.DataFrame, review_cost: float, no_model: float) -> go.Figure:
    rows = []
    for _, r in ops.iterrows():
        flagged = r["Caught"] + r["False alarms"]
        rows.append((r["Operating point"] + f" ({r['Threshold']:.2f})", r["Missed loss"], flagged * review_cost))
    names = ["No model"] + [r[0] for r in rows]
    missed = [no_model] + [r[1] for r in rows]
    review = [0.0] + [r[2] for r in rows]
    fig = go.Figure()
    fig.add_bar(x=names, y=missed, name="Fraud that got through", marker_color=CORAL)
    fig.add_bar(x=names, y=review, name="Analyst review cost", marker_color=AMBER)
    totals = [m + r for m, r in zip(missed, review)]
    fig.add_scatter(x=names, y=totals, mode="text", text=[f"{x:,.0f}" for x in totals], textposition="top center", showlegend=False)
    fig.update_layout(barmode="stack", title="Total cost on the test set (EUR)")
    fig.update_yaxes(range=[0, max(totals) * 1.18])
    return _base(fig, 380)


def recall_precision_k(bud: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_scatter(x=bud["K (reviewed)"], y=bud["Recall@K"], name="Recall@K", mode="lines+markers", line=dict(color=TEAL, width=3))
    fig.add_scatter(x=bud["K (reviewed)"], y=bud["Precision@K"], name="Precision@K", mode="lines+markers", line=dict(color=CORAL, width=3))
    fig.update_layout(title="If analysts review the K riskiest transactions")
    fig.update_xaxes(type="log", title="K (log scale)")
    fig.update_yaxes(range=[0, 1.05], tickformat=".0%")
    return _base(fig, 360)


def importance_bars(imp: pd.Series, title: str = "Global importance (mean |SHAP|)") -> go.Figure:
    s = imp.sort_values()
    fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h", marker=dict(color=s.values, colorscale=[[0, "#2b3a66"], [1, TEAL]]),
                           text=[f"{v:.3f}" for v in s.values], textposition="outside"))
    fig.update_layout(title=title)
    fig.update_xaxes(range=[0, float(s.max()) * 1.18])
    return _base(fig, 380, legend=False)


def waterfall(reasons: pd.DataFrame, base: float, final_logit: float) -> go.Figure:
    r = reasons.iloc[::-1]
    colors = [CORAL if v > 0 else TEAL for v in r["shap"]]
    labels = [f"{f} = {v:.2f}" for f, v in zip(r["feature"], r["value"])]
    fig = go.Figure(go.Bar(x=r["shap"], y=labels, orientation="h", marker_color=colors,
                           text=[f"{v:+.2f}" for v in r["shap"]], textposition="outside"))
    fig.add_vline(x=0, line_color="rgba(255,255,255,.35)")
    fig.update_layout(title="What moved this score (red pushes toward fraud, teal toward normal)")
    fig.update_xaxes(title="SHAP contribution (log-odds)")
    return _base(fig, 400, legend=False)


def score_hist(scores: np.ndarray, thr: float) -> go.Figure:
    fig = go.Figure(go.Histogram(x=scores, nbinsx=40, marker_color=VIOLET, opacity=.9))
    fig.add_vline(x=thr, line_color=CORAL, line_dash="dash", annotation_text=f"threshold {thr:.2f}", annotation_font_color=CORAL)
    fig.update_layout(title="Distribution of risk scores")
    fig.update_yaxes(type="log", title="transactions (log)")
    fig.update_xaxes(title="risk score", range=[0, 1])
    return _base(fig, 330, legend=False)


def split_bars(facts: dict) -> go.Figure:
    names = ["Train", "Validation", "Test"]
    tot = [facts["train"][0], facts["val"][0], facts["test"][0]]
    fr = [facts["train"][1], facts["val"][1], facts["test"][1]]
    fig = go.Figure()
    fig.add_bar(x=names, y=tot, name="Transactions", marker_color=VIOLET, text=[f"{t:,}" for t in tot], textposition="outside")
    fig.update_layout(title="Time-ordered split (oldest to newest)")
    fig.update_yaxes(range=[0, max(tot) * 1.18])
    for n, f, t in zip(names, fr, tot):
        fig.add_annotation(x=n, y=t / 2, text=f"<b>{f}</b> frauds<br>{100*f/t:.3f}%", showarrow=False, font=dict(color="#fff", size=13))
    return _base(fig, 340, legend=False)
