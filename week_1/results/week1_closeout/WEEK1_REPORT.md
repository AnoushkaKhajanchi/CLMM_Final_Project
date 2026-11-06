# Week 1 completion report

**Status: Week 1 feasibility and documentation complete; main evaluation requires Week 2 repairs.**

Run: `week1_memalpha_4bit_01`. Recorded run creation: 2026-11-06T18:37:11Z.
Team: three members; names not supplied. Review and closeout prepared by Codex from the supplied executed notebook and run archive. This is not a claim of independent teammate review.

## Decision

Retain the adapted, quantized Mem-alpha-4B project. The run completed on the assigned A100 without evidence of a GPU-memory capacity failure. Fix generated-output truncation and calibrate the reader before freezing the baseline comparison. No additional GPU run is required to close the feasibility week; the current accuracy is not a final experimental result.

## Environment and method

- GPU: NVIDIA A100-SXM4-40GB; 39.49 GiB total reported memory.
- Writer: `YuWangX/Memalpha-4B`; fixed reader: `Qwen/Qwen3-4B`.
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2` on CPU.
- Quantization: NF4 four-bit, double quantization, float16 compute; bitsandbytes 0.50.2 recorded in pip-freeze.
- Backend: Transformers; one LLM resident at a time; greedy generation with thinking disabled.
- Input chunks: 1,024 tokens; write response limit: 2,048; answer limit: 128; prompt-plus-output guard: 8,192.
- Data: original MemoryAgentBench Conflict_Resolution, SH 6K and MH 6K, first five questions each; full context ingested.
- Core, semantic and episodic memory enabled. Reader receives all stored memory for the primary condition. Full-original-context answers and four simple supporting-fact reader controls are recorded separately.
- All exact model/dataset revisions and code commits are preserved in [manifest.json](evidence/run/manifest.json); installed dependencies in [pip-freeze.txt](evidence/run/pip-freeze.txt).

This is an adapted baseline, not exact reproduction of the published system: four-bit precision, local embeddings and reader, a Transformers backend, explicit core memory, and custom chunking/raw-data adapter replace parts of the released setup. The paid GPT-4.1-mini baseline is removed. Apply the same adaptation to future compared writers.

## Completed checks

- Direct insert/update/search/delete and restore checks passed in the notebook.
- All three synthetic chunks completed; final answers for Ada and Ben were correct.
- Ben's preference remains in semantic memory after Ada's update. Ada's old Paris entry also remains alongside her new Rome entry, without an explicit historical marker on the old semantic fact.
- Four supplied-fact reader controls passed (4/4 exact match).
- Both benchmark source contexts were fully consumed: concatenated saved chunks equal the originals.
- Checkpoint state chains and final memory snapshots agree. Actual recovery after a Colab disconnect is not demonstrated by this run; local mocked recovery tests are documented separately.
- Both answer conditions completed and scoring was independently recalculated from saved predictions and aliases.
- Five update events reviewed in [MANUAL_REVIEW.md](MANUAL_REVIEW.md).
- The supplied notebook has 12 executed code cells and no saved error outputs. Its saved run name, hardware, completion messages and reported outcomes agree with the archive. It is retained unchanged as execution evidence; the maintained source notebook is a separate file.

## Measurements

| Measurement | Single-hop 6K | Multi-hop 6K |
|---|---:|---:|
| Chunks | 7.00 | 7.00 |
| Write seconds | 1039.90 | 1042.73 |
| Writer peak allocated GiB | 3.17 | 3.17 |
| Writer peak reserved GiB | 4.17 | 4.17 |
| Memory tokens (reader tokenizer) | 5986.00 | 6141.00 |
| Tool calls | 371.00 | 365.00 |
| Reported tool errors | 0.00 | 0.00 |
| Chunks with no calls | 0.00 | 0.00 |
| Write responses at output limit | 7.00 | 7.00 |
| Stored-memory answer seconds | 3.87 | 11.49 |
| Stored-memory exact match | 1/5 | 0/5 |
| Stored-memory substring match | 2/5 | 0/5 |
| Full-context exact match | 2/5 | 0/5 |
| Stored-memory answers at limit | 0/5 | 0/5 |
| Full-context answers at limit | 0/5 | 2/5 |

Both SH/MH rows share the same original context hash but have different questions. These are not two independent histories. Their separately generated memories differ. Ten pilot questions do not establish a reliable benchmark ranking.

## Findings and limitations

1. **Every benchmark write response hit the token limit (14/14).** Input ingestion completed, but generated memory operations were cut off.
2. **Reported zero tool errors is misleading.** The upstream repair function accepted incomplete JSON, including a semantic insert of the fragment `Urs`. Complete, meaningful operations must be distinguished from repaired fragments before main evaluation.
3. **The reader is a confound.** It scored 0/5 on multi-hop even with full original context; two such answers were capped. The four simple controls do not establish competence on difficult counterfactual chains.
4. **Recency information is lost in inspected semantic entries.** Source serial numbers are omitted while the reader's prompt asks it to use those numbers. A consistent provenance policy is needed across baselines.
5. **Correct QA can hide retained stale facts.** In the toy trace, Paris remains as a present-tense fact while Rome is added and answered correctly. Ben's unrelated fact is preserved.
6. **Operation pattern:** the benchmark runs contain 722 insert calls and 14 core updates; no semantic/episodic updates or deletes. This describes this capped pilot only, not general RL behavior.
7. **Chunk boundaries can split individual facts.** The first benchmark chunk ends mid-fact. Although no source characters are lost, the effect of this segmentation must be considered when revising chunking.

One unresolved attribution question is whether a missing updated fact reflects the response cap, the writer's selection policy, or both. Inspecting the raw generation and later memory state is necessary; a bad answer alone cannot decide the cause.

## Compute and effort

Benchmark memory construction took 34.71 minutes total. Summed logged chunk wall time plus question-generation time, including toy and reader controls, is 36.12 minutes. This is not total session/billing time: setup, downloads, some restoration overhead and other work are excluded. The executed notebook reports writer/reader loading at approximately 10.1/34.4 seconds for that execution.

Measured peak writer allocation was 3.17 GiB; reader generation reached about 4.00 GiB allocated. Reader controls show 8.32 GiB reserved. These measurements do not capture all possible initialization peaks and do not prove performance on a smaller GPU.

The notebook projects approximately 1.99 GPU-hours for three writer conditions, two builds per condition and 100 questions per build, at current speeds. This excludes repairs, additional repetitions and extension overhead. For scheduling only, reserve a provisional 3–4 GPU-hour window for that small matrix and re-estimate after the repairs; this is not a measured requirement or a guarantee of Colab availability. Available compute units and actual group person-hours were not supplied. The original Week 1 effort budget was nine combined person-hours.

## Handoff

The completed evidence bundle is indexed in [README.md](README.md). Three parallel assignments and acceptance criteria are in [WEEK2_HANDOFF.md](WEEK2_HANDOFF.md). No scope pivot to 1.7B is recommended on current compute evidence. The group should tell the TA that its implementation is open-source-only and quantized, with the paid baseline removed; no message has been sent on the group's behalf.
