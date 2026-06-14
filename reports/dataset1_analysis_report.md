# Báo cáo phân tích Dataset 1 - sau khi cập nhật nguồn dữ liệu

## 1. Executive Summary

Dataset 1 đã được cập nhật lại nguồn dữ liệu. Bản hiện tại gồm **946 dòng** và **19 cột**, bao phủ từ **2023-01-01** đến **2023-12-31**. Khác với phân tích cũ, dữ liệu hiện tại là một subset hẹp: **New York**, **USA**, **Standalone**.

Các phát hiện chính:

- Dataset hiện có **946 giao dịch**, nhỏ hơn nhiều so với bản phân tích trước đó.
- Dữ liệu giao dịch cốt lõi sạch: không có duplicate row, không trùng `transaction_id`, không missing ở `unit_price`, `quantity`, `product_category`, `product_name`, `total_amount`.
- Tổng doanh thu là **$6,515.71**, tổng quantity là **1,600**, average transaction là **$6.89**, median là **$5.00**.
- `Coffee` là nhóm sản phẩm doanh thu lớn nhất với **$2,849.61** (43.7% tổng doanh thu).
- Doanh thu tập trung mạnh ở khung sáng, đặc biệt **8h** có doanh thu cao nhất (**$880.42**).
- Limitation lớn nhất: dữ liệu chỉ đại diện cho **New York / USA / Standalone**, không còn dùng để so sánh nhiều thành phố/quốc gia/store type trong nội bộ Dataset 1.

## 2. Dataset Overview

- File phân tích: `data/dataset1/dataset1.csv`
- Số dòng: **946**
- Số cột gốc: **19**
- Số cột sau feature engineering: **28**
- Số country: **1**
- Số city: **1**
- Số store type: **1**
- Số customer_id unique: **945**
- Số product_category: **6**
- Số product_name: **43**
- Phạm vi thời gian: **2023-01-01 06:16:26** đến **2023-12-31 14:14:15**
- Số ngày có giao dịch: **328**
- Số tháng quan sát: **12**

Nhóm biến chính:

- Giao dịch: `transaction_id`, `unit_price`, `quantity`, `discount_applied`, `total_amount`
- Thời gian: `timestamp`, `month`, `weekday`, `hour`, `is_weekend`
- Không gian/scope: `city`, `country`, `store_type`
- Sản phẩm: `product_category`, `product_name`
- Khách hàng: `customer_id`, `customer_age_group`, `customer_gender`, `loyalty_member`
- Bối cảnh: `weather_condition`, `temperature_c`, `holiday_name`

## 3. Feature Engineering

Các biến được tạo thêm:

- `date`, `month`, `weekday`, `hour`, `is_weekend` từ `timestamp`.
- `is_holiday` từ `holiday_name.notna()`.
- `expected_gross_amount = unit_price * quantity`.
- `discount_amount = expected_gross_amount - total_amount`.
- `discount_rate_pct = discount_amount / expected_gross_amount * 100`.

Kiểm tra sau feature engineering:

- Timestamp parse errors: **0**
- Các dòng không giảm giá khớp **100.00%** với `unit_price * quantity`.
- Có **128** dòng áp dụng discount, với các mức giảm ước tính quanh 5%, 10%, 15%, 20%.

## 4. Data Quality Assessment

### 4.1. Missing values

| column             |   missing_count |   missing_pct |
|:-------------------|----------------:|--------------:|
| holiday_name       |             927 |         97.99 |
| customer_age_group |              56 |          5.92 |
| customer_gender    |              54 |          5.71 |
| temperature_c      |              30 |          3.17 |
| weather_condition  |              30 |          3.17 |
| transaction_id     |               0 |          0    |
| payment_method     |               0 |          0    |
| loyalty_member     |               0 |          0    |

Diễn giải:

- `holiday_name` missing **97.99%**, nhiều khả năng biểu thị phần lớn giao dịch không rơi vào ngày lễ.
- `customer_age_group` missing **5.92%** và `customer_gender` missing **5.71%**, nên phân tích nhân khẩu học cần thận trọng.
- `weather_condition` và `temperature_c` missing **3.17%**, ảnh hưởng phân tích weather.

### 4.2. Duplicates và khóa giao dịch

- Duplicate rows: **0**
- Duplicate `transaction_id`: **0**
- Unique `transaction_id`: **946**

