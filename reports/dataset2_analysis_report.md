# Báo cáo phân tích Dataset 2

## 1. Executive Summary

Dataset 2 là dữ liệu giao dịch coffee shop gồm **149,116 dòng** và **11 cột gốc**, bao phủ từ **2023-01-01** đến **2023-06-30**. Dataset không có sẵn `total_amount`, nên báo cáo tạo biến doanh thu bằng công thức `transaction_qty * unit_price`.

Các phát hiện chính:

- Dữ liệu rất sạch về missing và duplicate: không có missing, không có duplicate row, không trùng `transaction_id`.
- Tổng doanh thu dẫn xuất là **$698,812.33**, tổng quantity bán ra là **214,470**.
- Average transaction line là **$4.69**, median là **$3.75**.
- Dataset bao phủ **3 store/location** trong **6 tháng** đầu năm 2023.
- `Coffee` là category doanh thu lớn nhất với **$269,952.45** (38.6% tổng doanh thu).
- Doanh thu theo giờ peak rõ nhất ở khung **8-10 giờ sáng**, đặc biệt giờ **10** có doanh thu cao nhất (**$88,673.39**).

## 2. Dataset Overview

- File phân tích: `data/dataset2/dataset2.csv`
- Số dòng: **149,116**
- Số cột gốc: **11**
- Số cột sau feature engineering: **18**
- Số store_id: **3**
- Số store_location: **3**
- Số product_id: **80**
- Số product_category: **9**
- Số product_type: **29**
- Số product_detail: **80**
- Phạm vi thời gian: **2023-01-01 07:06:11** đến **2023-06-30 20:57:19**
- Số ngày quan sát: **181**
- Số tháng quan sát: **6**

Nhóm biến chính:

- Giao dịch: `transaction_id`, `transaction_qty`, `unit_price`, `total_amount`
- Thời gian: `transaction_date`, `transaction_time`, `transaction_datetime`, `month`, `day_of_week`, `hour`, `is_weekend`
- Store/location: `store_id`, `store_location`
- Sản phẩm: `product_id`, `product_category`, `product_type`, `product_detail`

## 3. Feature Engineering

Các biến được tạo thêm:

- `transaction_datetime`: ghép `transaction_date` và `transaction_time`, parse bằng `pd.to_datetime`.
- `date`: ngày giao dịch từ `transaction_datetime`.
- `month`: tháng giao dịch.
- `day_of_week`: thứ trong tuần.
- `hour`: giờ trong ngày.
- `is_weekend`: cờ cuối tuần.
- `total_amount`: `transaction_qty * unit_price`.

Kiểm tra sau feature engineering:

- Datetime parse errors: **0**
- `transaction_qty`, `unit_price`, `total_amount` không có giá trị âm hoặc bằng 0.
- `total_amount` là biến dẫn xuất, nên khi modeling cần tránh leakage nếu dùng `transaction_qty` và `unit_price` làm feature trực tiếp.

## 4. Data Quality Assessment

### 4.1. Missing values

| column           |   missing_count |   missing_pct |
|:-----------------|----------------:|--------------:|
| transaction_id   |               0 |             0 |
| transaction_date |               0 |             0 |
| transaction_time |               0 |             0 |
| transaction_qty  |               0 |             0 |
| store_id         |               0 |             0 |
| store_location   |               0 |             0 |
| product_id       |               0 |             0 |
| unit_price       |               0 |             0 |
| product_category |               0 |             0 |
| product_type     |               0 |             0 |

Đánh giá: Dataset 2 không có missing ở các cột gốc. Đây là điểm mạnh lớn so với nhiều dataset giao dịch thực tế.

### 4.2. Duplicates và khóa giao dịch

- Duplicate rows: **0**
- Duplicate `transaction_id`: **0**
- Unique `transaction_id`: **149,116**

Đánh giá: `transaction_id` là duy nhất theo dòng. Tuy nhiên chưa có thông tin xác nhận đây là invoice/order id hay chỉ là line id; vì vậy không nên dùng dataset này để phân tích basket/co-purchase nếu thiếu hóa đơn chung.

