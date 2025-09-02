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





## 🚀 Quickstart

### Prereqs
- Python 3.10+  
- (Optional) create a virtual env

```bash
## 🖥️ Run Instructions 

1. **Clone the repo**
```bash
git clone https://github.com/parthib-paul/International-Trade-Analysis.git
cd International-Trade-Analysis
pip install -r requirements.txt
python scripts/etl.py --in data/raw --out data/processed
python model/train.py --data data/processed/dataset.csv --save-dir model/artifacts
python app/main.py



