# CHƯƠNG 2: GIỚI THIỆU DỮ LIỆU

## 2.1. Mục đích của chương

Chương này trình bày tổng quan về bộ dữ liệu được sử dụng trong đề tài **“Phân tích ảnh hưởng của các yếu tố đến doanh thu bán lẻ theo ngày theo nhóm sản phẩm”**. Nội dung chính bao gồm nguồn dữ liệu, phạm vi dữ liệu, đơn vị quan sát, biến mục tiêu, các nhóm biến giải thích, đặc điểm chất lượng dữ liệu và mức độ phù hợp của dữ liệu đối với bài toán phân tích doanh thu và dự báo.

Bộ dữ liệu được sử dụng trong phân tích là file:

```text
data/m5-forecasting-accuracy/processed/m5_store_dept_daily_with_weather.csv
```

Đây là bộ dữ liệu bán lẻ đã được tổng hợp ở cấp độ **ngày - cửa hàng - nhóm sản phẩm**, đồng thời được bổ sung thêm các thông tin về lịch, sự kiện, SNAP và thời tiết. Dữ liệu phù hợp để nghiên cứu sự thay đổi của doanh thu theo thời gian, theo nhóm sản phẩm, theo cửa hàng và theo các yếu tố ngoại sinh như sự kiện hoặc điều kiện thời tiết.

## 2.2. Tổng quan về bộ dữ liệu

Bộ dữ liệu gồm **135.870 dòng** và **56 cột**, bao phủ giai đoạn từ **29/01/2011** đến **22/05/2016**, tương ứng **1.941 ngày** quan sát.

Mỗi dòng dữ liệu đại diện cho doanh thu của một **nhóm sản phẩm (`dept_id`) tại một cửa hàng (`store_id`) trong một ngày cụ thể (`date`)**. Nói cách khác, đơn vị phân tích của bộ dữ liệu là:

```text
date × store_id × dept_id
```

Dữ liệu bao gồm:

- 10 cửa hàng: `CA_1`, `CA_2`, `CA_3`, `CA_4`, `TX_1`, `TX_2`, `TX_3`, `WI_1`, `WI_2`, `WI_3`.
- 3 bang/khu vực: `CA`, `TX`, `WI`.
- 3 ngành hàng chính: `FOODS`, `HOBBIES`, `HOUSEHOLD`.
- 7 nhóm sản phẩm: `FOODS_1`, `FOODS_2`, `FOODS_3`, `HOBBIES_1`, `HOBBIES_2`, `HOUSEHOLD_1`, `HOUSEHOLD_2`.

Số dòng thực tế bằng đúng số dòng kỳ vọng:

```text
1.941 ngày × 10 cửa hàng × 7 nhóm sản phẩm = 135.870 dòng
```

Ngoài ra, dữ liệu không có dòng trùng lặp theo khóa `date - store_id - dept_id`. Điều này cho thấy dữ liệu có cấu trúc panel đầy đủ, phù hợp cho phân tích theo chuỗi thời gian và so sánh giữa các nhóm sản phẩm.

## 2.3. Biến mục tiêu

Biến mục tiêu chính của đề tài là:

```text
daily_revenue
```

Biến này thể hiện doanh thu bán lẻ theo ngày của một nhóm sản phẩm tại một cửa hàng. Đây là biến phù hợp nhất với mục tiêu nghiên cứu vì đề tài tập trung vào việc phân tích các yếu tố ảnh hưởng đến doanh thu bán lẻ theo ngày.

Một số thống kê mô tả của `daily_revenue`:

| Chỉ tiêu | Giá trị |
|---|---:|
| Số quan sát | 135.870 |
| Trung bình | 1.410,01 |
| Độ lệch chuẩn | 1.384,23 |
| Nhỏ nhất | 0,00 |
| Trung vị | 985,79 |
| Phân vị 75% | 1.900,51 |
| Phân vị 99% | 6.484,88 |
| Lớn nhất | 11.198,95 |

Phân phối doanh thu có xu hướng lệch phải. Điều này có nghĩa là phần lớn quan sát có doanh thu ở mức vừa phải, trong khi một số nhóm sản phẩm hoặc cửa hàng có doanh thu rất cao. Đây là đặc điểm thường gặp trong dữ liệu bán lẻ, đặc biệt khi các nhóm sản phẩm có quy mô nhu cầu khác nhau.

