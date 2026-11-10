# Week 2 — Repair the pipeline and establish baselines

Status: planned; no experiment results or implementation claimed.

Read the [detailed three-person handoff](../week_1/results/week1_closeout/WEEK2_HANDOFF.md).

| Role | Parallel work | Deliverable |
|---|---|---|
| A — pipeline/experiments | Detect incomplete tool calls, pilot less truncation, preserve complete input facts, measure runtime | Corrected versioned notebook and pilot results |
| B — analysis | Inspect development traces, refine stale-memory and provenance labels | Evidence-linked annotations and error rubric |
| C — reader/extension | Test correct-supporting-fact controls, investigate answer caps, specify conflict checking | Reader diagnostic table and extension specification |

Target approximately three person-hours each, including coordination. By midweek review the pilot evidence; freeze matched settings before launching Qwen3-4B and Mem-alpha baselines. High accuracy is not a prerequisite, but uninterpretable truncation/reader failures need resolution. All compared writers must share parser, chunking, precision, embeddings, provenance treatment and reader settings.

## Week 2 work so far

- [Lost-facts audit](scripts/audit_lost_facts.py) and its [Week 1 results](results/lost_facts_v1/): about 22% of input facts never reached memory because of the write cutoff.
- [Question trace](docs/question_trace_v1.md): 4/10 pilot questions were unanswerable from memory due to the cutoff.
- [Chunking-fix notebook](notebooks/Week2_Chunking_Fix.ipynb): the Week 1 notebook with 256-token chunks cut on whole facts. Run once on an L4: see [chunking-fix results](docs/chunk256_results_v1.md).

## File locations

- `notebooks/`: GPU-dependent work and Colab experiments (`.ipynb`).
- `scripts/`: CPU-only utilities, if needed.
- `docs/`: protocol notes, reviews and report sections.
- `results/`: versioned configurations, compact logs, tables and figures.

Use a unique run folder for each configuration. Preserve earlier-week evidence and record changes explicitly. A/B/C are role labels until the group assigns names.
