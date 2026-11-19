# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): ABC
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-ABC-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S1

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
| 1 | Trần Văn Quang | 2A202604032 | Kỹ sư cổng: guards, chốt mốc và tích hợp | Có |
| 2 | Nguyễn Hoàng Ân | 2A202604025 | Kỹ sư cổng: đánh giá, kiểm thử và monitors | |
| 3 | Vũ Trọng Thắng | 2A202604022 | Sản phẩm và kinh doanh | |
| 4 | Phạm Văn Chiêu | 2A202604033 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Các mục đóng góp, bằng chứng và exit ticket được trình bày theo phần việc phụ trách của từng thành viên. Số liệu kết quả tham chiếu báo cáo đã lưu trong repo. Nhóm đã thống nhất quyết định v2: Tiếp tục pilot có kiểm soát.

## TranVanQuang-2A202604032

### Phần việc phụ trách

Nhóm trưởng; phụ trách `lab10/guards.py`, Phiếu B mục B7.1, phần kỹ thuật trong Phiếu C mục C6–C7–C9. Viết 2–3 cổng vòng 1 từ pre-mortem/HAZOP, sửa cổng theo thẻ ở vòng 2; phối hợp cả nhóm về nhánh nguyên nhân ngoài kỹ thuật. Tổng hợp Phiếu B và Phiếu C từ nội dung các thành viên gửi; điều phối ký tiêu chí, chốt vòng 1, nhận đúng thẻ và kiểm tra phiên bản cuối.

### Đóng góp cụ thể

Phụ trách thiết kế và tích hợp các cổng trong lab10/guards.py: kiểm phiên bản chính sách, quyền ghi tiền và tác động lên bên thứ ba ở vòng 1; bổ sung kiểm tra tracking mâu thuẫn, quyền lợi bị từ chối hoặc chi thiếu khi xử lý S1 ở vòng 2. Tổng hợp giải pháp kỹ thuật, phân tích giới hạn của cổng và nguyên nhân ngoài kỹ thuật vào Phiếu B B7.1, Phiếu C C6–C7–C9. Điều phối ký tiêu chí, chốt checkpoint vòng 1, nhận thẻ S1 và tích hợp nội dung Phiếu B/C; kiểm tra phiên bản cuối để nhóm chốt v2. Sử dụng AI hỗ trợ đọc code, soạn cổng và rà tài liệu; đối chiếu giải pháp với trace và báo cáo kiểm thử.

### Bằng chứng

lab10/guards.py; bản vòng 1 lab10/guards_round1.py; Phiếu B B7.1/B8; Phiếu C C6/C7/C9. Commit ký tiêu chí 62560b8; commit chốt vòng 1 518c05d; commit nhận thẻ S1 a6ab359; checkpoint 8e3b74dc. Báo cáo R-S1-grade-20261119-095556-9f65fc là bằng chứng kiểm chứng phiên bản cổng cuối: PASS-VISIBLE và không phát sinh lỗi hồi quy trên bộ nền.

### Exit ticket

Một điều học được: Cổng phải kiểm tra trước hành động ghi và bao phủ cả nhánh từ chối; chỉ chặn khoản hoàn vượt mức chưa ngăn được từ chối sai quyền lợi. Một điều còn chưa chắc: Cổng hiện tại có giữ đúng giới hạn khi nhiều worker cùng ghi ledger và tracking cập nhật chậm hay không.

## NguyenHoangAn-2A202604025

### Phần việc phụ trách

Phụ trách `lab10/monitors.py`; Phiếu A câu 1.3; Phiếu B mục B0–B2, B7.2–B7.3; Phiếu C mục C0–C2 và C8. Chỉ chạy eval/grade sau khi tiêu chí đã ký và push. Đọc trace, cùng một người không viết code xây dựng hai ticket behavioral test; đo các mốc base/prepared/after, kiểm regression và thêm ít nhất một monitor mới không dùng nhãn. Cung cấp số liệu và mã lần chạy cho quyết định của nhóm.

### Đóng góp cụ thể