### 4.3. Store/product mapping

- Mỗi `store_id` map đúng 1 `store_location`.
- Không có `product_id` nào map sang nhiều category/type/detail.
- Có **15 product_id** xuất hiện với nhiều `unit_price`.

Diễn giải: product mapping nhìn chung nhất quán. Việc một số product_id có nhiều giá có thể do thay đổi giá, size/variant, khuyến mãi hoặc cách ghi nhận; cần metadata để kết luận đó là lỗi hay logic nghiệp vụ.

### 4.4. Giá trị bất thường và outliers

| column          |   q1 |   q3 |   lower_bound |   upper_bound |   outlier_count |   outlier_pct |
|:----------------|-----:|-----:|--------------:|--------------:|----------------:|--------------:|
| transaction_qty |  1   | 2    |         -0.5  |          3.5  |              36 |          0.02 |
| unit_price      |  2.5 | 3.75 |          0.62 |          5.62 |           4,212 |          2.82 |
| total_amount    |  3   | 6    |         -1.5  |         10.5  |           3,273 |          2.19 |

Diễn giải:

- `transaction_qty` tối đa là **8**, nhưng quantity cao rất hiếm.
- `unit_price` tối đa là **$45.00** và `total_amount` tối đa là **$360.00**.
- Outlier chủ yếu đến từ sản phẩm giá cao như coffee beans/branded items, nên không nên xóa tự động.

## 5. Exploratory Data Analysis

### 5.1. Doanh thu theo tháng

| month   |   transactions |   quantity |   revenue |   avg_transaction |
|:--------|---------------:|-----------:|----------:|------------------:|
| 2023-01 |         17,314 |     24,870 |   81677.7 |              4.72 |
| 2023-02 |         16,359 |     23,550 |   76145.2 |              4.65 |
| 2023-03 |         21,229 |     30,406 |   98834.7 |              4.66 |
| 2023-04 |         25,335 |     36,469 |  118941   |              4.69 |
| 2023-05 |         33,527 |     48,233 |  156728   |              4.67 |
| 2023-06 |         35,352 |     50,942 |  166486   |              4.71 |

Nhận xét:

- Doanh thu tăng rõ từ tháng 1 đến tháng 6.
- Tháng 6 có doanh thu cao nhất: **$166,485.88**.
- Vì dataset chỉ có nửa đầu năm, không nên kết luận trend cả năm hoặc seasonality dài hạn.

### 5.2. Doanh thu theo ngày trong tuần

| day_of_week   |   transactions |   revenue |   avg_transaction |
|:--------------|---------------:|----------:|------------------:|
| Monday        |         21,643 |  101677   |              4.7  |
| Tuesday       |         21,202 |   99455.9 |              4.69 |
| Wednesday     |         21,310 |  100314   |              4.71 |
| Thursday      |         21,654 |  100768   |              4.65 |
| Friday        |         21,701 |  101373   |              4.67 |
| Saturday      |         20,510 |   96894.5 |              4.72 |
| Sunday        |         21,096 |   98330.3 |              4.66 |

Nhận xét: doanh thu theo ngày trong tuần khá cân bằng; không có ngày nào vượt trội cực mạnh. Điều này gợi ý hour-of-day quan trọng hơn weekday trong dataset này.

### 5.3. Doanh thu theo giờ

|   hour |   transactions |   quantity |   revenue |   avg_transaction |
|-------:|---------------:|-----------:|----------:|------------------:|
|     10 |         18,545 |     26,713 |   88673.4 |              4.78 |
|      9 |         17,764 |     25,370 |   85169.5 |              4.79 |
|      8 |         17,654 |     25,197 |   82699.9 |              4.68 |
|      7 |         13,428 |     19,449 |   63526.5 |              4.73 |
|     11 |          9,766 |     14,035 |   46319.1 |              4.74 |
|     15 |          8,979 |     12,923 |   41733.1 |              4.65 |
|     14 |          8,933 |     12,907 |   41304.7 |              4.62 |
|     16 |          9,093 |     12,881 |   41122.8 |              4.52 |
|     13 |          8,714 |     12,439 |   40367.4 |              4.63 |
|     12 |          8,708 |     12,690 |   40192.8 |              4.62 |

