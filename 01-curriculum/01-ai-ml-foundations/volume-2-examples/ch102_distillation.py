"""Chapter 102. Knowledge distillation: the temperature-softened loss by hand and
in code, a feature-matching loss, and the cost arithmetic behind the decision.

Run: python ch102_distillation.py
"""
import numpy as np

# [listing]
def softmax(z, T=1.0):
    e = np.exp((z - z.max()) / T)
    return e / e.sum()


def distill_loss(z_student, z_teacher, label, T=2.0, alpha=0.5):
    hard = -np.log(softmax(z_student)[label])              # cross-entropy, T = 1
    p_t, p_s = softmax(z_teacher, T), softmax(z_student, T)
    soft = np.sum(p_t * np.log(p_t / p_s))                 # KL(teacher || student)
    return hard, soft, alpha * hard + (1 - alpha) * T ** 2 * soft


classes = ["refund", "dispute", "payout"]                  # ticket intents
z_teacher = np.array([4.0, 2.0, 0.0])
z_student = np.array([2.0, 2.0, 0.0])
print("teacher at T=1:", softmax(z_teacher).round(3))
print("teacher at T=2:", softmax(z_teacher, 2).round(3))
print("student at T=2:", softmax(z_student, 2).round(3))
hard, soft, total = distill_loss(z_student, z_teacher, label=0)
print(f"hard loss {hard:.3f}  soft loss {soft:.3f}  total {total:.3f}")

h_teacher = np.array([1.0, 0.0, 2.0, 1.0])                 # teacher hidden state
h_student = np.array([0.5, 1.5])                           # student is narrower
W = np.array([[1.0, 0.0], [0.0, 0.0], [1.0, 1.0], [0.0, 1.0]])   # learned projection
print("feature loss:", np.sum((W @ h_student - h_teacher) ** 2))

tickets = 2_000_000                                        # per month
teacher, student, share = 0.004, 0.0002, 0.10              # USD per ticket; escalated
print(f"monthly cost: teacher USD {tickets * teacher:,.0f}, student USD "
      f"{tickets * student:,.0f}, student + {share:.0%} escalated USD "
      f"{tickets * (student + share * teacher):,.0f}")
# [/listing]

# Hand-worked: exponentials of [2, 1, 0] and [1, 1, 0]
e = np.exp
p_t = np.array([e(2), e(1), 1]) / (e(2) + e(1) + 1)
p_s = np.array([e(1), e(1), 1]) / (2 * e(1) + 1)
assert np.allclose(p_t.round(3), [0.665, 0.245, 0.090])
assert np.allclose(p_s.round(3), [0.422, 0.422, 0.155])
assert np.allclose(softmax(z_teacher, 2), p_t)
assert np.allclose(softmax(z_student, 2), p_s)
kl = np.sum(p_t * np.log(p_t / p_s))
assert np.isclose(soft, kl) and round(kl, 3) == 0.120
assert np.isclose(hard, -np.log(e(2) / (2 * e(2) + 1))) and round(hard, 3) == 0.759
assert np.isclose(total, 0.5 * hard + 0.5 * 4 * kl) and round(total, 3) == 0.619
# with the rounded hand values: 0.5 * 0.759 + 0.5 * 4 * 0.120 = 0.6195
assert np.isclose(0.5 * 0.759 + 0.5 * 4 * 0.120, 0.6195)
# the three hand-computed terms, from the rounded probabilities shown in the chapter
hand_terms = [0.665 * np.log(0.665 / 0.422), 0.245 * np.log(0.245 / 0.422),
              0.090 * np.log(0.090 / 0.155)]
assert np.allclose(np.round(hand_terms, 3), [0.302, -0.133, -0.049])
assert round(sum(hand_terms), 3) == 0.120
# With identical logits the soft loss is zero
assert np.isclose(distill_loss(z_teacher, z_teacher, 0)[1], 0.0)
# Feature loss by hand: W h_s = [0.5, 0, 2.0, 1.5]; differences -0.5, 0, 0, 0.5
assert np.allclose(W @ h_student, [0.5, 0.0, 2.0, 1.5])
assert np.isclose(np.sum((W @ h_student - h_teacher) ** 2), 0.5)
# Cost arithmetic
assert np.isclose(tickets * teacher, 8000) and np.isclose(tickets * student, 400)
assert np.isclose(tickets * (student + share * teacher), 1200)

# Q102.1: teacher logits [3, 1], T = 2 -> softmax of [1.5, 0.5]
assert np.allclose(softmax(np.array([3.0, 1.0]), 2).round(3), [0.731, 0.269])
assert np.allclose(softmax(np.array([3.0, 1.0])).round(3), [0.881, 0.119])
# Q102.2: escalation share at which the cascade costs half the teacher-only bill
# 2e6 * (0.0002 + s * 0.004) = 4000  ->  s = 0.45
assert np.isclose((4000 / tickets - student) / teacher, 0.45)
