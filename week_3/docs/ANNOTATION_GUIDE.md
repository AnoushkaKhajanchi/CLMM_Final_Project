# Development memory review

For each selected event record run/case, chunk index, source numbers, memory IDs, before/after state, operation, error/cap status and a short justification. Select successes and failures, separate notes and block notes, and visible/hidden conflicts. This selection is diagnostic, not a representative stale-rate estimate.

Labels:
- Correct replacement: newest valid fact present; superseded assertion removed or explicitly marked historical.
- Unmarked stale fact: old conflicting statement still presented as current.
- Updated fact lost: required new fact absent after review, not merely missed by exact matching.
- Unrelated loss: an unrelated valid fact disappears during the operation.
- Valid coexistence: new information does not supersede the same relation; both should remain.
- Provenance issue: number absent, invented, wrong, or refreshed merely because an old note was copied.
- Retrieval miss: relevant old entry not among candidates. Separate this from the writer ignoring a correctly retrieved entry.
- Invalid/capped operation: raw output malformed, incomplete, rejected, or response budget exhausted.
- Uncertain: paraphrase, historical wording or ambiguous semantics prevent a confident label.

Check all relevant memory components before claiming information is unavailable to the reader. The automated audit measures final semantic memory only. Review the source text alongside IDs: valid-looking markers do not guarantee correct attribution.

For the duplicate case, check duplicate count as well as text presence. For the coexistence case, both hobbies should remain. For the late-arriving-old-fact case, an explicitly historical Paris statement is acceptable; Rome must remain current. For block-note updates, verify every unrelated line survives, not just the one sampled retention phrase.

A reduction in old-fact presence is useful only alongside latest-fact retention and unrelated-fact retention. Deleting all memory is not an improvement. Report exact counts and denominators, distinguish selected-event annotations from whole-history proxies, and do not infer an RL effect without the matched Qwen writer baseline.
