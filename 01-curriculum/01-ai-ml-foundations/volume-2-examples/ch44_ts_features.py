"""Chapter 44. Rolling statistics, Bollinger Bands, RSI and MACD from scratch.

Every function uses only values up to and including day t (a trailing window).
The long series is synthetic: a seeded random walk, not a real price.
"""
import numpy as np


def sma(x, n):
    """Simple moving average of the last n values; NaN until n values exist."""
    out = np.full(len(x), np.nan)
    for t in range(n - 1, len(x)):
        out[t] = x[t - n + 1:t + 1].mean()
    return out


def rolling_std(x, n):
    """Standard deviation of the last n values (population form, divide by n)."""
    out = np.full(len(x), np.nan)
    for t in range(n - 1, len(x)):
        out[t] = x[t - n + 1:t + 1].std()
    return out


def ema(x, n):
    """Exponential moving average with alpha = 2 / (n + 1), started at x[0]."""
    alpha, out = 2 / (n + 1), np.empty(len(x))
    out[0] = x[0]
    for t in range(1, len(x)):
        out[t] = alpha * x[t] + (1 - alpha) * out[t - 1]
    return out


def rsi(x, n):
    """Wilder's relative strength index: 100 - 100 / (1 + avg gain / avg loss)."""
    change = np.diff(x)
    gain, loss = np.maximum(change, 0), np.maximum(-change, 0)
    out = np.full(len(x), np.nan)
    avg_gain, avg_loss = gain[:n].mean(), loss[:n].mean()   # first value: plain mean
    out[n] = 100 - 100 / (1 + avg_gain / avg_loss)
    for t in range(n + 1, len(x)):                          # then Wilder smoothing
        avg_gain = (avg_gain * (n - 1) + gain[t - 1]) / n
        avg_loss = (avg_loss * (n - 1) + loss[t - 1]) / n
        out[t] = 100 - 100 / (1 + avg_gain / avg_loss)
    return out


def macd(x, fast=12, slow=26, signal=9):
    line = ema(x, fast) - ema(x, slow)
    signal_line = ema(line, signal)
    return line, signal_line, line - signal_line


def synthetic_prices(days=250, seed=44):
    rng = np.random.default_rng(seed)
    return 100 * np.exp(np.cumsum(rng.normal(0.0003, 0.012, days)))


if __name__ == "__main__":
    # Hand example: seven closes.
    p = np.array([100.0, 102, 101, 104, 103, 106, 104])
    mid, sd = sma(p[:6], 5)[-1], rolling_std(p[:6], 5)[-1]
    print(f"day 6: SMA(5) = {mid:.2f}, std = {sd:.4f}, "
          f"bands = [{mid - 2 * sd:.2f}, {mid + 2 * sd:.2f}]")
    print("RSI(5) on days 6 and 7:", np.round(rsi(p, 5)[5:], 1))
    print("EMA(3):", ema(p, 3))

    # The same functions with the usual settings on 250 synthetic days.
    price = synthetic_prices()
    mid20, sd20 = sma(price, 20), rolling_std(price, 20)
    line, signal_line, hist = macd(price)
    print(f"last day: close {price[-1]:.2f}, SMA(20) {mid20[-1]:.2f}, bands "
          f"[{mid20[-1] - 2 * sd20[-1]:.2f}, {mid20[-1] + 2 * sd20[-1]:.2f}]")
    print(f"          RSI(14) {rsi(price, 14)[-1]:.1f}, MACD {line[-1]:.3f}, "
          f"signal {signal_line[-1]:.3f}, histogram {hist[-1]:.3f}")
    outside = np.mean(np.abs(price[19:] - mid20[19:]) > 2 * sd20[19:])
    print(f"share of days outside the bands: {outside:.3f}")

    # Checks against the hand calculation in the chapter.
    assert np.isclose(mid, 103.2) and np.isclose(sd, np.sqrt(2.96))
    assert np.allclose(rsi(p, 5)[5:], [80.0, 64.0])
    assert np.allclose(ema(p, 3), [100, 101, 101, 102.5, 102.75, 104.375, 104.1875])
    assert np.isclose((1.6 * 4 + 0) / 5, 1.28) and np.isclose((0.4 * 4 + 2) / 5, 0.72)
    # Causality: changing a future value never changes today's features.
    changed = price.copy()
    changed[200:] *= 1.5
    for f in (lambda x: sma(x, 20), lambda x: rsi(x, 14), lambda x: macd(x)[2]):
        assert np.allclose(f(price)[:200], f(changed)[:200], equal_nan=True)
    # Answers to Check yourself.
    q = np.array([10.0, 12, 11, 13, 14])
    assert np.isclose(sma(q, 5)[-1], 12.0) and np.isclose(rsi(q, 4)[-1], 100 - 100 / 6)
    assert np.isclose(2 / (9 + 1), 0.2)
