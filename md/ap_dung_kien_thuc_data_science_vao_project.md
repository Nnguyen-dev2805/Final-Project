# Phân tích các kiến thức đã học trong môn Khoa học Dữ liệu

## 1. Mục tiêu của tài liệu

Tài liệu này tổng hợp và phân tích các kiến thức đã học trong môn Khoa học Dữ liệu. Nội dung tập trung vào việc hiểu bản chất của từng khái niệm, cách sử dụng, khi nào nên dùng, khi nào không nên dùng, ưu điểm, nhược điểm và các lỗi diễn giải thường gặp.

Tài liệu này **chưa áp dụng vào project cụ thể**. Mục tiêu là tạo nền tảng lý thuyết vững trước khi quyết định kiến thức nào phù hợp để đưa vào một project phân tích dữ liệu.

## 2. Types of Bias

Bias là sai lệch có hệ thống trong quá trình thu thập, đo lường, chọn mẫu hoặc phân tích dữ liệu. Bias làm cho kết quả phân tích lệch khỏi sự thật của tổng thể cần nghiên cứu.

Điểm quan trọng: bias khác với random error. Random error có thể giảm khi tăng kích thước mẫu, còn bias có thể vẫn tồn tại dù dữ liệu rất lớn. Một dataset lớn nhưng bị bias vẫn có thể dẫn đến kết luận sai.

### 2.1. Coverage Bias

**Định nghĩa**

Coverage bias xảy ra khi sampling frame hoặc access frame không bao phủ đầy đủ target population. Nói cách khác, có một nhóm đối tượng đáng lẽ thuộc tổng thể nghiên cứu nhưng lại không có cơ hội xuất hiện trong dữ liệu.

**Ví dụ**

- Khảo sát online về thói quen học tập nhưng chỉ gửi cho sinh viên dùng email trường thường xuyên.
- Nghiên cứu người dùng mạng xã hội nhưng chỉ lấy dữ liệu từ một nền tảng.
- Phân tích hành vi khách hàng nhưng chỉ có dữ liệu từ khách hàng thành viên.

**Khi nào cần chú ý**

- Khi dữ liệu được lấy từ một nguồn duy nhất.
- Khi dataset không mô tả rõ phạm vi bao phủ.
- Khi muốn suy luận từ mẫu sang tổng thể lớn hơn.
- Khi một số nhóm người/khu vực/thời điểm có khả năng bị thiếu khỏi dữ liệu.

**Cách phát hiện**

- So sánh phạm vi dataset với target population.
- Kiểm tra metadata: dữ liệu được thu thập ở đâu, khi nào, từ ai.
- So sánh phân bố dữ liệu với nguồn tham chiếu đáng tin cậy nếu có.
- Tìm nhóm đối tượng đáng lẽ phải có nhưng không thấy trong dữ liệu.

**Cách xử lý**

- Giới hạn phạm vi kết luận đúng với dữ liệu hiện có.
- Bổ sung dữ liệu từ nguồn khác nếu có thể.
- Dùng weighting nếu biết nhóm nào bị thiếu và có tỷ lệ population thật.
- Ghi rõ limitation trong báo cáo.

**Ưu điểm khi phân tích coverage bias**

- Giúp tránh kết luận quá rộng.
- Làm report chuyên nghiệp hơn vì có đánh giá tính đại diện.
- Giúp người đọc hiểu dữ liệu nói được điều gì và không nói được điều gì.

**Nhược điểm/hạn chế**

- Không phải lúc nào cũng có dữ liệu tham chiếu để biết nhóm nào bị thiếu.
- Khó sửa hoàn toàn nếu dữ liệu ban đầu không bao phủ đúng population.
- Weighting có thể làm tăng variance nếu dùng không cẩn thận.

**Lỗi thường gặp**

- Thấy dataset lớn rồi mặc định là đại diện.
- Không phân biệt population trong dữ liệu và population muốn kết luận.
- Dùng kết quả từ một nhóm nhỏ để nói về toàn bộ xã hội/thị trường/người dùng.

### 2.2. Selection Bias

**Định nghĩa**

Selection bias xảy ra khi cách chọn dữ liệu làm cho một số đối tượng có xác suất được chọn cao hơn nhóm khác theo một cách có liên quan đến kết quả nghiên cứu.

**Ví dụ**

- Chỉ khảo sát người tự nguyện trả lời.
- Chỉ phân tích khách hàng còn hoạt động, bỏ qua khách hàng đã rời bỏ.
- Chỉ lấy dữ liệu từ cửa hàng có hệ thống ghi nhận tốt.

**Khi nào cần chú ý**

- Khi dữ liệu là convenience sample.
- Khi dữ liệu đến từ người tự chọn tham gia.
- Khi có quá trình lọc dữ liệu trước khi phân tích.
- Khi một số đối tượng khó tiếp cận hơn đối tượng khác.

**Cách phát hiện**

- Xem quy trình chọn mẫu.
- Kiểm tra xem tiêu chí lọc dữ liệu có liên quan đến outcome không.
- So sánh nhóm được chọn và nhóm không được chọn nếu có thông tin.
- Tự hỏi: "Ai có khả năng không xuất hiện trong dataset này?"

**Cách xử lý**

- Thiết kế quy trình sampling tốt hơn.
- Dùng random sampling nếu có thể.
- Ghi rõ tiêu chí chọn dữ liệu.
- Tránh diễn giải quan hệ nhân quả nếu selection bias có thể ảnh hưởng mạnh.

**Ưu điểm khi nhận diện selection bias**

- Giúp hiểu rõ giới hạn của kết quả.
- Giúp thiết kế sampling tốt hơn cho nghiên cứu sau.
- Giảm nguy cơ đưa ra quyết định sai dựa trên mẫu lệch.

**Nhược điểm/hạn chế**

- Khó biết selection bias mạnh đến mức nào nếu không có dữ liệu về nhóm bị loại.
- Nhiều dataset thực tế không ghi lại quá trình chọn mẫu.
- Việc sửa selection bias thường cần dữ liệu bổ sung.

