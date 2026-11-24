"""FraudSense - credit card fraud risk console (Streamlit)."""
from __future__ import annotations

import io

import numpy as np
import pandas as pd
import streamlit as st

from src import charts, inference as inf, ui
from src.config import (DEMO_CSV, FACTS, FEATURES, FRAUD_PROFILE, IMAGES, KEY_SIGNALS, RAW_COLS,
                        REPORTS, V_COLS)

st.set_page_config(page_title="FraudSense | Card Fraud Detection", page_icon="🛡️", layout="wide",
                   initial_sidebar_state="expanded")
ui.inject_theme()


# ----------------------------------------------------------------------------- data
@st.cache_resource(show_spinner=False)
def get_bundle() -> inf.Bundle:
    return inf.load_bundle()


@st.cache_data(show_spinner=False)
def report(name: str) -> pd.DataFrame:
    return pd.read_csv(REPORTS / name)


def image(name: str, caption: str = "") -> None:
    p = IMAGES / name
    if p.exists():
        st.image(str(p), caption=caption or None, width="stretch")


bundle = get_bundle()
FRIENDLY = {"log_amount": "Amount (log)", "hour_sin": "Time of day (sin)", "hour_cos": "Time of day (cos)"}
PAGES = ["🏠  Overview", "🔎  Risk Checker", "📦  Batch Scanner", "🧪  Model Lab",
         "🧠  Explainability", "📊  Data & EDA", "ℹ️  About"]

# ----------------------------------------------------------------------------- sidebar
with st.sidebar:
    ui.brand()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Decision policy**")
    policy = st.radio(
        "Flag a transaction when its score is at least",
        ["Cost-optimal", "F1-optimal", "Custom"], label_visibility="collapsed",
        help="Cost-optimal minimises missed-fraud loss plus review cost. F1-optimal balances precision and recall.")
    if policy == "Cost-optimal":
        THR = bundle.thr_cost
    elif policy == "F1-optimal":
        THR = bundle.thr_f1
    else:
        THR = st.slider("Custom threshold", 0.01, 0.99, 0.50, 0.01)
    st.caption(f"Active threshold: **{THR:.2f}**")
    st.markdown("---")
    if bundle.ready:
        st.markdown('<span class="chip teal">● Model loaded</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="chip amber">● Model file missing</span>', unsafe_allow_html=True)
    st.caption("LightGBM · time-ordered validation · native SHAP")


def need_model() -> bool:
    if bundle.ready:
        return False
    ui.callout(
        "<b>Model file not found.</b> Copy <code>fraud_model.txt</code> from your Kaggle output into the "
        "<code>model/</code> folder (or run <code>python train.py --data data/creditcard.csv</code>), then refresh this page. "
        "The Overview, Model Lab, Explainability and Data pages work without it.", "warn")
    return True


