"""Chapter 16: train from scratch, freeze and probe, or fine-tune everything."""
import numpy as np

from ch00_payflow_data import sigmoid

# By hand: how many weights each level of adaptation trains.
d, r = 768, 8                                  # one 768 x 768 weight matrix, rank 8
full, low_rank, head = d * d, 2 * d * r, d * 2 + 2
print(f"one matrix {full:,} weights   rank-{r} update {low_rank:,} "
      f"({low_rank / full:.1%})   two-class head {head:,}")
assert (full, low_rank, head) == (589824, 12288, 1538)
assert np.isclose(low_rank / full, 0.021, atol=5e-4)

rng = np.random.default_rng(16)
D, H = 20, 16                                  # raw features, hidden units
A_cards = rng.normal(0, 0.6, (5, D))           # hidden structure of card payments
A_bank = A_cards + 0.3 * rng.normal(0, 0.6, (5, D))   # bank transfers: similar
U_cards = rng.normal(0, 1.5, (8, 5))           # eight outcomes labeled on cards
u_bank = rng.normal(0, 1.5, (1, 5))            # one outcome on bank transfers


def make(n, A, U):
    X = rng.normal(size=(n, D))
    scores = np.tanh(X @ A.T) @ U.T + 0.3 * rng.normal(size=(n, len(U)))
    return X, (scores > 0).astype(float)


def accuracy(X, Y, W1, b1, W2, b2):
    return np.mean((np.tanh(X @ W1 + b1) @ W2 + b2 > 0) == Y)


def fresh(outputs):
    return (rng.normal(0, 0.3, (D, H)), np.zeros(H), rng.normal(0, 0.3, (H, outputs)),
            np.zeros(outputs))


def train(X, Y, W1, b1, W2, b2, rate, freeze_backbone=False, epochs=1000):
    W1, b1, W2, b2 = W1.copy(), b1.copy(), W2.copy(), b2.copy()
    for epoch in range(epochs):
        hidden = np.tanh(X @ W1 + b1)
        D2 = (sigmoid(hidden @ W2 + b2) - Y) / len(X)
        if not freeze_backbone:
            D1 = (D2 @ W2.T) * (1 - hidden ** 2)
            W1, b1 = W1 - rate * X.T @ D1, b1 - rate * D1.sum(axis=0)
        W2, b2 = W2 - rate * hidden.T @ D2, b2 - rate * D2.sum(axis=0)
    return W1, b1, W2, b2


def adapt(Xb, Yb, pre):
    scratch = train(Xb, Yb, *fresh(1), rate=1.0)
    new_head = (pre[0], pre[1], np.zeros((H, 1)), np.zeros(1))
    probe = train(Xb, Yb, *new_head, rate=1.0, freeze_backbone=True)
    tuned = train(Xb, Yb, *probe, rate=0.3)    # start from the probe, lower rate
    return scratch, probe, tuned


Xc, Yc = make(5000, A_cards, U_cards)
pre = train(Xc, Yc, *fresh(8), rate=1.0)       # pretraining on plentiful card labels
print(f"pretrained on cards: accuracy {accuracy(Xc, Yc, *pre):.3f}")

Xtest, Ytest = make(5000, A_bank, u_bank)
print("bank labels   scratch   frozen+head   fine-tuned   cards after fine-tune")
for n in (30, 100, 300, 1000, 3000):
    scratch, probe, tuned = adapt(*make(n, A_bank, u_bank), pre)
    kept = accuracy(Xc, Yc, tuned[0], tuned[1], pre[2], pre[3])
    print(f"{n:>11}   {accuracy(Xtest, Ytest, *scratch):.3f}     "
          f"{accuracy(Xtest, Ytest, *probe):.3f}         "
          f"{accuracy(Xtest, Ytest, *tuned):.3f}        {kept:.3f}")
