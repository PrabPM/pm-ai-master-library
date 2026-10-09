"""Chapter 7: a log line that leaks a card number, and one that cannot."""
import json
import logging
import re
import sys
import textwrap
from datetime import UTC, datetime

PAN_LIKE = re.compile(r"\b(?:\d[ -]?){12,18}\d\b")
SECRET_KEYS = {"card_number", "cvv", "authorization", "api_key", "password"}
FIXED_NOW = datetime(2026, 7, 13, 14, 5, 9, tzinfo=UTC)  # so output is repeatable


def luhn_ok(digits: str) -> bool:
    """The checksum every real card number passes."""
    total = 0
    for index, char in enumerate(reversed(digits)):
        n = int(char)
        if index % 2 == 1:
            n = n * 2 - 9 if n > 4 else n * 2
        total += n
    return total % 10 == 0


def mask_pans(text: str) -> str:
    def replace(match: re.Match) -> str:
        digits = re.sub(r"\D", "", match.group())
        return f"[PAN ****{digits[-4:]}]" if luhn_ok(digits) else match.group()
    return PAN_LIKE.sub(replace, text)


def redact(value):
    """Walk any JSON-like value; drop secret keys, mask card-like numbers."""
    if isinstance(value, dict):
        return {k: "[REDACTED]" if k.lower() in SECRET_KEYS else redact(v)
                for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    return mask_pans(value) if isinstance(value, str) else value


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        event = {"ts": FIXED_NOW.isoformat(), "level": record.levelname,
                 "service": "payments-api", "env": "production",
                 "event": record.getMessage()}
        event.update(redact(getattr(record, "fields", {})))
        return json.dumps(event)


class PageWidthHandler(logging.StreamHandler):
    """Production writes one event per line. The book wraps lines to fit a page."""

    def emit(self, record: logging.LogRecord) -> None:
        line = self.format(record)
        self.stream.write(textwrap.fill(line, 84, subsequent_indent="    ") + "\n")


def make_logger(name: str, formatter: logging.Formatter) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.handlers.clear()
    handler = PageWidthHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


if __name__ == "__main__":
    request = {"merchant_id": "m_harbor", "amount_minor": 12_000, "currency": "USD",
               "card_number": "4111 1111 1111 1111", "cvv": "123"}

    print("-- the leak")
    plain = make_logger("plain", logging.Formatter("%(levelname)s %(message)s"))
    plain.info(f"authorizing payment {request}")

    print("-- the structured, redacted version")
    log = make_logger("structured", JsonFormatter())
    log.info("payment.authorize.succeeded", extra={"fields": {
        "trace_id": "4bf92f3577b34da6", "payment_id": "pay_1001",
        "merchant_id": "m_harbor", "amount_minor": 12_000, "currency": "USD",
        "outcome": "approved", "latency_ms": 212}})

    print("-- defense in depth: a careless caller still cannot leak")
    log.warning("payment.authorize.debug", extra={"fields": {
        "request": request, "note": "card 4111111111111111 retried",
        "order_ref": "1234567890123456"}})