Thiết kế offline metric chọn phiên bản chính sách ở Phiếu A câu 1.3; tổng hợp nhật ký đo, đọc trace và phân tích lỗi ở Phiếu B B0–B2. Phụ trách phần kiểm thử hành vi và kiểm tra cổng ở B7.2–B7.3; đối chiếu kết quả base/prepared/after, kiểm hồi quy trên bộ nền và cung cấp số liệu cho quyết định của nhóm. Với S1, phân tích chênh lệch trước/sau, cập nhật C0–C2/C8 và bổ sung ba monitor không dùng nhãn trong lab10/monitors.py: tracking bất nhất, chênh lệch độ trễ khai báo với dữ liệu và chạm giới hạn lỗi hãng. Dùng AI hỗ trợ đọc trace, soạn monitor và rà số liệu; số liệu kết luận lấy từ báo cáo thực tế. Báo cáo cuối đạt PASS-VISIBLE, chưa có kết quả test ẩn.

### Bằng chứng

Phiếu A câu 1.3, commit 6d43c82; Phiếu B B0/B1/B2/B7.2/B7.3; Phiếu C C0/C1/C2/C8; lab10/monitors.py. Mốc nền vòng 1 R-base-before-20261119-160126-b45eeb và R-base-prepared-20261119-161425-5cdd59. Sau sửa: R-S1-after-20261119-095541-9f65fc, R-base-after-20261119-095550-9f65fc; grade cuối R-S1-grade-20261119-095556-9f65fc ghi nhận S1 đạt 65/65 và bộ nền đạt 110/110. Nội dung hai ticket kiểm thử hành vi tham chiếu B7.2–B7.3; không đánh đồng việc ghi thiết kế test với bằng chứng đã có một người độc lập thực thi.

### Exit ticket

Một điều học được: Phải đọc trace và tách kết quả theo từng mốc để biết cổng thực sự ngăn lỗi nào; monitor không dùng nhãn giúp phát hiện tín hiệu bất thường nhưng không tự chứng minh quyết định đúng. Một điều còn chưa chắc: Bộ thử nhỏ và các seed hiện có đã bao phủ đủ trường hợp thực tế chưa; cần đo tiếp độ trễ cảnh báo và kết quả chuyển người trong pilot.

## VuTrongThang-2A202604022

### Phần việc phụ trách

Chủ trì Phiếu A: câu 1.1, 1.5–1.6, tổng hợp phần của Ân và Chiêu, ghi bằng chứng ký ở A5. Phụ trách `config/acceptance_criteria.json` trước khi ký; Phiếu B mục B3, tổng hợp pre-mortem B6, B7.4 và B8; Phiếu C câu 3.2 trong C5 và C12. Đề xuất ngưỡng từ tài liệu Day 9 và số liệu vận hành của đề; lập phần `business` của `config/operating_gates.json` để Chiêu nhập thống nhất. Đọc chi phí, ROI và phân khúc xấu nhất, đề xuất quyết định v1/v2 để cả nhóm chốt.

### Đóng góp cụ thể

Chủ trì mục tiêu hệ thống, cách đọc khoảng tin cậy và tiêu chí thành công ở Phiếu A câu 1.1/1.5/1.6; tổng hợp đầu vào kỹ thuật, vận hành và pháp lý, ghi bằng chứng ký ở A5. Phụ trách ngưỡng trong config/acceptance_criteria.json trước khi ký và các giá trị business trong operating_gates.json. Phân tích bản đồ dữ liệu, drift, pre-mortem và góc nhìn kinh doanh ở B3/B6/B7.4/B8. Với S1, phân tích chi phí, ROI và phân khúc xấu nhất tại C5 câu 3.2 và C12: chi phí sau sửa 5.870đ/ticket, ROI 0,70; kho CT trong S1 tốn 7.053đ/ticket, còn nhóm kho không xác định ở bộ nền cần theo dõi riêng. Đối chiếu các ngưỡng đã ký để đề xuất v1 Cải tiến thêm và cùng nhóm chốt v2 Tiếp tục pilot có kiểm soát. Phần phân tích và tài liệu có sử dụng hỗ trợ AI, được đối chiếu với cấu hình và báo cáo.

