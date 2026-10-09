"""Chapter 5: validate at the edge, and give every failure a family."""
import json
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from fake_provider import AuthResult, FakeProvider, ProviderTimeout


# --- The boundary model: what the outside world is allowed to send ---------
class CreatePaymentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)

    merchant_id: str = Field(pattern=r"^m_[a-z0-9]{3,20}$")
    amount_minor: int = Field(gt=0, le=5_000_000)
    currency: Literal["USD", "JPY", "KWD"]
    card_token: str = Field(pattern=r"^tok_[a-z0-9_]{3,40}$")


# --- The error families ----------------------------------------------------
class PayFlowError(Exception):
    http_status = 500
    code = "internal_error"
    retryable = False
    public_message = "Something went wrong on our side."


class InvalidRequest(PayFlowError):        # the caller sent something wrong
    http_status, code = 422, "invalid_request"
    public_message = "The request is not valid."


class PaymentDeclined(PayFlowError):       # the business said no, correctly
    http_status, code = 402, "card_declined"
    public_message = "The card was declined."


class ProviderDown(PayFlowError):          # a dependency failed, outcome unknown
    http_status, code, retryable = 503, "provider_unavailable", True
    public_message = "Please retry with the same idempotency key."


class CardProvider(Protocol):
    def authorize(self, amount_minor: int, currency: str, card_token: str,
                  idempotency_key: str | None = None) -> AuthResult: ...


def authorize(body: str, provider: CardProvider) -> dict:
    try:
        request = CreatePaymentRequest.model_validate_json(body)
    except ValidationError as exc:
        raise InvalidRequest(f"{exc.error_count()} validation errors") from exc
    try:
        result = provider.authorize(
            request.amount_minor, request.currency, request.card_token)
    except ProviderTimeout as exc:
        raise ProviderDown("authorize timed out") from exc
    if not result.approved:
        raise PaymentDeclined(result.reason)
    return {"status": "authorized", "provider_ref": result.provider_ref}


def handle(body: str, provider: CardProvider, correlation_id: str) -> tuple[int, dict]:
    """The outermost layer: turn any failure into one stable public shape."""
    try:
        return 200, authorize(body, provider)
    except PayFlowError as exc:
        error, cause = exc, exc.__cause__
    except Exception as exc:  # a bug: tell the caller nothing specific
        error, cause = PayFlowError("unexpected"), exc
    print(f"  log  {correlation_id} {error.code}: {error} "
          f"(cause: {type(cause).__name__ if cause else 'none'})")
    return error.http_status, {"error": {
        "code": error.code, "message": error.public_message,
        "retryable": error.retryable, "correlation_id": correlation_id}}


class BrokenProvider:
    def authorize(self, *args, **kwargs):
        return None  # a bug: the caller will crash on .approved


if __name__ == "__main__":
    good = {"merchant_id": "m_harbor", "amount_minor": 12_000,
            "currency": "USD", "card_token": "tok_visa_4242"}
    bad = {"merchant_id": "harbor", "amount_minor": "120.00",
           "currency": "usd", "card_token": "tok_visa_4242", "is_admin": True}

    print("-- what Pydantic says about the bad payload")
    try:
        CreatePaymentRequest.model_validate(bad)
    except ValidationError as exc:
        for err in exc.errors():
            print(f"  {err['loc'][0]:<13}{err['type']:<24}{err['msg']}")

    cases = [
        ("valid request", good, FakeProvider()),
        ("user error", bad, FakeProvider()),
        ("business rejection", good | {"card_token": "tok_insufficient_funds"},
         FakeProvider()),
        ("dependency failure", good, FakeProvider(plan=["timeout_after_work"])),
        ("internal defect", good, BrokenProvider()),
    ]
    for number, (label, payload, provider) in enumerate(cases, start=1):
        print(f"-- {label}")
        status, response = handle(json.dumps(payload), provider, f"req_{number:04d}")
        if status == 200:
            print("  http", status, response)
        else:
            err = response["error"]
            print("  http", status, err["code"], "| retryable:", err["retryable"])
    print("-- the full public error shape")
    print(json.dumps(response, indent=2))
