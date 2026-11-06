# Five-event memory review

Reviewer: Codex, based on supplied logs. Independent teammate agreement has not been recorded. Selection: the three toy chunks and first/last SH chunks specified by the notebook. This is a deliberately selected diagnostic sample, not a random sample or a stale-memory-rate estimate.

Working labels: **correct insert**, **retention preserved**, **unmarked superseded fact**, **incomplete operation accepted**, and **recency missing**. An old semantic statement is flagged as unmarked superseded when the incoming numbered fact replaces the same relation, but the old statement remains asserted in present tense without historical qualification. This provisional rubric needs group agreement before quantitative annotation.

## 1. Synthetic chunk 0 — initial insert

[Evidence](evidence/run/synthetic_update/chunk_000.json). Input: `1. Ada lives in Paris.` Before: empty memory. After: semantic ID `902b` contains `Ada lives in Paris.` and episodic memory records the event; core memory is updated. Three calls execute without reported errors; output is not capped. **Label: correct insert.** There is no prior conflict or unrelated fact to test yet. No intermediate QA was run, so no intermediate answer is claimed.

## 2. Synthetic chunk 1 — unrelated fact retained

[Evidence](evidence/run/synthetic_update/chunk_001.json). Input: `2. Ben likes chess.` Before: Ada's Paris fact exists. After: Ben's chess fact is added as `746a`; Ada's semantic and episodic entries remain. Core memory is rewritten around Ben, so retention is demonstrated across the memory system, not in core alone. Three calls execute without reported errors; output is not capped. **Labels: correct insert; retention preserved.**

## 3. Synthetic chunk 2 — updated answer with stale entry retained

[Evidence](evidence/run/synthetic_update/chunk_002.json). Input: `3. Ada now lives in Rome.` The writer updates core, inserts semantic ID `e583` with the Rome fact and adds an episode. It does not update/delete semantic ID `902b`, which still says `Ada lives in Paris.` Ben's chess entry remains. Three calls execute without reported errors; output is not capped. **Labels: unmarked superseded fact; retention preserved.** Final reader answers are Rome and chess, both correct. The reader can resolve this simple answer despite the retained old semantic statement; this is not evidence of clean replacement.

## 4. Single-hop chunk 0 — incomplete tool call accepted

[Evidence](evidence/run/factconsolidation_sh_6k/chunk_000.json). Before: empty memory. The generation reaches 2,048 tokens and ends inside an insert argument: `{"memory_type": "semantic_memory", "content": "Urs`. The repaired call is reported successful and creates semantic ID `fe6a` containing only `Urs`. **Label: incomplete operation accepted.** There are 55 calls and zero reported tool errors, illustrating why these counts alone are insufficient. This row focuses on parser/truncation behavior, not a selected conflict or global retention assessment. The input also ends mid-fact at `72. Stephen Crane`; this is a separate chunk-boundary issue.

## 5. Single-hop chunk 6 — within-chunk conflict and truncated episode

[Evidence](evidence/run/factconsolidation_sh_6k/chunk_006.json). The incoming chunk contains fact 447 (`Roy Rogers is married to Dale Evans.`), then fact 452 (`Roy Rogers is married to John McVie.`). No Roy Rogers semantic entries are present before this chunk; after it, both statements are stored (`0d40` and `d33c`) without source serial numbers or an explicit historical label on the superseded statement. **Labels: unmarked superseded fact; recency missing.** This is a conflict within one input chunk, not a cross-chunk replacement. Unrelated-fact retention was not comprehensively assessed for this row. The response also reaches 2,048 tokens; its final episodic insert ends inside JSON and is repaired into a successful but incomplete summary (`362c`). **Additional label: incomplete operation accepted.** No selected pilot question directly queries Roy Rogers, so no corresponding QA outcome is claimed.

## What this review establishes

The pipeline can insert facts and preserve an unrelated toy fact, but these selected traces reveal retained conflicting statements and acceptance of incomplete operations. They motivate protocol repair and a larger, consistently annotated review. No population stale-memory percentage or causal claim about RL is supported by these five rows.