### Bằng chứng

Commit c426c77 về mục tiêu, ngưỡng chất lượng và kinh doanh; commit ký 62560b8. Phiếu A A1/A3/A4/A5; config/acceptance_criteria.json và acceptance_criteria.lock; phần business trong config/operating_gates.json. Phiếu B B3/B6/B7.4/B8; Phiếu C C5 câu 3.2 và C12; submission/submission.json ghi hai quyết định. Báo cáo R-S1-grade-20261119-095556-9f65fc cung cấp chi phí, ROI và số liệu phân khúc dùng trong kết luận.

### Exit ticket

Một điều học được: Quyết định đi tiếp phải dựa đồng thời vào chất lượng, an toàn, chi phí và vận hành theo ngưỡng đã ký; không dùng ROI tốt để bù cho lỗi an toàn hoặc che phân khúc kém hiệu quả. Một điều còn chưa chắc: Chi phí toàn phần và ROI trong pilot thật có giữ được như mô phỏng khi tăng tải và tăng thời gian duyệt thủ công hay không.

## PhamVanChieu-2A202604033

### Phần việc phụ trách

Phụ trách Phiếu A câu 1.2 và 1.4; Phiếu B mục B4–B5, B7.5–B7.6; Phiếu C mục C3–C4, câu 3.3 trong C5, C10–C11. Là đầu mối nhập `config/operating_gates.json`: tự phụ trách `operations`/`legal`, nhận giá trị `business` từ Thắng. Viết HAZOP, checklist có PIC, runbook và phương án giờ cao điểm; cập nhật rủi ro sau sự cố. Điền `submission/submission.json`; phối hợp Ân chạy lệnh collect và kiểm đủ hồ sơ. Mục C3 chỉ làm phần ứng với thẻ được giao; thẻ S4 theo ngoại lệ của đề.

### Đóng góp cụ thể

Phụ trách mục tiêu vận hành/pháp lý và telemetry ở Phiếu A câu 1.2/1.4; chuẩn hóa cách đo tín hiệu không có nhãn. Xây dựng HAZOP, checklist có PIC, runbook và phương án giờ cao điểm tại B4/B5/B7.5/B7.6. Nhập cấu hình operations/legal và tích hợp giá trị business vào config/operating_gates.json, giữ rõ người nhận việc, công suất duyệt, SLA, ghi chú và kiểm mẫu. Với S1, cập nhật rủi ro và phân tích vận hành/pháp lý ở C3/C4, C5 câu 3.3, C10/C11; nêu giới hạn lịch sử lỗi hãng 7 ngày, đối soát và diễn tập tiếp quản. Hoàn thiện submission/submission.json, phối hợp thu thập bộ nộp và kiểm tra đủ hồ sơ. Phần tài liệu có sử dụng hỗ trợ AI, được đối chiếu với cấu hình và báo cáo thực tế.

### Bằng chứng

Commit 59d9f5a và 72fd158 về mục tiêu vận hành/pháp lý, telemetry và chuẩn hóa Phiếu A. Phiếu B B4/B5/B7.5/B7.6; config/operating_gates.json và bản vòng 1 config/operating_gates.round1.json. Phiếu C C3/C4/C5 câu 3.3/C10/C11; submission/submission.json, submission/manifest.json và bộ hồ sơ submission/docs. Báo cáo R-S1-grade-20261119-095556-9f65fc cung cấp số liệu hàng chờ, tỉ lệ chuyển người và vi phạm pháp lý; lệnh kiểm bài nộp xác nhận đủ thành phần, kèm cảnh báo thời gian đã ghi trong Phiếu C.

### Exit ticket

Một điều học được: Chuyển người chỉ có ý nghĩa khi xác định rõ người nhận, năng lực xử lý, SLA, căn cứ đối soát và điều kiện dừng; có log không đồng nghĩa ca đã được giải quyết. Một điều còn chưa chắc: Cần tổ chức nguồn dữ liệu và quy trình nào để theo dõi đủ lịch sử lỗi hãng 7 ngày, khiếu nại thực tế và diễn tập tiếp quản trước khi mở rộng pilot.
