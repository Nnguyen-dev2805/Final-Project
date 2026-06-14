from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd


ARTIFACT_DIR = Path(__file__).resolve().parent / "artifacts"


MODEL_FILES = {
    "M5 store-dept revenue": "m5_model.joblib",
    "Maven product-type revenue": "maven_model.joblib",
    "Weather category sales": "weather_sales_model.joblib",
}


def load_model_artifact(model_file: str) -> dict[str, Any]:
    path = ARTIFACT_DIR / model_file
    if not path.exists():
        raise FileNotFoundError(
            f"Missing artifact: {path}. Run `python app/train_artifacts.py` first."
        )
    return joblib.load(path)


def make_prediction_input(row: pd.Series, feature_cols: list[str]) -> pd.DataFrame:
    values = {col: row.get(col, np.nan) for col in feature_cols}
    return pd.DataFrame([values], columns=feature_cols)


def predict_from_row(artifact: dict[str, Any], row: pd.Series) -> float:
    model = artifact["model"]
    feature_cols = artifact["feature_cols"]
    pred = float(model.predict(make_prediction_input(row, feature_cols))[0])
    return max(pred, 0.0)


def metric_frame(metrics: dict[str, Any]) -> pd.DataFrame:
    rows = []
    for key, value in metrics.items():
        if isinstance(value, (int, float, np.integer, np.floating)):
            rows.append({"metric": key, "value": float(value)})
        else:
            rows.append({"metric": key, "value": value})
    return pd.DataFrame(rows)


def feature_importance_frame(artifact: dict[str, Any], top_n: int = 15) -> pd.DataFrame:
    pipeline = artifact["model"]
    if not hasattr(pipeline, "named_steps"):
        return pd.DataFrame()

    preprocessor = pipeline.named_steps.get("preprocessor")
    estimator = pipeline.named_steps.get("model")
    if preprocessor is None or estimator is None or not hasattr(estimator, "feature_importances_"):
        return pd.DataFrame()

    try:
        names = preprocessor.get_feature_names_out()
    except Exception:
        names = np.asarray(artifact.get("feature_cols", []), dtype=object)

    importances = np.asarray(estimator.feature_importances_)
    if len(names) != len(importances):
        return pd.DataFrame()

    frame = pd.DataFrame({"feature": names, "importance": importances})
    frame = frame.sort_values("importance", ascending=False).head(top_n)
    return frame.reset_index(drop=True)


def row_label(row: pd.Series, id_cols: list[str], target_col: str) -> str:
    preferred = [
        "date",
        "store_id",
        "store",
        "dept_id",
        "product_type",
        "category",
        "store_city",
        "store_state",
    ]
    cols = [col for col in preferred if col in row.index and col in id_cols]
    if not cols:
        cols = [col for col in id_cols if col in row.index][:4]

    parts = []
    for col in cols:
        value = row[col]
        if pd.isna(value):
            continue
        if col == "date":
            try:
                value = pd.to_datetime(value).date()
            except Exception:
                pass
        parts.append(f"{col}={value}")

    target_value = row.get(target_col, np.nan)
    if pd.notna(target_value):
        parts.append(f"actual={float(target_value):,.2f}")
    return " | ".join(parts)


def editable_numeric_features(artifact: dict[str, Any]) -> list[str]:
    priority_patterns = [
        "temperature",
        "precipitation",
        "rain",
        "snowfall",
        "wind",
        "shortwave",
        "coupon",
        "revenue_lag",
        "category_sales_lag",
        "roll_mean",
        "rolling",
    ]
    numeric_features = artifact.get("numeric_features", [])
    selected = [
        col
        for col in numeric_features
        if any(pattern in col.lower() for pattern in priority_patterns)
    ]
    if len(selected) < 8:
        selected += [col for col in numeric_features if col not in selected]
    return selected[:10]
