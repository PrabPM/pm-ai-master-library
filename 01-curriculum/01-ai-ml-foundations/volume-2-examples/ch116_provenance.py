"""Chapter 116: a signed manifest for a model, and a recall driven by a bill of
materials.

Standard library only. Real systems sign with a private key and verify with the
matching public key. The standard library has no public-key signatures, so this
sketch uses a keyed hash (HMAC) to show the same verify-or-reject logic.
"""
import hashlib
import hmac
import json

SIGNING_KEY = b"demo-key-kept-in-a-vault"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def make_manifest(files):
    """One digest per file, sorted so the manifest is the same every time."""
    return {name: sha256(blob) for name, blob in sorted(files.items())}


def sign(manifest):
    body = json.dumps(manifest, sort_keys=True).encode()
    return hmac.new(SIGNING_KEY, body, hashlib.sha256).hexdigest()


def verify(files, manifest, signature):
    if not hmac.compare_digest(sign(manifest), signature):
        return "REJECT: manifest signature does not verify"
    for name, blob in files.items():
        if manifest.get(name) != sha256(blob):
            return f"REJECT: {name} does not match the manifest"
    return "LOAD"


# A bill of materials per deployed model: what went into it.
BOM = {
    "dispute-summarizer@1.4": {"base": "open-base-7b@2.1",
                               "datasets": ["tickets-2025Q4", "disputes-2025"]},
    "support-drafts@3.0": {"base": "open-base-7b@2.1",
                           "datasets": ["tickets-2025Q4", "macros-v9"]},
    "kyb-extractor@2.2": {"base": "doc-base@1.0", "datasets": ["kyb-forms-2026"]},
    "ticket-router@5.1": {"base": "small-encoder@4.2",
                          "datasets": ["tickets-2025Q4"]},
    "fraud-score@12.0": {"base": None, "datasets": ["payments-2026H1"]},
}


def affected_by(component):
    return sorted(m for m, parts in BOM.items()
                  if component == parts["base"] or component in parts["datasets"])


if __name__ == "__main__":
    files = {"weights.bin": b"\x00\x01\x02" * 1000, "tokenizer.json": b'{"v": 1}',
             "config.json": b'{"layers": 12}'}
    manifest = make_manifest(files)
    signature = sign(manifest)
    for name, d in manifest.items():
        print(f"{name:<15} sha256 {d[:16]}")
    print("signature", signature[:16])
    print("as shipped:        ", verify(files, manifest, signature))

    changed = b"\x00\x01\x03" + files["weights.bin"][3:]
    tampered = dict(files, **{"weights.bin": changed})
    print("one byte changed:  ", verify(tampered, manifest, signature))

    forged = dict(manifest, **{"weights.bin": sha256(tampered["weights.bin"])})
    print("manifest rewritten:", verify(tampered, forged, signature))

    hit = affected_by("tickets-2025Q4")
    print(f"built on tickets-2025Q4: {len(hit)} of {len(BOM)} models")
    print("  " + ", ".join(hit))
    print("built on open-base-7b@2.1:")
    print("  " + ", ".join(affected_by("open-base-7b@2.1")))

    assert verify(files, manifest, signature) == "LOAD"
    assert verify(tampered, manifest, signature).startswith("REJECT: weights.bin")
    assert verify(tampered, forged, signature).startswith("REJECT: manifest")
    assert len(hit) == 3 and len(affected_by("open-base-7b@2.1")) == 2
