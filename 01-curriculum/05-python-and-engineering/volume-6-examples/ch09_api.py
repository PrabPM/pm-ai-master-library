"""Chapter 9: API contracts. Pagination that survives new data, and tenant checks."""
import base64
import json

# PayFlow's payments, newest first. IDs grow over time.
PAYMENTS = [{"id": f"pay_{n}", "merchant_id": "m_harbor"}
            for n in range(1008, 1000, -1)]
PAYMENTS.append({"id": "pay_0999", "merchant_id": "m_kumo"})
API_KEYS = {"key_harbor_live": "m_harbor", "key_kumo_live": "m_kumo"}


def page_by_offset(rows: list[dict], offset: int, limit: int) -> list[str]:
    return [row["id"] for row in rows[offset:offset + limit]]


def encode_cursor(last_id: str) -> str:
    return base64.urlsafe_b64encode(json.dumps({"after": last_id}).encode()).decode()


def page_by_cursor(rows: list[dict], cursor: str | None, limit: int):
    """Return (ids, next_cursor). The cursor says where the last page ended."""
    after = json.loads(base64.urlsafe_b64decode(cursor))["after"] if cursor else None
    matching = [r for r in rows if after is None or r["id"] < after]
    page = [row["id"] for row in matching[:limit]]
    more = len(matching) > limit
    return page, (encode_cursor(page[-1]) if more else None)


def get_payment(api_key: str, payment_id: str) -> tuple[int, dict]:
    merchant_id = API_KEYS.get(api_key)
    if merchant_id is None:
        return 401, {"error": {"code": "invalid_api_key"}}         # authentication
    for row in PAYMENTS:
        if row["id"] == payment_id and row["merchant_id"] == merchant_id:
            return 200, row
    return 404, {"error": {"code": "payment_not_found"}}           # authorization


if __name__ == "__main__":
    harbor = [p for p in PAYMENTS if p["merchant_id"] == "m_harbor"]

    print("-- offset pagination while a new payment arrives")
    print("page 1:", page_by_offset(harbor, 0, 3))
    harbor.insert(0, {"id": "pay_1009", "merchant_id": "m_harbor"})  # new sale
    print("page 2:", page_by_offset(harbor, 3, 3), "<- pay_1006 again")

    print("-- cursor pagination over the same data")
    harbor.pop(0)
    page, cursor = page_by_cursor(harbor, None, 3)
    print("page 1:", page, "| next cursor:", cursor)
    harbor.insert(0, {"id": "pay_1009", "merchant_id": "m_harbor"})
    page, cursor = page_by_cursor(harbor, cursor, 3)
    print("page 2:", page)

    print("-- authentication is not authorization")
    print("no key:        ", get_payment("key_made_up", "pay_1001"))
    print("own payment:   ", get_payment("key_harbor_live", "pay_1001")[0])
    print("other merchant:", get_payment("key_harbor_live", "pay_0999"))
