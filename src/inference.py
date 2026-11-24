"""Model loading, feature engineering, scoring and per-transaction explanations."""
from __future__ import annotations

import json
from dataclasses import dataclass

import numpy as np
import pandas as pd

from .config import FEATURES, META_PATH, MODEL_PATH, RAW_COLS, V_COLS

try:
    import lightgbm as lgb
except Exception:  # pragma: no cover - lets the dashboard pages run without LightGBM
    lgb = None


@dataclass
class Bundle:
    booster: "lgb.Booster | None"
    meta: dict

    @property
    def ready(self) -> bool:
        return self.booster is not None

    @property
    def thr_f1(self) -> float:
        return float(self.meta.get("threshold_f1", 0.83))

    @property
    def thr_cost(self) -> float:
        return float(self.meta.get("threshold_cost", 0.64))


def load_bundle() -> Bundle:
    meta = json.loads(META_PATH.read_text()) if META_PATH.exists() else {}
    booster = None
    if lgb is not None and MODEL_PATH.exists():
        booster = lgb.Booster(model_file=str(MODEL_PATH))
    return Bundle(booster=booster, meta=meta)


def make_features(raw: pd.DataFrame) -> pd.DataFrame:
    """Exactly the feature engineering used in the notebook."""
    out = raw[V_COLS].astype(float).copy()
    out["log_amount"] = np.log1p(raw["Amount"].astype(float))
    hour = (raw["Time"].astype(float) // 3600) % 24
    out["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    out["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    return out[FEATURES]


def raw_from_inputs(values: dict, amount: float, hour: int) -> pd.DataFrame:
    row = {c: float(values.get(c, 0.0)) for c in V_COLS}
    row["Amount"] = float(amount)
    row["Time"] = float(hour) * 3600.0
    return pd.DataFrame([row])[RAW_COLS]


def validate_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in RAW_COLS if c not in df.columns]


def score(bundle: Bundle, raw: pd.DataFrame) -> np.ndarray:
    return bundle.booster.predict(make_features(raw))


def explain(bundle: Bundle, raw: pd.DataFrame) -> pd.DataFrame:
    """Native LightGBM SHAP contributions (log-odds) for each row, plus the bias term."""
    X = make_features(raw)
    contrib = bundle.booster.predict(X, pred_contrib=True)
    out = pd.DataFrame(contrib[:, :-1], columns=FEATURES, index=raw.index)
    out["_bias"] = contrib[:, -1]
    return out


def top_reasons(contrib_row: pd.Series, feature_row: pd.Series, k: int = 8) -> pd.DataFrame:
    s = contrib_row.drop(labels=["_bias"], errors="ignore")
    top = s.reindex(s.abs().sort_values(ascending=False).head(k).index)
    return pd.DataFrame({"feature": top.index, "value": [feature_row[f] for f in top.index],
                         "shap": top.values})


def risk_band(p: float, thr_cost: float, thr_f1: float) -> str:
    lo, hi = sorted((thr_cost, thr_f1))
    if p >= hi:
        return "high"
    if p >= lo:
        return "elevated"
    return "low"
