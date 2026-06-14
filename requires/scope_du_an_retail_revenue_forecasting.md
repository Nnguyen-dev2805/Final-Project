# Scope dự án sau khi thay Dataset 1 bằng M5 và Maven Market

## 1. Tên đề tài đề xuất

**Phân tích và dự đoán doanh thu bán lẻ theo ngày dựa trên thời gian, cửa hàng, nhóm sản phẩm, giá bán, sự kiện/ngày lễ và đặc điểm cửa hàng.**

Tên ngắn gọn có thể dùng trong báo cáo:

> **Daily retail revenue forecasting using store, product, time and external factors**

## 2. Lý do cần đặt lại scope

Scope ban đầu nghiêng về **coffee shop / cafe revenue**. Tuy nhiên, hai dataset mới được chọn để thay thế Dataset 1 là:

- **M5 Forecasting Accuracy**
- **Maven Market Datasets**

Hai dataset này không thuộc miền coffee shop. Chúng thuộc miền **retail / grocery / supermarket / multi-store sales**. Vì vậy, để project nhất quán và có khả năng dùng chung schema/model, scope nên được đặt lại thành:

> **Dự đoán doanh thu bán lẻ theo ngày của các cửa hàng dựa trên thời gian, cửa hàng, nhóm sản phẩm và các yếu tố bên ngoài.**

## 3. Bài toán chính

### 3.1. Target chính

Target chính là:

```text
daily_revenue
```

Tức là:

```text
store + category/product_group + date -> daily_revenue
```

### 3.2. Đơn vị phân tích chuẩn

Đơn vị phân tích chính nên chuẩn hóa về:

```text
source_dataset
date
store_id
category_group
daily_revenue
```

Nếu dataset có item/product chi tiết, có thể tạo thêm model phụ ở mức:

```text
source_dataset
date
store_id
item_id
daily_revenue
```

Tuy nhiên, model chính nên ở mức **store + category/product group + date** để dễ so sánh giữa M5 và Maven Market.

## 4. Vì sao chọn doanh thu theo ngày

### Ưu điểm

- **Giữ được chi tiết thời gian**: có thể phân tích weekday/weekend, đầu tháng/cuối tháng, mùa vụ, ngày lễ và sự kiện cụ thể.
- **Phù hợp với M5**: M5 có số lượng bán theo từng ngày (`d_1`, `d_2`, ...), nên có thể tính doanh thu ngày bằng số lượng bán trong ngày nhân với giá của tuần tương ứng.
- **Phù hợp với Maven Market**: Maven Market có transaction date, quantity và product retail price, nên tính doanh thu ngày khá trực tiếp.
- **Dễ giải thích trong báo cáo**: câu hỏi "ngày này cửa hàng/nhóm sản phẩm bán được bao nhiêu doanh thu?" rất rõ ràng.
- **Có thể aggregate lên tuần nếu cần**: daily là mức chi tiết hơn, sau này vẫn có thể tổng hợp thành weekly để so sánh hoặc làm mô hình phụ.

### Nhược điểm

- Dữ liệu có thể nhiễu hơn weekly vì doanh thu từng ngày dao động mạnh.
- M5 có giá theo tuần, nên doanh thu ngày là doanh thu ước tính bằng **daily units x weekly price**.
- Hai dataset khác nhau về thời gian tuyệt đối: Maven Market là 1997-1998, còn M5 là 2011-2016.
- Cần cẩn thận với leakage: không đưa quantity cùng ngày vào model nếu quantity đang được dùng để tính doanh thu.

Kết luận: **daily revenue là target chính hợp lý nếu mục tiêu là phân tích và dự đoán doanh thu theo ngày**, còn weekly revenue có thể dùng làm hướng phân tích phụ.

## 5. Dataset mới và cách tính doanh thu

## 5.1. M5 Forecasting Accuracy

### Bản chất dữ liệu

M5 là dataset Walmart sales forecasting, gồm:

- Sales theo ngày ở dạng wide: `d_1`, `d_2`, ..., `d_1941`
- Giá bán theo tuần: `sell_prices.csv`
- Calendar: `calendar.csv`
- Store/item hierarchy: `item_id`, `dept_id`, `cat_id`, `store_id`, `state_id`

### Phạm vi

- Khu vực: Mỹ, gồm các bang `CA`, `TX`, `WI`
- Store: 10 stores
- Item: 3,049 items
- Category lớn: `FOODS`, `HOUSEHOLD`, `HOBBIES`
- Thời gian sales train: `2011-01-29` đến `2016-05-22`

### Có tính được doanh thu theo ngày không?

Có. M5 không có revenue trực tiếp, nhưng có thể tính:

```text
daily_revenue = daily_units_sold * sell_price của item-store-week tương ứng
```

Trong đó:

- `daily_units_sold` lấy từ các cột `d_1`, `d_2`, ...
- `date` và `wm_yr_wk` lấy từ `calendar.csv`
- `sell_price` lấy từ `sell_prices.csv` theo `store_id + item_id + wm_yr_wk`

