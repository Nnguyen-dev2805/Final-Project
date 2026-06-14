# %% [markdown]
# # Phân tích Data Science tiếp theo cho M5
#
# File này được viết để copy từng cell vào `notebooks/m5/clean_m5.ipynb`.
#
# Giả định bạn đã chạy xong các cell trước đó và đang có biến:
#
# - `m5_daily`
# - `PROJECT_ROOT`
#
# Bảng `m5_daily` hiện đang ở mức:
#
# ```text
# date + store_id + dept_id -> daily_units, daily_revenue
# ```
#
# Mục tiêu của các cell dưới đây:
#
# 1. Kiểm tra chất lượng dữ liệu sau join.
# 2. Đánh giá bias/variation theo kiến thức môn học.
# 3. Phân tích phân phối doanh thu.
# 4. Phân tích theo category, department, store, state, thời gian, event và SNAP.
# 5. Dùng box plot và bootstrap để định lượng uncertainty.
# 6. Kết luận M5 có phù hợp với scope `daily retail revenue forecasting` hay không.

# %%
# Cell 1 - Chuẩn bị môi trường phân tích
#
# Cell này đảm bảo notebook đã có `m5_daily`, import đủ thư viện,
# tạo thêm một số cột phục vụ phân tích như `has_sales`, `log_daily_revenue`.

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

try:
    from IPython.display import display
except Exception:
    display = print

pd.set_option("display.max_columns", 100)
pd.set_option("display.float_format", "{:,.3f}".format)

if "m5_daily" not in globals():
    raise ValueError(
        "Bạn cần chạy các cell trước để tạo biến `m5_daily` trước khi chạy phần phân tích này."
    )

m5_daily = m5_daily.copy()
m5_daily["date"] = pd.to_datetime(m5_daily["date"])

m5_daily["has_sales"] = (m5_daily["daily_units"] > 0).astype(int)
m5_daily["log1p_daily_revenue"] = np.log1p(m5_daily["daily_revenue"])

print("M5 daily shape:", m5_daily.shape)
print("Date range:", m5_daily["date"].min(), "->", m5_daily["date"].max())
display(m5_daily.head())

# %%
# Cell 2 - Kiểm tra chất lượng dữ liệu sau join
#
# Cell này trả lời các câu hỏi:
# - Có duplicate key không?
# - Có missing value quan trọng không?
# - Có doanh thu âm không?
# - Có dòng không bán hàng không?
#
# Đây là phần dùng cho mục "data quality" trong báo cáo.

key_cols = ["date", "store_id", "dept_id"]

quality_summary = pd.DataFrame(
    [
        ("rows", len(m5_daily)),
        ("columns", m5_daily.shape[1]),
        ("duplicate_keys_date_store_dept", int(m5_daily.duplicated(key_cols).sum())),
        ("date_min", m5_daily["date"].min()),
        ("date_max", m5_daily["date"].max()),
        ("store_count", m5_daily["store_id"].nunique()),
        ("state_count", m5_daily["state_id"].nunique()),
        ("category_count", m5_daily["cat_id"].nunique()),
        ("department_count", m5_daily["dept_id"].nunique()),
        ("zero_revenue_rows", int((m5_daily["daily_revenue"] == 0).sum())),
        ("zero_revenue_pct", round((m5_daily["daily_revenue"] == 0).mean() * 100, 3)),
        ("negative_revenue_rows", int((m5_daily["daily_revenue"] < 0).sum())),
        ("missing_weighted_avg_price", int(m5_daily["weighted_avg_sell_price"].isna().sum())),
    ],
    columns=["metric", "value"],
)

missing_summary = (
    m5_daily.isna()
    .sum()
    .reset_index()
    .rename(columns={"index": "column", 0: "missing_count"})
)
missing_summary["missing_pct"] = missing_summary["missing_count"] / len(m5_daily) * 100
missing_summary = missing_summary.sort_values("missing_count", ascending=False)

print("Quality summary:")
display(quality_summary)

print("Missing summary:")
display(missing_summary)

# %%
# Cell 3 - Giải thích missing value của `weighted_avg_sell_price`
#
# `weighted_avg_sell_price` bị thiếu khi `daily_units = 0`.
# Đây là missing có ý nghĩa, không phải lỗi dữ liệu, vì:
#
# ```text
# weighted_avg_sell_price = daily_revenue / daily_units
# ```
#
# Nếu `daily_units = 0` thì giá weighted average không xác định.