Nhận xét:

- Giờ **10** có doanh thu cao nhất: **$88,673.39**.
- Các giờ 8-10 là peak revenue rõ ràng.
- Sau 18h doanh thu giảm mạnh, và dữ liệu gần như kết thúc quanh 20h.

### 5.4. Doanh thu theo store/location

|   store_id | store_location   |   transactions |   quantity |   revenue |   avg_transaction |
|-----------:|:-----------------|---------------:|-----------:|----------:|------------------:|
|          8 | Hell's Kitchen   |         50,735 |     71,737 |    236511 |              4.66 |
|          3 | Astoria          |         50,599 |     70,991 |    232244 |              4.59 |
|          5 | Lower Manhattan  |         47,782 |     71,742 |    230057 |              4.81 |

Nhận xét:

- **Hell's Kitchen** có doanh thu cao nhất: **$236,511.17**.
- Doanh thu giữa 3 store không chênh lệch quá lớn.
- Lower Manhattan có average transaction line cao hơn nhẹ, dù tổng doanh thu thấp hơn Hell's Kitchen.

### 5.5. Doanh thu theo product category

| product_category   |   transactions |   quantity |   revenue |   avg_transaction |   avg_unit_price |   product_types |   product_details |   revenue_pct |
|:-------------------|---------------:|-----------:|----------:|------------------:|-----------------:|----------------:|------------------:|--------------:|
| Coffee             |         58,416 |     89,250 | 269952    |              4.62 |             3.02 |               5 |                21 |         38.63 |
| Tea                |         45,449 |     69,737 | 196406    |              4.32 |             2.82 |               4 |                16 |         28.11 |
| Bakery             |         22,796 |     23,214 |  82315.6  |              3.61 |             3.55 |               3 |                11 |         11.78 |
| Drinking Chocolate |         11,468 |     17,457 |  72416    |              6.31 |             4.15 |               1 |                 4 |         10.36 |
| Coffee beans       |          1,753 |      1,828 |  40085.2  |             22.87 |            21.02 |               6 |                10 |          5.74 |
| Branded            |            747 |        776 |  13607    |             18.22 |            17.72 |               2 |                 3 |          1.95 |
| Loose Tea          |          1,210 |      1,210 |  11213.6  |              9.27 |             9.27 |               4 |                 8 |          1.6  |
| Flavours           |          6,790 |     10,511 |   8408.8  |              1.24 |             0.8  |               2 |                 4 |          1.2  |
| Packaged Chocolate |            487 |        487 |   4407.64 |              9.05 |             9.05 |               2 |                 3 |          0.63 |

Nhận xét:

- `Coffee` đứng đầu doanh thu: **$269,952.45**.
- `Tea` đứng thứ hai: **$196,405.95**.
- `Coffee beans`, `Branded`, `Loose Tea` có average transaction cao hơn nhưng số giao dịch ít hơn.

### 5.6. Top product type và product detail

Top product type theo revenue:

| product_category   | product_type          |   transactions |   quantity |   revenue |   avg_transaction |
|:-------------------|:----------------------|---------------:|-----------:|----------:|------------------:|
| Coffee             | Barista Espresso      |         16,403 |     24,943 |   91406.2 |              5.57 |
| Tea                | Brewed Chai tea       |         17,183 |     26,250 |   77081.9 |              4.49 |
| Drinking Chocolate | Hot chocolate         |         11,468 |     17,457 |   72416   |              6.31 |
| Coffee             | Gourmet brewed coffee |         16,912 |     25,973 |   70034.6 |              4.14 |
| Tea                | Brewed Black tea      |         11,350 |     17,462 |   47932   |              4.22 |
| Tea                | Brewed herbal tea     |         11,245 |     17,328 |   47539.5 |              4.23 |
| Coffee             | Premium brewed coffee |          8,135 |     12,431 |   38781.2 |              4.77 |
| Coffee             | Organic brewed coffee |          8,489 |     13,012 |   37746.5 |              4.45 |
| Bakery             | Scone                 |         10,173 |     10,465 |   36866.1 |              3.62 |
| Coffee             | Drip coffee           |          8,477 |     12,891 |   31984   |              3.77 |