Ví dụ:

```text
Một item bán 3 units vào ngày d_10.
d_10 thuộc tuần Walmart 11102.
Giá item đó tại store đó trong tuần 11102 là 2.50.

daily_revenue = 3 * 2.50 = 7.50
```

### Feature có thể ảnh hưởng đến doanh thu

- `store_id`
- `state_id`
- `cat_id`
- `dept_id`
- `item_id`
- `sell_price`
- `price_change`
- `weekday`, `wday`, `month`, `year`
- `event_name_1`, `event_type_1`, `event_name_2`, `event_type_2`
- `snap_CA`, `snap_TX`, `snap_WI`, chuẩn hóa thành `snap_active`
- Lag/rolling revenue từ lịch sử

### Ưu điểm

- Dữ liệu lớn, nhiều chuỗi store-item.
- Có item, department, category và state.
- Có calendar, event và SNAP.
- Có thể tính doanh thu theo ngày.
- Rất tốt cho bài toán forecasting.

### Nhược điểm

- Revenue không có sẵn, phải tính từ units và price.
- Price chỉ có theo tuần, không có giá riêng từng ngày.
- Không có weather.
- Không có địa chỉ hoặc tọa độ store.
- Nếu melt toàn bộ daily data sẽ tạo dữ liệu rất lớn, cần xử lý cẩn thận.

## 5.2. Maven Market Datasets

### Bản chất dữ liệu

Maven Market là dataset retail/grocery dạng star schema, gồm:

- Transactions 1997 và 1998
- Products
- Stores
- Customers
- Regions
- Returns
- Calendar

### Phạm vi

- Khu vực: USA, Mexico, Canada
- Stores: 24 stores
- Products: 1,560 products
- Customers: 10,281 customers
- Transactions: 269,720 dòng
- Thời gian: `1997-01-01` đến `1998-12-30`

### Có tính được doanh thu theo ngày không?

Có. Maven Market không có revenue trực tiếp trong transaction, nhưng có:

```text
quantity
product_retail_price
product_cost
```

Có thể tính:

```text
gross_revenue = quantity * product_retail_price
cost = quantity * product_cost
profit = gross_revenue - cost
```

Nếu tính cả hàng trả lại:

```text
return_value = return_quantity * product_retail_price
net_revenue = gross_revenue - return_value
```

Do đó, target chính có thể là:

```text
daily_revenue = sum(gross_revenue) theo date + store + category/product_group
```

Hoặc nếu xử lý returns:

```text
daily_net_revenue = daily_gross_revenue - daily_return_value
```

### Feature có thể ảnh hưởng đến doanh thu

- `transaction_date`
- `store_id`
- `store_type`
- `store_country`
- `store_city`
- `store_state`
- `total_sqft`
- `grocery_sqft`
- `sales_region`
- `sales_district`
- `product_id`
- `product_brand`
- `product_retail_price`
- `product_cost`
- `product_weight`
- `recyclable`
- `low_fat`
- `customer_country`
- `yearly_income`
- `gender`
- `education`
- `member_card`
- `occupation`
- `homeowner`

### Ưu điểm

- Tính được revenue, cost và profit.
- Có store, region, country.
- Có customer demographic.
- Có product price/cost.
- Có returns để tính net revenue.
- Phù hợp với retail multi-store.

### Nhược điểm

- Không có product category rõ ràng; có `product_brand` và `product_name`, nhưng thiếu category chuẩn.
- Không có promotion, coupon, weather.
- Dữ liệu khá cũ: 1997-1998.
- Có vẻ là dataset học tập/synthetic, cần ghi rõ trong báo cáo.

## 6. Scope chuẩn sau khi thay dataset

Scope mới nên viết như sau:

> Project tập trung phân tích và dự đoán doanh thu bán lẻ theo ngày ở mức cửa hàng và nhóm sản phẩm. Các dataset có schema gốc khác nhau sẽ được chuẩn hóa về một schema chung gồm thời gian, cửa hàng, nhóm sản phẩm, doanh thu, giá bán và các yếu tố bên ngoài như sự kiện/ngày lễ, SNAP, đặc điểm cửa hàng và đặc điểm khách hàng nếu có.

## 7. Schema chung đề xuất

Schema chuẩn tối thiểu:

```text
source_dataset
date
year
month
day_of_week
is_weekend
store_id
region
country
category_group
daily_revenue
avg_price
event_flag
event_type
store_type
store_size
```

Schema mở rộng nếu dataset có đủ:

```text
state
city
department_id
item_id
product_brand
product_cost
daily_profit
return_value
daily_net_revenue
snap_active
customer_segment
income_group
member_card
```

## 8. Feature nên tạo cho model

### Time features

```text
year
month
quarter
day_of_week
is_weekend
day_of_month
week_of_year
season
is_month_start
is_month_end
```

### Store/location features