**Lỗi thường gặp**

- Nhầm selection bias với missing values thông thường.
- Xóa dữ liệu thiếu quá mạnh làm tăng selection bias.
- Chỉ báo cáo kết quả trên nhóm còn lại mà không nói nhóm nào đã bị loại.

### 2.3. Nonresponse Bias

**Định nghĩa**

Nonresponse bias xảy ra khi đối tượng thuộc mẫu được chọn có thể được tiếp cận nhưng không phản hồi, và nhóm không phản hồi khác có hệ thống so với nhóm phản hồi.

**Ví dụ**

- Khảo sát mức độ hài lòng nhưng người không hài lòng không trả lời.
- Khảo sát thu nhập nhưng người thu nhập cao không muốn cung cấp thông tin.
- Survey sức khỏe nhưng nhóm bận rộn hoặc bệnh nặng ít phản hồi.

**Khi nào cần chú ý**

- Khi dữ liệu đến từ survey/questionnaire.
- Khi có tỷ lệ missing cao ở các câu hỏi nhạy cảm.
- Khi response rate thấp.
- Khi nhóm không phản hồi có thể khác nhóm phản hồi về hành vi hoặc outcome.

**Cách phát hiện**

- Tính response rate.
- So sánh đặc điểm cơ bản giữa respondent và nonrespondent nếu có.
- Kiểm tra missing pattern.
- Xem biến nào có missing nhiều nhất.

**Cách xử lý**

- Tăng response rate bằng reminder, incentive, thiết kế survey ngắn hơn.
- Dùng imputation nếu missing mechanism hợp lý.
- Dùng weighting adjustment nếu biết đặc điểm của nhóm không phản hồi.
- Báo cáo tỷ lệ không phản hồi và thảo luận limitation.

**Ưu điểm khi xử lý tốt**

- Kết quả survey đáng tin cậy hơn.
- Giảm sai lệch khi phân tích nhóm người dùng/khách hàng.
- Giúp report minh bạch hơn.

**Nhược điểm/hạn chế**

- Nếu nonresponse liên quan trực tiếp đến outcome, imputation có thể vẫn sai.
- Không thể biết chắc người không phản hồi sẽ trả lời thế nào.
- Weighting cần thông tin phụ trợ đáng tin cậy.

**Lỗi thường gặp**

- Xem missing values là ngẫu nhiên mà không kiểm tra.
- Xóa toàn bộ dòng thiếu dữ liệu làm mất thêm thông tin.
- Không báo cáo response rate.

### 2.4. Measurement Bias

**Định nghĩa**

Measurement bias xảy ra khi công cụ đo, quy trình đo, môi trường đo hoặc cách ghi nhận dữ liệu tạo ra sai lệch có hệ thống.

**Ví dụ**

- Cân bị lệch luôn đo cao hơn 0.5 kg.
- Cảm biến nhiệt độ đặt sai vị trí nên luôn đo nóng hơn thực tế.
- Câu hỏi survey được viết theo hướng dẫn dắt người trả lời.
- Nhân viên nhập liệu dùng cách phân loại khác nhau.

**Khi nào cần chú ý**

- Khi dữ liệu đến từ thiết bị đo.
- Khi dữ liệu được nhập thủ công.
- Khi có nhiều nguồn dữ liệu với chuẩn ghi nhận khác nhau.
- Khi biến đo lường là khái niệm trừu tượng như satisfaction, quality, risk.

**Cách phát hiện**

- Kiểm tra outlier và giá trị bất thường.
- So sánh nhiều nguồn đo nếu có.
- Kiểm tra consistency theo thời gian, địa điểm, người nhập.
- Xem tài liệu mô tả quy trình đo.

**Cách xử lý**

- Chuẩn hóa quy trình đo.
- Hiệu chỉnh thiết bị.
- Làm sạch dữ liệu và ghi lại rule xử lý.
- Kiểm tra độ tin cậy của biến đo.
- Dùng validation dataset nếu có.

**Ưu điểm khi phân tích measurement bias**

- Giúp tránh tin vào số liệu sai.
- Tăng chất lượng data cleaning.
- Hữu ích cho phần data quality trong report.

**Nhược điểm/hạn chế**

- Khó sửa nếu không biết lỗi đo xuất hiện từ đâu.
- Một số sai lệch không thể phát hiện chỉ bằng dữ liệu.
- Việc loại bỏ outlier quá mạnh có thể làm mất tín hiệu thật.

**Lỗi thường gặp**

- Xem mọi outlier là lỗi.
- Không kiểm tra đơn vị đo.
- Ghép nhiều nguồn dữ liệu mà không chuẩn hóa định nghĩa biến.

## 3. Types of Variation

Variation là sự biến động trong dữ liệu hoặc kết quả phân tích. Variation có thể đến từ chọn mẫu, phân công treatment, hoặc sai số đo.

Khác với bias, variation không nhất thiết làm kết quả lệch một chiều. Nó làm kết quả không ổn định giữa các mẫu, lần đo hoặc lần chạy.

### 3.1. Sampling Variation

**Định nghĩa**

Sampling variation là sự thay đổi của statistic từ mẫu này sang mẫu khác do yếu tố ngẫu nhiên trong quá trình chọn mẫu.

**Ví dụ**

- Lấy 100 sinh viên để tính điểm trung bình, mỗi lần lấy mẫu có thể ra trung bình khác nhau.
- Chia train/test khác nhau làm accuracy của model thay đổi.
- Lấy mẫu giao dịch khác nhau làm doanh thu trung bình khác nhau.

**Khi nào cần chú ý**

- Khi dùng sample để suy luận cho population.
- Khi dataset nhỏ.
- Khi so sánh hai nhóm có kích thước mẫu khác nhau.
- Khi đánh giá mô hình bằng một lần train/test split.

**Cách đo lường**

- Standard error.
- Confidence interval.
- Bootstrap.
- Cross-validation.
- Repeated sampling simulation.

**Cách xử lý**

