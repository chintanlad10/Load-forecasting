## Greenfield City Energy Forecasting UI

This repository packages the entire AP Power Supply capstone workflow—from data cleaning and model training to a creative web experience that planners can use to generate daily demand forecasts on demand.

### What's inside

- **`train_model.py`** – deterministic training pipeline that cleans the CSV, engineers calendar signals, fits XGBoost, evaluates on the most recent 15 % of the timeline, and stores the model/metrics.
- **`models/xgboost_energy_requirement.joblib`** – serialized pipeline (imputer + XGBoost) plus feature ordering for inference.
- **`artifacts/training_report.json`** – experiment metadata (features, MAPE/MAE/R²) so the UI can surface live numbers.
- **`app.py` + `templates/` + `static/`** – Flask backend with a UX-focused single-page site that showcases the research story and exposes the prediction form.
- **`project_config.py` / `data_utils.py`** – shared constants and helpers to avoid inconsistent preprocessing between training and inference.

### Quick start

1. **Set up Python deps**

   ```powershell
   python -m venv .venv
   .\\.venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

2. **Train / refresh the model**

   ```powershell
   python train_model.py
   ```

   - Cleans `AP-PowerSupply.csv`, adds calendar features, splits chronologically (85 % / 15 %).
   - Stores the fitted pipeline under `models/` and evaluation stats under `artifacts/`.

3. **Launch the UX**

   ```powershell
   python app.py
   ```

   Visit `http://127.0.0.1:5000` to explore the storytelling sections, review live metrics, and submit scenarios. The form accepts the same operational fields used in the dataset, automatically injects calendar features from the chosen date, and calls `/predict` via Fetch for instant results.

### Scenario presets & light-touch inputs

- Choose among three presets (Latest day, Median profile, Stress demand) to auto-fill the entire form with realistic baselines.
- Tweak only the fields you actually know—leave the rest blank and the backend will fall back to the active preset, so you no longer need to provide every single number.
- The “Input cheat sheet” on the page explains each field in plain language, making it clear what real-world value should be entered.

### Customising inputs

- All human-entered fields are described in `project_config.USER_INPUT_FEATURES`. Update the descriptions or add/remove keys there and re-run `train_model.py` if the feature set changes.
- Default field values are computed from the median of the cleaned dataset. If you want seeded scenarios (e.g. last observed day), adjust `default_feature_values` in `data_utils.py`.

### Testing the API without the UI

```powershell
python -c "from app import app, default_inputs, default_date; client = app.test_client(); payload = {'target_date': default_date, **default_inputs}; print(client.post('/predict', json=payload).json)"
```

### Next ideas

1. Persist multiple historical models with their review-stage metrics and add a drop-down to compare live.
2. Stream automatic forecasts for the next 7 days using the latest recorded row plus scenario inputs.
3. Wire alerts (email/Teams) when predicted demand crosses user-defined thresholds.
