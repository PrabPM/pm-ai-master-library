"""Chapter 20: byte-pair encoding from scratch on a tiny PayFlow corpus.

Run: python ch20_bpe.py
"""
from collections import Counter

corpus = ("pay pay pay pay payout payout payout paid paid "
          "refund refund refunded")
word_counts = Counter(corpus.split())


def merge_word(symbols, pair):
    """Replace every adjacent occurrence of pair in one word by the joined symbol."""
    out, i = [], 0
    while i < len(symbols):
        if symbols[i:i + 2] == pair:
            out.append(symbols[i] + symbols[i + 1])
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return tuple(out)


def train_bpe(word_counts, num_merges):
    words = {tuple(w): c for w, c in word_counts.items()}    # start from characters
    merges = []
    for _ in range(num_merges):
        pairs = Counter()
        for symbols, count in words.items():
            for pair in zip(symbols, symbols[1:]):
                pairs[pair] += count
        best = max(pairs, key=pairs.get)        # most frequent; ties: first seen
        merges.append((best, pairs[best]))
        words = {merge_word(s, best): c for s, c in words.items()}
    return merges


def encode(word, merges):
    symbols = tuple(word)
    for pair, _ in merges:                      # replay the merges in learned order
        symbols = merge_word(symbols, pair)
    return list(symbols)


merges = train_bpe(word_counts, num_merges=10)
print("merges, with pair counts:")
print("  " + " ".join(f"{a + b}({count})" for (a, b), count in merges))

text = "payouts refunded repaid txn_9f3a"
total = 0
for word in text.split():
    pieces = encode(word, merges)
    total += len(pieces)
    print(f"{word:9s} -> {len(pieces)} tokens  {pieces}")
print(f"{len(text.split())} words, {len(text)} characters, {total} tokens")

# Cost follows tokens. Prices are illustrative, in USD per million tokens.
tokens_in, tokens_out, price_in, price_out = 1700, 300, 2.00, 10.00
per_request = (tokens_in * price_in + tokens_out * price_out) / 1e6
print(f"request with {tokens_in} tokens in, {tokens_out} out: USD {per_request:.4f}; "
      f"40,000 a day: USD {per_request * 40_000:,.0f}")

# Checks against the hand count in the chapter.
assert merges[0] == (("p", "a"), 9)
assert merges[1] == (("pa", "y"), 7)
assert encode("payout", merges) == ["payout"]
assert encode("payouts", merges) == ["payout", "s"]
assert len(encode("txn_9f3a", merges)) == 8
assert total == 17
assert abs(per_request - 0.0064) < 1e-12
