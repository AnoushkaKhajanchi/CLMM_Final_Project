# Week 3 — writer diagnosis, reader calibration and conflict checking

**Implementation ready; GPU experiments and result-based decisions pending.** No Week 3 accuracy, retention improvement, or completion of GPU evaluation is claimed. No paid model APIs are used. Week 2 evidence is unchanged.

## Agreed protocol

- 256-token, whole-fact chunking; 2,048-token write budget; 16,384 prompt-plus-output guard recorded directly in manifests.
- Same instruction for all writers: preserve original numbers as `[source_fact_id=N]` on each fact line. Record chunk indices automatically. Do not use operation time as fact freshness or repair missing source numbers using gold answers.
- Synthetic development cases plus a saved 20-question development / 80-question reserved split per task. [Split file](docs/question_split.json).
- **Exposure uncertainty:** the team cannot confirm which questions were previously inspected. The reserved set is NOT certified untouched. It shares the already inspected history. Disclose this or identify a genuinely unexposed evaluation set before making a held-out claim. These notebooks evaluate only development questions.
- New run names for new settings. Week 1 and Week 2 results remain historical evidence.

## Run order and three-person ownership

### Person A: reader diagnostics, then matched baselines

Upload [Reader diagnostics](notebooks/Week3_reader_diagnostics.ipynb) to Colab. Select a GPU, install, restart, then continue from configuration. Run the default explicit-prompt, non-thinking, 512-answer-token candidate. Use a new run name to compare `READER_STYLE='original'` at the same budget. Both runs use synthetic supporting facts/distractors and 20 development questions per benchmark task with full original context.

Thinking is optional: use `READER_THINKING=True`, a new run name, and a suitable larger answer budget (e.g. 1,024 for a bounded pilot). Missing final answers and output caps must count as failures/limitations, not be discarded. Change one factor at a time. Stop expanding the search if it consumes the week's effort budget.

After reviewing these results, select ONE reader configuration for all development comparisons. A weak reader does not prevent studying memory consistency, but it limits QA claims.

### Person B: memory evaluation

Review the writer-diagnostic traces and about 15–20 representative development events. Use the [annotation guide](docs/ANNOTATION_GUIDE.md). Run the CPU audit on final memories:

```bash
python week_3/scripts/audit_memory.py /path/to/run/factconsolidation_sh_6k > /tmp/sh_audit.json
python week_3/scripts/summarize_run.py /path/to/run > /tmp/run_summary.json
```

These tools are review aids. They distinguish old-fact presence, latest-fact retention, non-conflicting relation retention and provenance formatting. Exact-wording matches cannot establish semantic absence or historical status. Inspect core/episodic memory manually where it matters.

### Person C: controlled writer tests and extension

Upload [Writer diagnostics](notebooks/Week3_writer_diagnostics.ipynb). It runs six synthetic cases under baseline, explicit conflict instructions, and retrieval plus those instructions (18 short tests). Cases include visible/hidden conflict, multi-fact note, duplicate, coexistence and an older fact arriving later.

Use these traces to decide whether the extension works as intended. The hidden case seeds the old fact outside the five recent semantic entries. Retrieved candidates include complete note contents and real memory IDs; the prompt requires preservation of unrelated lines. Text-presence summary flags need human review.

The implemented extension performs lexical-overlap retrieval over existing semantic/episodic notes before each chunk's writer generation, then asks the writer to choose replacement or coexistence. It does not use gold conflict pairs, answers, future facts, or a forced last-write-wins rule. Top six complete entries are offered. This is a simple candidate implementation, not a proven improvement. Whole-chunk notes can dominate retrieval; inspect candidate quality and do not delete unrelated content.

### Shared: development comparison after the diagnostics

Run [Development evaluation](notebooks/Week3_development_evaluation.ipynb) separately for:

| Run label | WRITER_ID | CONDITION |
|---|---|---|
| qwen_baseline | Qwen/Qwen3-4B | baseline |
| memalpha_baseline | YuWangX/Memalpha-4B | baseline |
| memalpha_retrieval | YuWangX/Memalpha-4B | retrieval |

Set the chosen reader style/thinking/budget identically in all three. Use unique RUN_NAME values. All three use provenance instructions and strict parsing. The extension adds conflict instructions and retrieval; the synthetic prompted condition helps explain which part matters. A prompt-only benchmark ablation is optional if time allows.

The notebook constructs each full history, then answers only its 20 development questions in stored-memory and full-context conditions. SH/MH share the source history but retain separately built states here for continuity; they are not independent histories. GPU nondeterminism means a single run is exploratory. Record differences, do not silently choose the best run.

## What is implemented

- Three self-contained GPU notebooks; the CPU protocol module is embedded so uploading a notebook alone works.
- Strict JSON validation before upstream tool execution. Incomplete calls are rejected and logged; failed tools roll back individual changes.
- Provenance instructions, per-chunk logs, retrieved notes, raw generations, errors, caps, latency and GPU usage.
- Pinned Week 2 model/data revisions, settings hashes, checkpoint resume, local embeddings and blocked paid clients.
- CPU audits and regression tests. Run `python -m unittest discover -s week_3/tests -v` from the repository root.

No synthetic success thresholds are hardcoded as evidence of semantic correctness. No final-evaluation runner is included: the method and reader must be frozen first.

## Week 3 completion checklist

- [x] Agreed protocol implemented and candidate question split saved.
- [x] Writer tests, reader tests and extension implemented.
- [x] CPU checks and notebook syntax validated locally.
- [ ] Run writer diagnostics and review the 18 traces.
- [ ] Run reader diagnostics; record one selected reader configuration and its limitations.
- [ ] Run matched development comparisons and audit their saved memories.
- [ ] Review representative conflicts, provenance and unrelated-fact retention.
- [ ] Complete the [decision record](docs/DECISION_RECORD.md), freeze the extension for Week 4, and disclose/resolve evaluation exposure uncertainty.

Upload the exported ZIPs for analysis. The GPU-dependent portion cannot be completed from the local CPU environment. Plan roughly 3–4 person-hours each, with inference running separately; prioritize diagnosis and a valid comparison over 32K or model-family expansion.
