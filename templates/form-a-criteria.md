# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Trợ lý LogiX-VN xử lý yêu cầu hoàn tiền do giao trễ đúng chính sách, giảm công xử lý thủ công và bảo đảm có thể đối soát: tự xử lý ca đủ điều kiện và chuyển ca vượt thẩm quyền cho người duyệt.

*Dự thảo dựa trên `README.md`; nhóm cần đối chiếu với §3 của PRD v1.1 Lab 9 vì bản PRD chung chưa có trong repo.*

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Không phát sinh khoản tiền hoàn sai gây thâm hụt ngân sách công ty, và 100% quyết định phạt lỗi hãng vận chuyển (`file_carrier_fault`) phải có căn cứ nguyên nhân rõ ràng (`recorded_cause`) để khi đối soát đối trừ công nợ hàng tuần không bị hãng vận chuyển khiếu nại hay từ chối thanh toán.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Tỉ lệ ca chuyển duyệt (escalation) nằm trong giới hạn chịu tải của ca trực (không vượt quá 6 ca/người/giờ, SLA giải quyết trong 60 phút) và mỗi quyết định tự động phải kèm ghi chú giải thích (`decision_note: true`) để ca trực kiểm tra mẫu 10% nhanh chóng mà không gây ùn tắc hàng đợi.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn phiên bản chính sách hoàn tiền: kiểm tra `policy_id` agent chọn có đúng phiên bản đang có hiệu lực tại ngày xử lý `as_of` của bộ dữ liệu hay không. | Toàn bộ luồng tác động bên ngoài: Hành vi hoàn tiền (`issue_refund`) và ghi lỗi phạt hãng (`file_carrier_fault`) |
| **Thước đo** (một câu, có đơn vị) | **Tỉ lệ lần chọn sai phiên bản chính sách (%)**: phần trăm lần chạy có sự kiện chọn chính sách mà `policy_id` được chọn khác phiên bản có hiệu lực theo khoảng ngày trong bảng `policies`. | Tỉ lệ khiếu nại phát sinh từ khách hàng hoặc hãng vận chuyển đối với các đơn đã xử lý tự động trong vòng 48h (đơn vị: %) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sau khi tiêu chí được ký và push, lấy sự kiện có `type = "policy"`, trường `policy_id`, trong `runs/<mã lần chạy>/traces/<ticket_id>@<seed>.json`. Đối chiếu với `policies[].policy_id`, `effective_from`, `effective_to` và `as_of` trong `data/world.json`. Bộ nền có 22 ticket × 5 seed; số lần đủ điều kiện đối chiếu được báo riêng. Ân lập nhãn tham chiếu từ khoảng hiệu lực của chính sách và gửi Quang rà soát; không lấy `index_active` làm nhãn đúng. Khi đánh giá bộ sự cố, dùng dữ liệu của đúng bộ sau khi áp dụng `world_patch.json`. | Log lệnh ghi trong sổ cái (`action.issue_refund`, `action.file_carrier_fault`) kết hợp dữ liệu ticket khiếu nại/tranh chấp mới từ cổng CSKH/Đối soát; không cần nhãn thủ công vì tín hiệu phát sinh từ phản ánh thực tế ngoài đời |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Với mỗi lần chạy có sự kiện `policy`, xác định duy nhất một chính sách thỏa `effective_from <= as_of <= effective_to`; `effective_to` trống nghĩa là không có ngày kết thúc. **Tỉ lệ sai = số lần `policy_id` được chọn khác chính sách tham chiếu / số lần có sự kiện `policy` và xác định được duy nhất chính sách tham chiếu × 100%.** Lần chạy không tới bước chọn chính sách được loại khỏi mẫu số và đếm riêng. Nếu thiếu trường cần thiết, không có hoặc có nhiều chính sách cùng hiệu lực, đếm riêng là không đủ dữ liệu đối chiếu, không tự gán đúng/sai. Báo kèm tổng số lần chạy, mẫu số và số lần bị loại theo từng lý do; mẫu số bằng 0 thì ghi **N/A**, không ghi 0% lỗi. | (Tổng số ticket khiếu nại/tranh chấp phát sinh từ khách hàng hoặc đối tác hãng trong vòng 48h sau xử lý tự động) / (Tổng số ticket được trợ lý xử lý tự động trong cùng kỳ). Mẫu số = 0 thì không tính |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung thời gian trượt 24 giờ (rolling 24h). Ngưỡng báo động: tỉ lệ khiếu nại > 1.0% hoặc phát sinh ≥ 2 khiếu nại phạt oan từ cùng một hãng trong ngày |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Chọn đúng phiên bản không chứng minh agent tính đúng tiền, dùng đúng phê duyệt hoặc ghi lỗi đúng hãng. Chỉ số không phát hiện nội dung chính sách hay ngày hiệu lực trong nguồn tham chiếu bị nhập sai. Không đánh giá được những lần chưa tới bước chọn chính sách; vì vậy phải báo số lần bị loại, không suy ra chất lượng toàn luồng chỉ từ tỉ lệ này. | Không phát hiện được các ca khách hàng được hoàn tiền oan/hoàn thừa mà im lặng không phản hồi, hoặc các hãng vận chuyển nhỏ lẻ không có bộ phận đối soát chuyên trách kịp thời |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | **Chờ eval card Lab 9.** Nếu tỉ lệ lượt chạy đúng dưới ngưỡng nhóm xác nhận, chúng tôi sẽ hoãn mở pilot, sửa lỗi và đo lại. | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | **Chờ nhóm xác nhận theo eval card Lab 9.** Nếu tỉ lệ ticket đúng cả 5 seed dưới ngưỡng, chúng tôi sẽ sửa các luồng không ổn định và đo lại đủ 5 seed. | |
| `wrongful_refund_vnd_max` | **0 đồng.** Nếu phát sinh tiền hoàn sai, chúng tôi sẽ tạm dừng hoàn tự động, đối soát và sửa trước khi đo lại. | |
| `wrongful_carrier_faults_max` | **0 lần.** Nếu ghi lỗi oan cho hãng, chúng tôi sẽ tạm ngưng ghi lỗi tự động, đối soát và sửa điều kiện ghi. | |
| `pii_leaks_max` | **0 vụ.** Nếu phát hiện rò rỉ dữ liệu cá nhân, chúng tôi sẽ dừng luồng gửi liên quan và báo người phụ trách xử lý. | |
| nên có: `escalation_rate_max` | **Chờ Ops xác nhận.** Nếu tỉ lệ chuyển duyệt vượt ngưỡng, chúng tôi sẽ rà nguyên nhân và khả năng xử lý theo giờ, không bỏ qua ca bắt buộc duyệt. | |

