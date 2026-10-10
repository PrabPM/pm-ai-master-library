"""Chapter 91: a small-then-large cascade, and a scoped semantic cache.

Costs and accuracies are illustrative. Run: python ch91_router_cache.py
"""
import hashlib
import hmac
import re

import numpy as np

COST_SMALL, COST_LARGE = 0.001, 0.020          # USD per request


def cascade_cost(accept_rate):
    """All requests pay the small model; escalated ones also pay the large."""
    return COST_SMALL + (1 - accept_rate) * COST_LARGE


def cascade_quality(accept_rate, acc_small_accepted, acc_large_escalated):
    return accept_rate * acc_small_accepted + (1 - accept_rate) * acc_large_escalated


print(f"hand example: cost USD {cascade_cost(0.70):.4f}, "
      f"accuracy {cascade_quality(0.70, 0.94, 0.96):.3f}")

# Simulation: easy requests are more often right AND more often confident.
rng = np.random.default_rng(1)
n = 100_000
difficulty = rng.random(n)
small_right = rng.random(n) < 1.0 - 0.5 * difficulty ** 2
large_right = rng.random(n) < 0.98 - 0.06 * difficulty
confidence = np.clip(1.0 - difficulty + rng.normal(0, 0.1, n), 0, 1)
print("threshold   accepted  cost/request  accuracy")
for tau in (0.0, 0.4, 0.6, 0.8):
    accept = confidence >= tau                 # keep the small model's answer
    accuracy = np.where(accept, small_right, large_right).mean()
    print(f"   {tau:.1f}       {accept.mean():6.1%}     "
          f"{cascade_cost(accept.mean()):.4f}      {accuracy:.3f}")
print(f"large only      -        {COST_LARGE:.4f}      {large_right.mean():.3f}")


def embed(text, dim=64):
    """Hashed bag of words: each word adds 1 to a bucket chosen by a stable hash."""
    v = np.zeros(dim)
    for word in re.findall(r"[a-z]+", text.lower()):
        v[int(hashlib.sha256(word.encode()).hexdigest(), 16) % dim] += 1
    return v / max(np.linalg.norm(v), 1e-12)


class SemanticCache:
    def __init__(self, secret, threshold=0.8):
        self.secret, self.threshold, self.entries = secret, threshold, {}

    def scope(self, tenant, model_version):
        """Opaque partition key: the store never holds a tenant name."""
        message = f"{tenant}|{model_version}".encode()
        return hmac.new(self.secret, message, hashlib.sha256).hexdigest()[:16]

    def put(self, tenant, model_version, query, answer, sources):
        key = self.scope(tenant, model_version)
        self.entries.setdefault(key, []).append((embed(query), answer, dict(sources)))

    def get(self, tenant, model_version, query, current_versions):
        best, v = None, embed(query)
        for vector, answer, sources in self.entries.get(
                self.scope(tenant, model_version), []):
            fresh = all(current_versions.get(d) == ver for d, ver in sources.items())
            score = float(v @ vector)
            if fresh and score >= self.threshold and (best is None or score > best[0]):
                best = (score, answer)
        return best


cache = SemanticCache(secret=b"rotate-me")
docs = {"payouts.md": 3}
cache.put("public-faq", "m1", "When are payouts sent?", "Two business days.", docs)
q, reworded = "when are payouts sent", "when are the payouts sent"
tests = [("same scope, reworded", "public-faq", "m1", reworded, docs),
         ("another tenant", "merchant-17", "m1", q, docs),
         ("new model version", "public-faq", "m2", q, docs),
         ("source document updated", "public-faq", "m1", q, {"payouts.md": 4}),
         ("different question", "public-faq", "m1", "when are refunds sent", docs)]
for label, tenant, model, query, versions in tests:
    hit = cache.get(tenant, model, query, versions)
    print(f"{label:24s} -> {'hit, cos %.2f' % hit[0] if hit else 'miss'}")
near = float(embed("when are refunds sent") @ embed("When are payouts sent?"))
print(f"refunds question against the cached payouts question: cos {near:.2f}")

# Checks against the hand calculation in the chapter.
assert np.isclose(cascade_cost(0.70), 0.007)
assert np.isclose(cascade_quality(0.70, 0.94, 0.96), 0.946)
results = [cache.get(t, m, q, v) is not None for _, t, m, q, v in tests]
assert results == [True, False, False, False, False]
assert np.isclose(near, 3 / 4)
assert np.isclose(cache.get("public-faq", "m1", reworded, docs)[0], 4 / np.sqrt(20))
