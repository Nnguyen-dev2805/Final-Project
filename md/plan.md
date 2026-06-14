# Plan: Kiểm tra ảnh hưởng của feature địa điểm trong model chung

## 1. Vấn đề cần giải quyết

Dataset 1 và Dataset 2 đều thuộc cùng bối cảnh New York, nhưng mức độ chi tiết về địa điểm khác nhau:

```text
Dataset 1: New York
Dataset 2: Astoria, Hell's Kitchen, Lower Manhattan
```

Như vậy, spatial scope không phải là khác vùng địa lý, vì tất cả đều nằm trong New York City. Vấn đề chính là khác cấp độ địa lý:

```text
Dataset 1: cấp city
Dataset 2: cấp area / neighborhood / store location
```

Feature địa điểm chỉ ảnh hưởng đến model nếu đưa các cột như `location`, `area`, `store_location`, `city` vào làm input. Nếu không đưa các cột này vào model, khác biệt địa điểm sẽ không ảnh hưởng trực tiếp đến quá trình học của model. Tuy nhiên, model cũng sẽ không học được sự khác nhau về doanh thu giữa các khu vực.

## 2. Hướng giải quyết

Để đánh giá feature địa điểm có nên đưa vào model chung hay không, sẽ train và so sánh 2 model:

```text
Model 1: không dùng area/location
Model 2: có dùng area/location
```

Mục tiêu là kiểm tra xem địa điểm có thật sự giúp dự đoán doanh thu tốt hơn hay chỉ làm model học sự khác nhau giữa Dataset 1 và Dataset 2.

## 3. Model 1: Không dùng area/location

### Input features

Model 1 chỉ dùng các feature không liên quan trực tiếp đến địa điểm:

```text
hour
weekday
month
is_weekend
product_category
weather_condition
temperature_c
is_holiday
```

Không dùng:

```text
city
area
location
store_location
source_dataset
```

### Mục đích

Model 1 dùng để tạo baseline sạch hơn, tránh việc model học nhầm sự khác nhau về cấp độ địa lý giữa hai dataset.

Model này trả lời câu hỏi:

```text
Nếu chỉ dựa trên thời gian, sản phẩm, thời tiết và ngày lễ,
model có dự đoán doanh thu tốt không?
```

### Ưu điểm

- Giảm rủi ro model học nhầm `New York` như một location ngang hàng với `Astoria`, `Hell's Kitchen`, `Lower Manhattan`.
- Công bằng hơn khi Dataset 1 không có area chi tiết.
- Phù hợp để làm baseline ban đầu.

### Nhược điểm

- Mất thông tin về địa điểm.
- Không học được khác biệt doanh thu giữa các khu vực trong New York.
- Nếu doanh thu phụ thuộc mạnh vào location, model có thể kém hơn.

## 4. Model 2: Có dùng area/location

### Input features

Model 2 bổ sung feature địa điểm:

```text
hour
weekday
month
is_weekend
product_category
weather_condition
temperature_c
is_holiday
area
```

Có thể tạo schema địa điểm như sau:

```text
city = New York

area:
- Dataset 1: city_level_unknown
- Dataset 2: Astoria
- Dataset 2: Hell's Kitchen
- Dataset 2: Lower Manhattan
```

### Mục đích

Model 2 kiểm tra xem thông tin địa điểm có cải thiện khả năng dự đoán doanh thu hay không.

Model này trả lời câu hỏi:

```text
Khi thêm area/location vào model, metric có tốt hơn Model 1 không?
```

### Ưu điểm

- Giữ được thông tin địa điểm của Dataset 2.
- Có thể học được khu vực nào có doanh thu cao/thấp hơn.
- Phù hợp với bài toán doanh thu vì location có thể là yếu tố bên ngoài ảnh hưởng đến sức mua.

### Nhược điểm

- Dataset 1 không có area chi tiết, nên phải gán `city_level_unknown`.
- Model có thể học `area = city_level_unknown` gắn với Dataset 1.
- Nếu không đánh giá riêng theo dataset, metric tổng thể có thể gây hiểu nhầm.

## 5. Cách đánh giá

Cần so sánh Model 1 và Model 2 bằng cùng một cách chia train/test.

Metric nên dùng:

```text
MAE
RMSE
R2
MAPE nếu revenue không có nhiều giá trị gần 0
```

Không chỉ báo cáo metric tổng thể. Cần báo cáo riêng:

```text
Overall
Dataset 1 only
Dataset 2 only
```

Bảng kết quả mong muốn:

| Model | Features | Overall MAE | Dataset 1 MAE | Dataset 2 MAE | Nhận xét |
|---|---|---:|---:|---:|---|
| Model 1 | Không dùng location | | | | Baseline |
| Model 2 | Có dùng area/location | | | | Kiểm tra giá trị của địa điểm |

## 6. Cách kết luận

### Trường hợp Model 2 tốt hơn trên cả Dataset 1 và Dataset 2

Kết luận:

```text
Feature địa điểm có giá trị dự đoán doanh thu.
Có thể đưa area/location vào model chung.
```

### Trường hợp Model 2 chỉ tốt trên Dataset 2 nhưng kém trên Dataset 1

Kết luận:

```text
Feature địa điểm có ích cho Dataset 2, nhưng đang gây lệch với Dataset 1
vì Dataset 1 không có area chi tiết.
```

Hướng xử lý:

- Không dùng area trong model chung chính.
- Hoặc giữ area nhưng báo cáo rõ giới hạn.
- Hoặc train model riêng cho từng dataset/location level.

### Trường hợp Model 2 không cải thiện so với Model 1

Kết luận:

```text
Feature địa điểm chưa tạo thêm giá trị dự đoán rõ ràng.
Nên ưu tiên model đơn giản hơn là Model 1.
```

### Trường hợp Model 2 tốt overall nhưng Dataset 1 kém

Kết luận:

```text
Metric tổng thể bị ảnh hưởng bởi Dataset 2 vì Dataset 2 có nhiều dòng hơn.
Không nên chỉ dựa vào overall metric.
```

Hướng xử lý:

- Báo cáo metric riêng theo `source_dataset`.
- Cân nhắc sample weight.
- Cân nhắc train trên khoảng thời gian chung 01-06/2023.

## 7. Khuyến nghị hiện tại

Nên thực hiện theo thứ tự:

```text
1. Train Model 1 không dùng area/location để làm baseline.
2. Train Model 2 có dùng area/location.
3. So sánh metric overall và metric riêng theo Dataset 1, Dataset 2.
4. Chỉ đưa area/location vào model chính nếu Model 2 cải thiện ổn định trên cả hai dataset.
```

Đây là cách làm hợp lý vì không giả định trước rằng location chắc chắn tốt hay chắc chắn xấu. Mình để dữ liệu và metric quyết định.
