"""Chapter 31: image tokens, and the cost of a general model versus a pipeline.

Prices and accuracies are illustrative, not quotes or benchmark results.
Run: python ch31_multimodal.py
"""
import numpy as np


def image_tokens(height, width, patch=14):
    """A vision transformer cuts the image into square patches, one token each."""
    return (height // patch) * (width // patch)


for side in (224, 448, 896):
    n = image_tokens(side, side)
    print(f"{side} x {side} image, 14-pixel patches: {n:5d} tokens")

pages = 3
tokens_doc = pages * image_tokens(448, 448)
print(f"a {pages}-page KYB document at 448 x 448 per page: {tokens_doc:,} image tokens")


def cost_per_document(model_cost, accuracy, review_cost=0.50):
    """Every document pays the model; the ones it gets wrong also pay a human."""
    return model_cost + (1 - accuracy) * review_cost


general = cost_per_document(model_cost=0.010, accuracy=0.96)
pipeline = cost_per_document(model_cost=0.002, accuracy=0.88)
volume = 50_000
print(f"general multimodal model: USD {general:.3f} per document, "
      f"USD {general * volume:,.0f} per month")
print(f"OCR-and-rules pipeline:   USD {pipeline:.3f} per document, "
      f"USD {pipeline * volume:,.0f} per month")

# Accuracy the pipeline would need for the two options to cost the same.
break_even = 1 - (general - 0.002) / 0.50
print(f"pipeline accuracy needed to tie: {break_even:.1%}")

# Checks against the hand calculation in the chapter.
assert image_tokens(224, 224) == 256 and image_tokens(448, 448) == 1024
assert tokens_doc == 3072
assert np.isclose(general, 0.030) and np.isclose(pipeline, 0.062)
assert np.isclose(break_even, 0.944)
