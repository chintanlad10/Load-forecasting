from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor

from data_utils import load_clean_dataset
from project_config import (
    ARTIFACT_DIR,
    BASE_DIR,
    DATA_PATH,
    MODEL_DIR,
    MODEL_PATH,
    REPORT_PATH,
)


@dataclass
class DatasetSplit:
    features: pd.DataFrame
    target: pd.Series


def safe_mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.where(np.abs(y_true) < 1e-3, 1e-3, y_true)
    return float(np.mean(np.abs((y_true - y_pred) / y_true)))


def split_dataset(df: pd.DataFrame, target_col: str) -> Tuple[DatasetSplit, DatasetSplit, List[str]]:
    if target_col not in df.columns:
        raise ValueError(f"{target_col} is not available in the dataframe columns.")

    feature_cols = [col for col in df.columns if col != target_col]
    target = df[target_col]

    split_index = int(len(df) * 0.85)
    train_features = df.loc[: split_index - 1, feature_cols]
    test_features = df.loc[split_index:, feature_cols]
    train_target = target.iloc[:split_index]
    test_target = target.iloc[split_index:]

    return DatasetSplit(train_features, train_target), DatasetSplit(test_features, test_target), feature_cols


def train_model(train_split: DatasetSplit, feature_names: List[str]) -> Pipeline:
    model = XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.9,
        colsample_bytree=0.9,
        reg_lambda=1.0,
        random_state=42,
        objective="reg:squarederror",
        tree_method="hist",
    )

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("model", model),
        ]
    )

    pipeline.fit(train_split.features[feature_names], train_split.target)
    return pipeline


def evaluate_model(pipeline: Pipeline, split: DatasetSplit, feature_names: List[str]) -> Dict[str, float]:
    predictions = pipeline.predict(split.features[feature_names])
    mae = mean_absolute_error(split.target, predictions)
    mape = safe_mape(split.target.to_numpy(), predictions)
    r2 = r2_score(split.target, predictions)
    return {"mae": mae, "mape": mape, "r2": r2}


def save_artifacts(pipeline: Pipeline, feature_names: List[str], metrics: Dict[str, float]) -> None:
    MODEL_DIR.mkdir(exist_ok=True)
    ARTIFACT_DIR.mkdir(exist_ok=True)

    joblib.dump(
        {
            "pipeline": pipeline,
            "feature_names": feature_names,
        },
        MODEL_PATH,
    )

    report = {
        "model_path": str(MODEL_PATH.relative_to(BASE_DIR)),
        "features": feature_names,
        "metrics": metrics,
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2))


def main() -> None:
    df = load_clean_dataset(DATA_PATH)
    target_column = "energy_required_mu"
    train_split, test_split, feature_names = split_dataset(df, target_column)

    pipeline = train_model(train_split, feature_names)
    metrics = evaluate_model(pipeline, test_split, feature_names)
    save_artifacts(pipeline, feature_names, metrics)

    print(
        f"Training complete. Model saved to {MODEL_PATH}. "
        f"Test MAPE: {metrics['mape'] * 100:.2f}%"
    )


if __name__ == "__main__":
    main()
