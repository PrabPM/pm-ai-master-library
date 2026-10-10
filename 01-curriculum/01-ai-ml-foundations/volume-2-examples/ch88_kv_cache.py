"""Chapter 88: KV-cache memory per token, prefix caching and chunked prefill.

Model shape, card size, speeds and price multipliers are illustrative.
Run: python ch88_kv_cache.py
"""
import numpy as np


def kv_bytes_per_token(layers, kv_heads, head_dim, bytes_per_number=2):
    """Keys and values (the 2) in every layer and key-value head."""
    return 2 * layers * kv_heads * head_dim * bytes_per_number


def concurrent_requests(card_gb, weights_gb, overhead_gb, per_token, tokens):
    free_bytes = (card_gb - weights_gb - overhead_gb) * 1e9
    return int(free_bytes // (per_token * tokens))


full = kv_bytes_per_token(layers=32, kv_heads=32, head_dim=128)
grouped = kv_bytes_per_token(layers=32, kv_heads=8, head_dim=128)
tokens = 2000                                  # 1,700 prompt + 300 answer
fit_full = concurrent_requests(24, 16, 1, full, tokens)
fit_grouped = concurrent_requests(24, 16, 1, grouped, tokens)
print(f"KV bytes per token: {full:,} (32 key-value heads), {grouped:,} (8)")
print(f"2,000-token request: {full * tokens / 1e9:.2f} GB or "
      f"{grouped * tokens / 1e9:.2f} GB; a 24 GB card holds {fit_full} or {fit_grouped}")


def prefill_tokens(shared, unique, hit_rate):
    """Tokens still to process when the shared prefix is cached."""
    return unique + (1 - hit_rate) * shared


shared, unique = 1200, 500
work = [prefill_tokens(shared, unique, h) for h in (0.0, 0.5, 0.9)]
print("prefill tokens at hit rate 0%, 50%, 90%:", ", ".join(f"{w:.0f}" for w in work))


def billed_multiplier(hit_rate, read=0.10, write=1.25):
    """Hosted pricing: hits get a discount, misses pay to write."""
    return hit_rate * read + (1 - hit_rate) * write


print(f"hosted API: shared part billed at {billed_multiplier(0.9):.3f}x at 90% hits; "
      f"break-even hit rate {(1.25 - 1) / (1.25 - 0.10):.1%}")

# Chunked prefill: a long prompt arrives while other requests are streaming.
prompt, prefill_speed, decode_step, chunk = 8000, 10_000, 0.02, 1000
whole = prompt / prefill_speed
pieces = prompt // chunk
piece = chunk / prefill_speed
print(f"8,000-token prompt whole: others stall {whole + decode_step:.2f} s, "
      f"its first token at {whole:.2f} s")
print(f"in {pieces} chunks: others stall {piece + decode_step:.2f} s, "
      f"its first token at {pieces * (piece + decode_step):.2f} s")

# Checks against the hand calculation in the chapter.
assert full == 524_288 and grouped == 131_072
assert (fit_full, fit_grouped) == (6, 26)
assert prefill_tokens(1200, 500, 0.9) == 620
assert np.isclose(billed_multiplier(0.9), 0.215)
assert np.isclose(pieces * (piece + decode_step), 0.96)
