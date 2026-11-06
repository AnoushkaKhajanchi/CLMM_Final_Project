# Week 2 — Repair the pipeline and establish baselines

Status: planned; no experiment results or implementation claimed.

Read the [detailed three-person handoff](../week_1/results/week1_closeout/WEEK2_HANDOFF.md).

| Role | Parallel work | Deliverable |
|---|---|---|
| A — pipeline/experiments | Detect incomplete tool calls, pilot less truncation, preserve complete input facts, measure runtime | Corrected versioned notebook and pilot results |
| B — analysis | Inspect development traces, refine stale-memory and provenance labels | Evidence-linked annotations and error rubric |
| C — reader/extension | Test correct-supporting-fact controls, investigate answer caps, specify conflict checking | Reader diagnostic table and extension specification |

Target approximately three person-hours each, including coordination. By midweek review the pilot evidence; freeze matched settings before launching Qwen3-4B and Mem-alpha baselines. High accuracy is not a prerequisite, but uninterpretable truncation/reader failures need resolution. All compared writers must share parser, chunking, precision, embeddings, provenance treatment and reader settings.

Copy the maintained Week 1 notebook into this week's `notebooks/` when beginning implementation. No Week 2 code has been created yet.

## File locations

- `notebooks/`: GPU-dependent work and Colab experiments (`.ipynb`).
- `scripts/`: CPU-only utilities, if needed.
- `docs/`: protocol notes, reviews and report sections.
- `results/`: versioned configurations, compact logs, tables and figures.

Use a unique run folder for each configuration. Preserve earlier-week evidence and record changes explicitly. A/B/C are role labels until the group assigns names.
