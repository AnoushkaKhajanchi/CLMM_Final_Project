# Week 1: prove the project is feasible

**Budget: 9 combined person-hours, plus unattended download/inference time.**
The goal is a working, inspectable pilot and a measured compute decision. It is not a complete baseline comparison or a new conflict-resolution method.

## Task allocation

| Task | Person-hours | Owner | Done when |
|---|---:|---|---|
| Agree on roles and reduced scope | 0.5 | Whole group | Owners named; no paid APIs; 6K first; no retraining |
| Colab setup and direct memory-tool checks | 2.0 | Setup owner | GPU recorded; installs/imports succeed; tool checks pass |
| Inspect data, prompts, and evaluation | 1.5 | Evaluation owner | Explain serial-number precedence, SH/MH distinction, aliases, and scoring |
| Run pilot and collect timing/memory | 2.0 | Run owner | Toy + two complete 6K contexts, five questions per benchmark context, controls and ZIP saved |
| Inspect five update events | 1.5 | Analysis owner | Before/after states and tool calls reviewed in CSV |
| Write findings and choose Week 2 scope | 1.5 | Report owner, group review | Completed report and explicit keep/debug/pivot decision |
| **Total** | **9.0** | | |

Owners can be the same person. Count a 15-minute four-person meeting as one person-hour. Read/analyze/write while the single GPU job runs; do not have several people modify the same run directory.

## Suggested order

**Session 1:** upload the notebook, choose a GPU, run setup and CPU tool checks. Read upstream `memory.py`, `functions.py`, and the writer's prompt-formatting function together with the notebook's adaptations. Confirm that a tool can insert, update, search, and delete a memory.

**Session 2:** run the Mem-alpha writer. Inspect the three synthetic chunks before drawing conclusions from benchmark results. Both 6K contexts must be consumed in full, in original order. Reducing the number of questions does not reduce the cost of building each context's memory.

**Session 3:** unload the writer, run the fixed Qwen3-4B reader, inspect its controls, and export the evidence. Complete five manual-review rows and the short report.

## What the package runs

