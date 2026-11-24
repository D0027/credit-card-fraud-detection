<div align="center">

<img src="assets/banner.svg" alt="FraudSense banner: explainable credit card fraud detection" width="100%"/>

<a href="https://credit-card-fraud-detection-027.streamlit.app/">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=20&pause=1400&color=0F8F84&center=true&vCenter=true&width=760&height=40&lines=283%2C726+transactions.+473+frauds.+0.17%25+positives.;Time-ordered+split.+Test+set+read+once.;Every+alert+comes+with+a+SHAP+explanation.;The+alert+line+is+set+with+money%2C+not+vanity+metrics." alt="FraudSense typing animation"/>
</a>

<br/>

### Catch fraud in a 0.17%-fraud world, explain every decision, and set the alert line using money instead of vanity metrics.

<br/>

<a href="https://credit-card-fraud-detection-027.streamlit.app/"><img src="assets/btn-live-demo.svg" alt="Launch live demo" height="50"/></a>
&nbsp;
<a href="https://credit-card-fraud-detection-027.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit" height="46"/></a>

<br/><br/>

<img src="assets/badge-python.svg" alt="Python 3.10+"/>
<img src="assets/badge-lightgbm.svg" alt="Model: LightGBM tuned"/>
<img src="assets/badge-shap.svg" alt="Explainability: SHAP"/>
<img src="assets/badge-streamlit.svg" alt="Streamlit app"/>
<img src="assets/badge-plotly.svg" alt="Plotly charts"/>
<img src="assets/badge-prauc.svg" alt="test PR-AUC 0.752"/>
<img src="assets/badge-license.svg" alt="License: MIT"/>

<img src="assets/badge-dataset.svg" alt="Dataset: 283,726 transactions"/>
<img src="assets/badge-fraudrate.svg" alt="Fraud rate: 0.17%"/>
<img src="assets/badge-split.svg" alt="Split: time-ordered 70/15/15"/>

<br/><br/>

<b>
<a href="https://credit-card-fraud-detection-027.streamlit.app/">🚀 Live demo</a> &nbsp;·&nbsp;
<a href="#-results">📈 Results</a> &nbsp;·&nbsp;
<a href="#-the-app">🖥️ The app</a> &nbsp;·&nbsp;
<a href="#-quick-start">⚡ Quick start</a> &nbsp;·&nbsp;
<a href="#-how-it-works">🧠 How it works</a> &nbsp;·&nbsp;
<a href="#-gallery">📊 Gallery</a> &nbsp;·&nbsp;
<a href="#-limitations">⚠️ Limitations</a>
</b>

<br/><br/>

<img src="assets/divider.svg" alt="" width="100%"/>

</div>

## 🎯 The problem

Out of **283,726** real card transactions, only **473 (0.17%)** are fraud. A model that always says "normal" scores **99.83% accuracy** and catches **zero** fraud, so accuracy is useless here.

FraudSense is built around what actually matters: catching fraud, not annoying good customers, and knowing what each alert is worth.

<div align="center">

<img src="assets/stat-prauc.svg" alt="PR-AUC (test): 0.752" width="24%"/>
<img src="assets/stat-caught.svg" alt="Fraud caught: 75%" width="24%"/>
<img src="assets/stat-precision.svg" alt="Alert precision: 76.5%" width="24%"/>
<img src="assets/stat-saved.svg" alt="Cost saved vs no model: 57.4%" width="24%"/>

</div>

## ✨ Highlights

<table>
<tr>
<td width="33%" valign="top">

### ⏱️ Honest evaluation
Time-ordered train / validation / test split. Thresholds are chosen on validation, and the test set is read once.

</td>
<td width="33%" valign="top">

### 📏 Right metrics
PR-AUC first, then precision, recall, F1, Precision@K and a business cost simulation.

</td>
<td width="33%" valign="top">

### 🤖 5 models compared
Dummy, Logistic Regression, LR + SMOTE, Random Forest and a tuned LightGBM.

