"""Chapter 6: recall@k, MRR and nDCG for two retrievers on a toy help center.

"Keyword" is a small BM25 ranker. "Hybrid" is the same ranker after the query
is expanded with related words, a stand-in for the meaning-based match that an
embedding model provides. It keeps this script free of downloads.
"""
import math
import re

DOCS = {
    "D1": "Payout schedule: payouts are sent every business day for settled funds",
    "D2": "Payout delays after a bank account change: verification takes up to "
          "2 business days",
    "D3": "Error 412: the payout failed because bank account verification is pending",
    "D4": "Dispute holds: the disputed amount is deducted from the next payout",
    "D5": "Fees: 2.9% plus $0.30 for each successful card payment",
    "D6": "Refunds reduce the next payout by the refunded amount",
    "D7": "Risk reviews can pause payouts while an account is under review",
    "D8": "Bank outages: failed payouts are retried after the partner bank recovers",
}
# Each test question lists the passages a support lead judged useful (2) or
# partly useful (1). This is the "question, evidence" half of a golden set.
QUERIES = [
    ("why is my payout late after changing bank account", {"D2": 2, "D3": 1}),
    ("money has not arrived", {"D1": 1, "D2": 1, "D7": 1, "D8": 1}),
    ("error 412", {"D3": 2}),
    ("why was 640 dollars taken from my payout", {"D4": 2, "D6": 1}),
    ("how much do you charge per transaction", {"D5": 2}),
    ("payout paused account under review", {"D7": 2}),
]
RELATED = {"money": "payout payouts", "arrived": "sent delays", "late": "delays",
           "changing": "change", "taken": "deducted reduce", "charge": "fees",
           "transaction": "payment", "paused": "pause"}
STOP = {"is", "my", "the", "a", "do", "you", "why", "was", "how", "has", "not",
        "from", "for", "by", "to", "an", "of", "can", "are", "up", "per", "much"}


def tokens(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]


def bm25(query_terms, k1=1.5, b=0.75):
    docs = {d: tokens(t) for d, t in DOCS.items()}
    avg_len = sum(len(t) for t in docs.values()) / len(docs)
    scores = {}
    for d, terms in docs.items():
        score = 0.0
        for q in set(query_terms):
            df = sum(q in t for t in docs.values())
            if df == 0:
                continue
            idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
            tf = terms.count(q)
            norm = 1 - b + b * len(terms) / avg_len
            score += idf * tf * (k1 + 1) / (tf + k1 * norm)
        if score > 0:
            scores[d] = score
    return sorted(scores, key=lambda d: (-scores[d], d))


def keyword(query):
    return bm25(tokens(query))


def hybrid(query):
    terms = tokens(query)
    for t in list(terms):
        terms += RELATED.get(t, "").split()
    return bm25(terms)


# [listing]
def recall_at_k(ranked, relevant, k):
    """Share of the useful passages that appear in the top k."""
    return len(set(ranked[:k]) & set(relevant)) / len(relevant)


def reciprocal_rank(ranked, relevant):
    """1 / position of the first useful passage; 0 if none was returned."""
    for position, doc in enumerate(ranked, start=1):
        if doc in relevant:
            return 1 / position
    return 0.0


def ndcg_at_k(ranked, relevant, k):
    """Graded usefulness, discounted by position, against the ideal order."""
    def dcg(gains):
        return sum(g / math.log2(i + 2) for i, g in enumerate(gains))
    got = dcg([relevant.get(doc, 0) for doc in ranked[:k]])
    ideal = dcg(sorted(relevant.values(), reverse=True)[:k])
    return got / ideal
# [end listing]


def evaluate(retriever, k=3):
    rows = []
    for query, relevant in QUERIES:
        ranked = retriever(query)
        rows.append((recall_at_k(ranked, relevant, k),
                     reciprocal_rank(ranked, relevant),
                     ndcg_at_k(ranked, relevant, k), ranked[:k]))
    return rows


def main():
    kw, hy = evaluate(keyword), evaluate(hybrid)
    print(f"{'Question':<44}{'Keyword top 3':<16}{'Hybrid top 3'}")
    for (query, _), a, b in zip(QUERIES, kw, hy):
        print(f"{query[:42]:<44}{' '.join(a[3]) or '(nothing)':<16}"
              f"{' '.join(b[3]) or '(nothing)'}")
    print()
    print(f"{'Retriever':<12}{'Recall@3':>9}{'MRR':>7}{'nDCG@3':>8}")
    for name, rows in (("Keyword", kw), ("Hybrid", hy)):
        n = len(rows)
        print(f"{name:<12}{sum(r[0] for r in rows) / n:>9.2f}"
              f"{sum(r[1] for r in rows) / n:>7.2f}{sum(r[2] for r in rows) / n:>8.2f}")


if __name__ == "__main__":
    main()
