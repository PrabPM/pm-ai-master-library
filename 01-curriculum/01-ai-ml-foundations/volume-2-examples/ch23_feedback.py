"""Chapter 23: the preference signal. Bradley-Terry and the DPO loss on a toy policy.

Run: python ch23_feedback.py
"""
import numpy as np


def sigmoid(u):
    return 1.0 / (1.0 + np.exp(-u))


def softmax(z):
    e = np.exp(z - z.max())
    return e / e.sum()


# A reward model turns two scores into a probability that the first answer wins.
r_good, r_bad = 2.0, 0.5
p_win = sigmoid(r_good - r_bad)          # Bradley-Terry: about 0.82


def dpo_loss(logp_w, logp_l, ref_w, ref_l, beta):
    """Log-probabilities of the preferred (w) and rejected (l) answer."""
    margin = (logp_w - ref_w) - (logp_l - ref_l)
    return -np.log(sigmoid(beta * margin))


print(f"DPO loss, hand example    = {dpo_loss(-20.0, -24.0, -21.0, -23.0, 0.5):.4f}")
print(f"DPO loss, before training = {dpo_loss(-21.0, -23.0, -21.0, -23.0, 0.5):.4f}")

# A toy policy: one prompt, three candidate answers, one logit each.
answers = ["cites the policy", "vague apology", "invents a date"]
ref = np.array([0.0, 1.0, 0.5])            # reference logits (frozen)
theta = ref.copy()                         # the model we train starts as a copy
w, l, beta, lr = 0, 2, 0.5, 1.0            # agents preferred answer 0 over answer 2

print("step  loss    P(cites)  P(vague)  P(invents)")
for step in range(41):
    logp, logp_ref = np.log(softmax(theta)), np.log(softmax(ref))
    loss = dpo_loss(logp[w], logp[l], logp_ref[w], logp_ref[l], beta)
    if step % 20 == 0:
        probs = "    ".join(f"{p:.3f}" for p in softmax(theta))
        print(f"{step:4d}  {loss:.4f}  {probs}")
    pull = lr * beta * (1 - np.exp(-loss))     # size of the gradient step
    theta[w] += pull                           # preferred answer up
    theta[l] -= pull                           # rejected answer down

# Checks against the hand calculation in the chapter.
assert np.isclose(dpo_loss(-20.0, -24.0, -21.0, -23.0, 0.5), -np.log(sigmoid(1.0)))
assert np.isclose(dpo_loss(-21.0, -23.0, -21.0, -23.0, 0.5), np.log(2))
assert np.isclose(p_win, sigmoid(1.5))
assert softmax(theta)[w] > softmax(ref)[w] and softmax(theta)[l] < softmax(ref)[l]
