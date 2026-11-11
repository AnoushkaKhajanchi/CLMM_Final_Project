# Reader explicit-prompt v1: completed but unsuitable for comparisons

Original supplied archive is preserved unchanged as `original_run.zip`; its checksum and aggregate counts are in `summary.json`.

- Four basic controls: 0/4 exact match; 1/4 substring match.
- First control returned the correct Rome content with an added fact line and Answer label. The other controls returned source numbers (`1`, `2`, `2`) instead of chess, Rome and Oslo.
- Twenty single-hop and twenty multi-hop full-context development answers: 0/20 each on both reported metrics. No benchmark output caps occurred.
- Synthetic update with supporting facts returned the Rome fact line; synthetic chain with distractors returned the Lima fact line. Other synthetic variants returned numbers. These show both answer-format failures and unreliable behavior; the problem is not only strict exact-match scoring.

Sampling warnings are generated because the checkpoint supplies temperature/top-p/top-k presets while this notebook uses greedy decoding. They do not mean those presets sampled the answers, and switching to sampling is not the proposed fix.

The explicit prompt placed instructions inside the original template's question slot. This is a plausible contributor to source-number output, not a causal conclusion from one run. Revision v2 separates instructions, facts and the actual question, explicitly requests the factual value instead of its source ID, and gates benchmark execution on basic controls. The original-template option remains available as a controlled comparison.

Do not rescore numeric outputs by looking up the gold answer or reinterpret them as successful QA. Preserve this negative development result. Revision v2 needs a new GPU run; improvement is not yet demonstrated. This does not invalidate separate writer-diagnostic evidence.
