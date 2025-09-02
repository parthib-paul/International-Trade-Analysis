## 🌍 International Trade Analysis — ML Web App

A full-stack Flask app that predicts **trade balance** and visualizes economic trends across countries.  
Built with an automated **ETL pipeline** (10k+ WTO rows), a **Linear Regression** model (~80% accuracy), and a clean **Bootstrap** UI with robust input validation.



## ✨ Highlights

- **ML predictions:** Linear Regression on 7 economic features for 9 countries (≈80% test accuracy).
- **Automated ETL:** Pandas pipeline for currency normalization, missing-value handling, and dataset joins (10k+ WTO points).
- **Production-minded UI:** Flask + HTML/Bootstrap with **historical range checks** to cut user errors (≈40% reduction).
- **Visual analytics:** Matplotlib/Seaborn heatmaps + time-series, **base64-embedded** for smooth web rendering.



## 🧰 Tech Stack

- **Core:** Python, Flask, HTML/CSS/JS, Bootstrap  
- **Data/ML:** Pandas, NumPy, scikit-learn, Matplotlib, Seaborn  
- **Dev:** Jupyter, Git/GitHub



---

## 🚀 Quickstart

### 1) Prereqs
- Python 3.10+  
- (Optional) create a virtual env

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
### 2) pip install -r requirements.txt
### 3) python scripts/etl.py --in data/raw --out data/processed
### 4) python model/train.py --data data/processed/dataset.csv --save-dir model/artifacts
### 5) python app/main.py
# visit http://127.0.0.1:5000

