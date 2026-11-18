# Week 3 status: where we are, in plain English (Nov 18)

**Short version:** the testing setup is now trustworthy. Everything so far has been baselines and making the measurements fair. **The extension, the heart of the project, hasn't been run yet.**

For the full Week 3 plan and protocol, see Anoushka's [README](README.md). This file tells the story so far.

---

## Our question
When a fact changes, does Mem-α's memory keep up?

Two models are involved, like two students:

| Name | Plain English | Model |
|---|---|---|
| **Writer** | The note-taker. Reads the facts in batches and saves notes. | Mem-α (or plain Qwen, for comparison) |
| **Reader** | The test-taker. Answers questions using only the notes. | Qwen3-4B |

---

## The story so far

### 1. Make sure facts get written down (Dominick, Week 2, merged)
The writer was running out of room, so about 1 in 5 facts was never saved. Smaller batches fixed it: about 450 of 455 facts are saved now.

### 2. Measure the actual question (Dominick, Week 2, merged)
Of 161 facts that change later, Mem-α kept the old version **as if it were still true** in 160. It never updated or deleted anything. This is the "before" number our extension has to improve.

**Keeping old facts isn't the problem**, since a question might ask about the past ("who was Roy married to before?"). The problem is that **nothing marks them as old**. A good result is "married to John McVie (previously Dale Evans)", not just deleting the old fact.

### 3. Build the shared testing setup (Anoushka, on `main`)
Anoushka built the Week 3 framework:
- the rules every run follows (same batches, same limits, keep fact numbers on every note)
- 20 practice questions per question set, with the rest held back for a final test
- three notebooks: reader tests, writer tests, and the full comparison
- **the extension code**: before writing, Mem-α is shown related old notes and told to check for conflicts
- helper scripts and tests

Her first reader test scored 0 of 20: the reader answered with fact numbers instead of answers. She revised the prompt.

### 4. Tune the reader and run Mem-α (Farah, ZIP shared today)
Farah:
- compared reader settings. A clearer prompt plus "thinking" mode and more room to answer reached **17 of 20** single-hop questions from the full fact list (multi-hop: 1 of 20).
- put the best reader settings into Anoushka's comparison notebook, with one switch to choose the writer ([notebook](notebooks/CLMM_Week3_Integrated_Development_R2.ipynb)).
- ran the **Mem-α baseline**: 11 of 20 from memory vs. 16 of 20 from the full fact list.

### 5. Fix lost notes in the pipeline (Dominick, this branch)
Mem-α sometimes saves a whole batch of facts as one big note and occasionally ends it with a one-character typo (`"]` instead of `"}`). The notebook threw the whole note away, so about 16 facts were lost each time. In Farah's run that was 7 of 28 batches, about 100 facts. It explains most of the 11 vs. 16 gap.

Think of a mail room that throws away any letter with a smudged envelope. Mem-α wrote the notes fine; the notebook discarded them. **We didn't change Mem-α. We fixed the mail room:** it now repairs the typo and logs it. On Farah's saved run, all 13 thrown-away notes (198 facts) are recovered.

The same strict check is in Anoushka's other notebooks and `scripts/protocol.py`, so they should get the same fix.

---

## What's next, in order

1. **Writer baseline** (Dominick): plain Qwen as the note-taker (`RUN_VARIANT = 'qwen_baseline'`). This tells us whether Mem-α's memory training helps at all.
2. **Rerun the Mem-α baseline** with the fix (`memalpha_baseline`), since the first run lost facts.
3. **Run the extension** (`memalpha_retrieval`). Two suggested tweaks first:
    - Show a few related notes **per fact**. It's currently 6 per batch of ~16 facts. On Week 2 memory, 6 per batch shows the old fact for 82 of 152 conflicts; 2–3 per fact shows it for about 151.
    - Add a run with **only** the conflict instruction (`prompted`), to tell whether seeing old notes or being told to check is what helps.
4. **Compare all three** with the same reader, plus the outdated-fact counter (`week_2/scripts/count_conflicts.py`), which doesn't depend on the reader.

Steps 1 and 2 use the same notebook with one setting changed.