- Tăng kích thước mẫu nếu có thể.
- Dùng random sampling đúng cách.
- Báo cáo confidence interval thay vì chỉ báo cáo point estimate.
- Dùng cross-validation khi đánh giá model.

**Ưu điểm khi phân tích sampling variation**

- Giúp kết luận có độ tin cậy hơn.
- Tránh overclaim từ một kết quả đơn lẻ.
- Hỗ trợ so sánh nhóm một cách cẩn thận.

**Nhược điểm/hạn chế**

- Không giải quyết được bias.
- Với dữ liệu phụ thuộc theo thời gian hoặc nhóm, sampling đơn giản có thể không phù hợp.
- Confidence interval dễ bị hiểu sai nếu giả định không đúng.

**Lỗi thường gặp**

- Báo cáo một con số duy nhất mà không nói độ bất định.
- Tưởng mẫu lớn thì không cần kiểm tra bias.
- Shuffle dữ liệu time-series rồi đánh giá như dữ liệu độc lập.

### 3.2. Assignment Variation

**Định nghĩa**

Assignment variation là sự thay đổi kết quả do cách phân công đối tượng vào các nhóm treatment/control trong thí nghiệm.

**Ví dụ**

- Trong A/B test, nhóm A và nhóm B được gán ngẫu nhiên. Nếu random assignment khác đi, kết quả có thể thay đổi.
- Một số nhóm treatment tình cờ có nhiều người dùng hoạt động mạnh hơn.

**Khi nào cần chú ý**

- Khi làm controlled experiment.
- Khi thiết kế A/B test.
- Khi so sánh treatment và control.
- Khi sample size của experiment nhỏ.

**Cách đo lường**

- Randomization inference.
- Permutation test.
- Repeated random assignment simulation.
- Balance check giữa nhóm treatment và control.

**Cách xử lý**

- Random assignment đúng cách.
- Đảm bảo cỡ mẫu đủ lớn.
- Kiểm tra balance của covariates.
- Dùng blocking/stratification nếu có nhóm quan trọng.

**Ưu điểm**

- Giúp đánh giá kết quả thí nghiệm có ổn định không.
- Là nền tảng để suy luận nhân quả trong experiment.
- Giúp thiết kế A/B test đáng tin cậy hơn.

**Nhược điểm/hạn chế**

- Chỉ phù hợp khi thật sự có thí nghiệm hoặc assignment mechanism rõ.
- Không nên dùng để khẳng định causal effect từ observational data.
- Nếu randomization thất bại, kết quả có thể lệch.

**Lỗi thường gặp**

- Gọi mọi so sánh hai nhóm là experiment.
- Xem biến treatment trong observational data như được random assign.
- Không kiểm tra balance trước khi kết luận.

### 3.3. Measurement Error

**Định nghĩa**

Measurement error là sai số phát sinh trong quá trình đo lường. Sai số có thể ngẫu nhiên hoặc có hệ thống.

**Ví dụ**

- Người nhập nhầm số.
- Thiết bị đo dao động.
- Người trả lời survey nhớ sai.
- Dữ liệu thời gian bị sai timezone.

**Khi nào cần chú ý**

- Khi biến quan trọng được đo bằng thiết bị hoặc nhập thủ công.
- Khi dữ liệu có nhiều nguồn.
- Khi phát hiện giá trị bất thường.
- Khi biến có đơn vị đo hoặc định nghĩa phức tạp.

**Cách xử lý**

- Data validation.
- Range check.
- Consistency check.
- Duplicate check.
- So sánh với nguồn dữ liệu khác.
- Ghi rõ quy tắc cleaning.

**Ưu điểm khi xử lý tốt**

- Cải thiện chất lượng dữ liệu.
- Giảm lỗi trong mô hình.
- Làm insight đáng tin hơn.

**Nhược điểm/hạn chế**

- Không phải lỗi nào cũng phát hiện được.
- Sửa dữ liệu sai có thể đưa thêm giả định chủ quan.
- Loại bỏ quá nhiều dữ liệu có thể gây selection bias.

## 4. Simulation and Experiment Design

Simulation là phương pháp tạo ra nhiều kịch bản giả lập để hiểu hành vi của hệ thống hoặc độ bất định của kết quả. Experiment design là cách thiết kế thí nghiệm để kiểm tra giả thuyết một cách có kiểm soát.

### 4.1. Simulation

**Định nghĩa**

Simulation là quá trình mô phỏng một hiện tượng bằng cách định nghĩa quy tắc, tham số và yếu tố ngẫu nhiên, sau đó chạy nhiều lần để quan sát kết quả.

**Ví dụ từ slide rút bi**

Một bình có số lượng bi nhất định. Mỗi viên bi có màu. Ta rút bi nhiều lần để xem xác suất hoặc phân phối kết quả.

Trong setup này:

- **Number of marbles:** số phần tử trong population.
- **Color on each marble:** nhãn/category/thuộc tính của phần tử.
- **Number of draws:** số lần lấy mẫu hoặc số quan sát được chọn.

**Khi nào nên dùng simulation**

- Khi bài toán có yếu tố ngẫu nhiên.
- Khi muốn hiểu phân phối kết quả, không chỉ một kết quả duy nhất.
- Khi công thức lý thuyết khó tính trực tiếp.
- Khi muốn kiểm tra giả định hoặc kịch bản "what-if".

**Cách sử dụng cơ bản**

1. Xác định câu hỏi cần mô phỏng.
2. Xác định population hoặc phân phối đầu vào.
3. Xác định rule sinh dữ liệu hoặc rule lấy mẫu.
4. Chạy mô phỏng nhiều lần.
5. Tóm tắt kết quả bằng mean, median, quantile, confidence interval.
6. Kiểm tra độ nhạy với các giả định.

**Ưu điểm**

- Linh hoạt.
- Dễ giải thích trực quan.
- Hữu ích khi bài toán phức tạp.
- Cho thấy độ bất định của kết quả.

**Nhược điểm**

- Kết quả phụ thuộc mạnh vào giả định đầu vào.
- Nếu mô hình mô phỏng sai, kết quả cũng sai.
- Có thể tốn thời gian tính toán.
- Không tự chứng minh quan hệ nhân quả.

