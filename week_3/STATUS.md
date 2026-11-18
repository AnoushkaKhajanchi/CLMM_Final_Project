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

The fix lives in `scripts/protocol.py` and is copied into **all four** Week 3 notebooks. It repairs only that one typo; a note cut off mid-sentence is still rejected, so no half-facts are saved.

### 6. Tune the extension before running it (Dominick, this branch)
The extension code was already in Anoushka's framework. Two changes before we spend a GPU run on it:
- **Show related notes for every fact.** It used to show 6 notes per batch of ~16 facts, which included the old version of a changed fact only about 54% of the time. It now shows the 2 best-matching notes **per fact**: 151 of 152 on Week 2 memory, and 134 of 134 / 138 of 139 on Farah's run. The prompt gets longer but stays well under its limit.
- **Added an instruction-only run** (`memalpha_prompted`): the conflict instruction without the related notes. Comparing it with the full extension tells us whether *seeing* old notes or being *told to check* is what helps.

Also fixed: the fact-number counter missed tags at the end of a line and reported 0. Mem-α actually kept the number on 100% of lines.

---

## The runs, and what each one answers

All runs use the [same notebook](notebooks/CLMM_Week3_Integrated_Development_R2.ipynb), the same reader and the same 20 questions per set. Only the note-taker changes, through one setting:

| Run (`RUN_VARIANT`) | Note-taker | Question it answers |
|---|---|---|
| `qwen_baseline` | Plain Qwen, no memory training | How well does a regular model take notes? |
| `memalpha_baseline` | Mem-α as-is | Does Mem-α's training beat a regular model? |
| `memalpha_prompted` | Mem-α + "check for conflicts" instruction | Does telling it to check help? |
| `memalpha_retrieval` | Mem-α + instruction + related old notes shown | Does showing old notes fix outdated facts? (the extension) |

## What's next, in order

1. **Writer baseline** (Dominick): `qwen_baseline`.
2. **Rerun the Mem-α baseline** with the fix: `memalpha_baseline`. The first run lost facts.
3. **Run the extension:** `memalpha_prompted` and `memalpha_retrieval`.
4. **Compare** with the reader's scores plus the outdated-fact counter (`week_2/scripts/count_conflicts.py`), which doesn't depend on the reader.

Each run takes about an hour on Colab. Earlier runs (`locked_r2_01`, `parserfix_01`) used older code, so don't mix their results with the new `v3_01` runs.
