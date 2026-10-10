"""Chapter 113: team-draft interleaving on a toy ranking, and off-policy
evaluation with inverse propensity scoring (IPS).
"""
import numpy as np


def team_draft(rank_a, rank_b, coins, k=4):
    """Interleave two rankings. Each round a coin decides who picks first;
    each side adds its best result that is not shown yet."""
    shown, team = [], {}
    for a_first in coins:
        for side in ("AB" if a_first else "BA"):
            ranking = rank_a if side == "A" else rank_b
            pick = next((d for d in ranking if d not in team), None)
            if pick is not None and len(shown) < k:
                shown.append(pick)
                team[pick] = side
    return shown, team


def credit(team, clicked):
    a = sum(team[d] == "A" for d in clicked)
    return a, len(clicked) - a


def ips(logs):
    """logs: rows of (pi, mu, reward) for the action that was actually taken."""
    w = np.array([pi / mu for pi, mu, _ in logs])
    r = np.array([reward for _, _, reward in logs], dtype=float)
    return (w * r).mean(), (w * r).sum() / w.sum()        # IPS, self-normalized


if __name__ == "__main__":
    # --- Interleaving: two rankers of help articles for the support assistant.
    A = ["p1", "p2", "p3", "p4"]
    B = ["p3", "p1", "p5", "p2"]
    shown, team = team_draft(A, B, coins=[True, False])
    print("shown:", shown, "| teams:", [team[d] for d in shown])
    print("clicks on p3 and p5 -> credit (A, B):", credit(team, ["p3", "p5"]))

    rng = np.random.default_rng(3)
    look = [0.9, 0.6, 0.4, 0.25]                 # chance a position is examined
    wins = {"A": 0, "B": 0, "tie": 0}
    for _ in range(2000):
        shown, team = team_draft(A, B, coins=rng.random(2) < 0.5)
        clicked = [d for d, p in zip(shown, look)
                   if rng.random() < p * (0.6 if d in ("p3", "p5") else 0.05)]
        a, b = credit(team, clicked)
        wins["A" if a > b else "B" if b > a else "tie"] += 1
    share_b = wins["B"] / (wins["A"] + wins["B"])
    print(f"2,000 impressions: {wins}")
    print(f"B preferred in {share_b:.1%} of decided impressions")

    # --- IPS by hand: (candidate prob, logging prob, reward) of the logged action.
    logs = [(0.9, 0.5, 1), (0.1, 0.5, 0), (0.8, 0.8, 1), (0.2, 0.4, 1)]
    v_ips, v_snips = ips(logs)
    logged = np.mean([r for _, _, r in logs])
    print(f"logged policy {logged:.3f} | IPS {v_ips:.3f} | "
          f"self-normalized {v_snips:.3f}")

    # --- IPS on a simulated log where the truth is known.
    p_success = {"retry": 0.7, "wait": 0.5}
    mu, pi = {"retry": 0.5, "wait": 0.5}, {"retry": 0.9, "wait": 0.1}
    truth = sum(pi[a] * p_success[a] for a in pi)
    actions = rng.choice(["retry", "wait"], size=20_000, p=[mu["retry"], mu["wait"]])
    rewards = rng.random(20_000) < np.array([p_success[a] for a in actions])
    sim = [(pi[a], mu[a], r) for a, r in zip(actions, rewards)]
    est, _ = ips(sim)
    print(f"true value of candidate {truth:.3f} | IPS from 20,000 logs {est:.3f} | "
          f"logged policy earned {rewards.mean():.3f}")

    assert team_draft(A, B, [True, False])[0] == ["p1", "p3", "p5", "p2"]
    assert credit(team_draft(A, B, [True, False])[1], ["p3", "p5"]) == (0, 2)
    assert np.isclose(v_ips, 3.3 / 4) and np.isclose(v_snips, 3.3 / 3.5)
    assert np.isclose(logged, 0.75) and np.isclose(truth, 0.68)
    assert abs(est - truth) < 0.02 and share_b > 0.5