Top product detail theo revenue:

| product_category   | product_type          | product_detail               |   transactions |   quantity |   revenue |   avg_transaction |   unit_price |
|:-------------------|:----------------------|:-----------------------------|---------------:|-----------:|----------:|------------------:|-------------:|
| Drinking Chocolate | Hot chocolate         | Sustainably Grown Organic Lg |          2,961 |      4,453 |   21151.8 |              7.14 |         4.75 |
| Drinking Chocolate | Hot chocolate         | Dark chocolate Lg            |          3,029 |      4,668 |   21006   |              6.93 |         4.5  |
| Coffee             | Barista Espresso      | Latte Rg                     |          2,896 |      4,497 |   19112.2 |              6.6  |         4.25 |
| Coffee             | Barista Espresso      | Cappuccino Lg                |          2,772 |      4,151 |   17641.8 |              6.36 |         4.25 |
| Tea                | Brewed Chai tea       | Morning Sunrise Chai Lg      |          2,830 |      4,346 |   17384   |              6.14 |         4    |
| Coffee             | Barista Espresso      | Latte                        |          2,990 |      4,602 |   17257.5 |              5.77 |         3.75 |
| Coffee             | Premium brewed coffee | Jamaican Coffee River Lg     |          2,911 |      4,395 |   16481.2 |              5.66 |         3.75 |
| Drinking Chocolate | Hot chocolate         | Sustainably Grown Organic Rg |          2,842 |      4,329 |   16233.8 |              5.71 |         3.75 |
| Coffee             | Barista Espresso      | Cappuccino                   |          2,793 |      4,266 |   15997.5 |              5.73 |         3.75 |
| Coffee             | Organic brewed coffee | Brazilian Lg                 |          2,771 |      4,317 |   15109.5 |              5.45 |         3.5  |

Nhận xét:

- `Barista Espresso`, `Brewed Chai tea`, `Hot chocolate` là các product type tạo doanh thu lớn.
- Top product detail theo revenue có nhiều sản phẩm size lớn và đồ uống phổ biến như Hot Chocolate, Latte, Cappuccino.

### 5.7. Product mix theo store

Tỷ trọng doanh thu category theo store (%):

| store_location   |   Bakery |   Branded |   Coffee |   Coffee beans |   Drinking Chocolate |   Flavours |   Loose Tea |   Packaged Chocolate |   Tea |
|:-----------------|---------:|----------:|---------:|---------------:|---------------------:|-----------:|------------:|---------------------:|------:|
| Astoria          |    11.45 |      2.35 |    38.64 |           4.4  |                11.34 |       0.76 |        1.38 |                 0.47 | 29.21 |
| Hell's Kitchen   |    11.58 |      0.82 |    38.57 |           7.88 |                 9.97 |       1.22 |        1.89 |                 0.72 | 27.36 |
| Lower Manhattan  |    12.31 |      2.7  |    38.68 |           4.88 |                 9.78 |       1.64 |        1.55 |                 0.7  | 27.76 |

Nhận xét: product mix giữa các store khá giống nhau, trong đó Coffee và Tea chiếm tỷ trọng lớn nhất ở cả ba location. Hell's Kitchen có tỷ trọng Coffee beans cao hơn một chút.

## 6. Key Insights

