"""Chapter 51: stationarity, differencing and the autocorrelation function."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import adfuller

ASSETS = Path(__file__).resolve().parent.parent / "volume-1-assets"
ASSETS.mkdir(exist_ok=True)
plt.rcParams.update({
    "svg.fonttype": "none", "font.family": "Helvetica", "font.size": 11,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#1f2937",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280", "grid.color": "#e5e7eb"})

# ---- three synthetic PayFlow series, 140 days each ----
rng = np.random.default_rng(51)
n = 140
t = np.arange(n)
noise = np.zeros(n)
for i in range(1, n):                         # mild day-to-day memory
    noise[i] = 0.4 * noise[i - 1] + rng.normal(0, 1)
weekday = np.array([-6, -8, -4, 0, 6, 14, -2], dtype=float)  # Mon..Sun
series = {
    "stationary": 94 + 0.5 * noise,                  # approval rate, percent
    "trending": 100 + 0.6 * t + 3 * noise,           # payments, thousands
    "seasonal": 100 + weekday[t % 7] + 3 * noise,    # payments, thousands
}
series["trending, differenced"] = np.diff(series["trending"])
series["seasonal, lag-7 diff"] = series["seasonal"][7:] - series["seasonal"][:-7]


def acf(x, h):
    """Sample autocorrelation at lag h."""
    d = np.asarray(x, dtype=float) - np.mean(x)
    return float(np.sum(d[:-h] * d[h:]) / np.sum(d * d))


# The hand example: nine days of payments, in thousands.
x = np.array([40, 42, 43, 46, 48, 51, 52, 54, 56], dtype=float)
dx = np.diff(x)
print("level:  first-4 mean", x[:4].mean(), " last-4 mean", x[-4:].mean())
print("change: first-4 mean", dx[:4].mean(), "  last-4 mean", dx[4:].mean())
print(f"lag-1 autocorrelation: level {acf(x, 1):.3f}, change {acf(dx, 1):.3f}")

# The same diagnosis on the simulated series, before and after differencing.
print(f"\n{'series':22s} half 1  half 2  acf(1)  acf(7)  ADF p")
for name, s in series.items():
    half = len(s) // 2
    p = adfuller(s, regression="c", autolag="AIC", result_object=True).pvalue
    print(f"{name:22s}{s[:half].mean():7.2f} {s[half:].mean():7.2f} "
          f"{acf(s, 1):7.2f} {acf(s, 7):7.2f}  {p:.3f}")

# ---- checks: hand results against computed ones ----
assert np.isclose(x[:4].mean(), 42.75) and np.isclose(x[-4:].mean(), 53.25)
assert np.isclose(dx[:4].mean(), 2.0) and np.isclose(dx[4:].mean(), 2.0)
assert np.isclose(acf(x, 1), 172 / 254)
assert np.isclose(acf(dx, 1), -0.5)          # hand result: -2 / 4


def gap(s):
    """Second-half mean minus first-half mean."""
    return s[len(s) // 2:].mean() - s[:len(s) // 2].mean()


def adf_p(s):
    return adfuller(s, regression="c", autolag="AIC", result_object=True).pvalue


# The trend shows as a mean that moves; differencing removes it.
assert gap(series["trending"]) > 30
assert abs(gap(series["trending, differenced"])) < 1
# The weekly pattern shows as a spike in the autocorrelation at lag 7.
assert acf(series["seasonal"], 7) > 0.7
assert adf_p(series["trending"]) > 0.05 > adf_p(series["stationary"])
assert adf_p(series["trending, differenced"]) < 0.05


# ---- Figure 51.1 ----
def half_means(ax, s):
    """Dashed segments at the mean of each half of the plotted series."""
    h = len(s) // 2
    ax.plot([0, h], [s[:h].mean()] * 2, color="#1f2937", lw=1.2, ls="--")
    ax.plot([h, len(s)], [s[h:].mean()] * 2, color="#1f2937", lw=1.2, ls="--")


fig, axes = plt.subplots(2, 3, figsize=(7.2, 3.6), dpi=100)
top = [("stationary", "Stationary", "#15803d"),
       ("trending", "Trending", "#b91c1c"),
       ("seasonal", "Weekly season", "#b45309")]
bottom = [None, "trending, differenced", "seasonal, lag-7 diff"]
labels = [None, "Day-to-day change", "Change vs 7 days ago"]
for j, (key, title, color) in enumerate(top):
    ax = axes[0, j]
    ax.plot(series[key][:84], color=color, lw=1.2)
    half_means(ax, series[key][:84])
    ax.set_title(title, fontsize=11, color="#1f2937")
    ax.grid(True, axis="y")
    if bottom[j] is None:
        ax.set_xlabel("day")
    else:
        ax.tick_params(labelbottom=False)
    ax = axes[1, j]
    if bottom[j] is None:
        ax.axis("off")
        note = "Dashed lines: the mean\nof each half. Nothing\nto fix in this one."
        ax.text(0.5, 0.4, note, ha="center", va="center", color="#6b7280",
                fontsize=11, transform=ax.transAxes)
    else:
        ax.plot(series[bottom[j]][:77], color="#4f46e5", lw=1.2)
        half_means(ax, series[bottom[j]][:77])
        ax.set_title(labels[j], fontsize=11, color="#1f2937")
        ax.grid(True, axis="y")
        ax.set_xlabel("day")
fig.tight_layout()
fig.savefig(ASSETS / "ch51-three-series.svg", bbox_inches="tight")