price_missing_check = m5_daily[m5_daily["weighted_avg_sell_price"].isna()].copy()

print("Rows missing weighted_avg_sell_price:", len(price_missing_check))
print("Trong các dòng này, daily_units unique:", price_missing_check["daily_units"].unique())
print("Trong các dòng này, daily_revenue unique:", price_missing_check["daily_revenue"].unique())

display(price_missing_check.head(10))

price_missing_interpretation = pd.DataFrame(
    [
        {
            "issue": "weighted_avg_sell_price bị NaN",
            "cause": "daily_units = 0 nên không thể lấy daily_revenue / daily_units",
            "is_bad_missing": "Không",
            "recommended_action": "Giữ dòng doanh thu 0; tạo `has_sales`; khi model cần price thì fill bằng median theo store-dept hoặc dept",
        }
    ]
)

display(price_missing_interpretation)

# %%
# Cell 4 - Đánh giá bias theo kiến thức môn học
#
# Áp dụng nhóm kiến thức "Types of Bias":
# - Coverage bias
# - Selection bias
# - Nonresponse bias
# - Measurement bias
#
# Mục tiêu: không chỉ thống kê dữ liệu, mà còn đánh giá dữ liệu nói được gì
# và không nói được gì.

bias_audit = pd.DataFrame(
    [
        {
            "bias_type": "Coverage bias",
            "risk_in_m5": "Trung bình",
            "evidence": "M5 chỉ gồm 10 stores của Walmart tại CA, TX, WI; không đại diện cho toàn bộ retail/grocery Mỹ.",
            "impact": "Không nên kết luận rộng cho toàn bộ thị trường bán lẻ.",
            "action": "Giới hạn scope: Walmart-like retail stores ở 3 bang; khi gộp dataset khác cần dùng `source_dataset`.",
        },
        {
            "bias_type": "Selection bias",
            "risk_in_m5": "Trung bình",
            "evidence": "Dataset chỉ chứa các item/store được Walmart/Kaggle chọn; không rõ tiêu chí chọn store/item.",
            "impact": "Một số store hoặc product pattern có thể bị thiếu.",
            "action": "Báo cáo rõ phạm vi; không suy luận quá rộng ngoài dữ liệu.",
        },
        {
            "bias_type": "Nonresponse bias",
            "risk_in_m5": "Thấp / không phù hợp",
            "evidence": "M5 không phải survey nên không có đối tượng không phản hồi.",
            "impact": "Không phải bias chính của dataset này.",
            "action": "Không cần xử lý như survey, nhưng vẫn kiểm tra missing values.",
        },
        {
            "bias_type": "Measurement bias",
            "risk_in_m5": "Trung bình",
            "evidence": "Revenue không đo trực tiếp mà ước tính từ daily units * weekly price.",
            "impact": "Doanh thu ngày có thể chưa phản ánh thay đổi giá trong ngày nếu giá thực tế thay đổi trong tuần.",
            "action": "Ghi rõ revenue là estimated revenue; kiểm tra missing price và giá bất thường.",
        },
    ]
)

display(bias_audit)

# %%
# Cell 5 - Đánh giá variation và độ bất định
#
# Áp dụng nhóm kiến thức "Types of Variation":
# - Sampling variation: kết luận có thể thay đổi nếu xét sample khác.
# - Measurement error: revenue phụ thuộc price theo tuần.
# - Time variation: dữ liệu sales theo ngày có seasonal/trend.
#
# Cell này tạo bảng variation audit để đưa vào report.

variation_audit = pd.DataFrame(
    [
        {
            "variation_type": "Sampling variation",
            "risk_in_m5": "Thấp đến trung bình",
            "evidence": "Dữ liệu lớn nhưng vẫn chỉ là 10 stores và 3 states.",
            "analysis_plan": "Dùng bootstrap confidence interval cho mean revenue và so sánh event/SNAP.",
        },
        {
            "variation_type": "Measurement error",
            "risk_in_m5": "Trung bình",
            "evidence": "daily_revenue = daily_units * weekly sell_price; giá không đổi trong tuần.",
            "analysis_plan": "Kiểm tra price distribution, outlier price, và ghi rõ giả định.",
        },
        {
            "variation_type": "Time variation",
            "risk_in_m5": "Cao",
            "evidence": "Retail sales có seasonality theo ngày trong tuần, tháng, event.",
            "analysis_plan": "Phân tích trend, weekday/weekend, event, SNAP, rolling average.",
        },
    ]
)

