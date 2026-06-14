# Codex Task Prompt - M5 Phase 1 + 2 Adaptive Data Understanding and Join

You are a senior Data Scientist. I am assigning you the M5 dataset located at:

```text
data/m5-forecasting-accuracy/
```

Your job is to perform **Phase 1 + Phase 2 only**:

```text
Phase 1: Understand the raw M5 dataset.
Phase 2: Join the required tables and create revenue tables.
```

Important: **Do not assume the data is clean or that any expected result is true before checking it.**

You must write code, run each important cell, read the output, and then decide what the next cell should do based on the actual output.

This task is not just coding. You must behave like a real Data Scientist:

- inspect the raw data;
- question the schema;
- verify joins;
- detect data quality issues;
- explain what the output means;
- adjust the next analysis step if the output shows something unexpected.

Write all explanations and notebook markdown in Vietnamese with accents.

## Context Files to Read First

Before coding, read these files if they exist:

```text
promt/promt.md
md/phan_tich_yeu_cau_project.md
md/ap_dung_kien_thuc_data_science_vao_project.md
requires/scope_du_an_retail_revenue_forecasting.md
```

Use them only as project context. Do not blindly force the data to match the documents. If the actual data output contradicts the expected scope, report it clearly.

## Main Output

Create one notebook:

```text
notebooks/m5/phase1_2_m5_understanding_join_revenue.ipynb
```

The notebook must be executable from top to bottom.

After creating it, run the notebook. If a cell output reveals a problem, add or revise later cells to investigate that problem.

Do not create the final cleaned CSV in this phase unless there is a strong reason. If you think an intermediate file is necessary, explain why before writing it.

## Main Goal of This Phase

By the end of this phase, the notebook should answer these questions based on actual output:

1. What files are in the M5 dataset?
2. What does each main table represent?
3. What is the natural grain of the raw sales table?
4. What date range is covered?
5. What product/store hierarchy exists?
6. How should sales be joined with calendar and prices?
7. Can revenue be reconstructed from the available fields?
8. Are there missing price problems after the join?
9. What aggregated revenue tables can be created?
10. Which grain is more appropriate for the next phase of analysis?

Do not answer these from memory. Answer them after reading actual outputs.

## Required Dataset Files to Inspect

Inspect all files in:

```text
data/m5-forecasting-accuracy/
```

At minimum, inspect:

```text
calendar.csv
sell_prices.csv
sales_train_evaluation.csv
sales_train_validation.csv
sample_submission.csv
```

Then decide which files are needed for this phase.

If you choose to use `sales_train_evaluation.csv` as the main sales file, justify it using actual file shapes/date columns. If the output suggests another choice, explain that.

## Required Notebook Workflow

The notebook should follow this adaptive workflow.

### 1. Setup

Write cells to:

- import required libraries;
- detect the project root robustly;
- define paths;
- check file existence.

After running, write a short Vietnamese interpretation:

- Which files exist?
- Is the dataset folder complete enough to continue?

### 2. Raw File Inspection

Read the main CSV files.

For each file, show:

- shape;
- columns;
- first rows;
- dtypes;
- missing values summary;
- duplicate rows if relevant.

Then write a Vietnamese interpretation:

- What does this table appear to represent?
- What is the unit of one row?
- Does the table look like a fact table or dimension table?
- Are there immediate quality concerns?

Do not assume the answer before looking at output.

### 3. Sales File Comparison

Compare:

```text
sales_train_validation.csv
sales_train_evaluation.csv
```

Use code to inspect:

- shape;
- number of day columns;
- first day column;
- last day column;
- whether ID and metadata columns are the same.

Then decide which sales file to use for revenue reconstruction.

In the notebook, explain the decision in Vietnamese.

### 4. Schema and Hierarchy Understanding

Using actual outputs, investigate:

- number of states;
- number of stores;
- number of categories;
- number of departments;
- number of items;
- number of item-store series;
- store distribution by state;
- department distribution by category.

Then write a Vietnamese interpretation:

- What hierarchy exists in the data?
- What level can be used for product-group analysis?
- What limitations do you see at this point?

Do not use fixed numbers in markdown unless they come from the executed output.

### 5. Calendar Table Preparation

Prepare calendar features only after confirming how the `d` columns connect to calendar.

Create useful time/calendar fields if appropriate:

```text
date
year
month
quarter
week_of_year
day_of_month
day_of_year
day_of_week
day_of_week_num
is_weekend
year_month
event fields
SNAP fields
wm_yr_wk
d
```

After running, inspect:

- date range;
- number of calendar rows relevant to the selected sales file;
- event columns;
- SNAP columns;
- missing values.

Then explain:

- how calendar connects to sales;
- which calendar fields may be useful later;
- whether any event/SNAP fields need careful handling.

### 6. Price Table Inspection

Inspect `sell_prices.csv`.

Use code to check:

- key columns;
- uniqueness of `store_id + item_id + wm_yr_wk`;
- missing values;
- duplicate keys;
- price range and unusual values;
- date/week coverage relative to the selected sales calendar.

Then explain:

