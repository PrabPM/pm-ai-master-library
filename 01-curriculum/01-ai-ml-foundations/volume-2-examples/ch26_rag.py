"""Chapter 26: retrieval-augmented generation end to end on six PayFlow chunks.

Chunk, embed (bag of words), retrieve, rerank, answer with a citation, check.
Run: python ch26_rag.py
"""
import re
import textwrap

import numpy as np

DOCS = {
    "payouts": "Payouts are sent two business days after a payment settles. "
               "A payout is delayed when the merchant account is under review.",
    "refunds": "A refund returns the full amount to the customer within five "
               "business days.",
    "disputes": "The merchant must answer a dispute with evidence within seven days.",
    "reserves": "A reserve holds ten percent of each payout for ninety days when "
                "the dispute rate is high.",
    "faq": "Payout schedule: daily.",
}
STOP = set("a an the is are of to for with when after each can be my on there why "
           "how does do what".split())
FAMILY = {"held": "hold", "money": "payout", "late": "delayed"}  # what a reranker knows


def words(text):
    """Lower-case content words, with a trailing s removed (payouts -> payout)."""
    found = re.findall(r"[a-z]+", text.lower())
    return [w.rstrip("s") for w in found if w not in STOP]


def chunk(docs):
    """One chunk per sentence, with an id that can be cited."""
    out = {}
    for name, text in docs.items():
        for n, sentence in enumerate(re.split(r"(?<=\.)\s+", text.strip()), 1):
            out[f"{name}#{n}"] = sentence
    return out


CHUNKS = chunk(DOCS)
VOCAB = sorted({w for c in CHUNKS.values() for w in words(c)})


def embed(text):
    v = np.array([1.0 if w in words(text) else 0.0 for w in VOCAB])
    return v / max(np.linalg.norm(v), 1e-12)


INDEX = {cid: embed(text) for cid, text in CHUNKS.items()}       # built once, offline


def retrieve(query, k):
    q = embed(query)
    scored = sorted(((float(q @ v), cid) for cid, v in INDEX.items()), reverse=True)
    return scored[:k]


def rerank(query, candidates):
    """Reads query and chunk together: share of query words the chunk covers."""
    q = {FAMILY.get(w, w) for w in words(query)}
    scored = [(len(q & set(words(CHUNKS[cid]))) / len(q), cid) for _, cid in candidates]
    return sorted(scored, reverse=True)


def grounded(answer, cid):
    """Crude support check: every content word of the answer is in the cited chunk."""
    return set(words(answer)) <= set(words(CHUNKS[cid]))


query = "Can a payout be held?"
print("query:", query, "->", words(query))
for k in (3, 4):
    hits = retrieve(query, k)
    print(f"retrieve k={k}:", "  ".join(f"{cid} {s:.3f}" for s, cid in hits))
    score, best = rerank(query, hits)[0]
    print(f"  reranked top: {best} (covers {score:.0%} of the query)")
print(textwrap.fill(f"answer: {CHUNKS[best]} [{best}]", width=80))

claim = "A reserve holds thirty percent of each payout."
print("support check, quoted answer:", grounded(CHUNKS[best], best))
print("support check, invented claim:", grounded(claim, best))

# Checks against the hand calculation in the chapter.
top4 = retrieve(query, 4)
assert np.allclose([s for s, _ in top4], 1 / np.sqrt([3, 6, 7, 10]))
assert [c for _, c in top4] == ["faq#1", "payouts#2", "payouts#1", "reserves#1"]
assert rerank(query, top4)[0] == (1.0, "reserves#1")
assert rerank(query, retrieve(query, 3))[0][1] != "reserves#1"
