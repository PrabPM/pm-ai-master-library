"""Chapter 60: every number quoted in the question bank, checked."""
import numpy as np

# 1. cosine of (3, 4) and (6, 8) is 1 although they are 5 apart
u, v = np.array([3.0, 4.0]), np.array([6.0, 8.0])
assert np.isclose(u @ v / (np.linalg.norm(u) * np.linalg.norm(v)), 1.0)
assert np.isclose(np.linalg.norm(u - v), 5.0)

# 2. eigenvalues of [[2, 1], [1, 2]] are 3 and 1, with eigenvectors (1,1), (1,-1)
A = np.array([[2.0, 1.0], [1.0, 2.0]])
assert np.allclose(A @ np.array([1, 1]), 3 * np.array([1, 1]))
assert np.allclose(A @ np.array([1, -1]), 1 * np.array([1, -1]))

# 4. Bayes: 0.5% base rate, 90% recall, 2% false positives
assert np.isclose(0.9 * 0.005 / (0.9 * 0.005 + 0.02 * 0.995), 0.1844, atol=1e-4)

# 6. standard error of a mean: sd 80, n 1,600; quarter the error needs 16x the data
assert np.isclose(80 / np.sqrt(1600), 2.0)
assert np.isclose(80 / np.sqrt(4 * 1600), 1.0)

# 7. MLE of a rate: 18 of 20
assert np.isclose(18 / 20, 0.9)

# 8. twenty tests at the 5% level
assert np.isclose(1 - 0.95 ** 20, 0.64, atol=0.005)
assert np.isclose(0.05 / 20, 0.0025)

# 9. gradient of w1^2 + 3 w2 at (2, 5) is (4, 3)
f = lambda w: w[0] ** 2 + 3 * w[1]
w0, h = np.array([2.0, 5.0]), 1e-6
grad = [(f(w0 + h * e) - f(w0 - h * e)) / (2 * h) for e in np.eye(2)]
assert np.allclose(grad, [4.0, 3.0], atol=1e-5)

# 10. backprop: error -0.475 times input 2
p = 1 / (1 + np.exp(-0.1))
assert np.isclose((p - 1) * 2, -0.95, atol=1e-3)

# 11. mini-batches: updates per pass, and noise that falls with sqrt(batch)
assert 1_000_000 // 1_000 == 1_000
assert np.isclose(np.sqrt(1_000 / 4_000), 0.5)

# 12. Adam's averaging horizons: 1 / (1 - beta)
assert np.isclose(1 / (1 - 0.9), 10) and np.isclose(1 / (1 - 0.999), 1000)

# 13. entropy of a fair coin and of a 99/1 outcome, in bits
H = lambda p: float(-np.sum(np.array(p) * np.log2(p)))
assert np.isclose(H([0.5, 0.5]), 1.0) and np.isclose(H([0.99, 0.01]), 0.081, atol=5e-4)

# 14. cross-entropy of a confident right and a confident wrong prediction (nats)
assert np.isclose(-np.log(0.9), 0.105, atol=5e-4)
assert np.isclose(-np.log(0.1), 2.303, atol=5e-4)

# 15. KL divergence of the Lab 7 mixes, in bits
new, old = np.array([0.4, 0.3, 0.2, 0.1]), np.array([0.5, 0.3, 0.15, 0.05])
assert np.isclose(np.sum(new * np.log2(new / old)), 0.054, atol=5e-4)

# 16. perplexity: uniform over 50 tokens; 2 bits per token
assert np.isclose(np.exp(-np.log(1 / 50)), 50) and np.isclose(2 ** 2, 4)

# 17. critical path: two checks in parallel (2 h, 5 h), then a 1 h review
assert max(2, 5) + 1 == 6 and 2 + 5 + 1 == 8

# 19. stationarity: Lab-style growth check; 20. Sharpe arithmetic
assert np.isclose(0.5 / 2.881 * np.sqrt(12), 0.601, atol=1e-3)
assert np.isclose(1.0 * np.sqrt(2), 1.41, atol=0.005)
print("all question-bank numbers check out")