display(variation_audit)

# %%
# Cell 6 - Thống kê tổng thể doanh thu và sản lượng
#
# Cell này tạo các chỉ số tổng quan:
# - Tổng doanh thu ước tính
# - Tổng số lượng bán
# - Doanh thu trung bình/median
# - Tỷ lệ dòng không bán
#
# Đây là bảng "thống kê tổng thể" cho Dataset M5.

overall_stats = pd.DataFrame(
    [
        ("total_estimated_revenue", m5_daily["daily_revenue"].sum()),
        ("total_units_sold", m5_daily["daily_units"].sum()),
        ("mean_daily_revenue_per_store_dept", m5_daily["daily_revenue"].mean()),
        ("median_daily_revenue_per_store_dept", m5_daily["daily_revenue"].median()),
        ("max_daily_revenue_per_store_dept", m5_daily["daily_revenue"].max()),
        ("mean_daily_units_per_store_dept", m5_daily["daily_units"].mean()),
        ("median_daily_units_per_store_dept", m5_daily["daily_units"].median()),
        ("zero_revenue_pct", (m5_daily["daily_revenue"] == 0).mean() * 100),
        ("event_day_row_pct", (m5_daily["event_flag"] == 1).mean() * 100),
        ("snap_active_row_pct", (m5_daily["snap_active"] == 1).mean() * 100),
    ],
    columns=["metric", "value"],
)

display(overall_stats)

display(
    m5_daily[["daily_units", "daily_revenue", "weighted_avg_sell_price", "active_item_count", "item_count"]]
    .describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
)

# %%
# Cell 7 - Phân tích phân phối doanh thu
#
# Áp dụng kiến thức visualization:
# - Histogram để xem phân phối.
# - Log transform để xử lý revenue lệch phải.
# - Box plot để nhìn median/IQR/outlier.
#
# Lưu ý: outlier trong retail không tự động là lỗi, có thể là ngày bán rất mạnh.

fig, axes = plt.subplots(1, 3, figsize=(18, 4))

axes[0].hist(m5_daily["daily_revenue"], bins=60)
axes[0].set_title("Distribution of Daily Revenue")
axes[0].set_xlabel("daily_revenue")
axes[0].set_ylabel("count")
axes[0].grid(True, alpha=0.3)

axes[1].hist(m5_daily["log1p_daily_revenue"], bins=60)
axes[1].set_title("Distribution of log1p(Daily Revenue)")
axes[1].set_xlabel("log1p_daily_revenue")
axes[1].set_ylabel("count")
axes[1].grid(True, alpha=0.3)

axes[2].boxplot(m5_daily["daily_revenue"], vert=True, showfliers=True)
axes[2].set_title("Box Plot of Daily Revenue")
axes[2].set_ylabel("daily_revenue")
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

revenue_distribution_notes = pd.DataFrame(
    [
        {
            "observation": "Doanh thu có xu hướng lệch phải",
            "evidence": "Mean thường lớn hơn median; histogram raw có đuôi phải.",
            "meaning": "Một số store-dept-day có doanh thu rất cao so với phần lớn ngày bình thường.",
            "next_action": "Khi model có thể dùng log transform hoặc metric ít nhạy outlier như MAE/WAPE.",
        }
    ]
)

display(revenue_distribution_notes)

# %%
# Cell 8 - Phân tích theo category và department
#
# Câu hỏi:
# - Category nào đóng góp doanh thu lớn nhất?
# - Department nào là động lực chính?
# - Department nào có doanh thu biến động mạnh?
#
# Đây là insight cốt lõi cho phần domain/topic.

dept_summary = (
    m5_daily.groupby(["cat_id", "dept_id"], as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        std_daily_revenue=("daily_revenue", "std"),
        max_daily_revenue=("daily_revenue", "max"),
        zero_revenue_pct=("daily_revenue", lambda s: (s == 0).mean() * 100),
        avg_price=("weighted_avg_sell_price", "mean"),
        avg_active_items=("active_item_count", "mean"),
        item_count=("item_count", "max"),
    )
)

dept_summary["revenue_share_pct"] = dept_summary["total_revenue"] / dept_summary["total_revenue"].sum() * 100
dept_summary["cv_revenue"] = dept_summary["std_daily_revenue"] / dept_summary["avg_daily_revenue"]
dept_summary = dept_summary.sort_values("total_revenue", ascending=False)