Đánh giá: khóa giao dịch sạch, phù hợp để phân tích theo transaction.

### 4.3. Scope sau cập nhật

| Field | Unique values | Nhận xét |
|---|---:|---|
| `country` | 1 | Chỉ có USA |
| `city` | 1 | Chỉ có New York |
| `store_type` | 1 | Chỉ có Standalone |

Đánh giá: đây là subset hẹp. Các kết luận chỉ nên viết trong phạm vi New York Standalone, không khái quát ra nhiều thành phố/quốc gia/store type.

### 4.4. Giá trị bất thường và outliers

| column        |   q1 |   q3 |   lower_bound |   upper_bound |   outlier_count |   outlier_pct |
|:--------------|-----:|-----:|--------------:|--------------:|----------------:|--------------:|
| unit_price    | 2.9  |  4.6 |          0.35 |          7.15 |              19 |          2.01 |
| quantity      | 1    |  2   |         -0.5  |          3.5  |              64 |          6.77 |
| temperature_c | 4.97 | 22.1 |        -20.71 |         47.79 |               0 |          0    |
| total_amount  | 3.46 |  8.1 |         -3.49 |         15.06 |              67 |          7.08 |

Diễn giải:

- `unit_price`, `quantity`, `total_amount` không có giá trị âm hoặc bằng 0.
- `temperature_c` có giá trị âm nhưng hợp lý với New York mùa đông.
- Outlier ở `total_amount` và `quantity` có thể là giao dịch lớn hoặc sản phẩm giá cao; không nên xóa tự động.

## 5. Exploratory Data Analysis

### 5.1. Doanh thu theo tháng

| month   |   transactions |   quantity |   revenue |   avg_transaction |
|:--------|---------------:|-----------:|----------:|------------------:|
| 2023-01 |             92 |        172 |    788.82 |              8.57 |
| 2023-02 |             67 |        125 |    510.88 |              7.63 |
| 2023-03 |             80 |        127 |    495.94 |              6.2  |
| 2023-04 |             65 |        105 |    410.04 |              6.31 |
| 2023-05 |             78 |        128 |    485.77 |              6.23 |
| 2023-06 |             80 |        117 |    456.28 |              5.7  |
| 2023-07 |             85 |        146 |    609.18 |              7.17 |
| 2023-08 |             68 |        127 |    534.83 |              7.87 |
| 2023-09 |             76 |        131 |    482.58 |              6.35 |
| 2023-10 |             84 |        126 |    487.9  |              5.81 |

Nhận xét:

- Tháng có doanh thu cao nhất là **2023-01** với **$788.82**.
- Vì số dòng mỗi tháng khá nhỏ, chênh lệch tháng cần diễn giải thận trọng.

### 5.2. Doanh thu theo ngày trong tuần

| weekday   |   transactions |   revenue |   avg_transaction |
|:----------|---------------:|----------:|------------------:|
| Monday    |             92 |    707.07 |              7.69 |
| Tuesday   |            104 |    673.66 |              6.48 |
| Wednesday |            119 |    828.82 |              6.96 |
| Thursday  |            160 |   1089.18 |              6.81 |
| Friday    |            133 |    949.39 |              7.14 |
| Saturday  |            184 |   1261.28 |              6.85 |
| Sunday    |            154 |   1006.31 |              6.53 |

Nhận xét:

- Ngày có doanh thu cao nhất là **Saturday** với **$1,261.28**.
- Thứ Bảy và Chủ Nhật có số giao dịch/doanh thu cao, nhưng cần kiểm tra thêm nếu muốn kết luận pattern cuối tuần.

### 5.3. Doanh thu theo giờ

|   hour |   transactions |   revenue |   avg_transaction |
|-------:|---------------:|----------:|------------------:|
|      8 |            105 |    880.42 |              8.38 |
|      9 |            104 |    818.88 |              7.87 |
|     10 |             73 |    640.46 |              8.77 |
|      7 |             78 |    605.82 |              7.77 |
|     15 |             74 |    413.22 |              5.58 |
|     14 |             65 |    388.68 |              5.98 |
|     12 |             48 |    372.87 |              7.77 |
|     11 |             71 |    355.68 |              5.01 |
|     17 |             52 |    317.46 |              6.1  |
|     13 |             33 |    306.46 |              9.29 |

Nhận xét:

- Giờ **8** có doanh thu cao nhất: **$880.42**.
- Khung **7-10h** là nhóm giờ mạnh nhất, phù hợp bối cảnh coffee shop buổi sáng.

### 5.4. Doanh thu theo product category

| product_category   |   transactions |   quantity |   revenue |   avg_transaction |   avg_unit_price |   products |   revenue_pct |
|:-------------------|---------------:|-----------:|----------:|------------------:|-----------------:|-----------:|--------------:|
| Coffee             |            453 |        769 |   2849.61 |              6.29 |             3.79 |         18 |         43.73 |
| Tea                |            236 |        387 |   1384.15 |              5.87 |             3.6  |         12 |         21.24 |
| Sandwich           |             86 |        156 |    912.29 |             10.61 |             6    |          3 |         14    |
| Smoothie           |             42 |         82 |    490.12 |             11.67 |             5.94 |          4 |          7.52 |
| Merchandise        |             19 |         34 |    465.3  |             24.49 |            13.74 |          2 |          7.14 |
| Pastry             |            110 |        172 |    414.24 |              3.77 |             2.41 |          4 |          6.36 |

Nhận xét:

- `Coffee` đóng góp doanh thu cao nhất: **$2,849.61**.
- `Tea` đứng thứ hai: **$1,384.15**.
- `Merchandise` ít giao dịch nhưng average transaction cao nhất.

### 5.5. Top product theo doanh thu

| product_name           | product_category   |   transactions |   quantity |   revenue |   avg_transaction |   avg_unit_price |
|:-----------------------|:-------------------|---------------:|-----------:|----------:|------------------:|-----------------:|
| Ham & Cheese Croissant | Sandwich           |             30 |         62 |    334.4  |             11.15 |             5.5  |
| Chicken & Avocado Wrap | Sandwich           |             30 |         50 |    321.09 |             10.7  |             6.5  |
| Tote Bag               | Merchandise        |             11 |         21 |    310.5  |             28.23 |            15    |
| Large Berry Blast      | Smoothie           |             20 |         45 |    281.92 |             14.1  |             6.3  |
| Vegan Falafel Wrap     | Sandwich           |             26 |         44 |    256.8  |              9.88 |             6    |
| Large Mocha            | Coffee             |             29 |         50 |    252.98 |              8.72 |             5.2  |
| Medium Cappuccino      | Coffee             |             36 |         62 |    240    |              6.67 |             4    |
| Large Americano        | Coffee             |             36 |         69 |    235.98 |              6.56 |             3.45 |
| Small Matcha Latte     | Tea                |             25 |         59 |    235.7  |              9.43 |             4.05 |
| Single Espresso        | Coffee             |             41 |         80 |    230.26 |              5.62 |             2.9  |

Nhận xét:

- Top product theo doanh thu không chỉ gồm coffee, mà còn có sandwich, smoothie và merchandise.
- Điều này cho thấy doanh thu chịu ảnh hưởng bởi cả số giao dịch, quantity và đơn giá.

### 5.6. Thanh toán, khách hàng, weather và holiday

Payment method:

| payment_method   |   transactions |   revenue |   avg_transaction |
|:-----------------|---------------:|----------:|------------------:|
| Credit Card      |            377 |   2662.29 |              7.06 |
| Cash             |            248 |   1612.01 |              6.5  |
| Debit Card       |            171 |   1160.53 |              6.79 |
| Mobile Wallet    |            150 |   1080.88 |              7.21 |

Customer age group:

| customer_age_group   |   transactions |   revenue |   avg_transaction |
|:---------------------|---------------:|----------:|------------------:|
| 25-34                |            212 |   1383.14 |              6.52 |
| 55-64                |            147 |   1192.69 |              8.11 |
| 35-44                |            164 |   1103.48 |              6.73 |
| 18-24                |            142 |   1065.01 |              7.5  |
| 45-54                |            125 |    833.57 |              6.67 |
| 65+                  |            100 |    596.59 |              5.97 |
| nan                  |             56 |    341.23 |              6.09 |

Weather:

| weather_condition   |   transactions |   revenue |   avg_transaction |   avg_temperature |
|:--------------------|---------------:|----------:|------------------:|------------------:|
| Sunny               |            434 |   2968.48 |              6.84 |             13.01 |
| Rainy               |            284 |   1837.99 |              6.47 |             13.95 |
| Cloudy              |            184 |   1364.34 |              7.41 |             14.26 |
| Missing             |             30 |    230.44 |              7.68 |                   |
| Snowy               |             14 |    114.46 |              8.18 |              0.39 |

