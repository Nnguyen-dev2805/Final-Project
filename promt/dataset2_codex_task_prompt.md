# Prompt gửi Codex: Phân tích Dataset 2 như một Data Scientist

Bạn là Codex, đóng vai trò **Data Scientist chuyên nghiệp** trong project môn Nhập môn Khoa học Dữ liệu.

Tôi là sếp/người quản lý project. Tôi giao cho bạn nhiệm vụ phân tích **Dataset 2** và báo cáo lại kết quả một cách nghiêm túc, có căn cứ, có code, có notebook đã chạy, và có báo cáo Markdown.

## 1. Bối cảnh bắt buộc phải đọc trước khi làm

Trước khi thực hiện bất kỳ phân tích nào, bạn phải đọc các file sau:

1. `promt/promt.md`
2. `md/phan_tich_yeu_cau_project.md`
3. `md/ap_dung_kien_thuc_data_science_vao_project.md`
4. Nếu đã tồn tại, đọc thêm `reports/dataset1_analysis_report.md` để hiểu cách report Dataset 1 đã được viết, nhưng **không được so sánh sâu với Dataset 1 trong nhiệm vụ này**.

Sau khi đọc, hãy dùng các file đó làm cơ sở để làm việc:

- Bám yêu cầu giữa kì/cuối kì của giảng viên.
- Áp dụng tư duy Data Science đúng đắn.
- Không áp dụng kỹ thuật chỉ để cho có.
- Ưu tiên data quality, EDA, insight có bằng chứng, và limitation rõ ràng.

## 2. Dataset cần phân tích

Dataset cần phân tích:

`data/dataset2/dataset2.csv`

Bạn phải xem đây là dataset thứ hai của project. Hãy phân tích dataset này độc lập trước. Chỉ được nhắc ngắn rằng dataset này có thể dùng để so sánh với Dataset 1 ở bước sau, nhưng chưa cần làm deep comparison.

## 3. Lưu ý cấu trúc Dataset 2

Dataset 2 có các cột ban đầu:

- `transaction_id`
- `transaction_date`
- `transaction_time`
- `transaction_qty`
- `store_id`
- `store_location`
- `product_id`
- `unit_price`
- `product_category`
- `product_type`
- `product_detail`

Dataset này **không có sẵn `total_amount`**, vì vậy cần tạo biến:

`total_amount = transaction_qty * unit_price`

Ngoài ra, cần ghép `transaction_date` và `transaction_time` thành một biến datetime, ví dụ:

`transaction_datetime = transaction_date + transaction_time`

Từ đó tạo thêm các biến:

- `date`
- `month`
- `day_of_week`
- `hour`
- `is_weekend`

## 4. Vai trò và phong cách làm việc

Bạn phải làm việc như một **Data Scientist thực thụ**:

- Đọc dữ liệu trước khi kết luận.
- Kiểm tra schema và kiểu dữ liệu.
- Kiểm tra missing values, duplicates, outliers, giá trị bất thường.
- Kiểm tra khóa giao dịch, `transaction_id`, `store_id`, `product_id`.
- Phân tích biến thời gian nếu có.
- Phân tích store/location nếu có.
- Phân tích sản phẩm theo category/type/detail nếu có.
- Tạo biến doanh thu đúng cách trước khi phân tích revenue.
- Tạo biểu đồ phù hợp với câu hỏi phân tích.
- Đọc kết quả sau mỗi bước và viết nhận xét.
- Không chỉ chạy code, mà phải giải thích kết quả.
- Không kết luận vượt quá dữ liệu.
- Phân biệt rõ mô tả, tương quan, dự đoán và quan hệ nhân quả.

## 5. Việc cần tạo ra

Bạn phải tạo ra 2 sản phẩm:

1. Notebook phân tích:

`notebooks/dataset2_analysis.ipynb`

2. Báo cáo Markdown gửi lại sếp:

`reports/dataset2_analysis_report.md`

Nếu file đã tồn tại, hãy đọc trước nội dung cũ rồi cập nhật cẩn thận, không xóa tùy tiện những phần quan trọng.

## 6. Yêu cầu đối với notebook

Notebook `notebooks/dataset2_analysis.ipynb` phải được viết như một notebook phân tích hoàn chỉnh, gồm cả Markdown cell và Code cell.

Notebook cần có tối thiểu các phần sau:

### 6.1. Giới thiệu

- Mục tiêu phân tích Dataset 2.
- Dataset nằm ở đâu.
- Những câu hỏi phân tích ban đầu.
- Lưu ý rằng `total_amount` cần được tạo từ `transaction_qty * unit_price`.

### 6.2. Import thư viện

