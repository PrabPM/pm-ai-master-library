"""NorthBank: a tiny in-memory stand-in for PayFlow's acquiring bank.

There is no network here. The list called `plan` scripts what goes wrong on
each call, so every failure in the book can be repeated exactly.
"""
from collections.abc import Callable
from dataclasses import dataclass, field


class ProviderTimeout(Exception):
    """We stopped waiting. The bank may or may not have done the work."""


class ProviderUnavailable(Exception):
    """The bank answered 503. It did not do the work."""


@dataclass(frozen=True)
class AuthResult:
    approved: bool
    provider_ref: str = ""
    reason: str = ""


@dataclass
class FakeProvider:
    plan: list[str] = field(default_factory=list)
    charges: list[dict] = field(default_factory=list)  # what the bank really did
    calls: int = 0
    on_call: Callable[[], None] | None = None  # runs while a call is "in flight"
    _seen: dict[str, AuthResult] = field(default_factory=dict)

    def authorize(self, amount_minor: int, currency: str, card_token: str,
                  idempotency_key: str | None = None) -> AuthResult:
        self.calls += 1
        if self.on_call is not None:
            hook, self.on_call = self.on_call, None
            hook()
        step = self.plan.pop(0) if self.plan else "ok"
        if step == "unavailable":
            raise ProviderUnavailable("503 from NorthBank")
        if step == "timeout_before_work":
            raise ProviderTimeout("no reply from NorthBank in 2s")
        if idempotency_key in self._seen:  # the bank has seen this key before
            result = self._seen[idempotency_key]
        elif card_token == "tok_insufficient_funds":
            result = AuthResult(False, reason="insufficient_funds")
        else:
            ref = f"nb_{len(self.charges) + 1:04d}"
            self.charges.append(
                {"ref": ref, "amount_minor": amount_minor, "currency": currency})
            result = AuthResult(True, provider_ref=ref)
        if idempotency_key is not None:
            self._seen[idempotency_key] = result
        if step == "timeout_after_work":
            raise ProviderTimeout("no reply from NorthBank in 2s")
        return result
