"""Chapter 111: eight evaluation metrics computed on a small labeled set.

Agent metrics: function-call accuracy, task success, plan fidelity.
RAG metrics: faithfulness, answer relevance, citation coverage,
context precision and context recall.
The labels are written by hand here; in production a reviewer or a judge model
supplies them.
"""
import numpy as np


def norm(value):
    return value.strip().lower() if isinstance(value, str) else float(value)


def same_call(a, b):
    """Same tool name and the same arguments after normalization."""
    return a[0] == b[0] and ({k: norm(v) for k, v in a[1].items()}
                             == {k: norm(v) for k, v in b[1].items()})


def function_call_accuracy(tasks, only_tool=None):
    right = total = 0
    for task in tasks:
        gold = list(task["gold"])
        for call in task["model"]:
            if only_tool and call[0] != only_tool:
                continue
            total += 1
            match = next((g for g in gold if same_call(call, g)), None)
            if match:
                gold.remove(match)          # each gold call can be used once
                right += 1
    return right / total


def levenshtein(a, b):
    """Fewest insertions, deletions and substitutions that turn a into b."""
    d = np.zeros((len(a) + 1, len(b) + 1), dtype=int)
    d[:, 0], d[0, :] = np.arange(len(a) + 1), np.arange(len(b) + 1)
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1,
                          d[i - 1, j - 1] + (a[i - 1] != b[j - 1]))
    return int(d[-1, -1])


def plan_fidelity(task):
    model = [c[0] for c in task["model"]]
    gold = [c[0] for c in task["gold"]]
    return 1 - levenshtein(model, gold) / max(len(model), len(gold))


def rag_scores(ex):
    claims = ex["claims"]                    # (supported, cited_ok, on_topic)
    hit = len(set(ex["retrieved"]) & ex["relevant"])
    return {
        "faithfulness": np.mean([c[0] for c in claims]),
        "answer relevance": np.mean([c[2] for c in claims]),
        "citation coverage": np.mean([c[1] for c in claims]),
        "context precision": hit / len(ex["retrieved"]),
        "context recall": hit / len(ex["relevant"]),
    }


def call(tool, **args):
    return (tool, args)


TASKS = [
    {"name": "A", "success": True,
     "gold": [call("get_payout_status", payout_id="po_207"),
              call("get_merchant_profile", merchant_id="m_juniper"),
              call("retry_payout", payout_id="po_207")],
     "model": [call("get_payout_status", payout_id="PO_207 "),
               call("get_merchant_profile", merchant_id="m_juniper"),
               call("retry_payout", payout_id="po_207")]},
    {"name": "B", "success": True,
     "gold": [call("get_payout_status", payout_id="po_311"),
              call("retry_payout", payout_id="po_311")],
     "model": [call("get_payout_status", payout_id="po_311"),
               call("get_merchant_profile", merchant_id="m_harbor"),
               call("retry_payout", payout_id="po_311")]},
    {"name": "C", "success": True,
     "gold": [call("list_failed_payouts", limit=10),
              call("get_payout_status", payout_id="po_208")],
     "model": [call("list_failed_payouts", limit=50),
               call("get_payout_status", payout_id="po_208")]},
    {"name": "D", "success": False,          # account closed: must not retry
     "gold": [call("get_payout_status", payout_id="po_415")],
     "model": [call("get_payout_status", payout_id="po_415"),
               call("retry_payout", payout_id="po_415")]},
]

RAG = [
    {"q": "Why did payout po_207 fail?",
     "retrieved": ["d1", "d2", "d3", "d4"], "relevant": {"d1", "d3"},
     "claims": [(1, 1, 1), (1, 1, 1), (0, 0, 1)]},
    {"q": "How long does a retried payout take to settle?",
     "retrieved": ["d5", "d6", "d7", "d8"], "relevant": {"d5", "d9"},
     "claims": [(1, 0, 1), (1, 1, 0)]},
    {"q": "Can a merchant change the payout bank account mid-cycle?",
     "retrieved": ["d10", "d11", "d12", "d13"], "relevant": {"d10"},
     "claims": [(1, 1, 1), (1, 1, 1), (1, 1, 1), (1, 0, 1)]},
]

if __name__ == "__main__":
    fca = function_call_accuracy(TASKS)
    fca_retry = function_call_accuracy(TASKS, only_tool="retry_payout")
    success = np.mean([t["success"] for t in TASKS])
    fidelity = [plan_fidelity(t) for t in TASKS]
    print(f"function-call accuracy  {fca:.3f}   (retry_payout only: {fca_retry:.3f})")
    print(f"task success rate       {success:.3f}")
    print(f"plan fidelity by task   {np.round(fidelity, 3)}  "
          f"mean {np.mean(fidelity):.3f}")
    print()
    rows = [rag_scores(ex) for ex in RAG]
    for metric in rows[0]:
        values = [r[metric] for r in rows]
        per_q = "  ".join(f"{v:.3f}" for v in values)
        print(f"{metric:<18} {per_q}   mean {np.mean(values):.3f}")

    assert np.isclose(fca, 7 / 10) and np.isclose(fca_retry, 2 / 3)
    assert np.isclose(success, 0.75)
    assert np.allclose(fidelity, [1, 2 / 3, 1, 1 / 2])
    means = {m: np.mean([r[m] for r in rows]) for m in rows[0]}
    assert np.isclose(means["faithfulness"], 8 / 9)
    assert np.isclose(means["answer relevance"], (1 + 0.5 + 1) / 3)
    assert np.isclose(means["citation coverage"], (2 / 3 + 1 / 2 + 3 / 4) / 3)
    assert np.isclose(means["context precision"], (0.5 + 0.25 + 0.25) / 3)
    assert np.isclose(means["context recall"], (1 + 0.5 + 1) / 3)
    assert levenshtein(["a", "b", "c"], ["a", "c"]) == 1
