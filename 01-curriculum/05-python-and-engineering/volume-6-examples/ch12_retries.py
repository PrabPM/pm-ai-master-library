"""Chapter 12: timeouts and retries. A retry storm, then backoff with jitter."""
import random
from collections import Counter
from collections.abc import Callable

from fake_provider import FakeProvider, ProviderTimeout, ProviderUnavailable


def delay_fixed(attempt: int, rng: random.Random) -> float:
    return 1.0


def delay_backoff(attempt: int, rng: random.Random, base: float = 1.0,
                  cap: float = 30.0) -> float:
    return min(cap, base * 2 ** attempt)


def delay_full_jitter(attempt: int, rng: random.Random, base: float = 1.0,
                      cap: float = 30.0) -> float:
    """Exponential backoff with full jitter: anywhere from 0 up to the capped step."""
    return rng.uniform(0, min(cap, base * 2 ** attempt))


def storm(policy: Callable, clients: int = 1000, retries: int = 4, seed: int = 12):
    """Every client fails at t=0 and retries. Count arrivals per 100 ms slot."""
    rng = random.Random(seed)
    slots: Counter[int] = Counter()
    for _ in range(clients):
        clock = 0.0
        for attempt in range(retries):
            clock += policy(attempt, rng)
            slots[int(clock * 10)] += 1
    return slots


def should_retry(error: Exception, idempotent: bool) -> bool:
    if isinstance(error, ProviderUnavailable):
        return True                 # the bank said it did nothing
    if isinstance(error, ProviderTimeout):
        return idempotent           # unknown outcome: only safe with a key
    return False                    # declines and validation errors never change


def call_with_retries(action: Callable, *, idempotent: bool, max_attempts: int = 4,
                      budget_seconds: float = 10.0, seed: int = 12):
    """Returns (result, log). Sleeps are simulated so the example runs instantly."""
    rng, waited, log = random.Random(seed), 0.0, []
    for attempt in range(max_attempts):
        try:
            result = action()
            log.append(f"attempt {attempt + 1}: ok")
            return result, log
        except Exception as error:
            name = type(error).__name__
            pause = delay_full_jitter(attempt, rng, base=0.5, cap=8.0)
            out_of_tries = attempt == max_attempts - 1
            out_of_time = waited + pause > budget_seconds
            if not should_retry(error, idempotent) or out_of_tries or out_of_time:
                log.append(f"attempt {attempt + 1}: {name} -> stop, do not retry")
                return None, log
            waited += pause
            log.append(f"attempt {attempt + 1}: {name} -> wait {pause:.2f}s")
    return None, log


if __name__ == "__main__":
    print("-- 1,000 clients fail together, then each retries 4 times")
    policies = {"fixed 1s": delay_fixed, "backoff": delay_backoff,
                "backoff + jitter": delay_full_jitter}
    print(f"{'policy':<18}{'busiest 100 ms':>16}{'100 ms slots used':>20}")
    for name, policy in policies.items():
        slots = storm(policy)
        print(f"{name:<18}{max(slots.values()):>16}{len(slots):>20}")
    waves = storm(delay_backoff)
    print("backoff waves at seconds:", [slot / 10 for slot in sorted(waves)])

    print("-- one client's schedule with full jitter (base 0.5s, cap 8s)")
    rng = random.Random(12)
    for attempt in range(6):
        ceiling = min(8.0, 0.5 * 2 ** attempt)
        pause = delay_full_jitter(attempt, rng, 0.5, 8.0)
        print(f"retry {attempt + 1}: wait {pause:5.2f}s"
              f"  (anywhere in 0 to {ceiling:.1f}s)")

    print("-- which failures get a retry")
    order = (12_000, "USD", "tok_visa_4242")
    print("with an idempotency key:")
    bank = FakeProvider(plan=["unavailable", "timeout_before_work"])
    result, log = call_with_retries(
        lambda: bank.authorize(*order, "m_harbor:order-7781"), idempotent=True)
    print("  " + "\n  ".join(log))
    print("  charges at the bank:", len(bank.charges))
    print("without a key:")
    bank = FakeProvider(plan=["timeout_after_work"])
    result, log = call_with_retries(lambda: bank.authorize(*order), idempotent=False)
    print("  " + "\n  ".join(log))
    print("  charges at the bank:", len(bank.charges), "<- outcome unknown to us")

    print("-- retries multiply through layers")
    for layers in (1, 2, 3):
        print(f"{layers} layer(s), 3 attempts each: "
              f"up to {3 ** layers} calls reach the bank")