# ----------------------------------------------------------------------------- pages
def page_overview() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>Catch card fraud without freezing good customers.</h1>
          <p>A LightGBM risk engine trained on 283,726 real card transactions where only 0.17% are fraud.
          Scores any transaction in milliseconds, explains why with SHAP, and picks its alert threshold
          from money, not from a vanity metric.</p>
          <span class="chip teal">PR-AUC 0.752 on unseen future data</span>
          <span class="chip coral">75% of fraud caught</span>
          <span class="chip amber">57% lower total cost than no model</span>
        </div>""", unsafe_allow_html=True)

    st.write("")
    ops = report("operating_points.csv").set_index("Operating point")
    c = ops.loc["Cost-optimal"]
    cols = st.columns(5)
    cards = [
        ("PR-AUC (test)", "0.752", "main metric, imbalanced data", ui.TEAL),
        ("ROC-AUC (test)", "0.976", "reference only", ui.VIOLET),
        ("Fraud caught", f"{c['Recall']:.0%}", f"{int(c['Caught'])} of 52 test frauds", ui.CORAL),
        ("Alert precision", f"{c['Precision']:.0%}", f"{int(c['False alarms'])} false alarms in 42,507 normal", ui.AMBER),
        ("Cost saved", "57.4%", "vs. having no model", ui.TEAL),
    ]
    for col, (a, b, d, acc) in zip(cols, cards):
        col.markdown(ui.kpi(a, b, d, acc), unsafe_allow_html=True)

    ui.section("How the pipeline works", "Every step is chosen to avoid the usual fraud-model mistakes: leakage, a lucky split and an inflated score.")
    steps = [
        ("Split by time", "Train on the oldest 70%, validate on the next 15%, test once on the newest 15%. No random shuffling."),
        ("Compare 5 models", "Dummy, Logistic Regression, LR + SMOTE, Random Forest and LightGBM, judged by PR-AUC."),
        ("Tune LightGBM", "10-trial random search with early stopping on validation PR-AUC."),
        ("Pick thresholds", "F1-optimal and cost-optimal, both chosen on validation only."),
        ("Explain", "Native SHAP contributions for the whole model and for each transaction."),
    ]
    for col, (i, (t, d)) in zip(st.columns(5), enumerate(steps, 1)):
        col.markdown(f'<div class="step"><div class="step-n">{i}</div><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)

    ui.section("The data in one picture")
    l, r = st.columns([1.15, 1])
    with l:
        st.plotly_chart(charts.split_bars(FACTS), width="stretch", config={"displayModeBar": False})
    with r:
        st.write("")
        ui.callout(f"<b>Accuracy is useless here.</b> A model that always says “normal” scores "
                   f"<b>{FACTS['always_normal_accuracy']}%</b> accuracy and catches zero fraud. That is why this project is judged on "
                   "PR-AUC, precision, recall and money.", "warn")
        st.write("")
        ui.callout(f"<b>{FACTS['transactions']:,}</b> transactions after removing <b>{FACTS['duplicates_removed']:,}</b> duplicates. "
                   f"<b>{FACTS['frauds']}</b> are fraud (<b>{FACTS['fraud_rate']}%</b>).")

    ui.section("Read the results honestly")
    a, b = st.columns(2)
    with a:
        ui.callout("<b>Small test set.</b> The test window holds only 52 frauds, so one extra catch moves recall by about 2 points. "
                   "Treat every test number as an estimate with wide error bars.", "bad")
    with b:
        ui.callout("<b>Random Forest scored higher.</b> It led LightGBM by 0.02 PR-AUC on validation and 0.02 on test. "
                   "LightGBM is deployed anyway for speed and native SHAP, and its ROC-AUC is better (0.976 vs 0.949).", "good")


def page_checker() -> None:
    ui.page_header("Risk Checker", "Describe one transaction and get a risk score with the reasons behind it.")
    if need_model():
        return

    defaults = {"amount": 59.90, "hour": 14, **{f"v_{c}": 0.0 for c in V_COLS}}
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)

    def preset(name: str) -> None:
        for c in V_COLS:
            st.session_state[f"v_{c}"] = 0.0
        if name == "Everyday purchase":
            st.session_state.update(amount=45.0, hour=14)
        elif name == "Fraud-like profile":
            for c, v in FRAUD_PROFILE.items():
                st.session_state[f"v_{c}"] = float(v)
            st.session_state.update(amount=3.5, hour=2)
        elif name == "Large unusual order":
            for c in ("V14", "V12", "V10"):
                st.session_state[f"v_{c}"] = -3.0
            st.session_state["v_V4"] = 2.5
            st.session_state.update(amount=1250.0, hour=3)

    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown("**Start from an example**")
        b1, b2, b3 = st.columns(3)
        b1.button("Everyday purchase", on_click=preset, args=("Everyday purchase",), width="stretch")
        b2.button("Large unusual order", on_click=preset, args=("Large unusual order",), width="stretch")
        b3.button("Fraud-like profile", on_click=preset, args=("Fraud-like profile",), width="stretch")
        st.caption("Presets are illustrative: the fraud-like profile uses approximate class averages of the anonymised PCA features, not a real customer record.")

        a1, a2 = st.columns(2)
        a1.number_input("Amount (EUR)", min_value=0.0, max_value=30000.0, step=1.0, key="amount")
        a2.slider("Hour of day", 0, 23, key="hour")

        st.markdown("**Key signals** (the features the model leans on most)")
        sc = st.columns(2)
        for i, c in enumerate(KEY_SIGNALS):
            sc[i % 2].slider(c, -25.0, 25.0, step=0.1, key=f"v_{c}")
        with st.expander("All other PCA components"):
            rest = [c for c in V_COLS if c not in KEY_SIGNALS]
            gc = st.columns(4)
            for i, c in enumerate(rest):
                gc[i % 4].number_input(c, step=0.1, format="%.2f", key=f"v_{c}")

    values = {c: st.session_state[f"v_{c}"] for c in V_COLS}
    raw = inf.raw_from_inputs(values, st.session_state["amount"], st.session_state["hour"])
    p = float(inf.score(bundle, raw)[0])
    band = inf.risk_band(p, bundle.thr_cost, bundle.thr_f1)
    flagged = p >= THR

    with right:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(ui.risk_ring(p, band), unsafe_allow_html=True)
        if flagged:
            st.markdown(f'<div style="text-align:center;margin-top:.8rem" class="chip coral">⚑ Flagged at threshold {THR:.2f}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center;margin-top:.8rem" class="chip teal">✓ Not flagged at threshold {THR:.2f}</div>', unsafe_allow_html=True)
        st.caption("The score ranks risk. It is not a literal probability because the model was trained with extra weight on fraud.")
        st.markdown("</div>", unsafe_allow_html=True)

    contrib = inf.explain(bundle, raw).iloc[0]
    feats = inf.make_features(raw).iloc[0]
    reasons = inf.top_reasons(contrib, feats, 8)
    reasons["feature"] = reasons["feature"]
    st.write("")
    w1, w2 = st.columns([1.3, 1], gap="large")
    with w1:
        st.plotly_chart(charts.waterfall(reasons, float(contrib["_bias"]), 0), width="stretch", config={"displayModeBar": False})
    with w2:
        st.markdown("**In plain words**")
        html_rows = ""
        for _, r in reasons.head(5).iterrows():
            up = r["shap"] > 0
            name = FRIENDLY.get(r["feature"], r["feature"])
            html_rows += (f'<div class="reason"><span><span class="f">{name}</span> <span class="d">= {r["value"]:.2f}</span></span>'
                          f'<span class="{"up" if up else "down"}">{"raises" if up else "lowers"} risk ({r["shap"]:+.2f})</span></div>')
        st.markdown(f'<div class="glass tight">{html_rows}</div>', unsafe_allow_html=True)
        logit = float(contrib.sum())
        st.caption(f"Starting point {contrib['_bias']:+.2f} + feature effects = {logit:+.2f} log-odds before the sigmoid.")


def page_batch() -> None:
    ui.page_header("Batch Scanner", "Score a whole file of transactions, review the riskiest ones, and download the results.")
    if need_model():
        return
    st.markdown(
        f'<div class="callout">Upload a CSV with these columns: <code>{", ".join(RAW_COLS[:3])}, … V28, Amount</code> '
        "(the same layout as the Kaggle file). An optional <code>Class</code> column adds an accuracy report.</div>", unsafe_allow_html=True)
    st.write("")
    up_col, demo_col = st.columns([3, 1])
    up = up_col.file_uploader("Transactions CSV", type=["csv"], label_visibility="collapsed")
    if demo_col.button("Load demo file", width="stretch", disabled=not DEMO_CSV.exists(),
                       help="Synthetic demo data generated by scripts/make_demo.py, not real transactions."):
        st.session_state["batch_df"] = pd.read_csv(DEMO_CSV)
        st.session_state["batch_name"] = "demo (synthetic)"
    if up is not None:
        st.session_state["batch_df"] = pd.read_csv(up)
        st.session_state["batch_name"] = up.name

    df = st.session_state.get("batch_df")
    if df is None:
        ui.callout("Nothing to scan yet. Drop a CSV above" + (" or load the demo file." if DEMO_CSV.exists() else "."))
        return
    missing = inf.validate_columns(df)
    if missing:
        ui.callout(f"<b>Missing columns:</b> {', '.join(missing)}. Add them and upload again.", "bad")
        return

    with st.spinner("Scoring transactions…"):
        scores = inf.score(bundle, df)
    res = df.copy()
    res["risk_score"] = scores
    res["flagged"] = scores >= THR
    n, nf = len(res), int(res["flagged"].sum())

    cols = st.columns(4)
    for col, (a, b, d, acc) in zip(cols, [
        ("Transactions scanned", f"{n:,}", st.session_state.get("batch_name", ""), ui.VIOLET),
        ("Flagged", f"{nf:,}", f"{100 * nf / n:.2f}% of the file", ui.CORAL),
        ("Highest score", f"{scores.max():.3f}", "riskiest transaction", ui.AMBER),
        ("Amount flagged", f"{res.loc[res.flagged, 'Amount'].sum():,.0f}", "sum of flagged amounts", ui.TEAL)]):
        col.markdown(ui.kpi(a, b, d, acc), unsafe_allow_html=True)

    if "Class" in res.columns and res["Class"].nunique() > 1:
        from sklearn.metrics import average_precision_score, roc_auc_score
        y = res["Class"].astype(int).values
        tp = int(((res.flagged) & (y == 1)).sum()); fp = int(((res.flagged) & (y == 0)).sum()); fn = int((~res.flagged & (y == 1)).sum())
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        st.write("")
        st.markdown("**Accuracy report** (uses your `Class` column)")
        cc = st.columns(5)
        for col, (a, b) in zip(cc, [("PR-AUC", f"{average_precision_score(y, scores):.3f}"), ("ROC-AUC", f"{roc_auc_score(y, scores):.3f}"),
                                    ("Precision", f"{prec:.1%}"), ("Recall", f"{rec:.1%}"), ("Caught / missed", f"{tp} / {fn}")]):
            col.markdown(ui.kpi(a, b, f"{fp} false alarms" if a == "Precision" else "", ui.TEAL), unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([1, 1.2], gap="large")
    with c1:
        st.plotly_chart(charts.score_hist(scores, THR), width="stretch", config={"displayModeBar": False})
    with c2:
        k = st.slider("Review queue size", 5, min(200, n), min(25, n))
        queue = res.sort_values("risk_score", ascending=False).head(k)
        show = ["risk_score", "flagged", "Amount", "Time"] + (["Class"] if "Class" in res.columns else [])
        st.dataframe(queue[show].style.format({"risk_score": "{:.3f}", "Amount": "{:,.2f}", "Time": "{:,.0f}"}),
                     width="stretch", height=300)

    st.markdown("**Explain a flagged transaction**")
    pick = st.selectbox("Row from the review queue", queue.index.tolist(),
                        format_func=lambda i: f"row {i} · score {res.loc[i, 'risk_score']:.3f} · amount {res.loc[i, 'Amount']:,.2f}")
    one = res.loc[[pick], RAW_COLS]
    contrib = inf.explain(bundle, one).iloc[0]
    reasons = inf.top_reasons(contrib, inf.make_features(one).iloc[0], 8)
    st.plotly_chart(charts.waterfall(reasons, float(contrib["_bias"]), 0), width="stretch", config={"displayModeBar": False})

    buf = io.StringIO()
    res.sort_values("risk_score", ascending=False).to_csv(buf, index=False)
    st.download_button("Download scored CSV", buf.getvalue(), "scored_transactions.csv", "text/csv")


def page_lab() -> None:
    ui.page_header("Model Lab", "Five models, one tuned winner, and the money math behind the alert threshold.")
    val, test = report("results_validation.csv"), report("results_test.csv")
    ops, bud, trials = report("operating_points.csv"), report("review_budget.csv"), report("tuning_trials.csv")
    t1, t2, t3, t4 = st.tabs(["Model comparison", "Tuning", "Threshold & cost", "Analyst budget"])

    with t1:
        st.plotly_chart(charts.model_bars(val, test), width="stretch", config={"displayModeBar": False})
        merged = val.merge(test, on="Model", suffixes=(" (val)", " (test)"))[["Model", "PR-AUC (val)", "PR-AUC (test)", "ROC-AUC (val)", "ROC-AUC (test)"]]
        st.dataframe(merged.style.format({c: "{:.4f}" for c in merged.columns if c != "Model"}), width="stretch", hide_index=True)
        ui.callout("<b>Deployed:</b> LightGBM (tuned). Precision 90.2%, recall 71.2% and F1 0.796 at the F1-optimal threshold. "
                   "Only the deployed model gets threshold metrics, because thresholds were tuned for it alone.", "good")
    with t2:
        st.plotly_chart(charts.tuning_scatter(trials), width="stretch", config={"displayModeBar": False})
        st.dataframe(trials.sort_values("val_PR_AUC", ascending=False).style.format(
            {"val_PR_AUC": "{:.4f}", "scale_pos_weight": "{:.1f}", "learning_rate": "{:.2f}"}), width="stretch", hide_index=True)
        st.caption("Trials 5 and 10 stopped after 1 to 2 rounds, which is what early stopping does with an unlucky configuration.")
    with t3:
        rc = st.slider("What does one analyst review cost? (EUR)", 1.0, 60.0, FACTS["review_cost"], 1.0)
        st.plotly_chart(charts.cost_bars(ops, rc, FACTS["no_model_cost"]), width="stretch", config={"displayModeBar": False})
        tot = {r["Operating point"]: r["Missed loss"] + (r["Caught"] + r["False alarms"]) * rc for _, r in ops.iterrows()}
        best = min(tot, key=tot.get)
        ui.callout(f"At <b>€{rc:.0f}</b> per review, the cheaper policy is <b>{best}</b> "
                   f"(€{tot[best]:,.0f} vs €{FACTS['no_model_cost']:,.0f} with no model). "
                   "Thresholds stay at the values tuned for €5; rerun <code>train.py --review-cost</code> to re-tune.")
        st.dataframe(ops.style.format({"Threshold": "{:.2f}", "Precision": "{:.1%}", "Recall": "{:.1%}", "F1": "{:.3f}",
                                       "Total cost": "{:,.0f}", "Missed loss": "{:,.0f}", "Review cost": "{:,.0f}"}),
                     width="stretch", hide_index=True)
        image("threshold_selection.png", "Validation: precision, recall, F1 and cost against the threshold")
    with t4:
        st.plotly_chart(charts.recall_precision_k(bud), width="stretch", config={"displayModeBar": False})
        ui.callout("Reviewing just the <b>25 riskiest</b> transactions finds <b>48%</b> of all fraud with 100% precision. "
                   "At 50 reviews you reach <b>75%</b> recall; beyond that each extra review mostly finds legitimate customers.")
        image("test_evaluation.png", "Test set: PR curve, ROC curve and confusion matrix")


def page_explain() -> None:
    ui.page_header("Explainability", "Why the model flags what it flags, using LightGBM's built-in SHAP values.")
    imp = report("feature_importance.csv").set_index("feature")["mean_abs_shap"]
    l, r = st.columns([1, 1.1], gap="large")
    with l:
        st.plotly_chart(charts.importance_bars(imp.head(10)), width="stretch", config={"displayModeBar": False})
    with r:
        st.write("")
        ui.callout("<b>How to read it.</b> SHAP splits a score into one contribution per feature. A positive contribution pushes a "
                   "transaction toward fraud, a negative one pushes it toward normal. The bars show the average size of those pushes on the test set.")
        st.write("")
        ui.callout("<b>V1 to V28 are anonymised PCA components</b>, so the dataset cannot tell us what V4 or V14 mean in the real world. "
                   "<b>hour_sin</b> is the only engineered feature in the top 4: the time of day matters.", "warn")
    image("shap_summary.png", "Global importance and the direction of each feature's effect (blue = low value, red = high value)")
    st.markdown("**Three real test transactions, explained**")
    image("shap_local.png", "A caught fraud, a missed fraud and a false alarm")
    ui.callout("The missed fraud and the false alarm are the interesting ones: they show which signals fooled the model, "
               "and where an analyst's judgement still adds value.")


def page_data() -> None:
    ui.page_header("Data & EDA", "What the dataset looks like and what was done to it before modelling.")
    cols = st.columns(4)
    for col, (a, b, d, acc) in zip(cols, [
        ("Transactions", f"{FACTS['transactions']:,}", "after de-duplication", ui.VIOLET),
        ("Frauds", f"{FACTS['frauds']}", f"{FACTS['fraud_rate']}% of all rows", ui.CORAL),
        ("Duplicates removed", f"{FACTS['duplicates_removed']:,}", "exact duplicate rows", ui.AMBER),
        ("Features", "31", "28 PCA + 3 engineered", ui.TEAL)]):
        col.markdown(ui.kpi(a, b, d, acc), unsafe_allow_html=True)
    st.write("")
    image("eda_overview.png", "Class balance, amount by class and fraud rate by hour")
    image("eda_top_features.png", "The six features whose distributions differ most between fraud and normal")
    ui.section("Feature engineering")
    st.markdown("""