- Writer: `YuWangX/Memalpha-4B`, NF4 4-bit, one sequence at a time, thinking disabled.
- Reader: `Qwen/Qwen3-4B`, same loading approach, run only after releasing the writer.
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`, CPU, local window pooling for long entries.
- Data: original `ai-hyz/MemoryAgentBench`, `Conflict_Resolution`; `factconsolidation_sh_6k` and `factconsolidation_mh_6k`.
- Main pilot: full context ingestion, then the first five questions from each context using only stored memory.
- Controls: a synthetic fact update and unrelated fact, four supplied-fact reader questions, and the same pilot questions with full context supplied directly.
- Scoring: upstream normalized exact match and substring exact match, taking the best accepted alias. Keep single-hop and multi-hop separate.

The chosen source rows and their exact hashes are saved. The pilot is development data. Do not use it to tune a conflict-checking method and then report it as a held-out evaluation. Questions from one shared context are correlated; the ten questions are not ten independent memory-construction trials. Before Week 2, define a practical development/test protocol and describe the shared-context limitation honestly.

## Evidence to keep

Keep the output ZIP, the executed notebook, a completed report, and the five-row review CSV. The ZIP contains:

- `manifest.json`: settings, source commits, model revisions, dataset revision.
- `hardware.json` and `pip-freeze.txt`: actual environment.
- `selected_examples.json`: exact benchmark data and question indices.
- `tool_checks.json`: direct infrastructure checks.
- Per-example `chunk_*.json`: input, rendered prompt, output, operations, timing, memory before/after.
- Per-example `memory_final.json` and `answer_*.json`: final memory and scored predictions.
- `reader_controls.json`, `summary.csv`, and `completion.json`.

Generation timings exclude downloads/model loads; write timings include generation and tools but not all startup/resume costs. Peak allocated/reserved GPU memory is recorded for each generation, not every possible initialization peak. Use Colab's GPU monitor as an additional observation. If loading fails, record that failure separately.

## Manual review: five events

Review all three synthetic events plus the first and last single-hop benchmark chunks. The last two are pipeline samples, not guaranteed conflict events. If one is not a conflict, mark it as such. You may replace it with a clearly identified conflict event, recording the selection reason.

For each: locate the incoming fact, inspect the model's proposed operation, read its execution result, and compare before/after memory. Distinguish:

- Correct insert/update; old fact retained only as explicitly historical information.
- Old fact still presented as current, duplicate incompatible facts, or unrelated fact deleted.
- No operation, tool argument/execution error, or output truncated at its token limit.
- Insufficient evidence to attribute the failure.

Do not infer “active stale-memory rate” from these five deliberately selected events. Define an annotation rubric and denominator before measuring it in Week 3. Presence of an old fact alone is not necessarily an error: history can be valid when clearly marked as history.

## Decision for Week 2

**Keep the adapted 4B design** if it completes the full contexts within available runtime, checkpoints work, and you can diagnose the logs. Low accuracy alone does not mean the project is infeasible.

**Debug first** if the writer makes no valid calls, hits the output limit repeatedly, or the reader fails simple supplied-fact controls. These issues can make the comparison uninterpretable. Allocate a bounded troubleshooting session; do not spend the entire project on environment repair.

**Propose a 1.7B scope change to the TA** if repeated clean-runtime 4B attempts fail or measured runtime exceeds your available compute. Qwen3-1.7B is not a smaller RL-trained Mem-alpha. The revised question would be whether conflict checking improves updates in small prompted memory agents. Use a new run name when changing models/configuration. If doing a wholly smaller-model feasibility run, change both writer and reader to Qwen3-1.7B and clearly label it separately.

For the retained project, the later comparison should be Qwen3-4B without memory-specific RL, adapted Mem-alpha-4B, and adapted Mem-alpha with conflict checking. Keep precision, embeddings, memory architecture, reader, chunking and data fixed. Remove GPT-4.1-mini from the proposal. Quantization can change behavior, so conclusions apply to the quantized setup; do not claim it isolates RL alone perfectly.

## Troubleshooting

| Symptom | Action |
|---|---|
| No GPU detected | Select GPU runtime and reconnect. |
| Import/version error after installation | Restart the session, resume at configuration; retain the traceback. |
| Missing `libbitsandbytes_cuda130.so` / CUDA version mismatch | Use the updated notebook with bitsandbytes 0.50.2. Update the old installation pin too, install, restart the session, then rerun from step 2. The new step 3 tests NF4 kernels before model loading. |
| Out of memory | Restart; ensure only one LLM is loaded. Record the failing cell and GPU. Do not silently truncate context. |
| Colab disconnects | Reconnect and rerun setup. Same run name/settings reuse saved chunks/questions. |
| Time-budget exception | Completed chunks/questions are saved. Rerun that stage when ready. |
| Authentication requested for a paid model API | Stop: this workflow needs no paid API key. Verify you are running this notebook. |
| No tool calls or many capped responses | Inspect exact rendered prompts and raw outputs; treat this as a writer/parser issue until understood. |
| Full-context reader succeeds but stored-memory reader fails | Inspect stored memory; this is evidence consistent with memory loss, not proof of a particular failure cause. |
| Both reader conditions fail | Inspect reader capability, prompt and scoring before blaming memory updates. |

## Minimal report outline for the final project

Create a shared report now with headings: research question; related work; experimental setup; baseline results; update-error analysis; conflict-checking extension; limitations; reproducibility. This week's completed template supplies the experimental-setup and feasibility notes. No extension implementation is needed this week.

## Sources

- https://github.com/wangyu-ustc/Mem-alpha
- https://huggingface.co/YuWangX/Memalpha-4B
- https://github.com/HUST-AI-HYZ/MemoryAgentBench
- https://huggingface.co/datasets/ai-hyz/MemoryAgentBench
- https://huggingface.co/Qwen/Qwen3-4B
- https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
- https://huggingface.co/docs/transformers/quantization/bitsandbytes
- https://research.google.com/colaboratory/faq.html