Sử dụng các thư viện phù hợp, ví dụ:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scipy` nếu cần

Không dùng thư viện phức tạp nếu không cần thiết.

### 6.3. Đọc dữ liệu

- Đọc file `data/dataset2/dataset2.csv`.
- Hiển thị vài dòng đầu.
- Kiểm tra shape.
- Kiểm tra danh sách cột.
- Kiểm tra kiểu dữ liệu.

### 6.4. Chuẩn hóa thời gian và tạo biến dẫn xuất

Bắt buộc thực hiện:

- Parse `transaction_date`.
- Parse `transaction_time`.
- Tạo `transaction_datetime`.
- Tạo `date`, `month`, `day_of_week`, `hour`, `is_weekend`.
- Tạo `total_amount = transaction_qty * unit_price`.

Sau khi tạo biến, kiểm tra:

- Có parse lỗi datetime không.
- Có `total_amount` âm hoặc bằng 0 bất hợp lý không.
- `transaction_qty` và `unit_price` có hợp lệ không.

### 6.5. Data dictionary sơ bộ

Tạo bảng mô tả các cột:

- Tên cột.
- Kiểu dữ liệu.
- Vai trò dự kiến.
- Ý nghĩa suy đoán từ dữ liệu.

Bao gồm cả các biến dẫn xuất như `transaction_datetime`, `month`, `hour`, `is_weekend`, `total_amount`.

Nếu chưa chắc ý nghĩa của cột nào, hãy ghi rõ là suy đoán.

### 6.6. Data quality assessment

Phân tích chất lượng dữ liệu:

- Missing values theo từng cột.
- Tỷ lệ missing.
- Duplicate rows.
- Duplicate `transaction_id`.
- Kiểm tra `transaction_id` có phải khóa duy nhất không.
- Kiểm tra `store_id` và `store_location`.
- Kiểm tra `product_id`, `product_category`, `product_type`, `product_detail`.
- Kiểm tra giá trị bất thường.
- Kiểm tra biến số âm hoặc bằng 0 bất hợp lý.
- Kiểm tra outliers của `transaction_qty`, `unit_price`, `total_amount`.
- Kiểm tra bias hoặc limitation có thể có.

Sau mỗi nhóm kiểm tra, phải có Markdown cell nhận xét.

### 6.7. Descriptive statistics

Phân tích thống kê mô tả:

- Với biến số: `transaction_qty`, `unit_price`, `total_amount`.
- Với biến phân loại: `store_location`, `product_category`, `product_type`, `product_detail`.
- Với biến thời gian: min date, max date, số ngày/tháng, phân bố theo giờ/ngày/tháng.

### 6.8. Exploratory Data Analysis

Thực hiện EDA bằng bảng và biểu đồ phù hợp.

Tối thiểu nên có:

- Tổng doanh thu và số giao dịch.
- Doanh thu theo tháng.
- Doanh thu theo ngày trong tuần.
- Doanh thu theo giờ.
- Doanh thu theo `store_location`.
- Doanh thu theo `store_id`.
- Doanh thu theo `product_category`.
- Doanh thu theo `product_type`.
- Top `product_detail` theo revenue.
- Box plot `total_amount` theo product category hoặc store location.
- Heatmap/pivot table theo giờ và ngày trong tuần nếu phù hợp.

Mỗi biểu đồ phải có:

- Tiêu đề rõ.
- Trục rõ.
- Nhận xét sau biểu đồ.

### 6.9. Bias, variation, measurement error

Dựa trên kiến thức đã học, phân tích:

- Dataset có thể có coverage bias không?
- Có thể có selection bias không?
- Có measurement bias hoặc measurement error không?
- Có sampling variation cần lưu ý không?
- Có vấn đề gì khi `transaction_id` có thể đại diện cho từng dòng sản phẩm thay vì một hóa đơn đầy đủ không?

Phần này không cần quá dài, nhưng phải thể hiện tư duy Data Science.

### 6.10. Insight chính

Tổng hợp các insight có bằng chứng từ dữ liệu.

Với mỗi insight, cần ghi:

- Insight là gì.
- Bằng chứng từ bảng/biểu đồ nào.
- Ý nghĩa.
- Hạn chế khi diễn giải.

### 6.11. Kết luận Dataset 2

Kết luận:

- Dataset này mạnh ở điểm nào.
- Dataset này yếu hoặc hạn chế ở điểm nào.
- Dataset này phù hợp để trả lời loại câu hỏi nào.
- Dataset này có thể dùng cho modeling không, nếu có thì target gợi ý là gì.
- Các bước tiếp theo nên làm.

## 7. Bắt buộc phải chạy notebook

Sau khi tạo notebook, bạn phải **tự chạy toàn bộ notebook từ đầu đến cuối**.

Yêu cầu:

- Chạy từng cell hoặc chạy toàn bộ notebook bằng công cụ phù hợp.
- Nếu cell lỗi, phải sửa lỗi và chạy lại.
- Không được để notebook có cell lỗi.
- Không được viết báo cáo dựa trên giả định chưa chạy.
- Kết quả trong report phải dựa trên output thật từ notebook.

Nếu môi trường thiếu thư viện hoặc không chạy được vì lý do kỹ thuật, phải ghi rõ lỗi và cách xử lý.

## 8. Yêu cầu đối với báo cáo Markdown

Sau khi chạy notebook và đọc output, hãy viết báo cáo:

`reports/dataset2_analysis_report.md`

Báo cáo này là để gửi lại cho tôi, người quản lý project.

Báo cáo phải có cấu trúc:

1. **Executive Summary**
   - Tóm tắt ngắn gọn dataset và phát hiện chính.

2. **Dataset Overview**
   - Số dòng, số cột.
   - Các nhóm biến chính.
   - Phạm vi thời gian.
   - Phạm vi store/location.

3. **Feature Engineering**
   - Cách tạo `transaction_datetime`.
   - Cách tạo `total_amount`.
   - Các biến thời gian dẫn xuất.

4. **Data Quality Assessment**
   - Missing values.
   - Duplicates.
   - Outliers hoặc giá trị bất thường.
   - Measurement issues.
   - Bias/limitation.

5. **Exploratory Data Analysis**
   - Các phân tích chính.
   - Các bảng/biểu đồ quan trọng.
   - Nhận xét rõ ràng.

6. **Key Insights**
   - Liệt kê insight quan trọng.
   - Mỗi insight phải có bằng chứng.

7. **Modeling Potential**
   - Dataset có phù hợp để xây baseline model không?
   - Gợi ý target variable.
   - Gợi ý feature.
   - Gợi ý loại model phù hợp.
   - Cảnh báo data leakage nếu có.

8. **Limitations**
   - Các điểm chưa chắc chắn.
   - Các bias có thể có.
   - Các giới hạn khi diễn giải.

9. **Recommendations / Next Steps**
   - Những việc nên làm tiếp theo với Dataset 2.
   - Những câu hỏi nên phân tích thêm.
   - Cần chuẩn bị gì để so sánh với Dataset 1 và Dataset 3.

## 9. Nguyên tắc viết báo cáo

- Viết bằng tiếng Việt.
- Giọng văn chuyên nghiệp, rõ ràng, báo cáo lại cho sếp.
- Không viết quá chung chung.
- Không chép toàn bộ output thô nếu quá dài.
- Chỉ đưa bảng tóm tắt hoặc kết quả quan trọng.
- Kết luận phải dựa trên output đã chạy.
- Nếu một kết quả chưa đủ bằng chứng, hãy viết thận trọng.

## 10. Nguyên tắc code

- Code sạch, dễ đọc.
- Có comment khi logic không hiển nhiên.
- Không hard-code đường dẫn tuyệt đối nếu không cần.
- Dùng relative path từ notebook cho đúng repo.
- Lưu biểu đồ nếu cần, nhưng không tạo file rác không cần thiết.
- Không xóa hoặc sửa dataset gốc.
- Nếu cần tạo dữ liệu processed, lưu sang file mới và giải thích rõ.

## 11. Một số câu hỏi phân tích gợi ý

Bạn có thể dùng các câu hỏi sau để định hướng EDA:

- Dataset 2 bao phủ thời gian nào?
- Store location nào tạo nhiều revenue nhất?
- Store nào có số giao dịch hoặc revenue cao nhất?
- Product category nào đóng góp revenue lớn nhất?
- Product type/detail nào là sản phẩm chủ lực?
- Doanh thu thay đổi thế nào theo tháng, ngày trong tuần và giờ?
- Có pattern rõ theo buổi sáng/trưa/chiều không?
- Có outlier nào trong transaction quantity, unit price hoặc total amount không?
- Dataset này phù hợp với bài toán dự đoán gì?

## 12. Kết quả cuối cùng cần báo lại

Sau khi hoàn thành, hãy báo lại cho tôi:

- Notebook đã tạo/chỉnh ở đâu.
- Report đã tạo/chỉnh ở đâu.
- Notebook đã chạy thành công chưa.
- Các insight chính ngắn gọn.
- Có lỗi hoặc hạn chế nào không.

Hãy bắt đầu bằng việc đọc các file nền tảng đã nêu, sau đó phân tích `data/dataset2/dataset2.csv`, tạo notebook, chạy notebook, đọc output, và viết report Markdown.
