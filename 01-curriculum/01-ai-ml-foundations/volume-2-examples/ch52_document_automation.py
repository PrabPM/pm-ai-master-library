"""Chapter 52: straight-through processing for onboarding documents and invoices.
Synthetic documents; every number is illustrative.
"""
from difflib import SequenceMatcher

import numpy as np


def invoice_adds_up(lines, tax_rate, total, tolerance=0.01):
    """A deterministic check no model can talk its way past."""
    subtotal = sum(lines)
    return abs(subtotal * (1 + tax_rate) - total) <= tolerance


def name_match(a, b):
    """Similarity of two business names after dropping case and punctuation."""
    clean = lambda s: "".join(ch for ch in s.lower() if ch.isalnum() or ch == " ")
    return SequenceMatcher(None, clean(a), clean(b)).ratio()


print("8 fields at 98%:", round(0.98 ** 8, 3), "  at 99.5%:", round(0.995 ** 8, 3))
print("invoice 400.00 + 250.50 + 99.50 at 8% tax = 810.00:",
      invoice_adds_up([400.00, 250.50, 99.50], 0.08, 810.00),
      "  misread as 280.50:", invoice_adds_up([400.00, 280.50, 99.50], 0.08, 810.00))
print("name match:",
      round(name_match("Juniper Bakery LLC", "JUNIPER BAKERY, L.L.C."), 2),
      " vs", round(name_match("Juniper Bakery LLC", "Jupiter Bank Ltd"), 2))

rng = np.random.default_rng(52)
docs, fields = 5000, 8
poor_scan = rng.random(docs) < 0.10                # blurred or skewed uploads
conf = np.where(poor_scan[:, None], rng.beta(6, 2, (docs, fields)),
                1 - rng.beta(0.3, 60, (docs, fields)))   # confidence per field
correct = rng.random((docs, fields)) < conf       # confidence here is calibrated
doc_ok = correct.all(axis=1)                      # every field right
checks_pass = doc_ok | (rng.random(docs) < 0.30)  # checks catch 70% of bad documents
REVIEW, ERROR = 4.0, 60.0                         # USD per review, per bad approval
print("threshold  straight-through  bad approvals  cost per 1,000 docs")
costs = {}
for tau in (0.50, 0.80, 0.90, 0.95, 0.99):
    auto = (conf.min(axis=1) >= tau) & checks_pass
    bad = auto & ~doc_ok
    costs[tau] = ((~auto).sum() * REVIEW + bad.sum() * ERROR) / docs * 1000
    print(f"   {tau:.2f}        {auto.mean():6.1%}          {bad.sum():4d}"
          f"         USD {costs[tau]:6,.0f}")
print(f"review everything: USD {REVIEW * 1000:,.0f} per 1,000 docs")

# ---- checks against the hand-worked numbers ----
assert np.isclose(0.98 ** 8, 0.851, atol=5e-4)
assert np.isclose(0.995 ** 8, 0.961, atol=5e-4)
assert np.isclose((400.00 + 250.50 + 99.50) * 1.08, 810.00)
assert invoice_adds_up([400.00, 250.50, 99.50], 0.08, 810.00)
assert not invoice_adds_up([400.00, 280.50, 99.50], 0.08, 810.00)
assert min(costs, key=costs.get) not in (0.50, 0.99)     # an interior optimum
