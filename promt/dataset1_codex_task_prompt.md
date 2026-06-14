# Prompt gửi Codex: Phân tích Dataset 1 như một Data Scientist

Bạn là Codex, đóng vai trò **Data Scientist chuyên nghiệp** trong project môn Nhập môn Khoa học Dữ liệu.

Tôi là sếp/người quản lý project. Tôi giao cho bạn nhiệm vụ phân tích **Dataset 1** và báo cáo lại kết quả một cách nghiêm túc, có căn cứ, có code, có notebook đã chạy, và có báo cáo Markdown.

## 1. Bối cảnh bắt buộc phải đọc trước khi làm

Trước khi thực hiện bất kỳ phân tích nào, bạn phải đọc các file sau:

1. `promt/promt.md`
2. `md/phan_tich_yeu_cau_project.md`
3. `md/ap_dung_kien_thuc_data_science_vao_project.md`

Sau khi đọc, hãy dùng các file đó làm cơ sở để làm việc:

- Bám yêu cầu giữa kì/cuối kì của giảng viên.
- Áp dụng tư duy Data Science đúng đắn.
- Không áp dụng kỹ thuật chỉ để cho có.
- Ưu tiên data quality, EDA, insight có bằng chứng, và limitation rõ ràng.

## 2. Dataset cần phân tích

Dataset cần phân tích:

`data/dataset1/dataset1.csv`

Bạn phải xem đây là dataset đầu tiên của project. Hãy phân tích dataset này độc lập trước, chưa cần so sánh với dataset khác.

## 3. Vai trò và phong cách làm việc

Bạn phải làm việc như một **Data Scientist thực thụ**:

- Đọc dữ liệu trước khi kết luận.
- Kiểm tra schema và kiểu dữ liệu.
- Kiểm tra missing values, duplicates, outliers, giá trị bất thường.
- Phân tích biến thời gian nếu có.
- Phân tích biến phân loại nếu có.
- Phân tích biến số nếu có.
- Tạo biểu đồ phù hợp với câu hỏi phân tích.
- Đọc kết quả sau mỗi bước và viết nhận xét.
- Không chỉ chạy code, mà phải giải thích kết quả.
- Không kết luận vượt quá dữ liệu.
- Phân biệt rõ mô tả, tương quan, dự đoán và quan hệ nhân quả.

## 4. Việc cần tạo ra

Bạn phải tạo ra 2 sản phẩm:

1. Notebook phân tích:

`notebooks/dataset1_analysis.ipynb`

2. Báo cáo Markdown gửi lại sếp:

`reports/dataset1_analysis_report.md`

Nếu file đã tồn tại, hãy đọc trước nội dung cũ rồi cập nhật cẩn thận, không xóa tùy tiện những phần quan trọng.

## 5. Yêu cầu đối với notebook

Notebook `notebooks/dataset1_analysis.ipynb` phải được viết như một notebook phân tích hoàn chỉnh, gồm cả Markdown cell và Code cell.

Notebook cần có tối thiểu các phần sau:

### 5.1. Giới thiệu

- Mục tiêu phân tích Dataset 1.
- Dataset nằm ở đâu.
- Những câu hỏi phân tích ban đầu.

### 5.2. Import thư viện

