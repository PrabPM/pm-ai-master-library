"""Chapter 84. A seeded canary rollout that pauses itself when a guardrail metric
(the decline rate) degrades, plus the sample-size arithmetic behind canary size."""
import math

import numpy as np

PER_MINUTE = 600                               # payments per minute at PayFlow
STAGES = [(0.05, 60), (0.25, 60), (0.50, 60)]  # (share on the new model, minutes)
BASE_RATE = 0.020                              # decline rate of the current model


def rollout(new_rate, seed, stages=STAGES, z_stop=3.0, window=30, min_n=300):
    """Ramp a new model. Returns (outcome, minute, new rate, current rate, z, harm)."""
    rng = np.random.default_rng(seed)
    hist, minute, harm = [], 0, 0.0            # harm: expected extra declines so far
    for share, minutes in stages:
        for _ in range(minutes):
            minute += 1
            n_new = round(PER_MINUTE * share)
            n_old = PER_MINUTE - n_new
            hist.append((n_new, rng.binomial(n_new, new_rate),
                         n_old, rng.binomial(n_old, BASE_RATE)))
            harm += n_new * (new_rate - BASE_RATE)
            n1, d1, n0, d0 = np.sum(hist[-window:], axis=0)
            if n1 < min_n:
                continue                       # too few payments to judge yet
            p1, p0 = d1 / n1, d0 / n0
            z = (p1 - p0) / math.sqrt(p0 * (1 - p0) * (1 / n1 + 1 / n0))
            if z >= z_stop:                    # guardrail breached: stop the ramp
                action = "rolled back" if p1 >= 2 * p0 else "paused"
                return action, minute, p1, p0, z, harm
    return "completed", minute, p1, p0, z, harm


# ---- 1. How many canary payments does it take to see 2.0% become 3.2%? -----------
def sample_size(p0, p1, z_alpha=1.645, z_beta=0.8416):
    """One-sided test of a rate against a known baseline: 5% false alarms, 80% power."""
    top = z_alpha * math.sqrt(p0 * (1 - p0)) + z_beta * math.sqrt(p1 * (1 - p1))
    return math.ceil((top / (p1 - p0)) ** 2)


need = sample_size(0.020, 0.032)
print(f"payments needed {need}: {need / (PER_MINUTE * 0.05):.0f} min at a 5% canary, "
      f"{need / (PER_MINUTE * 0.01):.0f} min at 1%")
assert need == 995

# ---- 2. Three rollouts with the same seed ----------------------------------------
print("\ncandidate      outcome      minute  new model  current     z  extra declines")
for label, rate in [("healthy 2.0%", 0.020), ("degraded 3.2%", 0.032),
                    ("broken 6.0%", 0.060)]:
    outcome, minute, p1, p0, z, harm = rollout(rate, seed=84)
    print(f"{label:14s} {outcome:11s} {minute:7d}  {p1:9.2%}  {p0:7.2%}  {z:+4.1f}  "
          f"{harm:14.0f}")
assert rollout(0.020, seed=84)[0] == "completed"
assert rollout(0.032, seed=84)[0] == "paused"
assert rollout(0.060, seed=84)[0] == "rolled back"

# ---- 3. Tuning the trigger: 400 seeded rollouts per row --------------------------
def summarize(z_stop, stages=STAGES, runs=400):
    healthy = [rollout(0.020, s, stages, z_stop) for s in range(runs)]
    degraded = [rollout(0.032, s, stages, z_stop) for s in range(runs)]
    stopped = [r for r in degraded if r[0] != "completed"]
    return (np.mean([r[0] != "completed" for r in healthy]), len(stopped) / runs,
            np.median([r[1] for r in stopped]), np.mean([r[5] for r in degraded]))


print("\ntrigger             healthy stopped  degraded stopped  median minute  "
      "extra declines")
table = {}
for label, z_stop, stages in [("5% canary, z >= 3.0", 3.0, STAGES),
                              ("5% canary, z >= 3.5", 3.5, STAGES),
                              ("1% canary, z >= 3.0", 3.0, [(0.01, 60)] + STAGES[1:])]:
    table[label] = summarize(z_stop, stages)
    fa, caught, med, harm = table[label]
    print(f"{label:19s} {fa:15.1%}  {caught:16.1%}  {med:13.0f}  {harm:14.0f}")
no_trigger = sum(PER_MINUTE * s * m for s, m in STAGES) * (0.032 - BASE_RATE)
print(f"{'no trigger':19s} {'-':>15s}  {'-':>16s}  {'-':>13s}  {no_trigger:14.0f}")
assert np.isclose(no_trigger, 345.6)
assert table["5% canary, z >= 3.5"][0] < table["5% canary, z >= 3.0"][0]
assert table["5% canary, z >= 3.5"][3] > table["5% canary, z >= 3.0"][3]
