# Week 2 parallel handoff — three people

Owner labels A/B/C are placeholders because names were not provided. Each member selects one role. Target: three person-hours each, including a short shared check-in; unattended GPU runtime is separate.

| Owner | Work that can start immediately | Deliverable by midweek |
|---|---|---|
| A — pipeline and experiments | Preserve Week 1 as v1. Flag incomplete raw JSON before repair and separate rejected/incomplete calls from valid executions. Pilot smaller input chunks (256 tokens is a starting candidate), preferably preserving whole fact lines, and remeasure caps/runtime. | New notebook version, raw validity logs, small pilot summary and proposed matched settings. |
| B — memory analysis | Inspect about 10 development events using the archived inputs, calls and states. Include completed/capped outputs and both retained and missing facts. Refine the stale-memory and provenance rubric. | Annotated development examples, evidence links and a short list of failure categories. |
| C — reader and extension design | Give development questions only their correct numbered supporting facts. Test single-hop updates and multi-hop chains. Examine answer-cap and prompt effects one at a time. Design retrieval-before-write with an explicit provenance policy. | Reader diagnostic table and extension specification; no tuning on held-out answers. |

## Shared end-of-week gate

1. Review A's generation-cap and incomplete-call rates. Do not treat repaired fragments as valid writes. Record unresolved limitations explicitly; do not demand high accuracy as a software acceptance test.
2. Review C's supporting-fact controls. If the reader cannot solve controlled chains, diagnose it before interpreting multi-hop memory results.
3. Agree on source-order/provenance treatment, chunking, parser behavior, precision, embedding model, fixed reader, and scoring. Apply the same configuration to all compared writers.
4. Freeze the development/evaluation protocol. The Week 1 questions and traces are development evidence; do not tune on them and later describe them as untouched test data. Shared contexts create correlated questions and need an explicit limitation.
5. Only then launch matched Qwen3-4B and Mem-alpha baseline runs. Use a new run name, never overwrite v1. Start final tables and method writing while inference runs.

## Dependencies and handoffs

- A gives B all raw responses, before/after snapshots, errors, configuration and timing. B can begin with v1 immediately.
- B gives C the error rubric and development cases; C need not wait for new baseline runs to diagnose the reader.
- C gives A a frozen reader configuration and later a versioned extension. Person A coordinates main GPU runs; do not have two runtimes write the same output folder.
- All three review the protocol together at the end of the week. A owns setup/quantitative results writing, B owns error analysis/limitations, C owns extension-method writing.

## Deferred work

No retraining, 32K expansion or additional model families in Week 2. The extension's final evaluation waits for a reliable baseline protocol. The Week 1 evidence does not justify a smaller-model pivot solely for compute reasons.
