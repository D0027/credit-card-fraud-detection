<div align="center">

# 🛡️ FraudSense

### Credit card fraud detection with explainable ML and a cost-aware alert threshold

Catch fraud in a 0.17%-fraud world, explain every decision, and set the alert line using money instead of vanity metrics.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-tuned-2DE2C5)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)
![PR-AUC](https://img.shields.io/badge/test%20PR--AUC-0.752-8B7CFF)
![License](https://img.shields.io/badge/License-MIT-green)

<!-- Add after deploying:  [**▶ Live demo**](https://your-app.streamlit.app) -->

</div>

---

## ✨ Highlights

| | |
|---|---|
| **Honest evaluation** | Time-ordered train / validation / test split. Thresholds are chosen on validation, and the test set is read once. |
| **Right metrics** | PR-AUC first. Accuracy is ignored because an "always normal" model already scores **99.83%**. |
| **5 models compared** | Dummy, Logistic Regression, LR + SMOTE, Random Forest and a tuned LightGBM. |
| **Money-based threshold** | Cost of missed fraud + cost of analyst reviews, with a live what-if slider in the app. |
| **Explainable** | Exact SHAP contributions from LightGBM, globally and for every single transaction. |
| **Advanced Streamlit UI** | Glass UI with an animated backdrop, a risk-score ring, interactive Plotly charts, batch scoring and CSV download. |

## 📈 Results (test set: newest 15% of transactions)

| Model | PR-AUC | ROC-AUC |
|---|---:|---:|
| Random Forest | 0.7731 | 0.9493 |
| **LightGBM (tuned), deployed** | **0.7516** | **0.9758** |
| Logistic Regression + SMOTE | 0.6999 | 0.9717 |
| Logistic Regression | 0.6921 | 0.9766 |
| Dummy | 0.0012 | 0.5000 |

LightGBM is deployed for speed and native SHAP even though Random Forest scored about 0.02 PR-AUC higher.

**Operating points for the deployed model**

| Policy | Threshold | Precision | Recall | F1 | Caught | Missed | False alarms | Total cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F1-optimal | 0.83 | 90.2% | 71.2% | 0.796 | 37 | 15 | 4 | €2,657 |
| Cost-optimal | 0.64 | 76.5% | 75.0% | 0.757 | 39 | 13 | 12 | **€2,627** |

Without a model, every fraud gets through and the test window costs **€6,169**. The cost-optimal policy cuts that by **57.4%**.

> ⚠️ The test window contains only **52 frauds**, so every test metric has wide error bars. The €5 review cost is an assumption, not a bank figure.

## 🖥️ The app

| Page | What it does |
|---|---|
| **Overview** | Headline metrics, pipeline, data split and an honest read of the results |
| **Risk Checker** | Enter one transaction, get a risk-score ring, a verdict and a SHAP breakdown of the reasons |
| **Batch Scanner** | Upload a CSV, score every row, review the riskiest, explain any row, download results |
| **Model Lab** | Model comparison, tuning trials, cost what-if slider, analyst review budget |
| **Explainability** | Global SHAP importance and local explanations (caught fraud, missed fraud, false alarm) |
| **Data & EDA** | Class balance, feature distributions and the feature engineering table |

A sidebar switch lets you flag transactions by the **cost-optimal** threshold, the **F1-optimal** threshold, or your own.

## 🚀 Quick start

```bash
git clone https://github.com/<your-username>/credit-card-fraud-detection.git
cd credit-card-fraud-detection
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The Risk Checker and Batch Scanner need the trained model in `model/fraud_model.txt`. Pick one option:

1. **Use the notebook output.** Run `notebooks/credit-card-fraud.ipynb` on Kaggle and copy `fraud_model.txt` into `model/`.
2. **Retrain locally.** Download [`creditcard.csv`](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) into `data/` and run:

```bash
python train.py --data data/creditcard.csv                 # reuses the notebook's best config (about 10 seconds)
python train.py --data data/creditcard.csv --tune 10       # or repeat the random search
python train.py --data data/creditcard.csv --review-cost 10   # re-tune thresholds for a different review cost
```

The Overview, Model Lab, Explainability and Data pages work even before a model file is added.

Want a quick batch demo? Click **Load demo file** in the Batch Scanner. It uses `data/sample_transactions.csv`, a **synthetic** file made by `scripts/make_demo.py`, so its scores only show how the app behaves.

## 🧠 How it works

```
creditcard.csv ─► de-duplicate ─► sort by Time ─► feature engineering
                                                    │  log1p(Amount), hour of day as sin/cos
                                                    ▼
          70% train ──► fit 5 models ──► LightGBM random search (val PR-AUC, early stopping)
          15% val   ──► pick F1-optimal and cost-optimal thresholds
          15% test  ──► evaluate once ──► SHAP explanations ──► model/fraud_model.txt ──► Streamlit app
```

- **Why a time split?** In real life a model trains on the past and scores the future. A random split leaks future patterns into training and inflates scores.
- **Why PR-AUC?** With 0.17% positives, PR-AUC reflects the quality of the alerts. ROC-AUC looks great even for weak models.
- **Why a cost threshold?** A missed fraud loses its full amount, while a false alarm costs an analyst review. The best threshold depends on that ratio.
- **Scores are for ranking.** The model uses `scale_pos_weight ≈ 23`, so a score of 0.9 is not a 90% probability.

## 📊 Gallery

<table>
<tr>
<td><img src="images/model_comparison.png" alt="Model comparison"></td>
<td><img src="images/threshold_selection.png" alt="Threshold selection"></td>
</tr>
<tr>
<td><img src="images/test_evaluation.png" alt="Test evaluation"></td>
<td><img src="images/shap_summary.png" alt="SHAP summary"></td>
</tr>
<tr>
<td><img src="images/shap_local.png" alt="Local SHAP explanations"></td>
<td><img src="images/eda_overview.png" alt="EDA overview"></td>
</tr>
</table>

## 📁 Project structure

```
credit-card-fraud-detection/
├── app.py                    # Streamlit app (7 pages)
├── train.py                  # rebuild the model from creditcard.csv
├── requirements.txt
├── .streamlit/config.toml    # dark theme + upload limit
├── src/
│   ├── config.py             # paths, constants, notebook facts
│   ├── inference.py          # feature engineering, scoring, SHAP
│   ├── charts.py             # Plotly figures
│   └── ui.py                 # CSS theme and HTML components
├── model/                    # fraud_model.txt (you add) + model_meta.json
├── reports/                  # result tables exported from the notebook run
├── images/                   # plots exported from the notebook run
├── notebooks/credit-card-fraud.ipynb
├── scripts/make_demo.py      # builds the synthetic demo CSV
└── data/                     # sample_transactions.csv (+ creditcard.csv, not committed)
```

## ☁️ Deploy on Streamlit Community Cloud

1. Push this repo to GitHub, including `model/fraud_model.txt` (about 0.6 MB).
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Choose the repo, set the main file to `app.py`, and deploy.
4. Paste the app link into the commented line near the top of this README.

## ⚠️ Limitations

- Only two days of European card transactions from September 2013, so there is no seasonality and fraud patterns have since drifted.
- `V1`–`V28` are anonymised PCA components, so their business meaning is unknown.
- 52 test frauds make precision and recall estimates noisy.
- This is a learning and portfolio project, not a production fraud system. A real one needs monitoring, drift checks, retraining and human review workflows.

## 🙏 Credits

Dataset: [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) by the Machine Learning Group, ULB, released under the Database Contents License (DbCL) v1.0. Reference: Dal Pozzolo, Caelen, Johnson and Bontempi, *Calibrating Probability with Undersampling for Unbalanced Classification*, IEEE CIDM 2015.

## 📄 License

Code released under the [MIT License](LICENSE). The dataset keeps its own license.
