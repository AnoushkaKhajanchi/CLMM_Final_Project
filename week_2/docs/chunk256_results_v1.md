# Chunking fix: results of run `week2_memalpha_4bit_chunk256_01`

Same pipeline as Week 1 except: 256-token chunks cut on whole fact lines (was 1,024 tokens, cut anywhere), and the reader's input+output guard raised from 8,192 to 16,384 tokens (see `settings_override.json`). Run on an **NVIDIA L4** (Week 1: A100), so runtimes are not directly comparable. Evidence: [evidence/](../results/week2_chunk256_01/evidence/) (original ZIP plus extracted files).

## Result

| | Week 1 (1,024-token chunks) | Week 2 (256-token chunks) |
|---|---:|---:|
| Write responses cut off | 14/14 | **0/56** |
| Facts that reached memory, SH | 353/455 | **452/455** |
| Facts that reached memory, MH | 347/455 | **449/455** |
| Stored-memory exact match, SH / MH | 1/5, 0/5 | 2/5, 0/5 |
| Full-text reader control, SH / MH | 2/5, 0/5 | 2/5, 0/5 |
| Write time, SH / MH (seconds) | 1,040 / 1,043 (A100) | 1,176 / 1,545 (L4) |

Fact counts come from [audit_lost_facts.py](../scripts/audit_lost_facts.py); per-fact CSVs are in [week2_chunk256_01/](../results/week2_chunk256_01/).

## What this shows

1. **The cutoff is fixed.** Almost every fact now reaches memory. The few still missing (SH: #51, #97, #363) are scattered, not end-of-chunk blocks.
2. **Mem-α never replaces an old fact.** Across both runs it made 552 semantic inserts and **zero semantic updates or deletes**. Every conflicting fact is now stored alongside the one it supersedes. That bears directly on research question 1. The conflict finder (next step) will measure this per conflict.
3. **The reader is now the bottleneck.** With memory nearly complete, stored-memory accuracy equals the full-text control (2/5 SH, 0/5 MH). Even with the original numbered facts in front of it, Qwen3-4B does not reliably pick the highest-numbered fact. For example, it answered "ice hockey" (#223) instead of "pesäpallo" (#310) in both conditions.
4. **One Week 1 failure is now fixed.** Joan Didion (SH-Q4) was unanswerable in Week 1 because the fact was lost to the cutoff. It is now correct.

## New behavior to know about

- **Sometimes the writer copies a whole chunk into one note.** In 19/28 SH chunks and 5/28 MH chunks, it saved all ~16 facts as a single semantic entry, with fact numbers kept, instead of one note per fact. The audit was updated to check notes line by line.
- **SH and MH diverged despite identical input.** The two runs read the same 455 facts but behaved differently from chunk 6 onward. Greedy decoding is not perfectly repeatable on GPU, so memory construction varies between runs. Treat single-run numbers with care.

## Decisions for the team

1. **Adopt 256-token, whole-fact chunking** (and the 16,384 guard) as the frozen setting for all compared writers.
2. **Fix or replace the reader before comparing writers.** Otherwise every writer will look equally bad. Options to test on the full-text control: enable Qwen3-4B's thinking mode, revise the prompt, or use a stronger open model.
3. **Provenance policy:** decide whether stored notes must keep fact numbers. Block notes keep them, per-fact notes do not, and the reader needs them to resolve conflicts.

Caveat: 10 questions, one run. These are pipeline diagnostics, not benchmark results.