- what level price is measured at;
- whether price is daily, weekly, transaction-level, or something else;
- what that means for revenue reconstruction.

Avoid claiming revenue is reliable until you check join quality.

### 7. Sales Wide-to-Long Transformation

Convert the selected sales table from wide format to long format.

The resulting table should contain something like:

```text
id
item_id
dept_id
cat_id
store_id
state_id
d
daily_units
```

If memory is an issue, process by store or chunk and explain the approach.

After running, inspect:

- shape;
- daily unit distribution;
- zero-unit rows;
- positive-unit rows;
- unexpected negative units if any.

Then interpret:

- whether zero-unit rows are expected;
- whether the transformed grain makes sense.

### 8. Join Sales + Calendar + Prices

Join in a careful, verifiable way:

```text
long_sales + calendar on d
then + sell_prices on store_id, item_id, wm_yr_wk
```

After joining, check:

- row count before and after join;
- missing calendar fields;
- missing price fields;
- rows with `daily_units > 0` and missing price;
- duplicate rows created by the join;
- negative or impossible values.

Create a quality summary table.

Then write a Vietnamese interpretation:

- Did the join work?
- Are there serious issues?
- Can revenue be reconstructed?
- If not, what issue must be solved first?

If the join reveals unexpected problems, add investigation cells before moving on.

### 9. Revenue Reconstruction

Only after verifying join quality, create revenue fields.

At item-day level, create:

```text
item_revenue = daily_units * sell_price
```

But do not blindly assume this is true invoice revenue. Explain based on data:

- whether revenue is directly provided or reconstructed;
- whether price is weekly or daily;
- what limitations that creates.

Check:

- negative revenue;
- zero revenue;
- positive units with zero revenue;
- positive units with missing price.

### 10. Aggregate Candidate Table 1: Store-Department-Day

Create a candidate table at this grain:

```text
date + store_id + dept_id
```

Name it:

```text
m5_store_dept_daily
```

Aggregate using only fields justified by the data.

At minimum, consider:

```text
daily_revenue
daily_units
item_count
active_item_count
weighted_avg_sell_price if valid
calendar fields
store/state fields
category/department fields
event/SNAP fields
```

After creating it, inspect:

- shape;
- duplicate keys;
- missing values;
- target distribution;
- zero revenue rows;
- basic describe output.

Then write a Vietnamese interpretation:

- What does one row mean?
- Is this grain useful?
- What analysis questions can this grain answer?
- Which columns are useful only for EDA and may become leakage in modeling?

### 11. Aggregate Candidate Table 2: Store-Day

Create another candidate table at this grain:

```text
date + store_id
```

Name it:

```text
m5_store_daily
```

Aggregate from the item-level joined table or from `m5_store_dept_daily`, but explain your choice.

After creating it, inspect:

- shape;
- duplicate keys;
- missing values;
- target distribution;
- zero revenue rows;
- basic describe output.

Then write a Vietnamese interpretation:

- What does one row mean?
- What information is lost compared with store-department-day?
- What project questions can this grain answer better?

### 12. Compare Candidate Grains

Create a comparison table between:

```text
m5_store_dept_daily
m5_store_daily
```

Compare them using actual output:

- row count;
- row meaning;
- product detail;
- target meaning;
- sparsity or zero-revenue behavior;
- modeling complexity;
- compatibility with other datasets such as Maven USA;
- recommended next use.

Do not make the recommendation before seeing the outputs.

### 13. Data Quality and Phase Conclusion

Write a final markdown conclusion in Vietnamese.

The conclusion must be based on actual notebook outputs and should cover:

- whether raw data reading succeeded;
- which sales file was chosen and why;
- whether the join succeeded;
- whether revenue can be reconstructed;
- what the main limitations are;
- which aggregate table should be used in the next phase;
- what must be investigated next.

If something is uncertain, say it is uncertain.

## Important Modeling/Leakage Note

Do not train a model in this phase.

However, while creating tables, flag columns that would be leakage in future modeling.

Examples of columns that may be leakage if predicting revenue before the day occurs:

```text
daily_units
active_item_count
has_sales
weighted_avg_sell_price if calculated using sold units
any value directly derived from same-day sales
```

Do not delete these columns automatically. They may be useful for EDA. Just clearly mark them as not safe for a future baseline prediction model.

## Adaptive Behavior Requirement

This is the most important instruction:

Do not follow a rigid checklist if the output shows a problem.

If a cell output reveals:

- unexpected missing values;
- join row explosion;
- duplicate keys;
- impossible prices;
- positive sales with missing prices;
- unexpected date mismatch;
- memory issues;
- target values that do not make sense;

then stop the normal flow, add diagnostic cells, explain the problem, and only continue when the issue is understood.

## Final Answer After Completing the Notebook

After running the notebook, reply with:

1. The notebook path.
2. What you actually found from the data.
3. Which sales file you used and why.
4. Whether the join succeeded.
5. Whether revenue reconstruction is valid enough for the next phase.
6. Shapes of the candidate aggregate tables.
7. Main data quality concerns.
8. Recommended next phase.

Keep the final response concise but grounded in actual outputs.