**Lỗi thường gặp**

- Không nói rõ giả định.
- Chạy quá ít lần mô phỏng.
- Nhầm kết quả mô phỏng với dữ liệu thực tế.
- Dùng phân phối đầu vào tùy tiện.

### 4.2. Experiment Design

**Định nghĩa**

Experiment design là quá trình thiết kế thí nghiệm để đo tác động của một treatment lên outcome trong điều kiện có kiểm soát.

**Các thành phần chính**

- **Treatment:** tác động hoặc thay đổi được áp dụng.
- **Control:** nhóm không nhận treatment hoặc nhận điều kiện chuẩn.
- **Outcome:** biến kết quả cần đo.
- **Random assignment:** phân ngẫu nhiên đối tượng vào nhóm treatment/control.
- **Sample size:** số lượng đối tượng đủ để phát hiện hiệu ứng.
- **Confounders:** biến gây nhiễu cần kiểm soát.

**Khi nào nên dùng**

- Khi muốn đánh giá tác động nhân quả.
- Khi có thể kiểm soát việc phân nhóm.
- Khi cần kiểm tra hiệu quả của một thay đổi, chính sách, giao diện, chương trình.

**Khi nào không nên dùng hoặc cần cẩn thận**

- Khi không thể random assignment.
- Khi treatment có rủi ro đạo đức.
- Khi sample size quá nhỏ.
- Khi nhóm treatment/control bị contamination.

**Ưu điểm**

- Là phương pháp mạnh để suy luận nhân quả.
- Randomization giúp giảm confounding.
- Kết quả dễ diễn giải nếu thiết kế tốt.

**Nhược điểm**

- Có thể tốn thời gian và chi phí.
- Không phải lúc nào cũng khả thi về đạo đức hoặc kỹ thuật.
- Kết quả trong thí nghiệm có thể không generalize ra môi trường thật.
- Cần thiết kế cẩn thận để tránh bias.

**Lỗi thường gặp**

- Không có control group.
- Không random assignment nhưng vẫn gọi là experiment.
- Thay đổi nhiều yếu tố cùng lúc nên không biết yếu tố nào gây hiệu ứng.
- Dừng thí nghiệm quá sớm khi thấy kết quả tạm thời tốt.

## 5. Types of Randomness

Randomness là yếu tố ngẫu nhiên trong mô phỏng, lấy mẫu, chia dữ liệu, hoặc thuật toán. Dùng randomness đúng cách giúp mô hình hóa uncertainty; dùng sai có thể làm kết quả không tái lập hoặc sai logic.

### 5.1. Random

**Ý nghĩa**

Tạo số ngẫu nhiên cơ bản, thường trong khoảng từ 0 đến 1.

**Khi dùng**

- Khởi tạo simulation.
- Tạo xác suất ngẫu nhiên.
- Quyết định một sự kiện có xảy ra hay không.

**Ưu điểm**

- Đơn giản, linh hoạt.
- Là nền tảng cho nhiều kỹ thuật mô phỏng.

**Nhược điểm**

- Nếu không đặt seed, kết quả khó tái lập.
- Không đủ cụ thể nếu bài toán cần phân phối rõ ràng.

**Lưu ý**

Luôn đặt random seed trong phân tích cần tái lập.

### 5.2. Uniform

**Ý nghĩa**

Uniform distribution là phân phối đều, mọi giá trị trong một khoảng có xác suất như nhau.

**Khi dùng**

- Khi thật sự không có lý do để giá trị nào xảy ra nhiều hơn giá trị khác.
- Mô phỏng lựa chọn công bằng.
- Tạo baseline ngẫu nhiên.

**Ưu điểm**

- Dễ hiểu.
- Dễ triển khai.
- Phù hợp với random selection công bằng.

**Nhược điểm**

- Thường quá đơn giản so với dữ liệu thật.
- Dùng sai có thể tạo mô phỏng phi thực tế.

**Lỗi thường gặp**

- Mặc định dùng uniform chỉ vì tiện, dù dữ liệu thật lệch rõ ràng.

### 5.3. Normal/Gauss

**Ý nghĩa**

Normal distribution là phân phối hình chuông, tập trung quanh mean, đối xứng hai bên.

**Khi dùng**

- Mô hình hóa sai số đo ngẫu nhiên.
- Mô hình hóa biến là tổng của nhiều yếu tố nhỏ độc lập.
- Dùng trong các phương pháp thống kê có giả định gần chuẩn.

**Ưu điểm**

- Có nền tảng lý thuyết mạnh.
- Nhiều phương pháp thống kê dựa trên normal distribution.
- Dễ diễn giải bằng mean và standard deviation.

**Nhược điểm**

- Không phù hợp với dữ liệu lệch mạnh.
- Không phù hợp với dữ liệu bị giới hạn một phía như doanh thu không âm nếu phân phối lệch.
- Nhạy với outlier nếu dùng mean/std.

**Cách kiểm tra trước khi dùng**

- Histogram.
- Q-Q plot.
- Skewness/kurtosis.
- So sánh mean và median.

### 5.4. Triangular

**Ý nghĩa**

Triangular distribution được xác định bởi ba giá trị: minimum, most likely, maximum.

**Khi dùng**

- Khi không có đủ dữ liệu lịch sử nhưng có ước lượng chuyên gia.
- Khi muốn mô phỏng kịch bản với giá trị thấp nhất, thường gặp nhất, cao nhất.
- Phân tích rủi ro đơn giản.

**Ưu điểm**

- Dễ dùng khi dữ liệu ít.
- Trực quan với người không chuyên.
- Tốt cho scenario analysis sơ bộ.

**Nhược điểm**

- Phụ thuộc vào ước lượng chủ quan.
- Không phản ánh được đuôi phân phối phức tạp.
- Có thể quá đơn giản cho dữ liệu thực tế.

### 5.5. Randint

**Ý nghĩa**

Sinh số nguyên ngẫu nhiên trong một khoảng.

**Khi dùng**