cat_summary = (
    m5_daily.groupby("cat_id", as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        zero_revenue_pct=("daily_revenue", lambda s: (s == 0).mean() * 100),
    )
)
cat_summary["revenue_share_pct"] = cat_summary["total_revenue"] / cat_summary["total_revenue"].sum() * 100
cat_summary = cat_summary.sort_values("total_revenue", ascending=False)

display(cat_summary)
display(dept_summary)

plt.figure(figsize=(10, 5))
plt.bar(dept_summary["dept_id"], dept_summary["total_revenue"])
plt.title("M5 - Total Revenue by Department")
plt.xlabel("Department")
plt.ylabel("Total Estimated Revenue")
plt.xticks(rotation=45)
plt.grid(True, axis="y", alpha=0.3)
plt.show()

# %%
# Cell 9 - Box plot doanh thu theo department
#
# Áp dụng kiến thức Box Plot:
# - So sánh median và IQR giữa các department.
# - Phát hiện outlier, nhưng không tự động xóa.

dept_order = dept_summary["dept_id"].tolist()
box_data = [m5_daily.loc[m5_daily["dept_id"] == dept, "daily_revenue"] for dept in dept_order]

plt.figure(figsize=(12, 5))
plt.boxplot(box_data, labels=dept_order, showfliers=False)
plt.title("M5 - Daily Revenue Distribution by Department")
plt.xlabel("Department")
plt.ylabel("Daily Revenue")
plt.xticks(rotation=45)
plt.grid(True, axis="y", alpha=0.3)
plt.show()

boxplot_notes = pd.DataFrame(
    [
        {
            "note": "Box plot không hiển thị outlier để dễ nhìn median/IQR.",
            "interpretation": "Department có median cao và IQR rộng thường vừa có doanh thu cao vừa biến động mạnh.",
            "caution": "Không xóa outlier chỉ vì box plot; cần xem outlier có phải ngày event/seasonality/store lớn hay không.",
        }
    ]
)

display(boxplot_notes)

# %%
# Cell 10 - Phân tích theo state và store
#
# Câu hỏi:
# - Bang nào đóng góp doanh thu lớn nhất?
# - Store nào bán mạnh nhất?
# - Có store nào quá khác biệt không?

state_summary = (
    m5_daily.groupby("state_id", as_index=False)
    .agg(
        stores=("store_id", "nunique"),
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        zero_revenue_pct=("daily_revenue", lambda s: (s == 0).mean() * 100),
    )
)
state_summary["revenue_share_pct"] = state_summary["total_revenue"] / state_summary["total_revenue"].sum() * 100
state_summary = state_summary.sort_values("total_revenue", ascending=False)

store_summary = (
    m5_daily.groupby(["state_id", "store_id"], as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        zero_revenue_pct=("daily_revenue", lambda s: (s == 0).mean() * 100),
    )
)
store_summary["revenue_share_pct"] = store_summary["total_revenue"] / store_summary["total_revenue"].sum() * 100
store_summary = store_summary.sort_values("total_revenue", ascending=False)

display(state_summary)
display(store_summary)

plt.figure(figsize=(10, 5))
plt.bar(store_summary["store_id"], store_summary["total_revenue"])
plt.title("M5 - Total Revenue by Store")
plt.xlabel("Store")
plt.ylabel("Total Estimated Revenue")
plt.xticks(rotation=45)
plt.grid(True, axis="y", alpha=0.3)
plt.show()

# %%
# Cell 11 - Heatmap store x department
#
# Cell này giúp nhìn cấu trúc doanh thu theo hai chiều:
# - Store
# - Department
#
# Đây là dạng dashboard/visual summary đơn giản, hữu ích cho report.

store_dept_pivot = m5_daily.pivot_table(
    index="store_id",
    columns="dept_id",
    values="daily_revenue",
    aggfunc="sum",
    fill_value=0,
)

plt.figure(figsize=(12, 6))
plt.imshow(store_dept_pivot.values, aspect="auto")
plt.colorbar(label="Total Estimated Revenue")
plt.xticks(range(len(store_dept_pivot.columns)), store_dept_pivot.columns, rotation=45)
plt.yticks(range(len(store_dept_pivot.index)), store_dept_pivot.index)
plt.title("M5 - Revenue Heatmap: Store x Department")
plt.xlabel("Department")
plt.ylabel("Store")
plt.tight_layout()
plt.show()

display(store_dept_pivot)

