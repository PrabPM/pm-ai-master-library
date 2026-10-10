"""Chapter 46. Mean-variance optimization and the maximum-Sharpe portfolio.

Three synthetic funds A, B and C for PayFlow's own spare cash. Returns and risks
are yearly and invented for the example. The bank deposit pays 2%.
"""
import numpy as np
from scipy.optimize import minimize

NAMES = ["A", "B", "C"]
RF = 0.02


def covariance(sigma, corr_ab):
    """Covariance matrix when only A and B are correlated."""
    corr = np.eye(3)
    corr[0, 1] = corr[1, 0] = corr_ab
    return np.outer(sigma, sigma) * corr


def stats(w, mu, cov):
    ret, risk = w @ mu, np.sqrt(w @ cov @ w)
    return ret, risk, (ret - RF) / risk


def tangency(mu, cov):
    """Closed form: weights proportional to inverse covariance times excess return."""
    z = np.linalg.solve(cov, mu - RF)
    return z / z.sum()


def long_only(mu, cov):
    """Maximize the Sharpe ratio numerically with weights between 0 and 1."""
    result = minimize(lambda w: -stats(w, mu, cov)[2], x0=np.full(3, 1 / 3),
                      bounds=[(0, 1)] * 3, method="SLSQP", tol=1e-12,
                      constraints={"type": "eq", "fun": lambda w: w.sum() - 1})
    return result.x


def show(label, w, mu, cov):
    ret, risk, sharpe = stats(w, mu, cov)
    weights = "  ".join(f"{n} {x:6.3f}" for n, x in zip(NAMES, w))
    print(f"{label:<12}{weights}   return {ret:.2%}  risk {risk:.2%}"
          f"  Sharpe {sharpe:.3f}")


mu = np.array([0.08, 0.05, 0.03])
sigma = np.array([0.20, 0.10, 0.05])
cov = covariance(sigma, corr_ab=0.25)

if __name__ == "__main__":
    w = tangency(mu, cov)
    show("closed form", w, mu, cov)
    show("long-only", long_only(mu, cov), mu, cov)

    # Make A and B near-substitutes, then nudge one estimate by one point.
    cov2 = covariance(sigma, corr_ab=0.9)
    mu2 = np.array([0.09, 0.05, 0.03])
    print("with an A-B correlation of 0.9")
    show("A earns 8%", tangency(mu, cov2), mu, cov2)
    w2, w2_long = tangency(mu2, cov2), long_only(mu2, cov2)
    show("A earns 9%", w2, mu2, cov2)
    show("long-only", w2_long, mu2, cov2)

    # Checks against the hand calculation in the chapter.
    z = np.linalg.solve(cov, mu - RF)
    assert np.allclose(z, [1.2, 2.4, 4.0]) and np.isclose(z.sum(), 7.6)
    assert np.allclose(w, [1.2 / 7.6, 2.4 / 7.6, 4.0 / 7.6])
    assert np.isclose(np.linalg.det(cov[:2, :2]), 0.000375)
    assert np.isclose(stats(w, mu, cov)[2], np.sqrt(0.184))      # 0.429
    assert np.allclose(long_only(mu, cov), w, atol=1e-3)
    assert np.allclose((mu - RF) / sigma, [0.3, 0.3, 0.2])    # Sharpe of each alone
    assert w2[1] < 0 and abs(w2_long[1]) < 1e-6
    # No random long-only portfolio beats the tangency portfolio's Sharpe ratio.
    rng = np.random.default_rng(46)
    for cand in rng.dirichlet(np.ones(3), size=2000):
        assert stats(cand, mu, cov)[2] <= stats(w, mu, cov)[2] + 1e-12
    # Check yourself: two uncorrelated funds, excess 4% and 2%, risk 20% and 10%.
    z2 = np.array([0.04 / 0.04, 0.02 / 0.01])
    assert np.allclose(z2 / z2.sum(), [1 / 3, 2 / 3])
    assert np.isclose(w @ sigma, 0.0895, atol=1e-4)     # Q46.2: average risk 8.95%