- Chọn index ngẫu nhiên.
- Mô phỏng số lượng rời rạc.
- Sinh nhãn nhóm hoặc ID giả lập.

**Ưu điểm**

- Phù hợp cho biến rời rạc.
- Dễ triển khai.

**Nhược điểm**

- Nếu dùng phân phối đều cho số nguyên, có thể không phản ánh dữ liệu thật.
- Không phù hợp với biến liên tục.

### 5.6. Shuffle

**Ý nghĩa**

Xáo trộn thứ tự các phần tử.

**Khi dùng**

- Xáo dữ liệu trước khi chia train/test trong dữ liệu độc lập.
- Random assignment trong experiment.
- Permutation test.

**Ưu điểm**

- Đơn giản.
- Giúp giảm ảnh hưởng của thứ tự ban đầu.
- Hữu ích trong kiểm định ngẫu nhiên.

**Nhược điểm**

- Không phù hợp với dữ liệu time-series nếu cần giữ thứ tự thời gian.
- Có thể phá cấu trúc nhóm nếu dữ liệu có phân cấp.

### 5.7. Choice/Choices

**Ý nghĩa**

Chọn một hoặc nhiều phần tử từ danh sách, có thể có trọng số xác suất.

**Khi dùng**

- Mô phỏng lựa chọn category.
- Sampling theo xác suất khác nhau.
- Tạo dữ liệu giả lập có phân phối category mong muốn.

**Ưu điểm**

- Linh hoạt.
- Có thể mô phỏng lựa chọn có trọng số.

**Nhược điểm**

- Cần xác suất đầu vào hợp lý.
- Nếu xác suất sai, mô phỏng sai.

### 5.8. Sample

**Ý nghĩa**

Lấy mẫu từ tập dữ liệu. Có thể lấy mẫu có hoàn lại hoặc không hoàn lại tùy công cụ.

**Khi dùng**

- Random sampling.
- Bootstrap.
- Tạo subset để phân tích nhanh.

**Ưu điểm**

- Rất quan trọng trong thống kê.
- Dễ dùng để kiểm tra sampling variation.

**Nhược điểm**

- Mẫu nhỏ có thể không đại diện.
- Sampling sai cách có thể gây bias.

## 6. Monte Carlo Simulation

**Định nghĩa**

Monte Carlo simulation là phương pháp dùng nhiều lần lấy mẫu ngẫu nhiên hoặc mô phỏng ngẫu nhiên để ước lượng phân phối của một kết quả.

**Khi nên dùng**

- Khi bài toán có nhiều yếu tố bất định.
- Khi muốn biết khoảng kết quả có thể xảy ra thay vì chỉ một giá trị.
- Khi công thức chính xác khó tính.
- Khi cần scenario analysis hoặc risk analysis.

**Cách sử dụng cơ bản**

1. Xác định output cần ước lượng.
2. Xác định các input ngẫu nhiên và phân phối của chúng.
3. Sinh random values cho input.
4. Tính output.
5. Lặp lại nhiều lần.
6. Phân tích phân phối output.

**Kết quả thường báo cáo**

- Mean.
- Median.
- Standard deviation.
- Percentiles.
- Confidence interval hoặc simulation interval.
- Probability của một event.

**Ưu điểm**

- Mạnh và linh hoạt.
- Dễ mở rộng cho bài toán phức tạp.
- Giúp hiểu uncertainty.
- Phù hợp để trình bày bằng biểu đồ.

**Nhược điểm**

- Phụ thuộc hoàn toàn vào giả định phân phối đầu vào.
- Cần số lần chạy đủ lớn.
- Có thể tạo cảm giác chính xác giả nếu giả định yếu.
- Không thay thế dữ liệu thật.

**Lỗi thường gặp**

- Không kiểm tra sensitivity với giả định.
- Chọn phân phối đầu vào tùy tiện.
- Không đặt random seed.
- Báo cáo mean mà không báo cáo độ bất định.

## 7. Bootstrapping

**Định nghĩa**

Bootstrapping là phương pháp lấy mẫu có hoàn lại từ dữ liệu quan sát được để ước lượng độ bất định của statistic.

**Ý tưởng chính**

Nếu dataset hiện có đại diện hợp lý cho population, ta có thể xem nó như một population xấp xỉ. Bằng cách lấy mẫu có hoàn lại nhiều lần, ta tạo ra nhiều bootstrap samples và tính statistic trên từng sample.

**Khi nên dùng**

- Khi muốn ước lượng confidence interval.
- Khi phân phối lý thuyết của statistic khó xác định.
- Khi không muốn giả định normal distribution quá mạnh.
- Khi cần đánh giá độ ổn định của median, mean, correlation, difference between groups.

**Khi không nên dùng hoặc cần cẩn thận**

- Khi mẫu ban đầu quá nhỏ hoặc không đại diện.
- Khi dữ liệu có phụ thuộc thời gian mà bootstrap thường phá vỡ cấu trúc.
- Khi dữ liệu có nhóm/phân cấp nhưng bootstrap không giữ cấu trúc nhóm.
- Khi bias trong dữ liệu gốc quá mạnh.

**Cách sử dụng cơ bản**

1. Có dataset gốc với n quan sát.
2. Lấy mẫu n quan sát có hoàn lại.
3. Tính statistic quan tâm.
4. Lặp lại B lần, ví dụ 1,000 hoặc 10,000.
5. Dùng phân phối bootstrap để lấy confidence interval.

**Ưu điểm**

- Dễ hiểu và dễ triển khai.
- Ít phụ thuộc vào công thức lý thuyết.
- Phù hợp với nhiều statistic.
- Hữu ích trong report vì giúp thể hiện uncertainty.

**Nhược điểm**

- Không sửa được bias của dữ liệu gốc.
- Có thể sai nếu quan sát không độc lập.
- Tốn tính toán với dataset lớn hoặc statistic phức tạp.
- Kết quả phụ thuộc vào chất lượng sample ban đầu.

**Lỗi thường gặp**

