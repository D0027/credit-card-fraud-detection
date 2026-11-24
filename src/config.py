"""Paths, constants and the numbers reported by the notebook."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "model" / "fraud_model.txt"
META_PATH = ROOT / "model" / "model_meta.json"
REPORTS = ROOT / "reports"
IMAGES = ROOT / "images"
DEMO_CSV = ROOT / "data" / "sample_transactions.csv"

V_COLS = [f"V{i}" for i in range(1, 29)]
FEATURES = V_COLS + ["log_amount", "hour_sin", "hour_cos"]
RAW_COLS = ["Time"] + V_COLS + ["Amount"]

# Strongest drivers according to the notebook's SHAP analysis (mean |SHAP|, test set).
KEY_SIGNALS = ["V4", "V14", "V8", "V12", "V22", "V5", "V18", "V20", "V3", "V17", "V10"]

# Headline facts straight from the notebook run.
FACTS = {
    "transactions": 283_726,
    "duplicates_removed": 1_081,
    "frauds": 473,
    "fraud_rate": 0.167,
    "train": (198_608, 366),
    "val": (42_559, 55),
    "test": (42_559, 52),
    "always_normal_accuracy": 99.83,
    "no_model_cost": 6168.88,
    "review_cost": 5.0,
}

# Approximate class averages of the PCA components for legitimate vs fraudulent
# transactions in the public dataset. Used ONLY as illustrative presets in the UI.
FRAUD_PROFILE = {
    "V1": -4.77, "V2": 3.62, "V3": -7.03, "V4": 4.54, "V5": -3.15, "V6": -1.40, "V7": -5.57,
    "V8": 0.57, "V9": -2.58, "V10": -5.68, "V11": 3.80, "V12": -6.26, "V13": -0.11,
    "V14": -6.97, "V15": -0.09, "V16": -4.14, "V17": -6.67, "V18": -2.24, "V19": 0.68,
    "V20": 0.37, "V21": 0.71, "V22": 0.01, "V23": -0.04, "V24": -0.10, "V25": 0.04,
    "V26": 0.05, "V27": 0.17, "V28": 0.08,
}