Tỷ lệ dòng có doanh thu bằng 0 chỉ khoảng **0,27%**, cho thấy phần lớn các tổ hợp ngày - cửa hàng - nhóm sản phẩm đều có phát sinh bán hàng.

## 2.4. Các nhóm biến trong dữ liệu

Bộ dữ liệu có thể được chia thành một số nhóm biến chính sau.

### 2.4.1. Nhóm biến thời gian

Nhóm biến này mô tả đặc điểm lịch của từng ngày:

- `date`
- `d`
- `wm_yr_wk`
- `weekday`
- `wday`
- `month`
- `year`
- `quarter`
- `week_of_year`
- `day_of_month`
- `day_of_year`
- `day_of_week`
- `day_of_week_num`
- `is_weekend`
- `year_month`

Các biến này đặc biệt quan trọng vì doanh thu bán lẻ thường có tính mùa vụ, hiệu ứng cuối tuần, xu hướng theo năm và biến động theo các dịp đặc biệt trong năm. Do bài toán có yếu tố dự báo theo thời gian, nhóm biến lịch là nhóm biến có thể biết trước tại thời điểm dự báo và có giá trị sử dụng cao.

### 2.4.2. Nhóm biến định danh cửa hàng và sản phẩm

Nhóm biến này mô tả cửa hàng, bang và nhóm sản phẩm:

- `store_id`
- `state_id`
- `cat_id`
- `dept_id`

Trong đó, `dept_id` là biến đặc biệt quan trọng vì đề tài phân tích doanh thu theo nhóm sản phẩm. Các nhóm sản phẩm có quy mô doanh thu rất khác nhau. Tỷ trọng doanh thu theo `dept_id` như sau:

| Nhóm sản phẩm | Tỷ trọng doanh thu |
|---|---:|
| `FOODS_3` | 37,76% |
| `HOUSEHOLD_1` | 21,99% |
| `FOODS_2` | 13,36% |
| `HOBBIES_1` | 11,55% |
| `HOUSEHOLD_2` | 7,82% |
| `FOODS_1` | 6,89% |
| `HOBBIES_2` | 0,63% |

Mặc dù số quan sát của các nhóm sản phẩm là như nhau, đóng góp doanh thu lại rất khác biệt. Điều này cho thấy doanh thu cao không đến từ việc một nhóm có nhiều dòng dữ liệu hơn, mà đến từ mức bán trung bình cao hơn, số lượng bán ra lớn hơn hoặc quy mô mặt hàng hoạt động lớn hơn.

### 2.4.3. Nhóm biến doanh số, giá và độ phủ sản phẩm

Nhóm biến này phản ánh kết quả bán hàng và đặc điểm sản phẩm trong ngày:

- `daily_revenue`
- `daily_units`
- `item_count`
- `active_item_count`
- `weighted_avg_sell_price`
- `has_sales`

Trong đó:

- `daily_revenue` là biến mục tiêu.
- `daily_units` thể hiện số lượng sản phẩm bán ra trong ngày.
- `weighted_avg_sell_price` là giá bán trung bình có trọng số.
- `item_count` thể hiện số lượng mặt hàng thuộc nhóm sản phẩm.
- `active_item_count` thể hiện số lượng mặt hàng có phát sinh hoạt động bán.
- `has_sales` cho biết ngày đó có phát sinh bán hàng hay không.

Tuy nhiên, cần lưu ý rằng một số biến trong nhóm này có nguy cơ gây rò rỉ thông tin khi xây dựng mô hình dự báo. Cụ thể, doanh thu gần như bằng:

```text
daily_revenue ≈ daily_units × weighted_avg_sell_price
```

Vì vậy, `daily_units` không nên được sử dụng làm biến đầu vào nếu mục tiêu là dự báo `daily_revenue`, vì số lượng bán ra chỉ được biết sau khi ngày bán hàng kết thúc. Tương tự, `has_sales` cũng là biến hậu nghiệm. Các biến như `weighted_avg_sell_price` và `active_item_count` cần được xem xét thận trọng, chỉ nên sử dụng nếu có thể xác nhận rằng chúng được biết trước tại thời điểm dự báo.