# %%
# Cell 12 - Phân tích xu hướng thời gian
#
# Câu hỏi:
# - Tổng doanh thu theo ngày thay đổi như thế nào?
# - Có xu hướng tăng/giảm dài hạn không?
# - Rolling mean 28 ngày giúp giảm nhiễu ngày.

daily_total = (
    m5_daily.groupby("date", as_index=False)
    .agg(
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        active_store_dept=("has_sales", "sum"),
        event_flag=("event_flag", "max"),
    )
)

daily_total["rolling_revenue_28d"] = daily_total["total_revenue"].rolling(28, min_periods=7).mean()
daily_total["rolling_units_28d"] = daily_total["total_units"].rolling(28, min_periods=7).mean()

monthly_total = (
    m5_daily.groupby(["year", "month"], as_index=False)
    .agg(
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        avg_store_dept_revenue=("daily_revenue", "mean"),
    )
)
monthly_total["year_month"] = pd.to_datetime(
    monthly_total["year"].astype(str) + "-" + monthly_total["month"].astype(str) + "-01"
)

yearly_total = (
    m5_daily.groupby("year", as_index=False)
    .agg(
        total_revenue=("daily_revenue", "sum"),
        total_units=("daily_units", "sum"),
        avg_store_dept_revenue=("daily_revenue", "mean"),
    )
)

display(daily_total.head())
display(monthly_total.head())
display(yearly_total)

plt.figure(figsize=(15, 5))
plt.plot(daily_total["date"], daily_total["total_revenue"], alpha=0.35, label="Daily total revenue")
plt.plot(daily_total["date"], daily_total["rolling_revenue_28d"], linewidth=2, label="28-day rolling mean")
plt.title("M5 - Total Daily Revenue Over Time")
plt.xlabel("Date")
plt.ylabel("Total Estimated Revenue")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(15, 5))
plt.plot(monthly_total["year_month"], monthly_total["total_revenue"], marker="o", markersize=3)
plt.title("M5 - Monthly Revenue Over Time")
plt.xlabel("Month")
plt.ylabel("Total Estimated Revenue")
plt.grid(True, alpha=0.3)
plt.show()

# %%
# Cell 13 - Phân tích weekday/weekend
#
# Câu hỏi:
# - Doanh thu có khác giữa các ngày trong tuần không?
# - Cuối tuần có cao/thấp hơn ngày thường không?

weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