- Nghĩ bootstrap tạo ra thông tin mới.
- Bootstrap trên dữ liệu time-series mà không dùng block bootstrap.
- Chỉ báo cáo interval mà không giải thích ý nghĩa.

## 8. Advanced Diagrams

Visualization giúp khám phá dữ liệu, truyền đạt insight và phát hiện vấn đề dữ liệu. Advanced diagrams nên được dùng khi chúng giúp trả lời câu hỏi rõ ràng, không nên dùng chỉ vì đẹp.

### 8.1. Box Diagram / Box Plot

**Định nghĩa**

Box plot biểu diễn phân phối của biến số qua median, quartiles, interquartile range và outliers.

**Thành phần**

- Median: đường giữa box.
- Q1, Q3: phần dưới và trên của box.
- IQR = Q3 - Q1.
- Whiskers: khoảng dữ liệu nằm trong ngưỡng thường dùng.
- Outliers: điểm nằm ngoài whiskers.

**Khi nên dùng**

- So sánh phân phối của biến số giữa nhiều nhóm.
- Phát hiện outlier.
- Xem median và độ phân tán.
- Khi không muốn chỉ dùng mean.

**Ưu điểm**

- Gọn, hiệu quả.
- So sánh nhiều nhóm tốt.
- Thể hiện outlier rõ.
- Không cần giả định phân phối chuẩn.

**Nhược điểm**

- Không thể hiện chi tiết hình dạng phân phối như histogram.
- Với sample nhỏ, box plot có thể gây hiểu nhầm.
- Outlier theo box plot không nhất thiết là lỗi dữ liệu.

**Lỗi thường gặp**

- Xóa mọi outlier chỉ vì box plot đánh dấu.
- Không xem số lượng mẫu mỗi nhóm.
- So sánh box plot giữa nhóm có sample size quá khác nhau mà không thận trọng.

### 8.2. Candlestick Chart

**Định nghĩa**

Candlestick chart là biểu đồ thường dùng trong tài chính để biểu diễn open, high, low, close của một biến theo thời gian.

**Thành phần**

- Open: giá trị đầu kỳ.
- Close: giá trị cuối kỳ.
- High: giá trị cao nhất trong kỳ.
- Low: giá trị thấp nhất trong kỳ.
- Body: khoảng giữa open và close.
- Wick/shadow: khoảng từ high/low tới body.

**Khi nên dùng**

- Dữ liệu có cấu trúc thời gian rõ.
- Mỗi khoảng thời gian có thể định nghĩa open/high/low/close.
- Phân tích biến động trong mỗi kỳ.
- Dữ liệu tài chính hoặc dữ liệu có logic tương tự tài chính.

**Ưu điểm**

- Thể hiện nhiều thông tin trong một biểu đồ.
- Rất tốt để nhìn biến động theo thời gian.
- Giúp phát hiện volatility và pattern.

**Nhược điểm**

- Khó hiểu với người không quen.
- Không phù hợp nếu dữ liệu không có open/high/low/close tự nhiên.
- Dễ bị dùng sai cho dữ liệu không phù hợp.

**Lỗi thường gặp**

- Ép dữ liệu không có cấu trúc OHLC vào candlestick.
- Không giải thích rõ open/high/low/close được định nghĩa thế nào.
- Dùng candlestick khi line chart hoặc bar chart dễ hiểu hơn.

### 8.3. Network Diagram

**Định nghĩa**

Network diagram biểu diễn dữ liệu dưới dạng graph gồm nodes và edges. Node là đối tượng, edge là quan hệ giữa các đối tượng.

**Ví dụ node và edge**

- Node: người dùng; edge: quan hệ bạn bè.
- Node: sản phẩm; edge: cùng được mua.
- Node: website; edge: hyperlink.
- Node: thành phố; edge: luồng di chuyển.

**Khi nên dùng**

- Dữ liệu thật sự có quan hệ giữa các thực thể.
- Câu hỏi phân tích liên quan đến kết nối, cụm, trung tâm, lan truyền.
- Cần tìm community, hub, bridge, influence.

**Chỉ số thường dùng**

- Degree centrality.
- Betweenness centrality.
- Closeness centrality.
- PageRank.
- Clustering coefficient.
- Community detection.

**Ưu điểm**

- Biểu diễn quan hệ tốt hơn bảng truyền thống.
- Giúp phát hiện cấu trúc cụm.
- Hữu ích cho dữ liệu social, recommendation, transaction, knowledge graph.

**Nhược điểm**

- Dễ trở nên rối nếu quá nhiều node/edge.
- Layout có thể ảnh hưởng cảm nhận của người đọc.
- Cần định nghĩa edge rõ ràng.
- Network đẹp không đồng nghĩa insight tốt.

**Lỗi thường gặp**

- Tạo network khi dữ liệu không có quan hệ thật.
- Không giải thích edge weight.
- Diễn giải khoảng cách trên layout như khoảng cách thật dù layout chỉ là thuật toán vẽ.

## 9. Network Layouts

Network layout là cách sắp xếp node trong không gian để biểu diễn graph. Layout không thay đổi dữ liệu graph, nhưng ảnh hưởng cách người đọc nhìn thấy pattern.

### 9.1. Easy Network Layouts

**Ý nghĩa**

Các layout đơn giản như circular, shell, random, grid.

**Khi dùng**

- Graph nhỏ.
- Muốn trình bày rõ node/edge mà không cần phân tích cấu trúc phức tạp.
- Dùng làm bước đầu để kiểm tra graph.

**Ưu điểm**

- Dễ hiểu.
- Nhanh.
- Ít tham số.

**Nhược điểm**

- Không thể hiện tốt community hoặc centrality.
- Với graph lớn dễ rối.

### 9.2. Physics-driven Layouts

Physics-driven layouts mô phỏng lực hút/đẩy giữa các node để đặt node có quan hệ gần nhau hơn.

#### Spectral Layout

**Ý nghĩa**

Dùng eigenvectors của graph Laplacian để đặt node trong không gian.

**Khi dùng**

- Muốn nhìn cấu trúc tổng thể của graph.
- Graph có cấu trúc cụm tương đối rõ.

