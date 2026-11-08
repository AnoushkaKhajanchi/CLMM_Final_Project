"""Audit which input facts actually made it into memory (CPU only, read-only).

READS (never modifies) a saved run folder, e.g.
    week_1/results/week1_closeout/evidence/run/factconsolidation_sh_6k/
using only these fields of each chunk_###.json:
    input_chunk                   - the text the writer was given
    generation.hit_output_limit   - did the writer's reply get cut off?
    calls[].call.arguments        - the memory operations the writer asked for
    after.semantic                - semantic memory after this chunk

WRITES one CSV: one row per numbered input fact, saying whether it was stored.

For the FactConsolidation runs only (their chunks are slices of one long text).
"Not stored" means not found after ignoring case, numbering and stray quotes;
a paraphrased fact would also count as not stored.

Usage:
    python week_2/scripts/audit_lost_facts.py <run_folder> <output.csv>
"""
import csv
import json
import re
import sys
from pathlib import Path


def normalize(text):
    """Make formatting differences not count as a missing fact.

    The writer sometimes keeps the serial number ("342. Thomas Arne ...") and
    sometimes leaves a stray quote at the end ("... English.'"). Both are
    ignored here; any other wording change still counts as not stored.
    """
    text = re.sub(r"^\d+\.\s*", "", text.strip())
    return text.strip(" .'\"").lower()


def is_complete_json(arguments):
    """A call is incomplete if its arguments were cut off mid-JSON."""
    try:
        json.loads(arguments)
        return True
    except json.JSONDecodeError:
        return False


def main(run_folder, output_csv):
    chunk_files = sorted(Path(run_folder).glob("chunk_*.json"))
    chunks = [json.loads(f.read_text()) for f in chunk_files]

    # Chunks can split a fact in two (e.g. "72. Stephen Crane" | " is famous for...").
    # So rebuild the full text, then note which chunk each fact *finishes* in.
    full_text, chunk_ends = "", []
    for c in chunks:
        full_text += c["input_chunk"]
        chunk_ends.append(len(full_text))

    rows = []
    for m in re.finditer(r"^(\d+)\. (.+)$", full_text, re.M):
        chunk_i = next(i for i, end in enumerate(chunk_ends) if m.end() <= end)
        stored = {normalize(text) for e in chunks[chunk_i]["after"]["semantic"] for text in e.values()}
        rows.append({
            "fact_number": int(m.group(1)),
            "fact": m.group(2),
            "chunk": chunk_i,
            "chunk_was_cut_off": chunks[chunk_i]["generation"]["hit_output_limit"],
            "stored_verbatim": normalize(m.group(2)) in stored,
        })

    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # Short per-chunk summary on screen.
    print(f"{'chunk':>5} {'facts':>6} {'stored':>7} {'missing':>8} {'cut_off':>8} {'incomplete_calls':>17}")
    for i, c in enumerate(chunks):
        mine = [r for r in rows if r["chunk"] == i]
        stored = sum(r["stored_verbatim"] for r in mine)
        incomplete = sum(not is_complete_json(call["call"]["arguments"]) for call in c["calls"])
        print(f"{i:>5} {len(mine):>6} {stored:>7} {len(mine) - stored:>8} "
              f"{str(c['generation']['hit_output_limit']):>8} {incomplete:>17}")
    total_stored = sum(r["stored_verbatim"] for r in rows)
    print(f"TOTAL: {total_stored}/{len(rows)} facts stored verbatim -> {output_csv}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
