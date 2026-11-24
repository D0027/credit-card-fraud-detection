"""Rebuild the deployed model from creditcard.csv (mirrors the notebook).

    python train.py --data data/creditcard.csv
    python train.py --data data/creditcard.csv --review-cost 10 --tune 10

Writes model/fraud_model.txt and model/model_meta.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score

from src.inference import make_features

SEED = 42
TRAIN_FRAC, VAL_FRAC = 0.70, 0.15
# Best configuration found by the notebook's random search (validation PR-AUC 0.8457).
BEST_CFG = dict(num_leaves=31, learning_rate=0.03, min_child_samples=100, feature_fraction=1.0,
                bagging_fraction=1.0, lambda_l2=5.0, scale_pos_weight=23.273263818020226)
BEST_ROUNDS = 168


def params(cfg: dict) -> dict:
    return dict(objective="binary", metric="average_precision", bagging_freq=1, verbose=-1,
                seed=SEED, deterministic=True, force_row_wise=True, **cfg)


def metrics_at(y, p, thr):
    pred = p >= thr
    tp = int((pred & (y == 1)).sum()); fp = int((pred & (y == 0)).sum()); fn = int((~pred & (y == 1)).sum())
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return dict(tp=tp, fp=fp, fn=fn, precision=prec, recall=rec, f1=f1)


def cost(y, p, thr, amount, review_cost):
    pred = p >= thr
    return float(amount[(y == 1) & ~pred].sum() + pred.sum() * review_cost)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/creditcard.csv")
    ap.add_argument("--out", default="model")
    ap.add_argument("--review-cost", type=float, default=5.0, help="EUR per analyst review (assumption)")
    ap.add_argument("--tune", type=int, default=0, help="run N random-search trials instead of using the saved best config")
    args = ap.parse_args()

    raw = pd.read_csv(args.data)
    df = raw.drop_duplicates().sort_values("Time").reset_index(drop=True)
    print(f"rows {len(raw):,} -> {len(df):,} after removing duplicates | fraud {int(df.Class.sum())}")

    X, y, amt = make_features(df), df["Class"].values, df["Amount"].values
    n = len(df)
    i_tr, i_va = int(n * TRAIN_FRAC), int(n * (TRAIN_FRAC + VAL_FRAC))
    X_tr, y_tr = X.iloc[:i_tr], y[:i_tr]
    X_va, y_va, a_va = X.iloc[i_tr:i_va], y[i_tr:i_va], amt[i_tr:i_va]
    X_te, y_te, a_te = X.iloc[i_va:], y[i_va:], amt[i_va:]

    ds = {"feature_pre_filter": False}
    dtrain = lgb.Dataset(X_tr, label=y_tr, params=ds, free_raw_data=False)
    dval = lgb.Dataset(X_va, label=y_va, reference=dtrain, params=ds, free_raw_data=False)

    cfg, rounds = dict(BEST_CFG), BEST_ROUNDS
    if args.tune:
        rng = np.random.default_rng(SEED)
        ratio = (y_tr == 0).sum() / max((y_tr == 1).sum(), 1)
        space = dict(num_leaves=[15, 31, 63], learning_rate=[0.03, 0.05, 0.1], min_child_samples=[20, 50, 100],
                     feature_fraction=[0.7, 0.9, 1.0], bagging_fraction=[0.7, 0.9, 1.0], lambda_l2=[0.0, 1.0, 5.0],
                     scale_pos_weight=[1.0, float(np.sqrt(ratio)), float(ratio)])
        best = (-1.0, cfg, rounds)
        for t in range(args.tune):
            c = {k: v[rng.integers(len(v))] for k, v in space.items()}
            b = lgb.train(params(c), dtrain, 1000, valid_sets=[dval], callbacks=[lgb.early_stopping(50, verbose=False)])
            s = b.best_score["valid_0"]["average_precision"]
            print(f"trial {t + 1}/{args.tune}: val PR-AUC {s:.4f}")
            if s > best[0]:
                best = (s, c, b.best_iteration)
        _, cfg, rounds = best

    booster = lgb.train(params(cfg), dtrain, num_boost_round=rounds)
    p_va, p_te = booster.predict(X_va), booster.predict(X_te)

    cand = np.unique(np.concatenate([np.linspace(0.01, 0.99, 99), np.quantile(p_va, np.linspace(0.95, 0.9999, 250))]))
    f1s = [metrics_at(y_va, p_va, t)["f1"] for t in cand]
    costs = [cost(y_va, p_va, t, a_va, args.review_cost) for t in cand]
    thr_f1, thr_cost = float(cand[int(np.argmax(f1s))]), float(cand[int(np.argmin(costs))])

    pr, roc = float(average_precision_score(y_te, p_te)), float(roc_auc_score(y_te, p_te))
    print(f"\nTEST  PR-AUC {pr:.4f} | ROC-AUC {roc:.4f} | thresholds F1 {thr_f1:.2f}, cost {thr_cost:.2f}")
    for name, thr in [("F1-optimal", thr_f1), ("Cost-optimal", thr_cost)]:
        m = metrics_at(y_te, p_te, thr)
        print(f"  {name:12s} thr {thr:.2f} | precision {m['precision']:.3f} recall {m['recall']:.3f} "
              f"| caught {m['tp']} missed {m['fn']} false alarms {m['fp']} | cost {cost(y_te, p_te, thr, a_te, args.review_cost):,.2f}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    booster.save_model(str(out / "fraud_model.txt"))
    meta = {"features": list(X.columns),
            "feature_engineering": {"amount": "log1p(Amount)", "time": "hour of day -> sin/cos (Time // 3600 % 24)"},
            "deployed_model": "LightGBM (tuned)", "lgbm_params": cfg, "rounds": int(rounds),
            "threshold_f1": thr_f1, "threshold_cost": thr_cost, "review_cost_assumption": args.review_cost,
            "split": {"train_frac": TRAIN_FRAC, "val_frac": VAL_FRAC, "type": "time-ordered"},
            "test": {"n": int(len(y_te)), "frauds": int(y_te.sum()), "pr_auc": pr, "roc_auc": roc}}
    (out / "model_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"\nsaved {out / 'fraud_model.txt'} and {out / 'model_meta.json'}")


if __name__ == "__main__":
    main()
