"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _policy(ctx):
    day = H.d(ctx.as_of)
    current = [p for p in ctx.tools.lookup_policies() if H.d(p["effective_from"]) <= day
               and (not p.get("effective_to") or day <= H.d(p["effective_to"]))]
    return current[0] if len(current) == 1 else None


def pre_guard(ctx):
    """G1: pin the unique effective policy before reading untrusted text."""
    try:
        policy = _policy(ctx)
    except (KeyError, TypeError, ValueError):
        policy = None
    if policy is None:
        return Verdict.escalate("không xác định duy nhất chính sách hiệu lực")
    ctx.log("effective_policy", policy_id=policy["policy_id"])
    return Verdict.allow(policy_id=policy["policy_id"])


def _facts(ctx, action):
    if action.get("ticket_id") != ctx.ticket.get("ticket_id"):
        raise ValueError("thao tác không thuộc ticket đang xử lý")
    order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
    if not order or action.get("order_id", order["order_id"]) != order["order_id"]:
        raise ValueError("không xác minh được đơn hàng")
    if order["customer_id"] != ctx.ticket.get("customer_id"):
        raise ValueError("người gửi không có quyền với đơn")
    policy = _policy(ctx)
    if policy is None or not order.get("parcels"):
        raise ValueError("thiếu chính sách hoặc tracking")
    pid = ctx.ticket.get("parcel_id")
    if pid and not any(p["parcel_id"] == pid for p in order["parcels"]):
        raise ValueError("kiện được yêu cầu không thuộc đơn")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, parcel, policy, H.db_delay_days(parcel, ctx.as_of)


def _refund_gate(ctx, action, order, parcel, policy, delay):
    """G2: reconcile money, approval and duplicate writes against the ledger."""
    amount = action.get("amount_vnd")
    if type(amount) is not int or amount <= 0:
        return Verdict.deny("số tiền phải là số nguyên dương")
    if ctx.tools.ledger_rows(ticket_id=action["ticket_id"]):
        ctx.log("duplicate_refund_blocked")
        return Verdict.deny("ticket đã có khoản hoàn, không ghi lại")
    entitlement = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    refunded = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(order_id=order["order_id"]))
    remaining = max(0, entitlement - refunded)
    if remaining <= 0:
        ctx.log("refund_denied", db_delay_days=delay, entitlement_vnd=entitlement)
        return Verdict.deny("không còn quyền lợi hoàn tiền theo DB và sổ cái")
    amount = min(amount, remaining)
    approval_id = action.get("approval_id")
    if amount > policy["auto_limit_vnd"] or approval_id:
        approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
        valid = [a for a in ctx.tools.lookup_approvals(ticket_id=action["ticket_id"],
                    order_id=order["order_id"], customer_id=order["customer_id"])
                 if a.get("status") == "valid" and a.get("expires_at", "") >= ctx.as_of
                 and a.get("max_vnd", 0) >= amount
                 and (not approver or a.get("approver_id") == approver)]
        if not valid:
            return Verdict.escalate("thiếu phê duyệt đúng ticket, đơn, khách, hạn và hạn mức")
        approval_id = min(valid, key=lambda a: a["approval_id"])["approval_id"]
    limits = ctx.tools.ops_limits()
    if not approval_id:
        customer_total = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(customer_id=order["customer_id"])
                             if not r.get("approval_id"))
        customer_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
        if customer_cap is not None and customer_total + amount > customer_cap:
            return Verdict.escalate("tổng hoàn tự động cho khách vượt hạn mức, cần người duyệt")
        caps = [cap for cap in (limits.get("daily_auto_refund_budget_vnd"),
                (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")) if cap is not None]
        if caps and ctx.tools.auto_refund_today_vnd() + amount > min(caps):
            return Verdict.escalate("vượt trần hoàn tự động trong ngày")
    changes = {"amount_vnd": amount, "approval_id": approval_id, "payer": "LOGIX", "basis": "policy"}
    if any(action.get(key) != value for key, value in changes.items()):
        ctx.log("refund_reconciled", db_delay_days=delay, amount_vnd=amount)
        return Verdict.modify("đối chiếu quyền lợi và phê duyệt từ nguồn sự thật", **changes)
    return Verdict.allow()


def _third_party_gate(ctx, action, order, parcel, policy, delay):
    """G3: bind carrier actions to tracking and send only policy-approved fields."""
    if action["tool"] == "file_carrier_fault":
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny("tracking không đủ điều kiện ghi lỗi cho hãng")
        if ctx.tools.fault_rows(ticket_id=action["ticket_id"], parcel_id=parcel["parcel_id"]):
            return Verdict.deny("không ghi lỗi lặp cho cùng ticket và kiện")
        cap = ctx.tools.ops_limits().get("max_auto_strikes_per_carrier_per_day")
        if cap is not None and len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])) >= cap:
            ctx.log("carrier_strike_limit", carrier_id=parcel["carrier_id"])
            return Verdict.deny("đạt trần lỗi hãng tự động, giữ phần ghi lỗi cho người duyệt")
        changes = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                   "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(key) != value for key, value in changes.items()):
            return Verdict.modify("ghi lỗi đúng kiện, hãng và độ trễ theo tracking", **changes)
    else:
        faults = ctx.tools.fault_rows(ticket_id=action["ticket_id"], parcel_id=parcel["parcel_id"],
                                     carrier_id=parcel["carrier_id"])
        if not faults:
            return Verdict.deny("không gửi thông báo khi chưa có bản ghi lỗi hợp lệ")
        facts = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
                 "district": (order.get("recipient") or {}).get("district"), "delay_days": delay}
        blocked = set((ctx.gates or {}).get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        payload = {key: facts[key] for key in policy.get("carrier_notice_fields", [])
                   if key in facts and key not in blocked}
        if action.get("payload") != payload or action.get("carrier_id") != parcel["carrier_id"]:
            ctx.log("carrier_payload_filtered")
            return Verdict.modify("chỉ gửi dữ kiện có cấu trúc được chính sách cho phép", payload=payload,
                                  carrier_id=parcel["carrier_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool == "send_reply":
        if action.get("ticket_id") != ctx.ticket.get("ticket_id") or action.get("customer_id") != ctx.ticket.get("customer_id"):
            return Verdict.deny("câu trả lời không thuộc khách và ticket đang xử lý")
        paid = sum(r["amount_vnd"] for r in ctx.tools.ledger_rows(ticket_id=action["ticket_id"]))
        if action.get("amount_vnd", 0) != paid:
            text = (f"LogiX đã hoàn {paid:,}đ cho đơn {ctx.ticket.get('order_id')}.".replace(",", ".")
                    if paid else "LogiX chưa hoàn khoản nào cho yêu cầu này.")
            return Verdict.modify("trả lời theo tiền thực ghi trong sổ cái", text=text, amount_vnd=paid)
        return Verdict.allow()
    if tool not in {"issue_refund", "file_carrier_fault", "notify_carrier"}:
        return Verdict.deny("thao tác ghi chưa được cấp quyền")
    try:
        order, parcel, policy, delay = _facts(ctx, action)
        if tool == "issue_refund":
            return _refund_gate(ctx, action, order, parcel, policy, delay)
        return _third_party_gate(ctx, action, order, parcel, policy, delay)
    except (KeyError, TypeError, ValueError):
        return Verdict.escalate("dữ kiện thiếu hoặc không hợp lệ, cần người xác minh")