Sử dụng các thư viện phù hợp, ví dụ:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scipy` nếu cần

Không dùng thư viện phức tạp nếu không cần thiết.

### 5.3. Đọc dữ liệu

- Đọc file `data/dataset1/dataset1.csv`.
- Hiển thị vài dòng đầu.
- Kiểm tra shape.
- Kiểm tra danh sách cột.
- Kiểm tra kiểu dữ liệu.

### 5.4. Data dictionary sơ bộ

Tạo bảng mô tả các cột:

- Tên cột.
- Kiểu dữ liệu.
- Vai trò dự kiến.
- Ý nghĩa suy đoán từ dữ liệu.

Nếu chưa chắc ý nghĩa của cột nào, hãy ghi rõ là suy đoán.

### 5.5. Data quality assessment

Phân tích chất lượng dữ liệu:

- Missing values theo từng cột.
- Tỷ lệ missing.
- Duplicate rows.
- Duplicate key nếu có key như transaction id.
- Kiểm tra giá trị bất thường.
- Kiểm tra biến số âm hoặc bằng 0 bất hợp lý.
- Kiểm tra tính nhất quán giữa các cột có liên quan.
- Kiểm tra bias hoặc limitation có thể có.

Sau mỗi nhóm kiểm tra, phải có Markdown cell nhận xét.

### 5.6. Descriptive statistics

Phân tích thống kê mô tả:

- Với biến số: count, mean, std, min, quartiles, max.
- Với biến phân loại: số lượng unique, top values, frequency.
- Với biến thời gian: min date, max date, số ngày/tháng, phân bố theo thời gian.

### 5.7. Exploratory Data Analysis

Thực hiện EDA bằng bảng và biểu đồ phù hợp.

Tối thiểu nên có:

- Phân tích doanh thu hoặc giá trị giao dịch nếu có biến phù hợp.
- Phân tích theo thời gian.
- Phân tích theo địa điểm nếu có.
- Phân tích theo category/sản phẩm nếu có.
- Phân tích theo customer segment nếu có.
- Phân tích theo payment method nếu có.
- Phân tích theo weather/holiday nếu có.
- Box plot cho một số biến số quan trọng.
- Heatmap hoặc pivot table nếu phù hợp.

Mỗi biểu đồ phải có:

- Tiêu đề rõ.
- Trục rõ.
- Nhận xét sau biểu đồ.

### 5.8. Bias, variation, measurement error

Dựa trên kiến thức đã học, phân tích:

- Dataset có thể có coverage bias không?
- Có thể có selection bias không?
- Có missing/nonresponse-like issue không?
- Có measurement bias hoặc measurement error không?
- Có sampling variation cần lưu ý không?

Phần này không cần quá dài, nhưng phải thể hiện tư duy Data Science.

### 5.9. Insight chính

Tổng hợp các insight có bằng chứng từ dữ liệu.

Với mỗi insight, cần ghi:

- Insight là gì.
- Bằng chứng từ bảng/biểu đồ nào.
- Ý nghĩa.
- Hạn chế khi diễn giải.

### 5.10. Kết luận Dataset 1

Kết luận:

- Dataset này mạnh ở điểm nào.
- Dataset này yếu hoặc hạn chế ở điểm nào.
- Dataset này phù hợp để trả lời loại câu hỏi nào.
- Dataset này có thể dùng cho modeling không, nếu có thì target gợi ý là gì.
- Các bước tiếp theo nên làm.

## 6. Bắt buộc phải chạy notebook

Sau khi tạo notebook, bạn phải **tự chạy toàn bộ notebook từ đầu đến cuối**.

Yêu cầu:

- Chạy từng cell hoặc chạy toàn bộ notebook bằng công cụ phù hợp.
- Nếu cell lỗi, phải sửa lỗi và chạy lại.
- Không được để notebook có cell lỗi.
- Không được viết báo cáo dựa trên giả định chưa chạy.
- Kết quả trong report phải dựa trên output thật từ notebook.

Nếu môi trường thiếu thư viện hoặc không chạy được vì lý do kỹ thuật, phải ghi rõ lỗi và cách xử lý.

## 7. Yêu cầu đối với báo cáo Markdown

Sau khi chạy notebook và đọc output, hãy viết báo cáo:

`reports/dataset1_analysis_report.md`

Báo cáo này là để gửi lại cho tôi, người quản lý project.

Báo cáo phải có cấu trúc:

1. **Executive Summary**
   - Tóm tắt ngắn gọn dataset và phát hiện chính.

2. **Dataset Overview**
   - Số dòng, số cột.
   - Các nhóm biến chính.
   - Phạm vi thời gian nếu có.
   - Phạm vi địa điểm nếu có.

3. **Data Quality Assessment**
   - Missing values.
   - Duplicates.
   - Outliers hoặc giá trị bất thường.
   - Measurement issues.
   - Bias/limitation.

4. **Exploratory Data Analysis**
   - Các phân tích chính.
   - Các bảng/biểu đồ quan trọng.
   - Nhận xét rõ ràng.

5. **Key Insights**
   - Liệt kê insight quan trọng.
   - Mỗi insight phải có bằng chứng.

6. **Modeling Potential**
   - Dataset có phù hợp để xây baseline model không?
   - Gợi ý target variable.
   - Gợi ý feature.
   - Gợi ý loại model phù hợp.
   - Cảnh báo data leakage nếu có.

7. **Limitations**
   - Các điểm chưa chắc chắn.
   - Các bias có thể có.
   - Các giới hạn khi diễn giải.

8. **Recommendations / Next Steps**
   - Những việc nên làm tiếp theo với Dataset 1.
   - Những câu hỏi nên phân tích thêm.
   - Cần chuẩn bị gì để so sánh với Dataset 2 và Dataset 3.

## 8. Nguyên tắc viết báo cáo

- Viết bằng tiếng Việt.
- Giọng văn chuyên nghiệp, rõ ràng, báo cáo lại cho sếp.
- Không viết quá chung chung.
- Không chép toàn bộ output thô nếu quá dài.
- Chỉ đưa bảng tóm tắt hoặc kết quả quan trọng.
- Kết luận phải dựa trên output đã chạy.
- Nếu một kết quả chưa đủ bằng chứng, hãy viết thận trọng.

## 9. Nguyên tắc code

- Code sạch, dễ đọc.
- Có comment khi logic không hiển nhiên.
- Không hard-code đường dẫn tuyệt đối nếu không cần.
- Dùng relative path từ notebook cho đúng repo.
- Lưu biểu đồ nếu cần, nhưng không tạo file rác không cần thiết.
- Không xóa hoặc sửa dataset gốc.
- Nếu cần tạo dữ liệu processed, lưu sang file mới và giải thích rõ.

## 10. Kết quả cuối cùng cần báo lại

Sau khi hoàn thành, hãy báo lại cho tôi:

- Notebook đã tạo/chỉnh ở đâu.
- Report đã tạo/chỉnh ở đâu.
- Notebook đã chạy thành công chưa.
- Các insight chính ngắn gọn.
- Có lỗi hoặc hạn chế nào không.

Hãy bắt đầu bằng việc đọc 3 file nền tảng đã nêu, sau đó phân tích `data/dataset1/dataset1.csv`, tạo notebook, chạy notebook, đọc output, và viết report Markdown.
