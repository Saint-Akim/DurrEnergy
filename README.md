# DurrEnergyApp

A self-contained Streamlit dashboard app for solar performance analytics.

## Contents
- `app_ultra_modern_improved.py` – main Streamlit app
- `.streamlit/config.toml` – Streamlit theme/config
- Data files used by the app (CSV/XLSX)
- `test_ultra_modern_app.py` – optional smoke test

## Quick start
1) Install Python 3.10+
2) Create/activate a virtual environment (recommended)
3) Install requirements:
   - Minimal: `pip install streamlit pandas plotly requests openpyxl numpy`
4) Run the app:
   - `streamlit run app_ultra_modern_improved.py`

## Smoke test (optional)
Run a quick compatibility check:

```bash
python test_ultra_modern_app.py
```

## Notes
- The app prefers local data files in this folder. If a file is missing, it may attempt to fetch from GitHub.
- For deployment (Docker/Heroku/etc.), add a full `requirements.txt` and deployment manifests as needed.
