"""Chapter 99. Knowledge graphs and GraphRAG: build a tiny graph from four notes
and answer a two-hop question that word-overlap retrieval misses.

Run: python ch99_knowledge_graphs.py
"""
import re
from collections import defaultdict, deque

# [listing]
notes = ["Merchant Alder Goods logs in from device D-17.",
         "Device D-17 is also used by merchant Birch Supply.",
         "Birch Supply was terminated for fraud in March.",
         "Alder Goods sells garden tools in Ohio."]
question = "Is Alder Goods linked to a merchant terminated for fraud?"
STOP = {"is", "to", "a", "for", "in", "by", "from", "was", "also"}
words = lambda s: set(re.findall(r"[a-z0-9-]+", s.lower())) - STOP
print("words shared with the question, per note:",
      [len(words(question) & words(n)) for n in notes])

# In production a language model extracts triples; here, three patterns.
patterns = [(r"(?:Merchant )?(.+) logs in from device (\S+)\.", "uses_device", 1, 2),
            (r"Device (\S+) is also used by merchant (.+)\.", "uses_device", 2, 1),
            (r"(.+) was (terminated for fraud)", "status", 1, 2)]
graph = defaultdict(list)                          # node -> [(relation, node, note)]
for i, note in enumerate(notes):
    for pattern, relation, s, o in patterns:
        if m := re.match(pattern, note):
            graph[m.group(s)].append((relation, m.group(o), i))
            graph[m.group(o)].append((relation, m.group(s), i))

start, goal = "Alder Goods", "terminated for fraud"
queue, seen = deque([(start, [])]), {start}
while queue:                                       # breadth-first search
    node, path = queue.popleft()
    if node == goal:
        break
    for relation, nxt, i in graph[node]:
        if nxt not in seen:
            seen.add(nxt)
            queue.append((nxt, path + [f"{node} -{relation}[note {i}]- {nxt}"]))
print(*path, sep="\n")
# [/listing]

# Hand-worked overlap counts: content words of the question are
# {alder, goods, linked, merchant, terminated, fraud}
assert words(question) == {"alder", "goods", "linked", "merchant", "terminated",
                           "fraud"}
overlap = [len(words(question) & words(n)) for n in notes]
assert overlap == [3, 1, 2, 2]
# The bridge note (index 1) ranks last, so a top-2 or top-3 context drops it
ranked = sorted(range(4), key=lambda i: (-overlap[i], i))
assert ranked[-1] == 1 and ranked[:2] == [0, 2]
# The graph answer is a three-edge path that cites notes 0, 1 and 2
assert len(path) == 3
assert [int(re.search(r"note (\d)", p).group(1)) for p in path] == [0, 1, 2]
# Triples extracted: two uses_device edges and one status edge (stored both ways)
assert sum(len(v) for v in graph.values()) == 6
assert sorted(graph) == ["Alder Goods", "Birch Supply", "D-17",
                         "terminated for fraud"]
# Q99.2: indexing cost. 50,000 notes x 600 tokens through an extraction model
assert 50_000 * 600 == 30_000_000