```text
store_id
country
region
state
city
store_type
store_size
grocery_sqft
```

### Product/category features

```text
category_group
department_id
product_brand
item_id
```

### Price/cost features

```text
avg_price
price_change_1d
price_change_7d
avg_cost
gross_margin_rate
```

Với M5, price gốc theo tuần nên `price_change_1d` có thể thường bằng 0. Feature quan trọng hơn có thể là:

```text
price_change_from_previous_week
```

### Event/holiday features

```text
has_event
event_type
event_count
snap_active
is_pre_event_day
is_post_event_day
days_to_nearest_event
```

### Lag/rolling features

Đây là nhóm feature rất quan trọng cho forecasting:

```text
revenue_lag_1d
revenue_lag_7d
revenue_lag_14d
revenue_lag_28d
revenue_lag_365d
revenue_rolling_mean_7d
revenue_rolling_mean_28d
revenue_rolling_std_7d
revenue_growth_1d
revenue_growth_7d
```

## 9. Cần tránh leakage

Nếu mục tiêu là dự đoán doanh thu ngày tương lai, không nên đưa các biến chỉ biết sau khi bán vào model chính.

Cần cẩn thận với:

```text
daily_quantity của cùng ngày
gross_revenue của cùng ngày
profit của cùng ngày
return_value của cùng ngày
transaction_count của cùng ngày
```

Lý do:

- Với M5, `daily_revenue` được tính từ `daily_units_sold * sell_price`. Nếu đưa `daily_units_sold` cùng ngày vào model thì model đã biết gần như trực tiếp target.
- Với Maven Market, `daily_revenue` được tính từ `quantity * product_retail_price`. Nếu đưa `quantity` cùng ngày vào model thì cũng là leakage.

Cách dùng hợp lý:

- Dùng các biến này cho EDA.
- Hoặc tạo lag:

```text
daily_quantity_lag_1d
return_value_lag_1d
transaction_count_lag_1d
```

## 10. Model chính đề xuất

### Model 1: baseline không dùng `source_dataset`

Mục tiêu: xem hai dataset có thể dùng chung schema/model ở mức nào.

Feature ví dụ:

```text
day_of_week
is_weekend
month
store_type
category_group
avg_price
event_type
snap_active
revenue_lag_1d
revenue_lag_7d
revenue_rolling_mean_7d
```

### Model 2: có dùng `source_dataset`

Mục tiêu: cho phép model học khác biệt nguồn giữa M5 và Maven Market.

Thêm feature:

```text
source_dataset
```

Nếu Model 2 tốt hơn Model 1 rất nhiều, điều đó cho thấy hai dataset vẫn có khác biệt nguồn mạnh và chưa hoàn toàn interchangeable.

### Model 3: model riêng từng dataset

Mục tiêu: benchmark.

So sánh:

```text
shared model vs dataset-specific model
```

Nếu shared model gần bằng model riêng, khả năng dùng chung model là tốt.

## 11. Đánh giá khả năng dùng chung M5 và Maven Market

### Điểm chung

- Đều thuộc miền retail / grocery / supermarket.
- Đều có nhiều store.
- Đều có product/item.
- Đều có date.
- Đều có thể tính doanh thu theo ngày.
- Đều có thể tạo feature thời gian và lịch sử doanh thu.

### Điểm khác

- M5 có category chuẩn (`cat_id`, `dept_id`), còn Maven Market thiếu category rõ ràng.
- M5 có event/SNAP, Maven Market có customer/store demographic tốt hơn.
- M5 có price theo tuần, Maven Market có price/cost theo product.
- M5 ở Mỹ giai đoạn 2011-2016, Maven Market ở USA/Mexico/Canada giai đoạn 1997-1998.

### Hướng xử lý

- Chuẩn hóa target về `daily_revenue`.
- Chuẩn hóa đơn vị phân tích về `date + store + category/product_group`.
- Với M5 dùng `cat_id` hoặc `dept_id` làm `category_group`.
- Với Maven Market tạm dùng `product_brand` làm `category_group`, hoặc xây dựng mapping category từ `product_name` nếu cần.
- Tạo `source_dataset` để kiểm tra dataset shift.
- Đánh giá cả model chung và model riêng.

## 12. Kết luận scope

Sau khi thay Dataset 1 bằng M5 và Maven Market, project nên chốt theo hướng:

```text
Retail daily revenue forecasting
```

Không nên tiếp tục gọi là coffee shop revenue forecasting.

Target chính:

```text
daily_revenue
```

Đơn vị phân tích:

```text
store + category/product_group + date
```

Hai dataset mới đều có thể tham gia:

- **M5**: tính doanh thu ngày từ daily unit sales và weekly sell price.
- **Maven Market**: tính doanh thu ngày từ transaction quantity và retail price, có thể tính thêm profit và net revenue sau returns.

Đây là scope hợp lý, có tính Data Science rõ ràng, và phù hợp với yêu cầu chuẩn hóa dataset/interchangeable của project.
