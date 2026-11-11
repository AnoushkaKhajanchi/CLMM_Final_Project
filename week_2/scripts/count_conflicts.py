"""Count conflicting facts and whether memory kept the old version (CPU only, read-only).

A conflict is two or more facts with the same subject and relation but a
different answer, e.g.
    447. Roy Rogers is married to Dale Evans.   (old)
    452. Roy Rogers is married to John McVie.   (new: higher number wins)

READS (never modifies) from a saved run folder:
    chunks.json         - the input text, as fed to the writer
    memory_final.json   - memory after the last chunk (semantic section only)

WRITES one CSV with a row per conflict:
    only_new  - old fact gone, new fact kept  (the goal)
    both      - old and new both kept         (stale fact)
    only_old  - update never stored
    neither   - both missing

Usage:
    python week_2/scripts/count_conflicts.py <run_folder> <output.csv>
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from audit_lost_facts import normalize

# "<subject> <relation> <answer>." Relations found in FactConsolidation.
RELATIONS = [
    "is married to", "was born in the city of", "died in the city of", "is a citizen of",
    "plays the position of", "is associated with the sport of", "is located in the continent of",
    "is famous for", "was founded by", "was founded in the city of", "was created in the country of",
    "was performed by", "speaks the language of", "is employed by", "is affiliated with the religion of",
    "works in the field of", "worked in the city of", "was created by", "was developed by",
    "was written in the language of",
]
RELATION_RE = re.compile(r"^(.+? (?:%s)) (.+)$" % "|".join(map(re.escape, RELATIONS)))


def split_fact(fact):
    """Split a fact into (question part, answer). Returns None if no pattern fits."""
    fact = fact.strip().removesuffix(".")
    m = RELATION_RE.match(fact)
    if m:
        return m.group(1), m.group(2)
    # Otherwise "The capital of France is Paris" / "Aristotle's child is Nicomachus".
    if " is " in fact:
        key, answer = fact.rsplit(" is ", 1)
        return key + " is", answer
    return None


def main(run_folder, output_csv):
    run = Path(run_folder)
    text = "".join(json.loads((run / "chunks.json").read_text()))
    memory = json.loads((run / "memory_final.json").read_text())
    # A note may hold one fact or many (one per line), so check line by line.
    stored = {normalize(line) for e in memory["semantic"] for t in e.values() for line in t.splitlines()}

    groups, unmatched = defaultdict(list), []
    for number, fact in re.findall(r"^(\d+)\. (.+)$", text, re.M):
        parts = split_fact(fact)
        if parts is None:
            unmatched.append(number)
            continue
        groups[parts[0]].append((int(number), fact, parts[1]))

    rows = []
    for key, facts in groups.items():
        if len({answer for _, _, answer in facts}) < 2:
            continue  # no disagreement, so no conflict
        facts.sort()
        new_number, new_fact, new_answer = facts[-1]
        old = [f for f in facts[:-1] if f[2] != new_answer]
        old_kept = any(normalize(f[1]) in stored for f in old)
        new_kept = normalize(new_fact) in stored
        outcome = {(False, True): "only_new", (True, True): "both",
                   (True, False): "only_old", (False, False): "neither"}[(old_kept, new_kept)]
        rows.append({
            "question_part": key,
            "old_numbers": " ".join(str(f[0]) for f in old),
            "old_answers": " | ".join(f[2] for f in old),
            "new_number": new_number,
            "new_answer": new_answer,
            "old_in_memory": old_kept,
            "new_in_memory": new_kept,
            "outcome": outcome,
        })
    rows.sort(key=lambda r: r["new_number"])

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    counts = Counter(r["outcome"] for r in rows)
    stale = counts["both"] + counts["only_old"]
    print(f"conflicts: {len(rows)} | " + " | ".join(f"{k}: {counts[k]}" for k in ["only_new", "both", "only_old", "neither"]))
    print(f"stale rate (old fact still in memory): {stale}/{len(rows)} -> {output_csv}")
    if unmatched:
        print(f"facts with no recognized pattern (skipped): {unmatched}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
