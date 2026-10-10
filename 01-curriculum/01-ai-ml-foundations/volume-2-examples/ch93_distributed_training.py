"""Chapter 93. Distributed training: where the memory goes, and what sharding saves.

Accounting follows the ZeRO paper (Rajbhandari et al., 2019): with mixed-precision
Adam each parameter costs 2 bytes of fp16 weights, 2 bytes of fp16 gradients and
12 bytes of optimizer state (fp32 copy of the weight, momentum, variance).

Run: python ch93_distributed_training.py
"""
import numpy as np

# [listing]
GB = 1e9


def per_gpu_gb(params, n_gpus):
    """Model-state memory per GPU. Activations come on top."""
    w, g, opt = 2 * params, 2 * params, 12 * params     # bytes
    return {
        "data parallel": (w + g + opt) / GB,
        "shard optimizer state": (w + g + opt / n_gpus) / GB,
        "shard optimizer + gradients": (w + (g + opt) / n_gpus) / GB,
        "shard everything": (w + g + opt) / n_gpus / GB,
    }


print("10 billion parameters on 8 GPUs with 80 GB each")
for name, gb in per_gpu_gb(10e9, 8).items():
    print(f"  {name:28s}{gb:6.1f} GB  {'fits' if gb <= 80 else 'does not fit'}")


def bubble(stages, micro_batches):
    """Share of pipeline time that stages spend idle (GPipe)."""
    return (stages - 1) / (micro_batches + stages - 1)


print("4 pipeline stages, idle share by micro-batch count:",
      ", ".join(f"{m}: {bubble(4, m):.0%}" for m in (1, 4, 12, 16)))
# [/listing]

# Hand-worked values from the chapter: 10 billion parameters on 8 GPUs
hand = per_gpu_gb(10e9, 8)
assert np.isclose(hand["data parallel"], 160.0)
assert np.isclose(hand["shard optimizer state"], 20 + 20 + 120 / 8)        # 55
assert np.isclose(hand["shard optimizer + gradients"], 20 + 140 / 8)       # 37.5
assert np.isclose(hand["shard everything"], 160 / 8)                       # 20
assert np.isclose(bubble(4, 12), 3 / 15)

# The ZeRO paper's own example: 7.5 billion parameters, 64 workers
zero = per_gpu_gb(7.5e9, 64)
assert np.isclose(zero["data parallel"], 120.0)
assert round(zero["shard optimizer state"], 1) == 31.4
assert round(zero["shard optimizer + gradients"], 1) == 16.6
assert round(zero["shard everything"], 1) == 1.9

# 70 billion parameters on 64 GPUs: only full sharding fits in 80 GB
big = per_gpu_gb(70e9, 64)
assert np.isclose(big["data parallel"], 1120.0) and big["shard everything"] == 17.5
assert round(big["shard optimizer state"], 1) == 293.1
assert round(big["shard optimizer + gradients"], 1) == 155.3

# Q93.1: 20 billion parameters on 16 GPUs
q1 = per_gpu_gb(20e9, 16)
assert np.isclose(q1["data parallel"], 320.0)
assert np.isclose(q1["shard optimizer state"], 40 + 40 + 240 / 16)         # 95
assert np.isclose(q1["shard optimizer + gradients"], 40 + 280 / 16)        # 57.5
assert np.isclose(q1["shard everything"], 20.0)

# Q93.2: adapters holding 0.5% of 10 billion parameters. Frozen weights need
# 2 bytes each; only the adapters need gradients and optimizer state.
adapters = 0.005 * 10e9
lora_gb = (2 * 10e9 + 16 * adapters) / GB
assert np.isclose(lora_gb, 20.8)

# Q93.3: 8 stages need 4 x 8 = 32 micro-batches by GPipe's rule of thumb
assert np.isclose(bubble(8, 32), 7 / 39)
assert round(bubble(8, 32), 2) == 0.18 and np.isclose(bubble(8, 8), 7 / 15)