1. **Dataset 2 có chất lượng dữ liệu rất tốt.** Không missing, không duplicate, parse datetime không lỗi.
2. **Doanh thu tăng theo tháng từ tháng 1 đến tháng 6.** Tháng 6 đạt **$166,485.88**, cao nhất trong phạm vi dữ liệu.
3. **Khung sáng là peak revenue.** Giờ **10** cao nhất với **$88,673.39**; các giờ 8-10 tạo phần lớn doanh thu buổi sáng.
4. **Coffee và Tea là hai category chủ lực.** Coffee chiếm **38.6%**, Tea chiếm **28.1%** tổng doanh thu.
5. **Store/location có doanh thu gần nhau.** Hell's Kitchen cao nhất, nhưng khác biệt không quá cực đoan.
6. **Các sản phẩm giá cao tạo outlier hợp lý.** Coffee beans và Branded items làm tăng average transaction và outlier `total_amount`, nhưng đây có thể là tín hiệu nghiệp vụ chứ không phải lỗi.
7. **Mean transaction line ổn định trong phạm vi dataset.** Bootstrap 95% CI cho mean `total_amount` là **$4.67 - $4.71**.

## 7. Modeling Potential

Dataset có thể dùng cho baseline model, đặc biệt sau khi aggregate theo thời gian/store/product.

Gợi ý target:

- Doanh thu theo giờ/ngày/store/category sau khi aggregate.
- `transaction_qty`: dự đoán số lượng mua.
- `product_category` hoặc `product_type`: phân loại sản phẩm dựa trên bối cảnh thời gian/store.
- Demand forecasting theo ngày hoặc giờ.

Gợi ý feature:

- Thời gian: month, day_of_week, hour, is_weekend.
- Store: store_id, store_location.
- Sản phẩm: product_category, product_type, product_detail nếu không gây leakage.
- Giá: unit_price nếu target không phải `total_amount` trực tiếp hoặc nếu bài toán được thiết kế phù hợp.

Cảnh báo data leakage:

- Nếu target là `total_amount`, không nên dùng trực tiếp cả `transaction_qty` và `unit_price` như feature chính, vì `total_amount` được tính từ hai biến đó.
- Nếu dự đoán tương lai, nên chia train/test theo thời gian thay vì shuffle ngẫu nhiên.
- Nếu `transaction_id` chỉ là line id, không nên dùng nó làm feature.

Model baseline phù hợp:

- Regression sau aggregate: Linear Regression, Random Forest Regressor.
- Classification: Logistic Regression, Decision Tree, Random Forest cho target category/type.
- Time-series baseline: moving average, naive forecast hoặc backtesting đơn giản theo ngày/giờ.

## 8. Limitations

- Dataset chỉ bao phủ **6 tháng đầu năm 2023**, chưa đủ để phân tích mùa vụ cả năm.
- Chỉ có **3 store/location**, nên không thể đại diện cho toàn bộ thị trường coffee shop.
- Không có thông tin khách hàng, thời tiết, ngày lễ hoặc phương thức thanh toán.
- `total_amount` là biến dẫn xuất, không phải cột gốc; cần ghi rõ khi báo cáo.
- Một số `product_id` có nhiều `unit_price`; cần metadata để giải thích chính xác.
- Chưa rõ `transaction_id` là invoice id hay line id, nên không nên phân tích basket/co-purchase.

## 9. Recommendations / Next Steps

- Giữ rõ biến `total_amount` là derived variable trong report và notebook.
- Aggregate dữ liệu theo giờ/ngày/store/category để phân tích demand và chuẩn bị forecasting.
- Kiểm tra thêm product_id có nhiều unit_price để hiểu thay đổi giá hoặc variant.
- Khi so sánh với Dataset 1 và Dataset 3, cần đối chiếu scope theo temporal, spatial, domain và source.
- Nếu xây model, bắt đầu bằng baseline đơn giản và tránh leakage từ công thức `total_amount`.
- Cân nhắc bổ sung dataset thời tiết/ngày lễ/khách hàng nếu muốn phân tích yếu tố bối cảnh.

## 10. Output đã tạo

- Notebook đã chạy: `notebooks/dataset2_analysis.ipynb`
- Báo cáo Markdown: `reports/dataset2_analysis_report.md`
