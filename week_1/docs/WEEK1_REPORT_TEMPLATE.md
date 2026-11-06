# Week 1 feasibility report

Date: ___  Group members: ___  Run name: ___

## Decision

Keep adapted 4B / Debug before proceeding / Propose 1.7B scope change: ___

Evidence supporting the decision (2-3 sentences): ___

## Environment

GPU and total GPU memory: ___
Writer / reader / embedding model: ___
Quantization and compute dtype: ___
Source commits, model/dataset revisions: attach `manifest.json`.
Environment: attach `hardware.json` and `pip-freeze.txt`.
Time spent by people: ___ hours. Approximate runtime used: ___ hours.

## Pipeline checks

- Direct memory-tool checks passed: ___
- All three synthetic chunks processed: ___
- Ada's final stored location; treatment of old location: ___
- Ben's unrelated preference preserved in memory and answered correctly: ___
- Supplied-fact reader controls: ___ / 4 exact matches.
- Complete SH and MH 6K contexts ingested without truncation: ___
- Saved checkpoints successfully inspected/reused: ___

## Pilot measurements

Copy numbers from `summary.csv`; leave missing values blank rather than guessing.

| Measurement | SH 6K | MH 6K |
|---|---:|---:|
| Chunks processed | | |
| Memory construction seconds | | |
| Peak writer allocated GPU GiB | | |
| Peak writer reserved GPU GiB | | |
| Memory tokens under reader tokenizer | | |
| Tool calls / tool errors | | |
| Chunks with no calls | | |
| Write responses hitting token limit | | |
| Stored-memory exact matches / questions | /5 | /5 |
| Stored-memory substring matches / questions | /5 | /5 |
| Full-context exact matches / questions | /5 | /5 |
| Stored-memory answering seconds | | |
| Answer responses hitting token limit | | |

These are pilot observations from one shared context per task, not robust benchmark estimates.

## Five-event review

Attach `manual_review_template.csv` with completed rows.
One trace explained in plain language (input -> operation -> memory -> answer): ___
One unresolved ambiguity: ___

## Compute projection

Planned writer conditions: ___
Contexts per condition: ___  Questions per context: ___  Repetitions: ___
Estimated hours = repetitions x conditions x sum over contexts of
(memory construction seconds + question count x seconds per question) / 3600.

Estimate: ___ GPU hours. Extra allowance for model loading, failures, reader controls and conflict-checking overhead: ___
Available Colab compute/runtime and practical scheduling constraints: ___

Do not multiply context-ingestion time by the question count. The notebook's illustrative estimate assumes three writer conditions with baseline-like speed; the extension may be slower.

## Protocol changes to document

Four-bit inference; Transformers backend; CPU MiniLM embeddings; local fixed Qwen reader; explicit core memory; project chunking and raw benchmark adapter; GPT-4.1-mini removed. Additional changes: ___

## Week 2 assignments

| Task | Owner | Due |
|---|---|---|
| Resolve remaining pipeline issues | | |
| Freeze evaluation/development protocol | | |
| Run matched Qwen3-4B and Mem-alpha baselines | | |
| Verify scoring manually on examples | | |
| Write experimental setup section | | |

Artifact location / output ZIP: ___
Executed notebook location: ___
TA scope discussion needed? If so, proposed change: ___
