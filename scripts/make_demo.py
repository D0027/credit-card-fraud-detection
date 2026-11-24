"""Generate a small SYNTHETIC transactions file for the Batch Scanner demo.

It is not real data and not a subset of the Kaggle file. Normal rows are random noise around zero;
fraud rows are drawn around approximate class averages of the PCA components.
    python scripts/make_demo.py [--rows 400] [--frauds 12] [--out data/sample_transactions.csv]
"""
import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.config import FRAUD_PROFILE, V_COLS  # noqa: E402


def build(rows: int, frauds: int, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    scales = np.linspace(1.9, 0.35, 28)
    X = rng.normal(0, scales, size=(rows, 28))
    y = np.zeros(rows, dtype=int)
    idx = rng.choice(rows, frauds, replace=False)
    y[idx] = 1
    prof = np.array([FRAUD_PROFILE[c] for c in V_COLS])
    X[idx] = prof + rng.normal(0, 1.6, size=(frauds, 28))
    amt = np.round(rng.lognormal(3.4, 1.3, rows), 2)
    amt[idx] = np.round(rng.lognormal(1.8, 1.8, frauds), 2)
    df = pd.DataFrame(X, columns=V_COLS)
    df.insert(0, "Time", np.sort(rng.uniform(0, 172_000, rows)).round(0).astype(int))
    df["Amount"] = amt
    df["Class"] = y
    return df.round(4)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", type=int, default=400)
    ap.add_argument("--frauds", type=int, default=12)
    ap.add_argument("--out", default="data/sample_transactions.csv")
    a = ap.parse_args()
    build(a.rows, a.frauds).to_csv(a.out, index=False)
    print("wrote", a.out)
