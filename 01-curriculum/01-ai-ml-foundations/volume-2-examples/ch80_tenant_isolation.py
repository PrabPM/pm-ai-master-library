"""Chapter 80. Tenant isolation in a shared vector store, tenant-scoped join keys,
and the noise a differentially private release needs."""
import hashlib
import hmac

import numpy as np

# ---- 1. A shared vector store with two tenants -----------------------------------
STORE = [                      # (tenant, chunk id, unit vector)
    ("merchant_a", "a1 payout schedule", (0.80, 0.60, 0.00)),
    ("merchant_a", "a2 refund policy", (0.60, 0.80, 0.00)),
    ("merchant_a", "a3 tax forms", (0.00, 0.00, 1.00)),
    ("merchant_b", "b1 payout dispute", (1.00, 0.00, 0.00)),
    ("merchant_b", "b2 payout hold", (0.96, 0.28, 0.00)),
]


def search(query, k, tenant=None, post_filter=None):
    """Top-k chunks by cosine similarity. `tenant` filters BEFORE ranking."""
    rows = [r for r in STORE if tenant is None or r[0] == tenant]
    ranked = sorted(rows, key=lambda r: -float(np.dot(query, r[2])))[:k]
    if post_filter is not None:               # filtering AFTER ranking
        ranked = [r for r in ranked if r[0] == post_filter]
    return [(r[1][:2], round(float(np.dot(query, r[2])), 2)) for r in ranked]


q = np.array([1.0, 0.0, 0.0])                 # merchant A asks about payouts
no_filter = search(q, k=2)
after = search(q, k=2, post_filter="merchant_a")
before = search(q, k=2, tenant="merchant_a")
print("no filter       ", no_filter)
print("filter after    ", after)
print("filter before   ", before)
assert no_filter == [("b1", 1.0), ("b2", 0.96)]          # a cross-tenant leak
assert after == []                                        # safe, and useless
assert before == [("a1", 0.8), ("a2", 0.6)]

# ---- 2. Tenant-scoped join keys --------------------------------------------------
def token(tenant_key, identifier):
    return hmac.new(tenant_key, identifier.encode(), hashlib.sha256).hexdigest()[:10]


email = "dana@example.com"
t_a = token(b"key-for-merchant-a", email)
t_b = token(b"key-for-merchant-b", email)
print(f"\nsame customer, tenant A {t_a}, tenant B {t_b}")
assert t_a != t_b and t_a == token(b"key-for-merchant-a", email)

# ---- 3. How much noise a private release needs -----------------------------------
def laplace_scale(sensitivity, epsilon):
    return sensitivity / epsilon


epsilon, cap = 0.5, 0.05                      # dispute rates are clipped to [0, 5%]
rng = np.random.default_rng(80)
print("\nmerchants  sensitivity  noise scale  noise sd   published (true 0.0120)")
for n in (400, 8):
    b = laplace_scale(cap / n, epsilon)       # one merchant moves a mean by cap / n
    published = 0.0120 + rng.laplace(0.0, b)
    print(f"{n:9d}  {cap / n:11.6f}  {b:11.5f}  {b * np.sqrt(2):8.5f}   "
          f"{published:.4f}")
assert np.isclose(laplace_scale(cap / 400, epsilon), 0.00025)
assert np.isclose(laplace_scale(cap / 8, epsilon), 0.0125)
draws = rng.laplace(0.0, 0.00025, 200_000)
assert np.isclose(draws.std(), 0.00025 * np.sqrt(2), rtol=0.02)