**Ưu điểm**

- Có nền tảng toán học.
- Có thể phát hiện cấu trúc global.

**Nhược điểm**

- Có thể khó giải thích với người không quen.
- Không luôn đẹp trực quan.

#### Kamada-Kawai Layout

**Ý nghĩa**

Cố gắng đặt các node sao cho khoảng cách hình học phản ánh graph distance.

**Khi dùng**

- Graph nhỏ đến trung bình.
- Muốn layout cân bằng và dễ nhìn.

**Ưu điểm**

- Thường cho hình đẹp.
- Biểu diễn khoảng cách graph khá trực quan.

**Nhược điểm**

- Tốn tính toán với graph lớn.
- Vẫn cần giải thích rằng khoảng cách là kết quả layout, không phải biến đo trực tiếp.

#### Fruchterman-Reingold Layout

**Ý nghĩa**

Force-directed layout phổ biến, node đẩy nhau và edge kéo node lại gần nhau.

**Khi dùng**

- Graph nhỏ/trung bình.
- Muốn visual hóa community hoặc cluster.

**Ưu điểm**

- Trực quan.
- Phổ biến.
- Dễ dùng.

**Nhược điểm**

- Kết quả phụ thuộc tham số và random seed.
- Graph lớn có thể rối.
- Layout đẹp nhưng không đủ để kết luận định lượng.

### 9.3. Data-driven Layout

**Ý nghĩa**

Data-driven layout đặt node dựa trên biến dữ liệu cụ thể, thay vì chỉ dựa trên cấu trúc graph.

**Ví dụ**

- Trục X là doanh thu.
- Trục Y là số lượng kết nối.
- Kích thước node là centrality.
- Màu node là community.

**Khi dùng**

- Khi muốn người đọc hiểu node theo biến dữ liệu rõ ràng.
- Khi có metadata quan trọng.
- Khi layout force-directed quá khó diễn giải.

**Ưu điểm**

- Dễ giải thích hơn.
- Gắn trực tiếp với biến phân tích.
- Giảm nguy cơ diễn giải sai layout.

**Nhược điểm**

- Có thể không thể hiện tốt cấu trúc network thuần túy.
- Cần chọn trục dữ liệu có ý nghĩa.

## 10. Report vs Dashboard

Report và dashboard đều dùng để truyền đạt kết quả phân tích, nhưng mục tiêu khác nhau.

### 10.1. Report

**Định nghĩa**

Report là tài liệu phân tích có cấu trúc, trình bày câu hỏi, dữ liệu, phương pháp, kết quả, diễn giải, hạn chế và kết luận.

**Khi nên dùng**

- Khi cần kể một câu chuyện phân tích hoàn chỉnh.
- Khi người đọc cần hiểu phương pháp và logic.
- Khi cần nộp bài học thuật hoặc báo cáo nghiên cứu.
- Khi kết luận cần được giải thích cẩn thận.

**Ưu điểm**

- Có mạch lập luận rõ.
- Phù hợp để giải thích methodology.
- Dễ trình bày limitation.
- Tốt cho đánh giá học thuật.

**Nhược điểm**

- Ít tương tác.
- Có thể dài.
- Không phù hợp để monitoring thời gian thực.

### 10.2. Dashboard

**Định nghĩa**

Dashboard là giao diện trực quan, thường có biểu đồ và bộ lọc, giúp theo dõi chỉ số hoặc khám phá dữ liệu tương tác.

**Khi nên dùng**

- Khi cần theo dõi KPI thường xuyên.
- Khi người dùng muốn tự lọc và khám phá dữ liệu.
- Khi dữ liệu cập nhật liên tục.
- Khi cần ra quyết định vận hành nhanh.

**Ưu điểm**

- Tương tác tốt.
- Dễ theo dõi chỉ số.
- Phù hợp cho business monitoring.
- Có thể cập nhật tự động.

**Nhược điểm**

- Dễ thiếu bối cảnh nếu không có giải thích.
- Không thay thế report phân tích sâu.
- Có thể làm người xem tự diễn giải sai.
- Thiết kế dashboard tốt tốn công.

### 10.3. Khi chọn report hay dashboard

Nên chọn **report** nếu mục tiêu là phân tích sâu, giải thích phương pháp, trình bày kết luận và limitation.

Nên chọn **dashboard** nếu mục tiêu là theo dõi chỉ số, cho phép người dùng tương tác, hoặc cập nhật dữ liệu thường xuyên.

Trong nhiều dự án thực tế, report dùng để trả lời câu hỏi phân tích chính, còn dashboard dùng để theo dõi các chỉ số sau khi insight đã được xác định.

## 11. scipy.optimize

`scipy.optimize` là module trong SciPy dùng để giải các bài toán tối ưu hóa. Tối ưu hóa nghĩa là tìm giá trị của biến đầu vào sao cho một hàm mục tiêu đạt giá trị nhỏ nhất hoặc lớn nhất.

Thông thường thư viện tối ưu hóa sẽ minimize một objective function. Nếu muốn maximize, ta có thể minimize giá trị âm của hàm mục tiêu.

### 11.1. Khi nào dùng optimization

Optimization phù hợp khi có:

- Một objective function rõ ràng.
- Các biến cần điều chỉnh.
- Ràng buộc hoặc miền giá trị hợp lệ.
- Tiêu chí đánh giá tốt/xấu rõ.

Ví dụ:

- Tối thiểu hóa cost.
- Tối đa hóa profit.
- Tối thiểu hóa loss của model.
- Tìm tham số tốt nhất cho một hàm.
- Tìm allocation tối ưu dưới ràng buộc ngân sách.

### 11.2. Black-box Optimization

**Định nghĩa**

Black-box optimization dùng khi không biết, không có, hoặc không muốn dùng đạo hàm của objective function. Ta chỉ có thể đưa input vào hàm và quan sát output.

**Ví dụ thuật toán**

- Nelder-Mead simplex.

**Khi nên dùng**