</td>
</tr>
<tr>
<td width="33%" valign="top">

### 💶 Money-based threshold
Cost of missed fraud plus cost of analyst reviews, with a live what-if slider in the app.

</td>
<td width="33%" valign="top">

### 🔍 Explainable
Exact SHAP contributions from LightGBM, globally and for every single transaction.

</td>
<td width="33%" valign="top">

### 🎨 Advanced Streamlit UI
Glass UI with an animated backdrop, a risk-score ring, interactive Plotly charts, batch scoring and CSV download.

</td>
</tr>
</table>

## 🖥️ The app

<div align="center">

**[👉 Try it live: credit-card-fraud-detection-027.streamlit.app](https://credit-card-fraud-detection-027.streamlit.app/)**

</div>

| Page | What it does |
|---|---|
| 🏠 **Overview** | Headline metrics, pipeline, data split and an honest read of the results |
| 🔎 **Risk Checker** | Enter one transaction, get a risk-score ring, a verdict and a SHAP breakdown of the reasons |
| 📦 **Batch Scanner** | Upload a CSV, score every row, review the riskiest, explain any row, download results |
| 🧪 **Model Lab** | Model comparison, tuning trials, cost what-if slider, analyst review budget |
| 🧠 **Explainability** | Global SHAP importance and local explanations (caught fraud, missed fraud, false alarm) |
| 📊 **Data & EDA** | Class balance, feature distributions and the feature engineering table |

A sidebar switch lets you flag transactions by the **cost-optimal** threshold, the **F1-optimal** threshold, or your own.

> [!TIP]
> **Quick tour:** open the *Risk Checker*, press **Fraud-like profile**, and watch the ring turn red. Then check the SHAP chart to see which signals pushed the score up.

```mermaid
flowchart LR
    T["Transaction<br/>V1-V28, Amount, Time"] --> F["Engineered features<br/>log_amount, hour_sin, hour_cos"]
    F --> M["LightGBM<br/>risk score"]
    M --> P{"Threshold policy<br/>cost / F1 / custom"}
    P -->|above| X["🚨 Flag for review"]
    P -->|below| OK["✅ Looks normal"]
    M --> S["SHAP<br/>why this score"]
    S --> X
    S --> OK

    classDef teal fill:#0f8f84,stroke:#0b6b63,color:#ffffff;
    classDef violet fill:#4b3fd1,stroke:#3a30a8,color:#ffffff;
    classDef red fill:#ff5c6c,stroke:#c94452,color:#ffffff;
    classDef green fill:#1fa971,stroke:#17825a,color:#ffffff;
    class F,M teal;
    class P,S violet;
    class X red;
    class OK green;
```

## 📈 Results

Test set = the newest 15% of transactions, read once.

| Model | PR-AUC | ROC-AUC |
|---|---:|---:|
| Random Forest | 0.7731 | 0.9493 |
| 🏆 **LightGBM (tuned), deployed** | **0.7516** | **0.9758** |
| Logistic Regression + SMOTE | 0.6999 | 0.9717 |
| Logistic Regression | 0.6921 | 0.9766 |
| Dummy | 0.0012 | 0.5000 |

```text
PR-AUC on the test set (each █ ≈ 0.025)

Random Forest        ███████████████████████████████  0.7731
LightGBM (deployed)  ██████████████████████████████   0.7516
LR + SMOTE           ████████████████████████████     0.6999
Logistic Regression  ████████████████████████████     0.6921
Dummy                                                 0.0012
```

LightGBM is deployed for speed and native SHAP even though Random Forest scored about 0.02 PR-AUC higher.

### Operating points for the deployed model

| Policy | Threshold | Precision | Recall | F1 | Caught | Missed | False alarms | Total cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F1-optimal | 0.83 | 90.2% | 71.2% | 0.796 | 37 | 15 | 4 | €2,657 |
| Cost-optimal | 0.64 | 76.5% | 75.0% | 0.757 | 39 | 13 | 12 | **€2,627** |

```text
Total cost over the test window (each █ ≈ €154)

No model             ████████████████████████████████████████  €6,169
F1-optimal           █████████████████                         €2,657
Cost-optimal         █████████████████                         €2,627   ← 57.4% saved
```

Without a model, every fraud gets through and the test window costs **€6,169**. The cost-optimal policy cuts that by **57.4%**.

> [!WARNING]
> The test window contains only **52 frauds**, so every test metric has wide error bars. The €5 review cost is an assumption, not a bank figure.

## 🧠 How it works

```mermaid
flowchart LR
    A["creditcard.csv<br/>283,726 rows"] --> B["De-duplicate<br/>sort by Time"]
    B --> C["Feature engineering<br/>log Amount, hour sin/cos"]
    C --> D["Time split<br/>70 / 15 / 15"]
    D --> E["5 models<br/>+ LightGBM tuning"]
    E --> F["Thresholds<br/>chosen on validation"]
    F --> G["One test<br/>evaluation"]
    G --> H["SHAP + Streamlit app"]

    classDef data fill:#0b1020,stroke:#0f8f84,color:#ffffff;
    classDef step fill:#0f8f84,stroke:#0b6b63,color:#ffffff;
    classDef final fill:#4b3fd1,stroke:#3a30a8,color:#ffffff;
    class A data;
    class B,C,D,E,F step;
    class G,H final;
```

| Question | Answer |
|---|---|
| ⏳ **Why a time split?** | In real life a model trains on the past and scores the future. A random split leaks future patterns into training and inflates scores. |
| 📐 **Why PR-AUC?** | With 0.17% positives, PR-AUC reflects the quality of the alerts. ROC-AUC looks great even for weak models. |
| 💶 **Why a cost threshold?** | A missed fraud loses its full amount, while a false alarm costs an analyst review. The best threshold depends on that ratio. |
| 🎚️ **Are scores probabilities?** | No, they are for ranking. The model uses `scale_pos_weight ≈ 23`, so a score of 0.9 is not a 90% probability. |

<details>
<summary><b>🧩 Feature engineering</b></summary>

<br/>

| Raw column | Becomes | Why |
|---|---|---|
| `V1` … `V28` | used as is | already PCA components from the data provider |
| `Amount` | `log_amount = log(1 + Amount)` | amounts are heavily right-skewed |
| `Time` (seconds) | `hour_sin`, `hour_cos` | hour of day as a circle, so 23:00 sits next to 00:00 |

</details>

<details>
<summary><b>⚙️ Final LightGBM configuration</b></summary>

<br/>

| Parameter | Value |
|---|---|
| `num_leaves` | 31 |
| `learning_rate` | 0.03 |
| `min_child_samples` | 100 |
| `feature_fraction` / `bagging_fraction` | 1.0 / 1.0 |
| `lambda_l2` | 5.0 |
| `scale_pos_weight` | ≈ 23.27 |
| Rounds | 168 (early stopping on validation PR-AUC) |

</details>

## 🚀 Quick start

```bash
git clone https://github.com/D0027/credit-card-fraud-detection.git
cd credit-card-fraud-detection
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

The trained model is already in `model/fraud_model.txt`, so the app works right away.

<details>
<summary><b>🔁 Retrain the model yourself</b></summary>

<br/>

Download [`creditcard.csv`](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) into `data/` and run:

```bash
python train.py --data data/creditcard.csv                    # reuses the notebook's best config (about 10 seconds)
python train.py --data data/creditcard.csv --tune 10          # or repeat the random search
python train.py --data data/creditcard.csv --review-cost 10   # re-tune thresholds for a different review cost
```

</details>

> [!NOTE]
> Want a quick batch demo? Click **Load demo file** in the Batch Scanner. It uses `data/sample_transactions.csv`, a **synthetic** file made by `scripts/make_demo.py`, so its scores only show how the app behaves.

## 📊 Gallery

<table>
<tr>
<td align="center" width="50%"><img src="images/model_comparison.png" alt="Model comparison" width="100%"><br/><sub><b>Model comparison</b></sub></td>
<td align="center" width="50%"><img src="images/threshold_selection.png" alt="Threshold selection" width="100%"><br/><sub><b>Threshold and cost selection</b></sub></td>
</tr>
<tr>
<td align="center" width="50%"><img src="images/test_evaluation.png" alt="Test evaluation" width="100%"><br/><sub><b>Test evaluation</b></sub></td>
<td align="center" width="50%"><img src="images/shap_summary.png" alt="SHAP summary" width="100%"><br/><sub><b>SHAP: global importance</b></sub></td>
</tr>
<tr>
<td align="center" width="50%"><img src="images/shap_local.png" alt="Local SHAP explanations" width="100%"><br/><sub><b>SHAP: single transactions</b></sub></td>
<td align="center" width="50%"><img src="images/eda_overview.png" alt="EDA overview" width="100%"><br/><sub><b>Data overview</b></sub></td>
</tr>
</table>

## 📁 Project structure

```text
credit-card-fraud-detection/
├── app.py                    # Streamlit app
├── train.py                  # rebuild the model from creditcard.csv
├── requirements.txt
├── .streamlit/config.toml    # dark theme + upload limit
├── assets/                   # SVG banner, buttons and badges used by this README
├── src/
│   ├── config.py             # paths, constants, notebook facts
│   ├── inference.py          # feature engineering, scoring, SHAP
│   ├── charts.py             # Plotly figures
│   └── ui.py                 # CSS theme and HTML components
├── model/                    # fraud_model.txt + model_meta.json
├── reports/                  # result tables exported from the notebook run
├── images/                   # plots exported from the notebook run
├── notebooks/credit-card-fraud.ipynb
├── scripts/make_demo.py      # builds the synthetic demo CSV
└── data/                     # sample_transactions.csv (+ creditcard.csv, not committed)
```

## 🛠️ Tech stack

<div align="center">

<img src="assets/tech-python.svg" alt="Python"/>
<img src="assets/tech-pandas.svg" alt="pandas"/>
<img src="assets/tech-numpy.svg" alt="NumPy"/>
<img src="assets/tech-sklearn.svg" alt="scikit-learn"/>
<img src="assets/tech-lightgbm.svg" alt="LightGBM"/>
<img src="assets/tech-shap.svg" alt="SHAP"/>
<img src="assets/tech-plotly.svg" alt="Plotly"/>
<img src="assets/tech-streamlit.svg" alt="Streamlit"/>
<img src="assets/tech-kaggle.svg" alt="Kaggle"/>

</div>

## ⚠️ Limitations

> [!CAUTION]
> This is a learning and portfolio project, not a production fraud system. A real one needs monitoring, drift checks, retraining and human review workflows.

- Only two days of European card transactions from September 2013, so there is no seasonality and fraud patterns have since drifted.
- `V1`–`V28` are anonymised PCA components, so their business meaning is unknown.
- 52 test frauds make precision and recall estimates noisy.

## 🙏 Credits

Dataset: [Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) by the Machine Learning Group, ULB, released under the Database Contents License (DbCL) v1.0. Reference: Dal Pozzolo, Caelen, Johnson and Bontempi, *Calibrating Probability with Undersampling for Unbalanced Classification*, IEEE CIDM 2015.

## 📄 License

Code released under the [MIT License](LICENSE). The dataset keeps its own license.

<div align="center">

<br/>

**If this project helped you, drop a ⭐ on the repo.**

<a href="https://credit-card-fraud-detection-027.streamlit.app/"><img src="assets/btn-open-app.svg" alt="Open the live app" height="50"/></a>

<br/>

<img src="assets/footer.svg" alt="" width="100%"/>

</div>