weekday_summary = (
    m5_daily.groupby("day_of_week", as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
)
weekday_summary["day_of_week"] = pd.Categorical(
    weekday_summary["day_of_week"], categories=weekday_order, ordered=True
)
weekday_summary = weekday_summary.sort_values("day_of_week")

weekend_summary = (
    m5_daily.groupby("is_weekend", as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
)

display(weekday_summary)
display(weekend_summary)

plt.figure(figsize=(9, 4))
plt.bar(weekday_summary["day_of_week"].astype(str), weekday_summary["avg_daily_revenue"])
plt.title("M5 - Average Store-Department Revenue by Day of Week")
plt.xlabel("Day of Week")
plt.ylabel("Average Daily Revenue")
plt.xticks(rotation=45)
plt.grid(True, axis="y", alpha=0.3)
plt.show()

# %%
# Cell 14 - Phân tích event/holiday
#
# Câu hỏi:
# - Ngày có event có doanh thu khác ngày thường không?
# - Event type nào có doanh thu trung bình cao hơn?

event_summary = (
    m5_daily.groupby("event_flag", as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
)

event_type_summary = (
    m5_daily[m5_daily["event_flag"] == 1]
    .groupby(["event_type", "event_name"], as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
    .sort_values("avg_daily_revenue", ascending=False)
)

display(event_summary)
display(event_type_summary.head(20))

event_daily = (
    m5_daily.groupby(["date", "event_flag"], as_index=False)
    .agg(total_revenue=("daily_revenue", "sum"))
)

plt.figure(figsize=(7, 4))
event_daily.boxplot(column="total_revenue", by="event_flag")
plt.title("Daily Total Revenue by Event Flag")
plt.suptitle("")
plt.xlabel("event_flag")
plt.ylabel("Total Daily Revenue")
plt.grid(True, alpha=0.3)
plt.show()

# %%
# Cell 15 - Phân tích SNAP
#
# SNAP là chương trình hỗ trợ thực phẩm ở Mỹ.
# Với M5, SNAP có thể ảnh hưởng mạnh nhất đến nhóm FOODS.
#
# Câu hỏi:
# - SNAP active có liên quan đến doanh thu không?
# - Ảnh hưởng này có khác nhau giữa FOODS, HOUSEHOLD, HOBBIES không?

snap_summary = (
    m5_daily.groupby("snap_active", as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
)

snap_by_cat = (
    m5_daily.groupby(["cat_id", "snap_active"], as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
)

snap_by_dept = (
    m5_daily.groupby(["dept_id", "snap_active"], as_index=False)
    .agg(
        rows=("daily_revenue", "size"),
        total_revenue=("daily_revenue", "sum"),
        avg_daily_revenue=("daily_revenue", "mean"),
        median_daily_revenue=("daily_revenue", "median"),
        total_units=("daily_units", "sum"),
    )
)

display(snap_summary)
display(snap_by_cat)
display(snap_by_dept)

snap_cat_pivot = snap_by_cat.pivot(index="cat_id", columns="snap_active", values="avg_daily_revenue")
snap_cat_pivot.columns = ["snap_0_avg_revenue", "snap_1_avg_revenue"]
snap_cat_pivot["diff_snap1_minus_snap0"] = (
    snap_cat_pivot["snap_1_avg_revenue"] - snap_cat_pivot["snap_0_avg_revenue"]
)
snap_cat_pivot["pct_diff"] = (
    snap_cat_pivot["diff_snap1_minus_snap0"] / snap_cat_pivot["snap_0_avg_revenue"] * 100
)

display(snap_cat_pivot.sort_values("pct_diff", ascending=False))

# %%
# Cell 16 - Bootstrap confidence interval
#
# Áp dụng kiến thức Bootstrapping:
# - Ước lượng khoảng tin cậy cho statistic.
# - Không giả định phân phối chuẩn quá mạnh.
#
# Lưu ý quan trọng:
# - Đây là bootstrap đơn giản.
# - Với time series, bootstrap thường có thể phá vỡ phụ thuộc thời gian.
# - Ở đây dùng để minh họa uncertainty trong EDA, không dùng làm bằng chứng nhân quả.

def bootstrap_mean_ci(values, n_boot=1000, ci=95, seed=42):
    values = pd.Series(values).dropna().to_numpy()
    if len(values) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    boot_means = []
    n = len(values)
    for _ in range(n_boot):
        sample = rng.choice(values, size=n, replace=True)
        boot_means.append(sample.mean())
    lower = np.percentile(boot_means, (100 - ci) / 2)
    upper = np.percentile(boot_means, 100 - (100 - ci) / 2)
    return values.mean(), lower, upper


def bootstrap_mean_diff_ci(values_a, values_b, n_boot=1000, ci=95, seed=42):
    a = pd.Series(values_a).dropna().to_numpy()
    b = pd.Series(values_b).dropna().to_numpy()
    if len(a) == 0 or len(b) == 0:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    boot_diffs = []
    for _ in range(n_boot):
        sa = rng.choice(a, size=len(a), replace=True)
        sb = rng.choice(b, size=len(b), replace=True)
        boot_diffs.append(sa.mean() - sb.mean())
    diff = a.mean() - b.mean()
    lower = np.percentile(boot_diffs, (100 - ci) / 2)
    upper = np.percentile(boot_diffs, 100 - (100 - ci) / 2)
    return diff, lower, upper


bootstrap_dept_rows = []
for dept in sorted(m5_daily["dept_id"].unique()):
    vals = m5_daily.loc[m5_daily["dept_id"] == dept, "daily_revenue"]
    mean_, lower_, upper_ = bootstrap_mean_ci(vals, n_boot=1000, seed=42)
    bootstrap_dept_rows.append(
        {
            "dept_id": dept,
            "mean_daily_revenue": mean_,
            "ci95_lower": lower_,
            "ci95_upper": upper_,
        }
    )

bootstrap_dept_ci = pd.DataFrame(bootstrap_dept_rows).sort_values("mean_daily_revenue", ascending=False)
display(bootstrap_dept_ci)

# So sánh ngày event vs non-event ở mức daily total để tránh lặp quá nhiều store-dept trong cùng một ngày.
event_values = daily_total.loc[daily_total["event_flag"] == 1, "total_revenue"]
non_event_values = daily_total.loc[daily_total["event_flag"] == 0, "total_revenue"]
event_diff, event_lower, event_upper = bootstrap_mean_diff_ci(
    event_values, non_event_values, n_boot=1000, seed=42
)

event_bootstrap_result = pd.DataFrame(
    [
        {
            "comparison": "mean(total_daily_revenue | event=1) - mean(total_daily_revenue | event=0)",
            "mean_diff": event_diff,
            "ci95_lower": event_lower,
            "ci95_upper": event_upper,
            "interpretation": "Nếu CI không chứa 0, event days có khác biệt trung bình rõ hơn; vẫn không kết luận nhân quả.",
        }
    ]
)

display(event_bootstrap_result)

# %%
# Cell 17 - Phân tích giá bán weighted average
#
# Câu hỏi:
# - Giá trung bình khác nhau thế nào giữa department?
# - Giá có liên quan đến revenue không?
#
# Lưu ý:
# `weighted_avg_sell_price` chỉ có ý nghĩa khi có sales.

price_dept_summary = (
    m5_daily[m5_daily["has_sales"] == 1]
    .groupby(["cat_id", "dept_id"], as_index=False)
    .agg(
        avg_weighted_price=("weighted_avg_sell_price", "mean"),
        median_weighted_price=("weighted_avg_sell_price", "median"),
        min_weighted_price=("weighted_avg_sell_price", "min"),
        max_weighted_price=("weighted_avg_sell_price", "max"),
        avg_revenue=("daily_revenue", "mean"),
        total_revenue=("daily_revenue", "sum"),
    )
    .sort_values("avg_weighted_price", ascending=False)
)

display(price_dept_summary)

sample_for_scatter = m5_daily[m5_daily["has_sales"] == 1].sample(
    n=min(10000, (m5_daily["has_sales"] == 1).sum()),
    random_state=42,
)

plt.figure(figsize=(7, 5))
plt.scatter(
    sample_for_scatter["weighted_avg_sell_price"],
    sample_for_scatter["daily_revenue"],
    alpha=0.25,
    s=10,
)
plt.title("M5 - Weighted Avg Price vs Daily Revenue")
plt.xlabel("Weighted Avg Sell Price")
plt.ylabel("Daily Revenue")
plt.grid(True, alpha=0.3)
plt.show()

price_corr = m5_daily[["weighted_avg_sell_price", "daily_revenue", "daily_units", "active_item_count"]].corr()
display(price_corr)

# %%
# Cell 18 - Outlier analysis bằng IQR
#
# Áp dụng kiến thức Box Plot/IQR:
# - Outlier không tự động là dữ liệu sai.
# - Với retail, outlier có thể là seasonal peak, event, store lớn, department lớn.

def iqr_outlier_summary(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    mask = (df[col] < lower) | (df[col] > upper)
    return {
        "column": col,
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": lower,
        "upper_bound": upper,
        "outlier_count": int(mask.sum()),
        "outlier_pct": mask.mean() * 100,
    }


outlier_summary = pd.DataFrame(
    [
        iqr_outlier_summary(m5_daily, "daily_revenue"),
        iqr_outlier_summary(m5_daily, "daily_units"),
        iqr_outlier_summary(m5_daily[m5_daily["has_sales"] == 1], "weighted_avg_sell_price"),
    ]
)

display(outlier_summary)

top_revenue_rows = (
    m5_daily.sort_values("daily_revenue", ascending=False)
    .head(30)
    .reset_index(drop=True)
)

display(top_revenue_rows)

outlier_notes = pd.DataFrame(
    [
        {
            "rule": "Không xóa outlier tự động",
            "reason": "Retail có ngày cao điểm thật, đặc biệt theo store/department/event.",
            "next_action": "Kiểm tra top rows: store nào, department nào, có event/SNAP không, có lặp theo mùa không.",
        }
    ]
)

display(outlier_notes)

# %%
# Cell 19 - Bảng feature dùng được và feature leakage
#
# Cell này chuẩn bị cho bước model sau này.
# Với target `daily_revenue`, không nên dùng biến cùng ngày được tạo từ kết quả bán hàng.

safe_feature_table = pd.DataFrame(
    [
        ("time", "year, month, quarter, week_of_year, day_of_week, is_weekend", "Dùng được"),
        ("store", "store_id, state_id", "Dùng được"),
        ("product_group", "cat_id, dept_id", "Dùng được"),
        ("price", "weighted_avg_sell_price hoặc listed price feature", "Dùng được nhưng cần xử lý missing và tránh price tương lai nếu forecast thật"),
        ("event", "event_flag, event_type, event_name", "Dùng được nếu biết lịch sự kiện trước"),
        ("snap", "snap_active", "Dùng được nếu lịch SNAP biết trước"),
        ("lag", "revenue_lag_1d, revenue_lag_7d, rolling_mean_7d", "Nên tạo ở bước modeling"),
    ],
    columns=["feature_group", "features", "modeling_decision"],
)

leakage_feature_table = pd.DataFrame(
    [
        ("daily_units", "Leakage cao", "daily_revenue = daily_units * price, nên daily_units cùng ngày gần như tiết lộ target."),
        ("daily_revenue", "Target", "Không dùng làm feature cùng ngày."),
        ("active_item_count", "Có thể leakage", "Số item có bán trong ngày chỉ biết sau khi bán; nên dùng lag nếu cần."),
        ("has_sales", "Leakage cao", "has_sales cùng ngày chỉ biết sau kết quả bán."),
        ("weighted_avg_sell_price", "Cần cẩn thận", "Được tính weighted theo item có bán, có thể phụ thuộc sales mix cùng ngày; tốt hơn tạo listed price feature từ tất cả item."),
    ],
    columns=["feature", "risk_level", "reason"],
)

print("Safe feature groups:")
display(safe_feature_table)

print("Leakage-prone features:")
display(leakage_feature_table)

# %%
# Cell 20 - Kết luận tự động cho phần M5
#
# Cell này tạo một bảng nhận xét có thể copy vào báo cáo.

top_cat = cat_summary.iloc[0]
top_dept = dept_summary.iloc[0]
top_state = state_summary.iloc[0]
top_store = store_summary.iloc[0]

m5_conclusion = pd.DataFrame(
    [
        {
            "aspect": "Scope",
            "finding": "M5 phù hợp với retail daily revenue forecasting.",
            "evidence": f"{m5_daily['store_id'].nunique()} stores, {m5_daily['state_id'].nunique()} states, {m5_daily['cat_id'].nunique()} categories, {m5_daily['dept_id'].nunique()} departments.",
        },
        {
            "aspect": "Target",
            "finding": "Có thể tính daily_revenue.",
            "evidence": "daily_revenue = daily_units * sell_price theo item-store-week; không có missing price ở dòng có units > 0.",
        },
        {
            "aspect": "Data quality",
            "finding": "Bảng daily store-dept sạch ở mức key chính.",
            "evidence": f"Duplicate keys = {int(m5_daily.duplicated(key_cols).sum())}; negative revenue rows = {int((m5_daily['daily_revenue'] < 0).sum())}.",
        },
        {
            "aspect": "Main category",
            "finding": f"Category doanh thu cao nhất là {top_cat['cat_id']}.",
            "evidence": f"Revenue share khoảng {top_cat['revenue_share_pct']:.2f}%.",
        },
        {
            "aspect": "Main department",
            "finding": f"Department doanh thu cao nhất là {top_dept['dept_id']}.",
            "evidence": f"Total revenue = {top_dept['total_revenue']:,.2f}.",
        },
        {
            "aspect": "Main location",
            "finding": f"State/store mạnh nhất lần lượt là {top_state['state_id']} và {top_store['store_id']}.",
            "evidence": f"Top state revenue = {top_state['total_revenue']:,.2f}; top store revenue = {top_store['total_revenue']:,.2f}.",
        },
        {
            "aspect": "Limitation",
            "finding": "Revenue là doanh thu ước tính, không phải doanh thu ghi nhận trực tiếp.",
            "evidence": "M5 có daily units và weekly price; giá không thay đổi trong từng tuần theo dữ liệu.",
        },
        {
            "aspect": "Next step",
            "finding": "Có thể tiếp tục tạo lag/rolling features và benchmark model.",
            "evidence": "Không dùng daily_units/has_sales cùng ngày để tránh leakage.",
        },
    ]
)

display(m5_conclusion)

print("=== Short narrative ===")
print(
    f"""
M5 phù hợp với scope retail daily revenue forecasting vì có {m5_daily['store_id'].nunique()} stores,
{m5_daily['state_id'].nunique()} states, {m5_daily['cat_id'].nunique()} categories và {m5_daily['dept_id'].nunique()} departments.
Sau khi join sales, calendar và sell_prices, ta tính được daily_revenue ở mức date + store + department.
Dữ liệu sau join không có duplicate key, không có doanh thu âm và không thiếu giá ở các dòng có bán hàng.
Hạn chế chính là doanh thu được ước tính từ daily units và weekly price, nên cần ghi rõ giả định đo lường trong báo cáo.
"""
)

