# Phân tích yêu cầu project giữa kì và cuối kì

## 1. Tóm tắt nhanh

Project môn Nhập môn Khoa học Dữ liệu được chia thành hai mốc chính:

- **Giữa kì (Midterm):** xác định ý tưởng project, chọn ít nhất 3 dataset, mô tả và đánh giá chất lượng từng dataset, sau đó so sánh tổng quan và rút ra kết luận ban đầu.
- **Cuối kì (Final):** kế thừa toàn bộ phần giữa kì, mở rộng thành project hoàn chỉnh hơn, có phạm vi rõ ràng, insight dữ liệu sâu hơn, so sánh sâu hơn, kết luận tốt hơn, source code, và có thể có mô hình dự đoán phù hợp với bài toán.

Nội dung cốt lõi không phải là xây dựng mô hình thật phức tạp, mà là **chứng minh mình hiểu dataset, biết đánh giá chất lượng dataset, biết so sánh các dataset, và rút ra insight có ý nghĩa**.

## 2. Yêu cầu giữa kì

### 2.1. Sản phẩm cần nộp

Theo slide, giữa kì cần có:

- **Short report:** file `.docx`, độ dài khoảng **10-20 trang A4**.
- **Slides:** file `.pptx`, thuyết trình khoảng **15 phút**.

### 2.2. Các việc cần làm

Giữa kì cần hoàn thành các việc sau:

1. **Imagine: What's your big, awesome project**
   - Cần xác định một ý tưởng project đủ lớn và có ý nghĩa.
   - Ý tưởng không nên chỉ là "phân tích một file CSV", mà nên có câu hỏi trung tâm, ví dụ:
     - Yếu tố nào ảnh hưởng đến doanh thu coffee shop?
     - Thời tiết, ngày lễ, vị trí cửa hàng và nhóm khách hàng tác động thế nào đến doanh số?
     - Có thể dự đoán doanh thu, giá trị giao dịch, hoặc nhu cầu sản phẩm dựa trên các đặc trưng này không?

2. **Choose at least 3 datasets**
   - Phải có tối thiểu **3 dataset**.
   - Các dataset nên liên quan với nhau trong cùng một chủ đề lớn.
   - Không nên chọn 3 dataset rồi phân tích tách rời; cần giải thích vì sao chúng được đặt chung trong một project.

3. **Introduce the datasets: Samples, fields, statistics, qualities**
   - Mỗi dataset cần được giới thiệu rõ:
     - Mẫu dữ liệu: một vài dòng đầu tiên.
     - Các trường/cột: tên cột, kiểu dữ liệu, ý nghĩa.
     - Thống kê cơ bản: số dòng, số cột, missing values, min/max/mean/median với biến số, tần suất với biến phân loại.
     - Chất lượng dữ liệu: missing, duplicate, outlier, định dạng sai, tính nhất quán, khả năng kết nối với dataset khác.

4. **General comparison & conclusion**
   - So sánh tổng quan giữa các dataset.
   - Kết luận dataset nào hữu ích nhất, dataset nào cần làm sạch nhiều, dataset nào có giá trị bổ sung.
   - Đưa ra hướng tiếp theo cho final.

## 3. Yêu cầu cuối kì

### 3.1. Sản phẩm cần nộp

Theo slide, cuối kì cần có:

- **Report:** độ dài khoảng **30-60 trang A4**.
- **Source codes:** nộp code phân tích, tiền xử lý, trực quan hóa, mô hình nếu có.

Slide không nói rõ có bắt buộc nộp slide cuối kì hay không, nhưng thông thường vẫn nên chuẩn bị slide thuyết trình nếu lớp hoặc giảng viên yêu cầu.

### 3.2. Các việc cần làm

Cuối kì cần bao gồm:

1. **Everything we did in midterm**
   - Toàn bộ nội dung giữa kì phải được giữ lại và cải thiện.
   - Không phải làm lại từ đầu, mà mở rộng từ nền tảng midterm.

