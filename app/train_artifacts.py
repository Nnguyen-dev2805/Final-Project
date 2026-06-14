from __future__ import annotations

import argparse
import json
import warnings
from datetime import datetime
from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


warnings.filterwarnings("ignore", category=FutureWarning)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIR = Path(__file__).resolve().parent
ARTIFACT_DIR = APP_DIR / "artifacts"

MAVEN_DATA = PROJECT_ROOT / "data" / "clean" / "product_type_store_daily_revenue 2.csv"
M5_DATA = (
    PROJECT_ROOT
    / "data"
    / "m5-forecasting-accuracy"
    / "processed"
    / "m5_store_dept_daily_with_weather.csv"
)
WEATHER_DATA = PROJECT_ROOT / "data" / "old dataset" / "dataset3" / "df_category_long.csv"


def ensure_artifact_dir() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def keep_existing(cols: Iterable[str], df: pd.DataFrame) -> list[str]:
    return [col for col in cols if col in df.columns]


def regression_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict[str, float]:
    y_true_arr = np.asarray(y_true, dtype=float)
    y_pred_arr = np.asarray(y_pred, dtype=float)
    mae = mean_absolute_error(y_true_arr, y_pred_arr)
    rmse = root_mean_squared_error(y_true_arr, y_pred_arr)
    denom = np.abs(y_true_arr).sum()
    wape = np.abs(y_true_arr - y_pred_arr).sum() / denom if denom else np.nan
    return {
        "rows": float(len(y_true_arr)),
        "mae": float(mae),
        "rmse": float(rmse),
        "wape": float(wape),
        "r2": float(r2_score(y_true_arr, y_pred_arr)),
    }


def make_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
    categorical_strategy: str = "ordinal",
) -> ColumnTransformer:
    numeric_pipe = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median"))]
    )

    if categorical_strategy == "onehot":
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    else:
        encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)

    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", encoder),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_features),
            ("cat", categorical_pipe, categorical_features),
        ],
        remainder="drop",
    )


def make_pipeline(
    numeric_features: list[str],
    categorical_features: list[str],
    params: dict,
    categorical_strategy: str = "ordinal",
) -> Pipeline:
    return Pipeline(
        steps=[
            (
                "preprocessor",
                make_preprocessor(numeric_features, categorical_features, categorical_strategy),
            ),
            ("model", LGBMRegressor(**params)),
        ]
    )


def sample_demo_rows(
    df: pd.DataFrame,
    feature_cols: list[str],
    id_cols: list[str],
    target_col: str,
    max_rows: int = 500,
    random_state: int = 42,
) -> pd.DataFrame:
    cols = list(dict.fromkeys(keep_existing(id_cols + [target_col] + feature_cols, df)))
    demo = df[cols].copy()
    if len(demo) > max_rows:
        demo = demo.sample(max_rows, random_state=random_state)
    demo = demo.sort_values(keep_existing(["date", "store_id", "store", "dept_id", "product_type", "category"], demo))
    return demo.reset_index(drop=True)


def save_artifact(file_name: str, artifact: dict) -> Path:
    ensure_artifact_dir()
    path = ARTIFACT_DIR / file_name
    joblib.dump(artifact, path, compress=3)
    return path