### 2.4.4. Nhóm biến sự kiện và SNAP

Dữ liệu có các biến mô tả sự kiện trong ngày:

- `event_name_1`
- `event_type_1`
- `event_name_2`
- `event_type_2`
- `event_count`

Ngoài ra, dữ liệu có các biến liên quan đến chương trình SNAP:

- `snap_CA`
- `snap_TX`
- `snap_WI`
- `snap_active`

Các biến sự kiện và SNAP có ý nghĩa lớn trong bán lẻ vì chúng có thể làm thay đổi hành vi mua sắm của khách hàng. Ví dụ, các ngày lễ lớn có thể làm giảm doanh thu nếu cửa hàng đóng cửa hoặc làm tăng doanh thu nếu khách hàng mua sắm nhiều hơn trước/sau sự kiện. SNAP có thể ảnh hưởng mạnh hơn đến nhóm thực phẩm so với các nhóm hàng khác.

Các biến này có ưu điểm là thường được biết trước theo lịch, do đó phù hợp để sử dụng trong phân tích và mô hình dự báo nếu được xử lý đúng cách.

### 2.4.5. Nhóm biến thời tiết

Bộ dữ liệu được bổ sung các biến thời tiết theo địa điểm đại diện:

- `weather_location_id`
- `location_name`
- `weather_spatial_level`
- `weather_code`
- `temperature_max_c`
- `temperature_min_c`
- `temperature_mean_c`
- `apparent_temperature_mean_c`
- `precipitation_mm`
- `rain_mm`
- `snowfall_cm`
- `wind_speed_max_kmh`
- `wind_gusts_max_kmh`
- `shortwave_radiation_mj_m2`
- `latitude_requested`
- `longitude_requested`
- `latitude_open_meteo`
- `longitude_open_meteo`
- `elevation_m`
- `timezone`
- `utc_offset_seconds`
- `weather_source`

Nhóm biến này giúp phân tích liệu điều kiện thời tiết có ảnh hưởng đến doanh thu bán lẻ hay không. Ví dụ, mưa lớn, nhiệt độ quá cao hoặc quá thấp có thể ảnh hưởng đến lượng khách đến cửa hàng. Tuy nhiên, khi sử dụng cho mô hình dự báo, cần lưu ý rằng thời tiết tương lai chỉ có thể biết thông qua dự báo thời tiết, không phải dữ liệu quan sát thực tế.

## 2.5. Chất lượng dữ liệu

Về cấu trúc, dữ liệu có chất lượng tốt:

- Không có dòng trùng theo `date - store_id - dept_id`.
- Panel dữ liệu đầy đủ theo ngày, cửa hàng và nhóm sản phẩm.
- Biến mục tiêu `daily_revenue` không có giá trị âm.
- Tỷ lệ doanh thu bằng 0 rất thấp, khoảng 0,27%.

Các giá trị thiếu chủ yếu nằm ở nhóm biến sự kiện:

| Cột | Số giá trị thiếu | Diễn giải |
|---|---:|---|
| `event_name_2` | 135.590 | Phần lớn ngày không có sự kiện thứ hai |
| `event_type_2` | 135.590 | Phần lớn ngày không có sự kiện thứ hai |
| `event_name_1` | 124.810 | Phần lớn ngày không có sự kiện chính |
| `event_type_1` | 124.810 | Phần lớn ngày không có sự kiện chính |
| `weighted_avg_sell_price` | 363 | Các dòng không có doanh thu và không có số lượng bán |

Đối với các cột sự kiện, missing không nhất thiết là lỗi dữ liệu mà có thể hiểu là ngày không có sự kiện. Do đó, khi phân tích hoặc mô hình hóa, có thể xử lý bằng cách gán nhãn như `No event`.

Đối với `weighted_avg_sell_price`, các giá trị thiếu xuất hiện ở những dòng không có doanh thu và không có số lượng bán. Điều này hợp lý vì khi không bán được sản phẩm, giá bán trung bình có trọng số không thể tính được.

## 2.6. Mức độ phù hợp với đề tài

Bộ dữ liệu phù hợp với đề tài vì đáp ứng được các yêu cầu phân tích chính:

Thứ nhất, dữ liệu có biến doanh thu theo ngày (`daily_revenue`), cho phép phân tích trực tiếp biến mục tiêu của đề tài.

