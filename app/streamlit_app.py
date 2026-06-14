from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from model_utils import (
    MODEL_FILES,
    editable_numeric_features,
    feature_importance_frame,
    load_model_artifact,
    metric_frame,
    predict_from_row,
    row_label,
)


st.set_page_config(
    page_title="Revenue Forecast Demo",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }
    div[data-testid="stMetric"] {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 0.8rem 0.9rem;
        background: #ffffff;
    }
    section[data-testid="stSidebar"] {
        background: #f8fafc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def cached_artifact(model_file: str) -> dict:
    return load_model_artifact(model_file)


def format_number(value: float | int | None, digits: int = 2) -> str:
    if value is None or pd.isna(value):
        return "-"
    return f"{float(value):,.{digits}f}"


def render_metrics(metrics: dict) -> None:
    cols = st.columns(4)
    cols[0].metric("MAE", format_number(metrics.get("mae")))
    cols[1].metric("RMSE", format_number(metrics.get("rmse")))
    cols[2].metric("WAPE", format_number(metrics.get("wape"), 4))
    cols[3].metric("R2", format_number(metrics.get("r2"), 4))


def scenario_row_controls(artifact: dict, row: pd.Series, model_key: str, row_idx: int) -> pd.Series:
    edited = row.copy()
    numeric_cols = [col for col in editable_numeric_features(artifact) if col in row.index]

    if not numeric_cols:
        return edited

    st.subheader("Scenario")
    grid = st.columns(2)
    for i, col in enumerate(numeric_cols):
        raw_value = row.get(col, 0.0)
        value = 0.0 if pd.isna(raw_value) else float(raw_value)
        step = max(abs(value) * 0.05, 1.0)
        with grid[i % 2]:
            edited[col] = st.number_input(
                col,
                value=value,
                step=float(step),
                format="%.4f",
                key=f"{model_key}-{row_idx}-{col}",
            )
    return edited


def render_prediction(artifact: dict, row: pd.Series) -> None:
    target_col = artifact["target_col"]
    actual = row.get(target_col, np.nan)
    predicted = predict_from_row(artifact, row)
    abs_error = abs(float(actual) - predicted) if pd.notna(actual) else np.nan

    cols = st.columns(3)
    cols[0].metric("Actual", format_number(actual))
    cols[1].metric("Predicted", format_number(predicted))
    cols[2].metric("Abs error", format_number(abs_error))

    compare = pd.DataFrame(
        {"value": [float(actual) if pd.notna(actual) else np.nan, predicted]},
        index=["Actual", "Predicted"],
    )
    st.bar_chart(compare, use_container_width=True, height=240)


def render_context_table(artifact: dict, row: pd.Series) -> None:
    target_col = artifact["target_col"]
    id_cols = [col for col in artifact.get("id_cols", []) if col in row.index]
    scenario_cols = [col for col in editable_numeric_features(artifact) if col in row.index]
    cols = list(dict.fromkeys(id_cols + [target_col] + scenario_cols))
    context = pd.DataFrame([row[cols]])
    st.dataframe(context, use_container_width=True, hide_index=True)


def main() -> None:
    st.title("Revenue Forecast Demo")

    with st.sidebar:
        model_name = st.selectbox("Model", list(MODEL_FILES.keys()))
        model_file = MODEL_FILES[model_name]

    try:
        artifact = cached_artifact(model_file)
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.code("source .venv-streamlit-demo/bin/activate\npython app/train_artifacts.py")
        return

    demo_rows = artifact["demo_rows"].copy()
    target_col = artifact["target_col"]
    labels = [
        row_label(demo_rows.iloc[i], artifact.get("id_cols", []), target_col)
        for i in range(len(demo_rows))
    ]

    with st.sidebar:
        st.caption(artifact["name"])
        row_idx = st.selectbox(
            "Sample",
            range(len(demo_rows)),
            format_func=lambda idx: labels[idx],
        )

    render_metrics(artifact.get("metrics", {}))

    left, right = st.columns([0.42, 0.58], gap="large")
    selected = demo_rows.iloc[int(row_idx)].copy()

    with left:
        edited = scenario_row_controls(artifact, selected, model_file, int(row_idx))

    with right:
        st.subheader("Prediction")
        render_prediction(artifact, edited)

    st.subheader("Selected row")
    render_context_table(artifact, edited)

    tabs = st.tabs(["Feature importance", "Model details"])
    with tabs[0]:
        importance = feature_importance_frame(artifact)
        if importance.empty:
            st.dataframe(pd.DataFrame(), use_container_width=True)
        else:
            chart_data = importance.set_index("feature")
            st.bar_chart(chart_data, use_container_width=True, height=360)
            st.dataframe(importance, use_container_width=True, hide_index=True)

    with tabs[1]:
        details = {
            "source_notebook": artifact.get("source_notebook"),
            "source_data": artifact.get("source_data"),
            "target_col": artifact.get("target_col"),
            "feature_count": len(artifact.get("feature_cols", [])),
            "numeric_feature_count": len(artifact.get("numeric_features", [])),
            "categorical_feature_count": len(artifact.get("categorical_features", [])),
            "trained_at": artifact.get("trained_at"),
            "notes": artifact.get("notes"),
        }
        st.dataframe(pd.DataFrame([details]).T.rename(columns={0: "value"}), use_container_width=True)
        st.dataframe(metric_frame(artifact.get("metrics", {})), use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()
