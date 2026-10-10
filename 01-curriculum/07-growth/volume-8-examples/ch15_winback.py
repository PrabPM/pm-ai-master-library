"""Chapter 15: what a win-back campaign really added, measured with a holdout."""
from math import sqrt

from scipy.stats import norm

sent, sent_back = 18_000, 468  # got the email and the $50 fee credit offer
held, held_back = 2_000, 34    # randomly held out, got nothing
CREDIT = 50

p_sent, p_held = sent_back / sent, held_back / held
lift = p_sent - p_held
se = sqrt(p_sent * (1 - p_sent) / sent + p_held * (1 - p_held) / held)
low, high = lift - 1.96 * se, lift + 1.96 * se
p_value = 2 * norm.sf(abs(lift / se))
incremental = lift * sent

print(f"Came back within 30 days: sent {p_sent:.2%}, holdout {p_held:.2%}")
print(f"Lift: {lift * 100:.2f} points (95% CI {low * 100:.2f} to {high * 100:.2f}), "
      f"p = {p_value:.4f}")
print(f"Reactivations the dashboard credits to the email: {sent_back}")
print(f"Reactivations the email caused: about {incremental:.0f}")
print(f"Credit cost per credited reactivation: ${CREDIT}")
print(f"Credit cost per caused reactivation: ${CREDIT * sent_back / incremental:,.0f}")
