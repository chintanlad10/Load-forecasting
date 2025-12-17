from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

from project_config import COLUMN_RENAMES, DATA_PATH


def _coerce_numeric(series: pd.Series) -> pd.Series:
    coerced = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace(r"[^0-9.\-]", "", regex=True)
    )
    return pd.to_numeric(coerced, errors="coerce")


def load_clean_dataset(path: Path | None = None) -> pd.DataFrame:
    dataset_path = path or DATA_PATH
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}")

    df = pd.read_csv(dataset_path)
    df = df.rename(columns=COLUMN_RENAMES)
    df["date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.drop(columns=["Date"])
    df = df.dropna(subset=["date"])
    df = df.sort_values("date").reset_index(drop=True)

    numeric_cols = [col for col in df.columns if col != "date"]
    for col in numeric_cols:
        df[col] = _coerce_numeric(df[col])

    df = df.fillna(method="ffill").fillna(method="bfill")

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_of_week"] = df["date"].dt.dayofweek
    df["day_of_year"] = df["date"].dt.dayofyear
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    df = df.drop(columns=["date"])
    return df


def calendar_features(target_date: datetime) -> Dict[str, int]:
    return {
        "year": target_date.year,
        "month": target_date.month,
        "day_of_week": target_date.weekday(),
        "day_of_year": target_date.timetuple().tm_yday,
        "is_weekend": int(target_date.weekday() >= 5),
    }


def default_feature_values(df: pd.DataFrame, feature_keys: Iterable[str]) -> Dict[str, float]:
    medians = df[list(feature_keys)].median(numeric_only=True)
    return {key: float(medians[key]) for key in feature_keys}


def latest_feature_values(df: pd.DataFrame, feature_keys: Iterable[str]) -> Dict[str, float]:
    if df.empty:
        return {key: 0.0 for key in feature_keys}
    latest_row = df.tail(1).iloc[0]
    return {key: float(latest_row[key]) for key in feature_keys}