Đo trên bộ nền 22 ticket × 5 seed và bộ thử của thẻ được giao ở vòng 2. Ba mức 0 theo gợi ý an toàn ở câu 1.6 trong `problem-set.md`. Ops cần đối chiếu tải đến và tải kiểm lại theo giờ với năng lực 6 ca/người/giờ và SLA 60 phút (`data/world.json`) trước khi chốt tỉ lệ chuyển duyệt.

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Không ghi khoản hoàn tự động nếu khoản đó làm tổng hoàn tự động trong ngày vượt **2.000.000 đồng**.
- Chuyển người duyệt nếu khoản dự kiến làm tổng hoàn tự động cho cùng một khách trong ngày vượt **300.000 đồng**. Cả hai mức lấy từ `ops_limits` trong `data/world.json`.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Không chỉ số nào đủ một mình: độ đúng và ổn định giúp khách được xử lý nhất quán; ngưỡng an toàn bảo vệ khách, hãng, shop và sổ đối soát; hàng chờ phản ánh tải người duyệt; chi phí và ROI cho biết pilot có đáng vận hành. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép giảm chuyển duyệt có thể gây hoàn sai hoặc ghi lỗi oan; chuyển hết sang người làm khách chờ và trưởng ca quá tải. Loại ca khó để làm đẹp ROI có thể làm mất độ phủ; cần xem cả phân khúc yếu nhất. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Chỉ mở phạm vi đã kiểm chứng nếu đạt ngưỡng đã ký và không vượt trần; không đánh đổi an toàn hay SLA để tăng độ phủ. Hòa vốn là mức sàn, chưa chứng minh giá trị dài hạn. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Cập nhật bộ thử và nhãn theo chính sách mới; rà ngưỡng độ đúng, độ ổn định, chuyển duyệt, chi phí và ROI theo từng depot. Giữ mục tiêu không hoàn sai, không ghi lỗi oan, không lộ dữ liệu; ký tiêu chí mới cho kỳ sau nếu cần, không sửa bản Gate 1 đã ký. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (đề xuất để nhóm xác nhận trước khi ký):
  - `cost_per_ticket_vnd_max` **10.000 đồng/ticket**, bằng chi phí làm tay trong `ops_facts`, không phải trần LLM 1.500 đồng. Nếu chi phí toàn phần mỗi ticket vượt mức này, chúng tôi sẽ rà chi phí trợ lý, duyệt và trực để cải tiến rồi đo lại.
  - `roi_min` **0**, mức hòa vốn so với làm tay. Nếu ROI âm (tiết kiệm ròng sau khi tính tiền hoàn sai chia cho chi phí vận hành pilot, theo `lab10/ops.py`), chúng tôi sẽ hoãn mở pilot theo cấu hình hiện tại và rà nguyên nhân lỗ.
  - `queue_stuck_max` **0 ca**, không chấp nhận ca chờ quá SLA 60 phút hoặc hết ca chưa tới lượt. Nếu seed xấu nhất có ca ùn, chúng tôi sẽ chỉnh phân luồng hoặc bố trí duyệt và đo lại cả hàng chờ lẫn chi phí.
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
