"""Chapter 11: webhooks. Verify the sender, survive duplicates and bad ordering."""
import hashlib
import hmac
import json

SECRET = b"whsec_northbank_demo"   # shared with NorthBank; lives in a secret manager
TOLERANCE_SECONDS = 300
RANK = {"created": 0, "authorized": 1, "captured": 2, "settled": 3}


class RejectedWebhook(Exception):
    pass


def sign(secret: bytes, timestamp: int, raw_body: bytes) -> str:
    """What NorthBank does before sending: HMAC over 'timestamp.body'."""
    message = str(timestamp).encode() + b"." + raw_body
    digest = hmac.new(secret, message, hashlib.sha256).hexdigest()
    return f"t={timestamp},v1={digest}"


def verify(secret: bytes, header: str, raw_body: bytes, now: int) -> None:
    """What PayFlow does on receipt. Raises unless the message is genuine and fresh."""
    try:
        parts = dict(item.split("=", 1) for item in header.split(","))
        timestamp, received = int(parts["t"]), parts["v1"]
    except (KeyError, ValueError) as exc:
        raise RejectedWebhook("malformed signature header") from exc
    if abs(now - timestamp) > TOLERANCE_SECONDS:
        raise RejectedWebhook("timestamp outside tolerance (possible replay)")
    message = str(timestamp).encode() + b"." + raw_body
    expected = hmac.new(secret, message, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, received):
        raise RejectedWebhook("signature mismatch")


class WebhookReceiver:
    def __init__(self) -> None:
        self.receipts: dict[str, bytes] = {}   # event_id -> raw body, kept as evidence
        self.status: dict[str, str] = {}       # payment_id -> current status
        self.log: list[str] = []

    def receive(self, header: str, raw_body: bytes, now: int) -> int:
        """Returns the HTTP status PayFlow answers with."""
        try:
            verify(SECRET, header, raw_body, now)
        except RejectedWebhook as exc:
            self.log.append(f"400 rejected: {exc}")
            return 400
        event = json.loads(raw_body)           # parse only after verifying
        if event["id"] in self.receipts:
            self.log.append(f"200 {event['id']} duplicate, already processed")
            return 200
        self.receipts[event["id"]] = raw_body
        self.apply(event)
        return 200

    def apply(self, event: dict) -> None:
        payment_id, new = event["payment_id"], event["status"]
        current = self.status.get(payment_id, "created")
        if RANK[new] <= RANK[current]:
            self.log.append(f"200 {event['id']} stale ({new}), kept {current}")
            return
        self.status[payment_id] = new
        self.log.append(f"200 {event['id']} applied: {current} -> {new}")


def naive_handler(events: list[dict]) -> tuple[str, int]:
    """Trusts arrival order and never asks 'have I seen this before?'"""
    status, merchant_credits = "created", 0
    for event in events:
        status = event["status"]              # last write wins
        if status == "captured":
            merchant_credits += 1             # side effect repeated per delivery
    return status, merchant_credits


if __name__ == "__main__":
    now = 1_783_951_509                       # 2026-07-13 14:05:09 UTC
    authorized = {"id": "evt_301", "payment_id": "pay_1001", "status": "authorized"}
    captured = {"id": "evt_302", "payment_id": "pay_1001", "status": "captured"}
    raw_auth = json.dumps(authorized).encode()
    raw_capt = json.dumps(captured, separators=(",", ":")).encode()

    print("-- who really sent this?")
    header = sign(SECRET, now, raw_capt)
    checks = {
        "genuine": (header, raw_capt, now),
        "tampered body": (header, raw_capt.replace(b"captured", b"settled"), now),
        "wrong secret": (sign(b"guess", now, raw_capt), raw_capt, now),
        "replayed an hour later": (header, raw_capt, now + 3600),
        "re-serialized JSON": (header, json.dumps(json.loads(raw_capt)).encode(), now),
    }
    for label, (hdr, body, when) in checks.items():
        try:
            verify(SECRET, hdr, body, when)
            print(f"{label:<24} accepted")
        except RejectedWebhook as exc:
            print(f"{label:<24} rejected: {exc}")

    print("-- delivered twice and out of order: captured, captured, authorized")
    status, credits = naive_handler([captured, captured, authorized])
    print(f"naive handler ends at: {status}, merchant credited {credits} times")
    receiver = WebhookReceiver()
    for raw in (raw_capt, raw_capt, raw_auth):
        receiver.receive(sign(SECRET, now, raw), raw, now)
    receiver.receive(f"t={now},v1=forged", raw_capt, now)
    for line in receiver.log:
        print(line)
    print("careful handler ends at:", receiver.status["pay_1001"])
    print("receipts stored:", sorted(receiver.receipts))