2. **Project scopes**
   - Cần xác định phạm vi project rõ ràng.
   - Phạm vi nên trả lời:
     - Dữ liệu bao phủ thời gian nào?
     - Bao phủ khu vực hoặc vị trí nào?
     - Tập trung vào domain/topic nào?
     - Dữ liệu đến từ nguồn nào, thu thập bằng cách nào?
     - Bài toán cuối cùng là phân tích, so sánh, dự đoán, hay kết hợp?

3. **Data insights**
   - Cần có insight sâu hơn từ dữ liệu, không chỉ dừng ở thống kê mô tả.
   - Insight nên có cấu trúc:
     - Quan sát thấy điều gì?
     - Bằng chứng từ bảng hoặc biểu đồ nào?
     - Điều đó có ý nghĩa gì với bài toán?
     - Có hạn chế hoặc khả năng gây nhiễu nào không?

4. **Deep comparison & conclusion**
   - So sánh sâu hơn giữa các dataset.
   - Có thể so sánh theo:
     - Phạm vi thời gian.
     - Phạm vi không gian/địa lý.
     - Độ đầy đủ của trường dữ liệu.
     - Chất lượng dữ liệu.
     - Giá trị phân tích.
     - Khả năng dùng để xây dựng mô hình.

5. **1-page Report & 1-page Comparison Report**
   - Cần chuẩn bị bản tóm tắt 1 trang về project.
   - Cần chuẩn bị bản so sánh 1 trang về các dataset.
   - Phần này có thể đặt ở phụ lục hoặc làm file riêng, nhưng trong report chính nên có nội dung tóm tắt tương ứng.

## 4. Giải thích thêm từ giảng viên về mô hình

Trong đoạn hỏi đáp, thầy xác nhận:

- Cuối kì **có thể xây dựng bất kỳ mô hình nào cũng được**.
- Mô hình được xem như **baseline model** cho một mô hình thực tế sau này trong dự án.
- Mô hình **không cần phức tạp**.
- Điều quan trọng là mô hình phải **phù hợp với project**.
- Ví dụ: nếu project là dự đoán thời tiết thì mô hình cũng phải dự đoán thời tiết.
- Mục tiêu chính vẫn là **chứng minh chất lượng dataset**.

Suy ra, với project của mình:

- Nên có một mô hình đơn giản nhưng đúng bài toán.
- Không nên đưa mô hình vào chỉ để cho có.
- Mô hình nên hỗ trợ câu hỏi nghiên cứu chính.
- Nên ưu tiên giải thích rõ dữ liệu, feature, metric, và hạn chế hơn là cố gắng làm model quá phức tạp.

## 5. Khung SCOPE theo slide

Slide về scope chia phạm vi project thành 4 chiều:

1. **Temporal (time)**
   - Dữ liệu trong khoảng thời gian nào?
   - Theo ngày, giờ, tháng, năm hay mùa?
   - Có đủ để phân tích xu hướng theo thời gian không?

2. **Spatial (space, location)**
   - Dữ liệu gắn với địa điểm nào?
   - Theo thành phố, quốc gia, cửa hàng, khu vực hay tọa độ?
   - Có so sánh được giữa các địa điểm không?

3. **Domain (topic, target)**
   - Chủ đề chính của project là gì?
   - Biến mục tiêu là gì?
   - Ví dụ: doanh thu, số lượng bán, hành vi khách hàng, nhu cầu sản phẩm, ảnh hưởng thời tiết.

4. **Source (instruments, protocols)**
   - Dữ liệu đến từ đâu?
   - Dữ liệu được thu thập bằng công cụ/quy trình nào?
   - Nguồn có đáng tin cậy không?
   - Có cần hợp nhất nhiều nguồn khác nhau không?

Đây là khung quan trọng để viết phần **Project Scope** trong final report.

## 6. Hiện trạng repo hiện tại