- Objective function không trơn.
- Không tính được gradient.
- Hàm mục tiêu là kết quả của simulation.
- Số chiều không quá lớn.

**Ưu điểm**

- Không cần đạo hàm.
- Linh hoạt.
- Dễ áp dụng với hàm phức tạp hoặc simulation.

**Nhược điểm**

- Có thể chậm.
- Không đảm bảo tìm global optimum.
- Kém hiệu quả với số chiều cao.
- Phụ thuộc điểm khởi tạo.

**Lỗi thường gặp**

- Dùng black-box optimizer cho bài toán có gradient rõ ràng làm chậm không cần thiết.
- Không kiểm tra nhiều điểm khởi tạo.
- Tin rằng kết quả là global optimum.

### 11.3. White-box Optimization

**Định nghĩa**

White-box optimization dùng thông tin cấu trúc của hàm mục tiêu, thường là gradient hoặc Hessian, để tối ưu hiệu quả hơn.

**Ví dụ thuật toán**

- Broyden-Fletcher-Goldfarb-Shanno (BFGS).
- Newton-Conjugate-Gradient.

**Khi nên dùng**

- Objective function trơn.
- Có thể tính gradient.
- Bài toán có nhiều biến.
- Cần tối ưu nhanh và chính xác hơn.

**Ưu điểm**

- Thường nhanh hơn black-box optimization.
- Hiệu quả với bài toán liên tục.
- Có nền tảng toán học mạnh.

**Nhược điểm**

- Cần gradient hoặc xấp xỉ gradient.
- Có thể mắc kẹt ở local optimum.
- Nhạy với scaling của biến.
- Không phù hợp với hàm không liên tục hoặc noisy quá mạnh.

**Lỗi thường gặp**

- Không chuẩn hóa biến đầu vào.
- Không kiểm tra convergence.
- Không hiểu objective function đang tối ưu điều gì.

### 11.4. Lưu ý chung khi dùng scipy.optimize

- Luôn xác định rõ objective function.
- Kiểm tra miền giá trị hợp lệ của tham số.
- Nếu có ràng buộc, dùng optimizer hỗ trợ constraints.
- Chạy từ nhiều initial points nếu nghi ngờ local optimum.
- Kiểm tra kết quả bằng logic nghiệp vụ hoặc phân tích nhạy cảm.
- Không dùng optimization nếu chưa có câu hỏi tối ưu rõ ràng.

## 12. Bảng tổng hợp nhanh

| Kiến thức | Dùng để làm gì | Khi nên dùng | Cẩn thận điều gì |
|---|---|---|---|
| Coverage bias | Kiểm tra độ bao phủ population | Khi muốn suy luận rộng | Dataset lớn không đồng nghĩa đại diện |
| Selection bias | Kiểm tra sai lệch do cách chọn mẫu | Khi dữ liệu được lọc/chọn theo tiện lợi | Khó sửa nếu thiếu dữ liệu nhóm bị loại |
| Nonresponse bias | Kiểm tra sai lệch do không phản hồi | Survey, missing nhạy cảm | Missing không luôn ngẫu nhiên |
| Measurement bias | Kiểm tra sai lệch đo lường có hệ thống | Dữ liệu từ thiết bị/quy trình nhập liệu | Outlier không luôn là lỗi |
| Sampling variation | Đánh giá biến động do chọn mẫu | Suy luận thống kê, train/test split | Không xử lý được bias |
| Assignment variation | Đánh giá biến động trong experiment | A/B test, controlled experiment | Không dùng cho observational data nếu không có assignment |
| Measurement error | Kiểm tra lỗi đo/ghi nhận | Data cleaning, validation | Sửa dữ liệu cần rule rõ |
| Simulation | Mô phỏng kịch bản và uncertainty | Bài toán có ngẫu nhiên/what-if | Phụ thuộc giả định đầu vào |
| Monte Carlo | Ước lượng phân phối kết quả bằng mô phỏng | Risk, scenario, uncertainty | Cần nhiều lần chạy và giả định hợp lý |
| Bootstrapping | Ước lượng uncertainty từ sample | Confidence interval cho statistic | Không sửa bias của sample gốc |
| Box plot | So sánh phân phối và outlier | EDA giữa nhiều nhóm | Outlier không tự động là dữ liệu sai |
| Candlestick chart | Biểu diễn OHLC theo thời gian | Dữ liệu tài chính/time series có OHLC | Không ép dùng nếu dữ liệu không phù hợp |
| Network diagram | Biểu diễn quan hệ node-edge | Dữ liệu có quan hệ thật | Cần định nghĩa edge rõ |
| Network layouts | Sắp xếp node để đọc graph | Khi trực quan hóa network | Layout không phải bằng chứng định lượng |
| Report | Trình bày phân tích có lập luận | Báo cáo học thuật/phân tích sâu | Ít tương tác |
| Dashboard | Theo dõi chỉ số tương tác | Monitoring/KPI | Dễ thiếu bối cảnh |
| scipy.optimize | Tìm tham số tối ưu | Có objective rõ | Không dùng khi chưa có bài toán tối ưu |

## 13. Kết luận

Các kiến thức trên là nền tảng quan trọng trong một quy trình Khoa học Dữ liệu nghiêm túc. Nhóm kiến thức về **bias** và **variation** giúp đánh giá độ tin cậy của dữ liệu và kết luận. Nhóm **simulation**, **Monte Carlo** và **bootstrapping** giúp định lượng uncertainty. Nhóm **advanced diagrams** và **network layouts** giúp trực quan hóa dữ liệu phức tạp. Phần **report vs dashboard** giúp chọn đúng hình thức trình bày. Cuối cùng, **scipy.optimize** hỗ trợ giải bài toán tối ưu khi có objective function rõ ràng.

Điểm quan trọng nhất là không dùng kỹ thuật chỉ vì kỹ thuật đó nâng cao. Một kỹ thuật chỉ nên được dùng khi nó phù hợp với câu hỏi phân tích, phù hợp với cấu trúc dữ liệu, và giúp kết luận trở nên rõ ràng hoặc đáng tin cậy hơn.