Holiday vs non-holiday:

| is_holiday   |   transactions |   revenue |   avg_transaction |
|:-------------|---------------:|----------:|------------------:|
| False        |            927 |   6353.96 |              6.85 |
| True         |             19 |    161.75 |              8.51 |

Nhận xét:

- Credit Card đóng góp doanh thu lớn nhất do số giao dịch cao.
- Weather nhóm Sunny/Rainy/Cloudy chiếm phần lớn quan sát.
- Holiday chỉ có **19** giao dịch, nên không nên kết luận mạnh về tác động ngày lễ.

## 6. Key Insights

1. **Dataset 1 mới là subset hẹp.** Dữ liệu chỉ có New York, USA, Standalone, nên không còn phù hợp để so sánh nhiều địa điểm/store type.
2. **Dữ liệu giao dịch cốt lõi sạch.** Không duplicate, không trùng transaction_id, không missing ở các biến giao dịch chính.
3. **Coffee là nhóm doanh thu chính.** Coffee tạo **$2,849.61**, chiếm **43.7%** tổng doanh thu.
4. **Khung sáng là peak revenue.** Giờ **8** có doanh thu cao nhất với **$880.42**; nhóm 7-10h nổi bật.
5. **Các nhóm nhỏ cần thận trọng.** Holiday, Snowy, Merchandise có ít quan sát, dễ bị ảnh hưởng bởi sampling variation.
6. **Bootstrap cho thấy mean transaction có uncertainty đáng kể hơn bản cũ.** 95% CI cho mean `total_amount` là **$6.53 - $7.29**.

## 7. Modeling Potential

Dataset vẫn có thể dùng cho baseline model, nhưng cần gắn chặt với phạm vi New York Standalone.

Gợi ý target:

- `total_amount`: dự đoán giá trị giao dịch.
- `quantity`: dự đoán số lượng sản phẩm trong giao dịch.
- `product_category`: phân loại nhóm sản phẩm.
- Doanh thu theo ngày/giờ sau khi aggregate.

Gợi ý feature:

- Thời gian: month, weekday, hour, is_weekend, is_holiday.
- Sản phẩm: product_category/product_name nếu target không bị leakage.
- Khách hàng: customer_age_group, customer_gender, loyalty_member.
- Bối cảnh: weather_condition, temperature_c.
- Payment/discount: payment_method, discount_applied.

Cảnh báo data leakage:

- Nếu target là `total_amount`, dùng trực tiếp `unit_price`, `quantity`, `expected_gross_amount` hoặc `discount_amount` có thể làm bài toán quá gần công thức.
- Nếu dự đoán theo thời gian, nên chia train/test theo thời gian.
- Không dùng `transaction_id` hoặc `customer_id` như feature dự đoán nếu không có lý do rõ.

## 8. Limitations

- Dataset hiện chỉ có **946 dòng**, nhỏ hơn nhiều so với bản trước.
- Chỉ bao phủ **New York / USA / Standalone**, không đại diện cho toàn bộ coffee shop hoặc nhiều địa điểm.
- Missing ở customer/weather vẫn tồn tại.
- Holiday và Snowy có rất ít quan sát, không đủ để kết luận mạnh.
- Không có metadata nguồn, nên chưa biết subset được lọc theo tiêu chí nào.
- Không thể kết luận quan hệ nhân quả giữa discount/weather/holiday và doanh thu.

## 9. Recommendations / Next Steps

- Ghi rõ Dataset 1 là subset New York Standalone trong report giữa kì/cuối kì.
- Không dùng Dataset 1 mới để kết luận về khác biệt city/country/store_type.
- So sánh Dataset 1 với Dataset 2 cần tập trung vào scope, schema, data quality và sản phẩm/doanh thu, không so sánh trực tiếp doanh thu tổng vì phạm vi khác nhau.
- Nếu cần phân tích không gian rộng hơn, cần bổ sung dataset khác hoặc dùng Dataset 2/Dataset 3.
- Nếu xây model, bắt đầu bằng baseline đơn giản và tránh leakage từ công thức doanh thu.

## 10. Output đã tạo lại

- Notebook đã chạy lại: `notebooks/dataset1_analysis.ipynb`
- Báo cáo Markdown đã cập nhật: `reports/dataset1_analysis_report.md`
