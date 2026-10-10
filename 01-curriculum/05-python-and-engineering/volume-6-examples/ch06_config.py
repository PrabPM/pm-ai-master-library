"""Chapter 6: configuration that fails at startup, and secrets that stay secret."""
from collections.abc import Mapping
from dataclasses import dataclass


class Secret:
    """Wraps a secret so printing or logging it shows stars, not the value."""

    def __init__(self, value: str) -> None:
        self._value = value

    def reveal(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return "Secret('********')"


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Settings:
    environment: str
    database_url: Secret
    northbank_api_key: Secret
    northbank_timeout_seconds: float
    webhook_secret: Secret


def parse_timeout(raw: str, problems: list[str]) -> float:
    try:
        seconds = float(raw)
    except ValueError:
        if raw:
            problems.append(f"NORTHBANK_TIMEOUT_SECONDS is not a number: {raw!r}")
        return 0.0
    if not 0.1 <= seconds <= 30:
        problems.append("NORTHBANK_TIMEOUT_SECONDS must be between 0.1 and 30")
    return seconds


def load_settings(env: Mapping[str, str]) -> Settings:
    """Read every setting once, at startup, and report every problem at once."""
    problems: list[str] = []

    def need(name: str) -> str:
        value = env.get(name, "").strip()
        if not value:
            problems.append(f"{name} is missing")
        return value

    environment = need("PAYFLOW_ENV")
    if environment not in {"", "dev", "staging", "production"}:
        problems.append("PAYFLOW_ENV must be dev, staging or production")
    api_key = need("NORTHBANK_API_KEY")
    if environment == "production" and api_key.startswith("test_"):
        problems.append("NORTHBANK_API_KEY is a test key in production")
    timeout = parse_timeout(need("NORTHBANK_TIMEOUT_SECONDS"), problems)
    database_url = need("PAYFLOW_DATABASE_URL")
    webhook_secret = need("NORTHBANK_WEBHOOK_SECRET")
    if problems:
        raise ConfigError("refusing to start:\n  - " + "\n  - ".join(problems))
    return Settings(environment, Secret(database_url), Secret(api_key), timeout,
                    Secret(webhook_secret))


def timeout_the_quiet_way(env: Mapping[str, str]) -> float:
    """The bug this chapter prevents: a typo silently becomes a default."""
    return float(env.get("NORTHBANK_TIMEOUT", "30"))


if __name__ == "__main__":
    broken = {"PAYFLOW_ENV": "production", "NORTHBANK_API_KEY": "test_abc123",
              "NORTHBANK_TIMEOUT_SECONDS": "2s"}
    print("-- the quiet way")
    print("timeout used:", timeout_the_quiet_way(broken), "seconds")
    print("-- the fail-fast way")
    try:
        load_settings(broken)
    except ConfigError as exc:
        print(exc)
    fixed = {"PAYFLOW_ENV": "production", "NORTHBANK_API_KEY": "live_9f8e7d",
             "NORTHBANK_TIMEOUT_SECONDS": "2", "NORTHBANK_WEBHOOK_SECRET": "whsec_k3y",
             "PAYFLOW_DATABASE_URL": "postgresql://payflow:hunter2@db.internal/pay"}
    settings = load_settings(fixed)
    print("-- started; printing settings is safe")
    for name, value in vars(settings).items():
        print(f"  {name} = {value!r}")
