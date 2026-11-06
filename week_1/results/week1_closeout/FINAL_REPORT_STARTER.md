# Do RL-trained memory agents forget correctly?

Working report outline for the adapted Mem-alpha conflict-resolution project. Week 1 observations below are pilot results; main experiments and extension findings remain future work.

## Research question

We investigate whether an RL-trained memory agent incorporates updated facts while preserving unrelated information, and whether an explicit conflict-checking step improves memory consistency. We distinguish the quality of stored memory from downstream question-answering accuracy.

## Related work — to develop

Discuss Mem-alpha's learned memory-management policy and MemoryAgentBench's FactConsolidation tasks. Explain the difference between preserving historical facts and representing superseded facts as currently valid. Verify the literature before making novelty claims.

## Experimental setup — established in Week 1

Our pilot uses Memalpha-4B as the memory writer and a fixed Qwen3-4B reader. Both use four-bit NF4 quantization with float16 computation; only one LLM is loaded at a time. Local MiniLM embeddings replace paid embeddings. The pilot consumes the complete single-hop and multi-hop 6K FactConsolidation context and answers the first five questions in each task. These tasks share the same source history. Core, semantic and episodic memory states, tool calls, raw outputs, timing and resource use are logged. Exact model revisions and settings accompany the evidence archive.

The planned comparison is Qwen3-4B without memory-specific RL, the adapted Mem-alpha baseline, and the adapted Mem-alpha system with conflict checking. Final settings will be frozen after the pilot issues are resolved. No training is planned.

## Pilot findings — not final baseline results

Both benchmark runs completed on an A100, taking approximately 17.3 minutes each for memory construction. Stored-memory exact match was 1/5 for single-hop and 0/5 for multi-hop. However, all 14 benchmark write responses hit the generation limit, and an incomplete JSON operation was repaired into a successful fragment insertion. The reader also scored 0/5 on multi-hop with the full original context. These confounds require repair and calibration before the main comparison.

A synthetic update preserved both the superseded Paris fact and the new Rome fact while producing the correct Rome answer. This motivates separate memory-content diagnostics and answer metrics.

## Main results — future work

Report matched writer comparisons, single-hop and multi-hop results separately, accepted-alias scoring, denominators, and runtime. Record final development/evaluation selection and avoid presenting pilot data as untouched held-out results.

## Memory error analysis — future work

Define active stale-memory annotation, distinguish missing facts from retained conflicts and reader failures, and explain event selection. Use evidence-linked traces and report ambiguity rather than inferring causes solely from wrong answers.

## Conflict-checking extension — future work

Describe retrieval before writing, the replacement/coexistence decision, provenance handling, and added inference cost. Compare against the same baseline protocol.

## Limitations and reproducibility

Discuss quantization, the adapted embedding/reader stack, correlated questions from shared contexts, small samples, reader capability, generation limits and possible loss of source serial numbers. Provide code/configuration revisions and instructions for replaying the final runs. Do not claim a clean effect of RL from unmatched model or inference conditions.