Hiện tại repo có:

- `data/dataset1/dataset1.csv`
- `notebooks/dataset1.ipynb`

Dataset hiện có là dữ liệu giao dịch coffee shop, gồm khoảng **20,000 dòng dữ liệu** và các cột chính:

- `transaction_id`
- `timestamp`
- `city`
- `country`
- `store_type`
- `product_category`
- `product_name`
- `unit_price`
- `quantity`
- `discount_applied`
- `payment_method`
- `customer_id`
- `customer_age_group`
- `customer_gender`
- `loyalty_member`
- `weather_condition`
- `temperature_c`
- `holiday_name`
- `total_amount`

Dataset này có tiềm năng tốt vì nó có cả 4 chiều scope:

- **Temporal:** có `timestamp`, có thể phân tích theo giờ/ngày/tháng/ngày lễ.
- **Spatial:** có `city`, `country`, có thể so sánh địa điểm.
- **Domain:** bán hàng coffee shop, sản phẩm, khách hàng, doanh thu.
- **Source/Context:** có thông tin thời tiết, nhiệt độ, ngày lễ, phương thức thanh toán.

Tuy nhiên, theo yêu cầu giữa kì, hiện tại project mới thấy **1 dataset**, trong khi cần **ít nhất 3 dataset**. Việc ưu tiên tiếp theo là bổ sung thêm 2 dataset liên quan.

## 7. Hướng project phù hợp với dữ liệu hiện tại

Một hướng project hợp lý là:

**"Phân tích và dự đoán doanh thu coffee shop dựa trên thời gian, địa điểm, sản phẩm, khách hàng và yếu tố môi trường."**

Câu hỏi nghiên cứu có thể gồm:

1. Doanh thu thay đổi như thế nào theo thời gian?
2. Thành phố/quốc gia nào có doanh thu cao hơn?
3. Nhóm sản phẩm nào đóng góp nhiều nhất vào doanh thu?
4. Ngày lễ có làm thay đổi hành vi mua hàng không?
5. Thời tiết và nhiệt độ có liên quan đến doanh thu hoặc loại sản phẩm được mua không?
6. Khách hàng thành viên loyalty có giá trị giao dịch khác khách hàng thường không?
7. Có thể dự đoán `total_amount`, `quantity`, hoặc nhóm sản phẩm dựa trên các biến đầu vào không?

## 8. Gợi ý bổ sung 2 dataset còn thiếu

Vì dataset hiện có đã là coffee shop sales, các dataset bổ sung nên cùng phục vụ một câu hỏi chung. Có thể chọn:

1. **Dataset 2: Weather dataset**
   - Dữ liệu thời tiết chi tiết theo ngày/giờ và thành phố.
   - Các trường có thể gồm: city, date/time, temperature, humidity, precipitation, wind, weather condition.
   - Mục đích: so sánh với thông tin thời tiết trong dataset sales, hoặc mở rộng phân tích tác động thời tiết đến doanh thu.

2. **Dataset 3: Holiday/Event/Calendar dataset**
   - Dữ liệu ngày lễ, sự kiện, cuối tuần, mùa trong năm theo quốc gia/thành phố.
   - Mục đích: đánh giá doanh thu vào ngày lễ, trước/sau ngày lễ, cuối tuần, mùa mua sắm.

3. **Lựa chọn thay thế: Demographic/Economic dataset**
   - Dữ liệu dân số, thu nhập trung bình, chi phí sinh hoạt, hoặc đặc trưng thành phố/quốc gia.
   - Mục đích: giải thích khác biệt doanh thu giữa các thành phố/quốc gia.

Nên chọn dataset sao cho có khóa nối dữ liệu:

- Theo `city`
- Theo `country`
- Theo `date` hoặc `timestamp`

## 9. Gợi ý mô hình baseline cho final

Theo thầy, mô hình nào cũng được miễn là phù hợp. Với project coffee shop, có thể chọn một trong các baseline sau:

1. **Regression model**
   - Mục tiêu: dự đoán `total_amount` hoặc doanh thu theo ngày/cửa hàng/thành phố.
   - Model đơn giản: Linear Regression, Random Forest Regressor, Gradient Boosting.
   - Metric: MAE, RMSE, R2.

2. **Classification model**
   - Mục tiêu: dự đoán `product_category` hoặc khách có phải `loyalty_member` không.
   - Model đơn giản: Logistic Regression, Decision Tree, Random Forest.
   - Metric: Accuracy, Precision, Recall, F1-score.

3. **Time-series baseline**
   - Mục tiêu: dự đoán doanh thu theo ngày/tháng.
   - Model đơn giản: moving average, naive forecast, ARIMA/Prophet nếu cần.
   - Metric: MAE, RMSE, MAPE.

Để an toàn và đúng yêu cầu, nên bắt đầu bằng model đơn giản, giải thích rõ:

- Vì sao chọn biến mục tiêu.
- Feature nào được dùng.
- Cách chia train/test.
- Kết quả model.
- Hạn chế của model.

## 10. Cấu trúc report giữa kì đề xuất

Report giữa kì 10-20 trang có thể gồm:

1. Giới thiệu project và động lực chọn đề tài.
2. Câu hỏi nghiên cứu.
3. Mô tả scope: temporal, spatial, domain, source.
4. Giới thiệu Dataset 1.
5. Giới thiệu Dataset 2.
6. Giới thiệu Dataset 3.
7. Thống kê mô tả và trực quan hóa ban đầu.
8. Đánh giá chất lượng từng dataset.
9. So sánh tổng quan giữa 3 dataset.
10. Kết luận và kế hoạch cho final.

## 11. Cấu trúc report cuối kì đề xuất

Report final 30-60 trang có thể gồm:

1. Abstract / Tóm tắt.
2. Introduction.
3. Problem statement và research questions.
4. Project scope.
5. Dataset description.
6. Data quality assessment.
7. Data cleaning và preprocessing.
8. Exploratory Data Analysis.
9. Data integration giữa các dataset.
10. Deep comparison giữa các dataset.
11. Insights chính.
12. Baseline model.
13. Evaluation kết quả model.
14. Discussion.
15. Limitation.
16. Conclusion.
17. Future work.
18. Appendix: 1-page report và 1-page comparison report.
19. Source code / link repo / hướng dẫn chạy code.

## 12. Checklist cần làm tiếp

Những việc nên làm tiếp theo:

- Xác định tên đề tài chính thức.
- Bổ sung ít nhất 2 dataset nữa.
- Tạo notebook riêng cho từng dataset hoặc một pipeline chung.
- Viết data dictionary cho mỗi dataset.
- Kiểm tra missing values, duplicate, outlier.
- Tạo các biểu đồ EDA quan trọng.
- Xác định khóa nối các dataset.
- Viết phần scope theo 4 chiều: time, location, domain, source.
- Chọn một baseline model phù hợp.
- Lưu lại tất cả code để nộp final.

## 13. Kết luận cách hiểu yêu cầu

Yêu cầu của thầy có thể hiểu ngắn gọn như sau:

- Giữa kì là giai đoạn **chọn đề tài, chọn 3 dataset, mô tả dataset, đánh giá chất lượng, so sánh tổng quan**.
- Cuối kì là giai đoạn **mở rộng thành project hoàn chỉnh, phân tích sâu, so sánh sâu, có insight, có source code, có thể có baseline model phù hợp**.
- Điểm quan trọng nhất là **chất lượng và cách hiểu dataset**, không phải model phức tạp.
- Project nên có scope rõ theo **thời gian, không gian, domain và nguồn dữ liệu**.
- Repo hiện tại mới có 1 dataset nên việc ưu tiên là **bổ sung thêm 2 dataset liên quan** và xây dựng câu chuyện phân tích thống nhất.