Thứ hai, dữ liệu có nhóm sản phẩm (`dept_id`), giúp so sánh ảnh hưởng của các yếu tố đến doanh thu giữa các nhóm sản phẩm khác nhau.

Thứ ba, dữ liệu có thông tin cửa hàng và bang (`store_id`, `state_id`), giúp kiểm tra liệu doanh thu cao đến từ nhóm sản phẩm, cửa hàng hay khu vực cụ thể.

Thứ tư, dữ liệu có trục thời gian dài hơn 5 năm, phù hợp để phân tích xu hướng, mùa vụ, hiệu ứng ngày trong tuần và xây dựng mô hình dự báo theo thời gian.

Thứ năm, dữ liệu có các yếu tố ngoại sinh như sự kiện, SNAP và thời tiết, cho phép phân tích sâu hơn các yếu tố có thể tác động đến hành vi mua sắm và doanh thu bán lẻ.

Tuy nhiên, khi sử dụng dữ liệu cho mô hình dự báo, cần đặc biệt chú ý đến nguy cơ rò rỉ dữ liệu. Các biến được tạo ra sau khi doanh số đã phát sinh, chẳng hạn `daily_units` hoặc `has_sales`, không nên được dùng làm biến đầu vào cho mô hình dự báo doanh thu. Ngoài ra, các biến như `weighted_avg_sell_price` và `active_item_count` cần được xem xét dựa trên việc chúng có thực sự được biết trước tại thời điểm dự báo hay không.

## 2.7. Định hướng sử dụng dữ liệu trong nghiên cứu

Từ cấu trúc dữ liệu trên, hướng phân tích phù hợp gồm ba phần chính.

Phần thứ nhất là phân tích mô tả nhằm hiểu doanh thu phân bố như thế nào, nhóm sản phẩm nào đóng góp nhiều nhất, cửa hàng/khu vực nào có doanh thu cao và doanh thu thay đổi ra sao theo thời gian.

Phần thứ hai là phân tích các yếu tố ảnh hưởng đến doanh thu, bao gồm nhóm sản phẩm, cửa hàng, ngày trong tuần, tháng, năm, sự kiện, SNAP và thời tiết. Ở phần này, cần so sánh không chỉ mức doanh thu tuyệt đối mà còn cần chuẩn hóa theo baseline của từng cửa hàng - nhóm sản phẩm để tránh kết luận sai do quy mô khác nhau.

Phần thứ ba là xây dựng mô hình dự báo doanh thu bằng LightGBM. Do dữ liệu có yếu tố thời gian, việc chia dữ liệu cần thực hiện theo thời gian thay vì chia ngẫu nhiên. Các đặc trưng trễ như lag và rolling mean chỉ được tính từ dữ liệu quá khứ để tránh rò rỉ thông tin.

## 2.8. Kết luận chương

Chương này đã giới thiệu tổng quan về bộ dữ liệu bán lẻ được sử dụng trong đề tài. Dữ liệu có cấu trúc panel hoàn chỉnh ở cấp độ ngày - cửa hàng - nhóm sản phẩm, với biến mục tiêu là `daily_revenue`. Bộ dữ liệu có quy mô đủ lớn, thời gian quan sát dài và chứa nhiều nhóm biến có ý nghĩa trong retail analytics như lịch, nhóm sản phẩm, cửa hàng, sự kiện, SNAP và thời tiết.

Về chất lượng, dữ liệu nhìn chung phù hợp cho phân tích và mô hình hóa. Các giá trị thiếu chủ yếu nằm ở nhóm biến sự kiện và có thể diễn giải hợp lý là không có sự kiện. Tuy nhiên, cần kiểm soát chặt chẽ nguy cơ rò rỉ dữ liệu khi xây dựng mô hình dự báo, đặc biệt với các biến liên quan trực tiếp đến kết quả bán hàng trong ngày.

Từ đặc điểm dữ liệu, nghiên cứu có thể tiếp tục đi vào phân tích khám phá để xác định các yếu tố ảnh hưởng đến doanh thu bán lẻ theo ngày, kiểm tra sự khác biệt giữa các nhóm sản phẩm và đánh giá khả năng dự báo doanh thu bằng mô hình LightGBM.