| Raw column | Becomes | Why |
|---|---|---|
| `V1` … `V28` | used as is | already PCA components from the data provider |
| `Amount` | `log_amount = log(1 + Amount)` | amounts are heavily right-skewed |
| `Time` (seconds) | `hour_sin`, `hour_cos` | hour of day as a circle, so 23:00 sits next to 00:00 |
""")
    ui.callout("The dataset covers just two days of European card transactions from September 2013, so seasonal and long-term patterns are not captured.", "warn")


def page_about() -> None:
    ui.page_header("About this project")
    a, b = st.columns(2, gap="large")
    with a:
        ui.section("Method")
        st.markdown("""
- **Data:** ULB / Worldline credit card fraud dataset (Kaggle), 284,807 rows, duplicates removed.
- **Split:** time-ordered 70 / 15 / 15. Thresholds and model choice come from validation; test is read once.
- **Metrics:** PR-AUC first, then precision, recall, F1, Precision@K and a cost simulation.
- **Model:** LightGBM, 168 rounds, learning rate 0.03, 31 leaves, `scale_pos_weight` ≈ 23.
- **Explainability:** `predict(pred_contrib=True)` for exact tree SHAP values.
""")
        ui.section("Tech stack")
        st.markdown("".join(f'<span class="chip">{t}</span>' for t in
                            ["Python", "LightGBM", "scikit-learn", "imbalanced-learn", "pandas", "NumPy", "Plotly", "Streamlit", "SHAP (native)"]),
                    unsafe_allow_html=True)
    with b:
        ui.section("Limitations")
        ui.callout("<ul style='margin:0;padding-left:1.1rem'>"
                   "<li>The test window has 52 frauds. Metrics carry wide uncertainty.</li>"
                   "<li>The €5 review cost is an assumption. A real bank would use its own.</li>"
                   "<li>Scores are for ranking, not calibrated probabilities.</li>"
                   "<li>Fraud patterns drift. A live system needs monitoring and regular retraining.</li>"
                   "<li>This is a learning project, not a production fraud system.</li></ul>", "warn")
        ui.section("Retrain")
        st.code("python train.py --data data/creditcard.csv --review-cost 5", language="bash")


{"🏠  Overview": page_overview, "🔎  Risk Checker": page_checker, "📦  Batch Scanner": page_batch,
 "🧪  Model Lab": page_lab, "🧠  Explainability": page_explain, "📊  Data & EDA": page_data, "ℹ️  About": page_about}[page]()

st.markdown('<div class="foot">FraudSense · built with LightGBM and Streamlit · for learning and portfolio use</div>', unsafe_allow_html=True)
