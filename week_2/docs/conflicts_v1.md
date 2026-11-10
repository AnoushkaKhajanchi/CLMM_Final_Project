# Does Mem-α remove outdated facts? (conflict counter, v1)

[count_conflicts.py](../scripts/count_conflicts.py) finds every conflict in the 455 input facts: two facts with the same subject and relation but different answers, where the higher-numbered fact is the correct one. It then checks the final semantic memory. It reads saved files only. Per-conflict CSVs are in [results/conflicts_v1/](../results/conflicts_v1/).

Example conflict: #447 "Roy Rogers is married to Dale Evans" → #452 "Roy Rogers is married to John McVie".

## Result

The input contains **161 conflicts**, each an old/new pair. Both runs read the same facts.

| Outcome in final memory | Week 1 SH | Week 1 MH | Week 2 SH | Week 2 MH |
|---|---:|---:|---:|---:|
| Only new (old removed) | 30 | 27 | 1 | 0 |
| **Both kept (stale)** | 96 | 95 | **159** | **159** |
| Only old (update missing) | 25 | 26 | 1 | 1 |
| Neither | 10 | 13 | 0 | 1 |
| **Stale rate** (old fact still present) | 121/161 | 121/161 | **160/161** | **160/161** |

## What this means

- **Mem-α never removed an outdated fact.** In Week 2, every case that isn't "both kept" involves a fact that never reached memory at all (#51, #97, #208 in the [lost-facts audit](../results/week2_chunk256_01/)). None is a replacement.
- **Week 1's "only new" cases weren't replacements either.** Week 1 had zero semantic updates or deletes, so those 30 cases are old facts that were lost to the write cutoff. Once the cutoff was fixed, they turned into "both kept." Fixing the pipeline made the stale rate look worse because it made the measurement honest.
- **For research question 1:** in our adapted setup, Mem-α treats memory as append-only. It stores the new fact but leaves the outdated one asserted as current, with nothing marking it as old. Correct answers then depend entirely on the reader working out which fact is newer, which [it often fails to do](chunk256_results_v1.md).
- **This is the baseline our extension must beat.** A check-before-write step should move conflicts from "both kept" to "only new" without deleting non-conflicting facts.

## Limits

- Matching uses exact wording, ignoring case, numbering and stray quotes. A reworded old fact (e.g. "formerly lived in Paris") would count as removed. Mem-α made no updates in these runs, so this did not occur.
- Conflict detection splits each fact at a known relation phrase (e.g. "is married to") or at the last " is ". All 455 facts matched a pattern; sampled pairs were checked by hand.
- One run per condition. Week 2 ran on an L4, Week 1 on an A100.