def train_maven() -> Path:
    print("[maven] Loading product-type revenue data...")
    df = pd.read_csv(MAVEN_DATA)
    df = df.rename(columns={"transaction_date": "date"})
    df["date"] = pd.to_datetime(df["date"])
    for col in ["first_opened_date", "last_remodel_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    df = df.sort_values(["store_id", "product_type", "date"]).reset_index(drop=True)
    group = df.groupby(["store_id", "product_type"], sort=False)

    for lag in [1, 2, 4, 8, 16]:
        df[f"revenue_lag_obs_{lag}"] = group["revenue"].shift(lag)

    shifted = group["revenue"].shift(1)
    for window in [4, 8, 16]:
        df[f"revenue_roll_mean_obs_{window}"] = (
            shifted.groupby([df["store_id"], df["product_type"]])
            .rolling(window, min_periods=2)
            .mean()
            .reset_index(level=[0, 1], drop=True)
        )
        df[f"revenue_roll_std_obs_{window}"] = (
            shifted.groupby([df["store_id"], df["product_type"]])
            .rolling(window, min_periods=2)
            .std()
            .reset_index(level=[0, 1], drop=True)
        )

    df["date_ordinal"] = df["date"].map(pd.Timestamp.toordinal)
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["dow_sin"] = np.sin(2 * np.pi * df["day_of_week_num"] / 7)
    df["dow_cos"] = np.cos(2 * np.pi * df["day_of_week_num"] / 7)
    df["is_month_start"] = df["date"].dt.is_month_start.astype(int)
    df["is_month_end"] = df["date"].dt.is_month_end.astype(int)

    categorical_features = keep_existing(
        [
            "store_id",
            "product_type",
            "store_type",
            "store_city",
            "store_state",
            "sales_district",
            "sales_region",
            "day_of_week",
            "weather_code",
        ],
        df,
    )
    numeric_base = [
        "year",
        "month",
        "quarter",
        "day",
        "day_of_week_num",
        "week_of_year",
        "is_weekend",
        "date_ordinal",
        "month_sin",
        "month_cos",
        "dow_sin",
        "dow_cos",
        "is_month_start",
        "is_month_end",
        "region_id",
        "total_sqft",
        "grocery_sqft",
        "grocery_sqft_ratio",
        "store_age_years",
        "years_since_remodel",
    ]
    numeric_weather = [
        "temperature_mean_c",
        "precipitation_mm",
        "snowfall_cm",
        "wind_speed_max_kmh",
        "shortwave_radiation_mj_m2",
        "is_rainy_day",
        "is_snowy_day",
        "is_windy_day",
    ]
    numeric_history = [
        f"revenue_lag_obs_{lag}" for lag in [1, 2, 4, 8, 16]
    ] + [
        feature
        for window in [4, 8, 16]
        for feature in [f"revenue_roll_mean_obs_{window}", f"revenue_roll_std_obs_{window}"]
    ]
    numeric_features = keep_existing(numeric_base + numeric_weather + numeric_history, df)
    feature_cols = numeric_features + categorical_features

    train_val = df[df["date"] <= "1998-09-30"].copy()
    test = df[df["date"] > "1998-09-30"].copy()

    params = {
        "objective": "regression_l1",
        "n_estimators": 500,
        "learning_rate": 0.05,
        "num_leaves": 31,
        "subsample": 0.85,
        "colsample_bytree": 0.90,
        "min_child_samples": 20,
        "random_state": 42,
        "verbose": -1,
    }
    model = make_pipeline(numeric_features, categorical_features, params, "onehot")
    model.fit(train_val[feature_cols], train_val["revenue"])
    pred = np.clip(model.predict(test[feature_cols]), 0, None)

    artifact = {
        "name": "Maven product-type daily revenue",
        "source_notebook": "notebooks/final-maven-last.ipynb",
        "source_data": str(MAVEN_DATA.relative_to(PROJECT_ROOT)),
        "target_col": "revenue",
        "feature_cols": feature_cols,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "id_cols": keep_existing(["date", "store_id", "store_city", "store_state", "product_type"], df),
        "model": model,
        "metrics": regression_metrics(test["revenue"], pred),
        "demo_rows": sample_demo_rows(
            test,
            feature_cols,
            ["date", "store_id", "store_city", "store_state", "product_type"],
            "revenue",
        ),
        "notes": "Observed-only frame: no synthetic zero-revenue product_type rows.",
        "trained_at": datetime.now().isoformat(timespec="seconds"),
    }
    path = save_artifact("maven_model.joblib", artifact)
    print(f"[maven] Saved {path}")
    print(json.dumps(artifact["metrics"], indent=2))
    return path


def prepare_m5_frame(source_df: pd.DataFrame) -> pd.DataFrame:
    out = source_df.copy()
    out["date"] = pd.to_datetime(out["date"])

    for col in ["event_name_1", "event_type_1", "event_name_2", "event_type_2"]:
        if col in out.columns:
            out[col] = out[col].fillna("No Event").astype(str)

    if "has_sales" not in out.columns:
        out["has_sales"] = (out["daily_revenue"] > 0).astype(int)

    out["store_dept_id"] = out["store_id"].astype(str) + "__" + out["dept_id"].astype(str)
    out["date_index"] = (out["date"] - out["date"].min()).dt.days + 1
    out["month_sin"] = np.sin(2 * np.pi * out["month"] / 12)
    out["month_cos"] = np.cos(2 * np.pi * out["month"] / 12)
    out["dow_sin"] = np.sin(2 * np.pi * out["day_of_week_num"] / 7)
    out["dow_cos"] = np.cos(2 * np.pi * out["day_of_week_num"] / 7)
    out["doy_sin"] = np.sin(2 * np.pi * out["day_of_year"] / 366)
    out["doy_cos"] = np.cos(2 * np.pi * out["day_of_year"] / 366)
    out["week_sin"] = np.sin(2 * np.pi * out["week_of_year"] / 53)
    out["week_cos"] = np.cos(2 * np.pi * out["week_of_year"] / 53)

    out["is_rainy_day"] = (out["precipitation_mm"] > 0).astype(int)
    out["is_heavy_rain_day"] = (out["precipitation_mm"] >= 10).astype(int)
    out["is_snowy_day"] = (out["snowfall_cm"] > 0).astype(int)
    out["is_hot_day"] = (out["temperature_mean_c"] >= 30).astype(int)
    out["is_cold_day"] = (out["temperature_mean_c"] <= 0).astype(int)

    out = out.sort_values(["store_id", "dept_id", "date"]).reset_index(drop=True)
    group = out.groupby(["store_id", "dept_id"], sort=False)

    for lag in [1, 7, 14, 28, 56]:
        out[f"revenue_lag_{lag}"] = group["daily_revenue"].shift(lag)

    shifted = group["daily_revenue"].shift(1)
    for window in [7, 14, 28, 56]:
        out[f"revenue_roll_mean_{window}"] = (
            shifted.groupby([out["store_id"], out["dept_id"]])
            .rolling(window, min_periods=1)
            .mean()
            .reset_index(level=[0, 1], drop=True)
        )

    for window in [7, 28]:
        out[f"revenue_roll_std_{window}"] = (
            shifted.groupby([out["store_id"], out["dept_id"]])
            .rolling(window, min_periods=2)
            .std()
            .reset_index(level=[0, 1], drop=True)
        )

    out["revenue_expanding_mean"] = group["daily_revenue"].transform(
        lambda s: s.shift(1).expanding(min_periods=1).mean()
    )
    out["zero_sales_roll_28"] = (
        group["has_sales"]
        .shift(1)
        .rsub(1)
        .groupby([out["store_id"], out["dept_id"]])
        .rolling(28, min_periods=1)
        .mean()
        .reset_index(level=[0, 1], drop=True)
    )
    return out


def train_m5() -> Path:
    print("[m5] Loading store-dept revenue data...")
    df = pd.read_csv(M5_DATA)
    df = prepare_m5_frame(df)

    history_features = [
        "revenue_lag_1",
        "revenue_lag_7",
        "revenue_lag_14",
        "revenue_lag_28",
        "revenue_lag_56",
        "revenue_roll_mean_7",
        "revenue_roll_mean_14",
        "revenue_roll_mean_28",
        "revenue_roll_mean_56",
        "revenue_roll_std_7",
        "revenue_roll_std_28",
        "revenue_expanding_mean",
        "zero_sales_roll_28",
    ]
    numeric_base = [
        "item_count",
        "snap_active",
        "event_count",
        "date_index",
        "year",
        "month_sin",
        "month_cos",
        "dow_sin",
        "dow_cos",
        "doy_sin",
        "doy_cos",
        "week_sin",
        "week_cos",
        "is_weekend",
    ]
    numeric_weather = [
        "temperature_max_c",
        "temperature_min_c",
        "temperature_mean_c",
        "apparent_temperature_mean_c",
        "precipitation_mm",
        "rain_mm",
        "snowfall_cm",
        "wind_speed_max_kmh",
        "wind_gusts_max_kmh",
        "shortwave_radiation_mj_m2",
        "is_rainy_day",
        "is_heavy_rain_day",
        "is_snowy_day",
        "is_hot_day",
        "is_cold_day",
    ]
    categorical_features = keep_existing(
        [
            "store_id",
            "state_id",
            "cat_id",
            "dept_id",
            "store_dept_id",
            "month",
            "day_of_week_num",
            "event_name_1",
            "event_type_1",
            "event_name_2",
            "event_type_2",
            "weather_code",
        ],
        df,
    )
    numeric_features = keep_existing(numeric_base + history_features + numeric_weather, df)
    feature_cols = numeric_features + categorical_features

    train_val = df[df["year"] <= 2015].copy()
    test = df[df["year"] == 2016].copy()

    params = {
        "objective": "regression_l1",
        "n_estimators": 700,
        "learning_rate": 0.04,
        "num_leaves": 64,
        "max_depth": -1,
        "min_child_samples": 50,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "random_state": 42,
        "n_jobs": -1,
        "verbosity": -1,
    }
    model = make_pipeline(numeric_features, categorical_features, params, "ordinal")
    model.fit(train_val[feature_cols], train_val["daily_revenue"])
    pred = np.clip(model.predict(test[feature_cols]), 0, None)

    artifact = {
        "name": "M5 store-dept daily revenue",
        "source_notebook": "notebooks/final-m5-last.ipynb",
        "source_data": str(M5_DATA.relative_to(PROJECT_ROOT)),
        "target_col": "daily_revenue",
        "feature_cols": feature_cols,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "id_cols": keep_existing(["date", "store_id", "state_id", "cat_id", "dept_id"], df),
        "model": model,
        "metrics": regression_metrics(test["daily_revenue"], pred),
        "demo_rows": sample_demo_rows(
            test,
            feature_cols,
            ["date", "store_id", "state_id", "cat_id", "dept_id"],
            "daily_revenue",
        ),
        "notes": "Feature engineering follows final-m5-last.ipynb with shifted history features.",
        "trained_at": datetime.now().isoformat(timespec="seconds"),
    }
    path = save_artifact("m5_model.joblib", artifact)
    print(f"[m5] Saved {path}")
    print(json.dumps(artifact["metrics"], indent=2))
    return path


def prepare_weather_frame() -> pd.DataFrame:
    usecols = {
        "store",
        "date",
        "scluster",
        "income",
        "poverty",
        "density",
        "hvalmean",
        "nocar",
        "urban",
        "shopindx",
        "compby",
        "min_ddist",
        "mean_ddist",
        "mean_dcvol",
        "max_dcvol",
        "total_sales",
        "price_level",
        "temperature",
        "apparent_temperature",
        "precipitation",
        "category",
        "category_sales",
        "has_category_coupon",
        "category_coupon_abs",
    }
    print("[weather] Loading category sales data. This file is large, please wait...")
    df = pd.read_csv(
        WEATHER_DATA,
        usecols=lambda col: col in usecols,
        parse_dates=["date"],
        low_memory=False,
    )

    if "total_sales" in df.columns:
        df = df[df["total_sales"] > 0].copy()

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["dayofweek"] = df["date"].dt.dayofweek
    df["has_coupon"] = (
        df["has_category_coupon"]
        if "has_category_coupon" in df.columns
        else (df["category_coupon_abs"].fillna(0) > 0)
    ).astype(int)
    df["coupon_abs"] = df["category_coupon_abs"].fillna(0)
    df["is_extreme_rain"] = (df["precipitation"].fillna(0) >= 20).astype(int)
    df["is_very_cold_day"] = (df["temperature"].fillna(0) <= -15).astype(int)

    df = df.sort_values(["store", "category", "date"]).reset_index(drop=True)
    group = df.groupby(["store", "category"], sort=False)

    for lag in [1, 7, 14, 28]:
        df[f"category_sales_lag_{lag}"] = group["category_sales"].shift(lag)

    shifted_sales = group["category_sales"].shift(1)
    for window in [7, 14, 28]:
        df[f"category_sales_roll_mean_{window}"] = (
            shifted_sales.groupby([df["store"], df["category"]])
            .rolling(window, min_periods=1)
            .mean()
            .reset_index(leveldone[0, 1], drop=True)
        )
        df[f"zero_sales_days_prev_{window}"] = (
            shifted_sales.fillna(0)
            .eq(0)
            .astype(int)
            .groupby([df["store"], df["category"]])
            .rolling(window, min_periods=1)
            .sum()
            .reset_index(level=[0, 1], drop=True)
        )

    df["category_sales_roll_median_7"] = (
        shifted_sales.groupby([df["store"], df["category"]])
        .rolling(7, min_periods=1)
        .median()
        .reset_index(level=[0, 1], drop=True)
    )
    df["category_sales_roll_std_7"] = (
        shifted_sales.groupby([df["store"], df["category"]])
        .rolling(7, min_periods=2)
        .std()
        .reset_index(level=[0, 1], drop=True)
    )

    for lag in [1, 7]:
        df[f"has_coupon_lag_{lag}"] = group["has_coupon"].shift(lag)
        df[f"coupon_abs_lag_{lag}"] = group["coupon_abs"].shift(lag)

    shifted_coupon = group["has_coupon"].shift(1)
    shifted_coupon_abs = group["coupon_abs"].shift(1)
    df["coupon_days_prev_7"] = (
        shifted_coupon.groupby([df["store"], df["category"]])
        .rolling(7, min_periods=1)
        .sum()
        .reset_index(level=[0, 1], drop=True)
    )
    df["coupon_abs_prev_7"] = (
        shifted_coupon_abs.groupby([df["store"], df["category"]])
        .rolling(7, min_periods=1)
        .sum()
        .reset_index(level=[0, 1], drop=True)
    )

    final_cols = [
        "category_sales",
        "store",
        "category",
        "date",
        "scluster",
        "price_level",
        "month",
        "dayofweek",
        "compby",
        "income",
        "poverty",
        "density",
        "hvalmean",
        "nocar",
        "urban",
        "shopindx",
        "category_sales_lag_1",
        "category_sales_lag_7",
        "category_sales_lag_14",
        "category_sales_lag_28",
        "category_sales_roll_mean_7",
        "category_sales_roll_mean_14",
        "category_sales_roll_mean_28",
        "category_sales_roll_median_7",
        "category_sales_roll_std_7",
        "zero_sales_days_prev_7",
        "zero_sales_days_prev_14",
        "zero_sales_days_prev_28",
        "has_coupon_lag_1",
        "has_coupon_lag_7",
        "coupon_abs_lag_1",
        "coupon_abs_lag_7",
        "coupon_days_prev_7",
        "coupon_abs_prev_7",
        "min_ddist",
        "mean_ddist",
        "mean_dcvol",
        "max_dcvol",
        "is_extreme_rain",
        "is_very_cold_day",
        "apparent_temperature",
    ]
    df = df[keep_existing(final_cols, df)].replace([np.inf, -np.inf], np.nan)
    df["category_sales"] = df["category_sales"].clip(lower=0)
    return df.dropna().reset_index(drop=True)


def train_weather_sales(max_train_rows: int = 350_000, max_test_rows: int = 150_000) -> Path:
    df = prepare_weather_frame()

    categorical_features = keep_existing(
        ["store", "category", "scluster", "price_level", "month", "dayofweek", "compby"],
        df,
    )
    feature_cols = [col for col in df.columns if col not in ["category_sales", "date"]]
    numeric_features = [col for col in feature_cols if col not in categorical_features]

    train = df[df["date"].dt.year.isin([1990, 1991, 1992])].copy()
    test = df[df["date"].dt.year == 1993].copy()

    train_used = train
    if len(train_used) > max_train_rows:
        train_used = train_used.sample(max_train_rows, random_state=42)

    test_used = test
    if len(test_used) > max_test_rows:
        test_used = test_used.sample(max_test_rows, random_state=42)

    params = {
        "objective": "regression_l1",
        "n_estimators": 350,
        "learning_rate": 0.05,
        "num_leaves": 64,
        "max_depth": -1,
        "min_child_samples": 50,
        "subsample": 0.85,
        "colsample_bytree": 0.85,
        "reg_alpha": 0.1,
        "reg_lambda": 1.0,
        "random_state": 42,
        "n_jobs": -1,
        "verbosity": -1,
    }
    model = make_pipeline(numeric_features, categorical_features, params, "ordinal")
    model.fit(train_used[feature_cols], train_used["category_sales"])
    pred = np.clip(model.predict(test_used[feature_cols]), 0, None)

    artifact = {
        "name": "Weather category daily sales",
        "source_notebook": "notebooks/final_weather_sales_project_report.ipynb",
        "source_data": str(WEATHER_DATA.relative_to(PROJECT_ROOT)),
        "target_col": "category_sales",
        "feature_cols": feature_cols,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "id_cols": keep_existing(["date", "store", "category", "scluster", "price_level"], df),
        "model": model,
        "metrics": regression_metrics(test_used["category_sales"], pred),
        "demo_rows": sample_demo_rows(
            test,
            feature_cols,
            ["date", "store", "category", "scluster", "price_level"],
            "category_sales",
        ),
        "notes": (
            "Trained on a reproducible sample for a fast Streamlit demo. "
            f"train_rows_used={len(train_used):,}; test_rows_scored={len(test_used):,}."
        ),
        "trained_at": datetime.now().isoformat(timespec="seconds"),
    }
    path = save_artifact("weather_sales_model.joblib", artifact)
    print(f"[weather] Saved {path}")
    print(json.dumps(artifact["metrics"], indent=2))
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Streamlit demo artifacts.")
    parser.add_argument(
        "--models",
        nargs="+",
        default=["m5", "maven", "weather"],
        choices=["m5", "maven", "weather"],
        help="Artifacts to train.",
    )
    parser.add_argument("--weather-max-train-rows", type=int, default=350_000)
    parser.add_argument("--weather-max-test-rows", type=int, default=150_000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requested = set(args.models)
    paths = []
    if "m5" in requested:
        paths.append(train_m5())
    if "maven" in requested:
        paths.append(train_maven())
    if "weather" in requested:
        paths.append(
            train_weather_sales(
                max_train_rows=args.weather_max_train_rows,
                max_test_rows=args.weather_max_test_rows,
            )
        )

    print("\nArtifacts created:")
    for path in paths:
        print(f"- {path.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
