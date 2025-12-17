from __future__ import annotations

import json
import warnings
from datetime import datetime
from typing import Any, Dict

import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request
from sklearn.exceptions import InconsistentVersionWarning

from data_utils import (
    calendar_features,
    default_feature_values,
    latest_feature_values,
    load_clean_dataset,
)
from project_config import (
    DATA_PATH,
    MODEL_PATH,
    REPORT_PATH,
    USER_INPUT_FEATURES,
)


DATE_FMT = "%Y-%m-%d"
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
warnings.filterwarnings("ignore", message=".*serialized model.*", category=UserWarning)
METHOD_CARDS = [
    {
        "title": "LSTM",
        "tagline": "Deep temporal memory",
        "details": "Benchmarked a sequence-to-one LSTM to capture complex seasonality from raw demand curves.",
    },
    {
        "title": "GRU",
        "tagline": "Faster recurrent gating",
        "details": "Paired GRUs with engineered load features to test a lighter recurrent alternative.",
    },
    {
        "title": "XGBoost",
        "tagline": "Best-performing core model",
        "details": "Tree boosting on calendar + supply mix features delivered the lowest validation MAPE (≈2%).",
    },
    {
        "title": "Stacked Ensemble",
        "tagline": "Safety net for extremes",
        "details": "Meta learner blends neural baselines with gradient boosted trees for stress scenarios.",
    },
]


def load_model_bundle():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Missing trained model at {MODEL_PATH}. Run train_model.py first."
        )
    return joblib.load(MODEL_PATH)


def load_training_report() -> Dict[str, Any]:
    if REPORT_PATH.exists():
        return json.loads(REPORT_PATH.read_text())
    return {}


def latest_observations(rows: int = 5) -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])
    df = df.sort_values("Date").tail(rows).copy()
    df["Date"] = df["Date"].dt.date
    return df


model_bundle = load_model_bundle()
pipeline = model_bundle["pipeline"]
feature_order = model_bundle["feature_names"]

clean_df = load_clean_dataset(DATA_PATH)
user_feature_keys = [item["key"] for item in USER_INPUT_FEATURES]
default_inputs = default_feature_values(clean_df, user_feature_keys)
latest_inputs = latest_feature_values(clean_df, user_feature_keys)
training_report = load_training_report()
recent_rows = latest_observations()
if not recent_rows.empty:
    last_date_value = recent_rows["Date"].max()
    default_date = last_date_value.isoformat() if hasattr(last_date_value, "isoformat") else str(last_date_value)
else:
    default_date = datetime.today().strftime(DATE_FMT)

stress_inputs = dict(latest_inputs)
stress_inputs["unrestricted_peak_demand_mw"] = stress_inputs.get("unrestricted_peak_demand_mw", 0) * 1.08
stress_inputs["deficit_surplus_mw"] = stress_inputs.get("deficit_surplus_mw", 0) - 200
stress_inputs["energy_delta_mu"] = stress_inputs.get("energy_delta_mu", 0) - 15

SCENARIO_PRESETS = [
    {
        "id": "latest",
        "label": "Latest recorded day",
        "description": "Uses the most recent cleaned row as the baseline, perfect for quick what-if tweaks.",
        "values": latest_inputs,
    },
    {
        "id": "median",
        "label": "Typical (median) day",
        "description": "Median across the full historical range. Helpful when you only know broad trends.",
        "values": default_inputs,
    },
    {
        "id": "stress",
        "label": "Stress demand (+8% peak, -200 MW reserve)",
        "description": "Pushes peak demand higher and increases deficit to simulate extreme heat-wave days.",
        "values": stress_inputs,
    },
]

SCENARIO_DEFAULTS = {scenario["id"]: scenario["values"] for scenario in SCENARIO_PRESETS}

app = Flask(__name__)


def build_feature_frame(payload: Dict[str, Any]) -> pd.DataFrame:
    target_date = payload.get("target_date")
    if not target_date:
        raise ValueError("Target date is required.")
    try:
        parsed_date = datetime.strptime(target_date, DATE_FMT)
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")

    scenario_id = payload.get("scenario_id") or "latest"
    scenario_defaults = SCENARIO_DEFAULTS.get(scenario_id, default_inputs)

    feature_values: Dict[str, float] = {}
    for item in USER_INPUT_FEATURES:
        raw_value = payload.get(item["key"])
        if raw_value is None or raw_value == "":
            feature_values[item["key"]] = scenario_defaults.get(item["key"], default_inputs.get(item["key"], 0.0))
            continue
        try:
            feature_values[item["key"]] = float(raw_value)
        except ValueError as exc:
            raise ValueError(f"Invalid number for {item['label']}") from exc

    feature_values.update(calendar_features(parsed_date))
    missing = [col for col in feature_order if col not in feature_values]
    if missing:
        raise ValueError(f"Missing engineered features: {', '.join(missing)}")

    ordered = {col: feature_values[col] for col in feature_order}
    return pd.DataFrame([ordered])


@app.get("/")
def index():
    stats = training_report.get("metrics", {})
    mape_pct = stats.get("mape", 0) * 100 if stats else None
    mae = stats.get("mae")
    return render_template(
        "index.html",
        feature_schema=USER_INPUT_FEATURES,
        default_inputs=default_inputs,
        default_date=default_date,
        scenario_presets=SCENARIO_PRESETS,
        metrics={
            "mape": mape_pct,
            "mae": mae,
            "r2": stats.get("r2"),
        },
        last_trained=training_report.get("model_path"),
        recent_rows=recent_rows.to_dict(orient="records"),
        method_cards=METHOD_CARDS,
    )


@app.post("/predict")
def predict():
    payload: Dict[str, Any]
    if request.is_json:
        payload = request.get_json() or {}
    else:
        payload = request.form.to_dict()

    try:
        frame = build_feature_frame(payload)
        prediction = float(pipeline.predict(frame)[0])
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    return jsonify(
        {
            "prediction": prediction,
            "unit": "MU",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
