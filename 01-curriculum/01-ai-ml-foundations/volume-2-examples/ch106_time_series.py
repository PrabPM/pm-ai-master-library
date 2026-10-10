"""Chapter 106. Modern time-series models: the seasonal-naive baseline, quantile
(pinball) loss, MASE and interval coverage on a synthetic hourly volume series.

Run: python ch106_time_series.py
"""
import numpy as np

# [listing]
def pinball(y, forecast, q):
    diff = y - forecast
    return np.maximum(q * diff, (q - 1) * diff)


print("q    forecast  loss if actual=120  loss if actual=160")
for q, f in [(0.1, 90), (0.5, 110), (0.9, 150)]:
    print(f"{q}  {f:8d}  {pinball(120, f, q):18.1f}  {pinball(160, f, q):18.1f}")

rng = np.random.default_rng(0)                     # six weeks, hourly
t = np.arange(6 * 168)
level = 100 + 40 * np.sin(2 * np.pi * (t % 24 - 8) / 24) + 15 * (t % 168 < 120)
y = level * (1 + 0.08 * rng.normal(size=t.size))
train, test = y[:-168], y[-168:]

m = 168                                            # season length: one week
snaive = train[-m:]                                # same hour, previous week
naive = np.full(m, train[-1])                      # last observed value
scale = np.abs(train[m:] - train[:-m]).mean()      # seasonal naive, in-sample MAE
for name, f in [("last value", naive), ("seasonal naive", snaive)]:
    mae = np.abs(test - f).mean()
    print(f"{name:14s} MAE {mae:5.2f}  MASE {mae / scale:.2f}")

resid = train[m:] - train[:-m]                     # the baseline's past errors
lo, hi = snaive + np.quantile(resid, 0.1), snaive + np.quantile(resid, 0.9)
inside = np.mean((test >= lo) & (test <= hi))
print(f"80% interval covers {inside:.0%} of test hours")
# [/listing]

# Hand-worked pinball losses for an actual of 120
assert np.isclose(pinball(120, 90, 0.1), 3.0)
assert np.isclose(pinball(120, 110, 0.5), 5.0)
assert np.isclose(pinball(120, 150, 0.9), 3.0)
assert np.isclose(np.mean([3.0, 5.0, 3.0]), 11 / 3)
# ...and for an actual of 160, above every forecast
assert np.isclose(pinball(160, 90, 0.1), 7.0)
assert np.isclose(pinball(160, 110, 0.5), 25.0)
assert np.isclose(pinball(160, 150, 0.9), 9.0)
# The 0.9 quantile charges under-forecasts nine times as much as over-forecasts
assert np.isclose(pinball(10, 0, 0.9) / pinball(0, 10, 0.9), 9.0)
# The median's pinball loss is half the absolute error
assert np.isclose(pinball(120, 110, 0.5), 0.5 * abs(120 - 110))

mae_naive = np.abs(test - naive).mean()
mae_snaive = np.abs(test - snaive).mean()
assert mae_snaive < mae_naive / 2                  # the seasonal baseline is strong
assert 0.8 < mae_snaive / scale < 1.2              # MASE near 1 by construction
assert 0.7 <= inside <= 0.9

# Q106.1: forecast 200 at q = 0.95; actual 260 and actual 180
assert np.isclose(pinball(260, 200, 0.95), 57.0)
assert np.isclose(pinball(180, 200, 0.95), 1.0)
# Q106.2: model MAE 6.3 against a seasonal-naive scale of 9.0 -> MASE 0.70
assert np.isclose(6.3 / 9.0, 0.70)
