# Week 1 results review

Source: `/Users/anoushkakhajanchi/Downloads/week1_memalpha_4bit_01.zip`.
Reviewed the supplied archive read-only; no experiment was rerun. The original archive was not modified.

## Decision

Keep the adapted, quantized 4B project for now. Feasibility is demonstrated on the assigned A100; the main experiment protocol is not ready to freeze. Fix output truncation and evaluate the reader before scaling up. There is no compute-based reason in this run to pivot to 1.7B.

## Verified completion and compute

- Both published contexts were ingested in full. Rejoining the saved chunks exactly reproduces each source context.
- Saved before/after memory states form consistent chains, and final snapshots match the last checkpoint.
- Synthetic tool/reader pipeline completed; supplied-fact reader controls scored 4/4 exact matches.
- Hardware: NVIDIA A100-SXM4-40GB, 39.49 GiB reported capacity; bitsandbytes 0.50.2.
- Single-hop memory construction: 1,039.90 seconds (17.33 minutes).
- Multi-hop memory construction: 1,042.73 seconds (17.38 minutes).
- Combined benchmark memory construction: 34.71 minutes, excluding downloads and model loading.
- Maximum logged writer allocated memory: 3.17 GiB; reader generation reached about 4.00 GiB allocated. The reader-control records show 8.32 GiB reserved. Allocated and reserved memory are different measurements; neither proves the peak during model loading.
- The two SH/MH rows have identical original context SHA-256 hashes and different questions. They are not independent memory histories. The two construction outputs differ, so do not assume these are identical repeated memory states.

## Pilot accuracy

| Task | Stored-memory exact match | Stored-memory substring match | Full-context exact match |
|---|---:|---:|---:|
| Synthetic | 2/2 | 2/2 | 2/2 |
| Single-hop | 1/5 | 2/5 | 2/5 |
| Multi-hop | 0/5 | 0/5 | 0/5 |

These are development/smoke observations, not reliable benchmark estimates. Single-hop substring scoring credits “The author of The Fairly OddParents.” although strict exact match does not. This is a formatting difference, not necessarily a wrong factual answer.

## Findings that affect validity

1. All 14 benchmark write responses reached the 2,048-token limit. At least some visibly end inside a JSON tool argument. The source contexts were not truncated; the model's generated memory operations were.
2. Zero reported tool errors is misleading. The upstream parser's JSON repair turned an incomplete final insert into a successful insertion of the fragment `Urs` in the first chunk of both benchmark runs. The notebook inherited this repair behavior, so its successful-call count is not a valid measure of complete, meaningful operations.
3. Across the benchmark runs, there were 722 insert calls and 14 update calls. All 14 updates targeted core memory; there were no semantic/episodic updates or deletes. This is a useful descriptive observation, not yet a general claim about the RL policy.
4. The writer drops source fact serial numbers in the inspected semantic entries. The reader's conflict prompt relies on those numbers to determine recency. Random memory IDs are not source timestamps. Freeze a deliberate provenance policy before comparing conditions, and apply any change equally to every writer baseline.
5. The reader fails all five multi-hop full-context controls; two of those responses also hit the 128-token answer cap. A low multi-hop stored-memory score cannot be interpreted as a pure memory failure.

## Concrete memory observations

- Synthetic final memory contains both `Ada lives in Paris.` and `Ada now lives in Rome.` The former is not explicitly marked historical. Ben's chess preference remains, and both final answers are correct. This illustrates how correct QA can coexist with potentially stale active memory.
- Single-hop original facts 223 and 310 associate goaltender with ice hockey and then pesäpallo. Both remain in semantic memory without their serial numbers; the reader answers ice hockey.
- Single-hop original facts 100 and 186 place rugby union's creation in England and then India. The inspected final semantic memory contains England but not the India statement. This is evidence of missing updated information in that memory component; inspect the full trace/core/episodic state before attributing the precise cause.
- Joan Didion's education fact is missing from inspected semantic memory. The full-context reader answers it correctly, while the stored-memory reader gives Bowdoin College. Again, check all memory components before concluding where the information was lost.

## Week 2: three people working in parallel

Allocate about three person-hours each, including coordination; unattended compute is separate.

**Person A — Repair the evaluation harness.** Preserve this run as v1. Create a new protocol/run directory. Detect incomplete raw JSON before repair; log rejected incomplete calls separately, preserving the raw output. Test a smaller input chunk size (e.g. 256 tokens) at the existing write limit on development material, then a full 6K context. Measure response-cap frequency, memory size and runtime. This is a pilot setting, not a guaranteed solution. Keep the eventual parser and chunking identical across compared writers.

**Person B — Trace memory errors and define annotations.** Review about 10 events spanning complete and truncated responses, including the examples above. Distinguish input missing, generated operation cut off, conflicting facts retained, recency information lost, and reader failure. Write the active-stale-memory rubric. Do not use this selected sample to estimate population rates.

**Person C — Calibrate the reader and specify the extension.** On development questions, supply only the correct numbered supporting facts and test the reader's ability to follow counterfactual updates and multi-hop chains. Test a larger answer cap separately from prompt changes. Compare supporting-fact, full-context, and stored-memory conditions. Specify how retrieval-before-write will access provenance, but postpone extension tuning on final evaluation answers.

Meet after these investigations to freeze the matched baseline settings. Re-run Qwen3-4B and Mem-alpha under that common protocol. If writer outputs are still universally capped or the reader cannot solve controlled supporting-fact questions, continue debugging before launching the main matrix.

## Compute projection caveat

The notebook's approximately 1.99 GPU-hour projection uses the current baseline timing for three conditions, two context builds per condition, and 100 questions per context. It excludes model loading, retries, changed chunking, repeated runs and conflict-check overhead. Recalculate after repairs. Because the two source contexts are identical, future evaluation may construct one shared memory per writer/run and answer SH/MH questions separately, if that reuse is documented consistently. Do not silently mix the two existing memories.
