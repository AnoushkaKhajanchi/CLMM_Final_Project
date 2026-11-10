# Week 2: Fixing the note-taking cutoff

A plain-English guide to what we're testing, what changed this week, what we found, and what's next. If you read only one file in this folder, read this one.

---

## 1. The project in one picture

Imagine two students:

- **Student 1, the note-taker**, reads a long list of facts a few at a time and writes notes.
- **Student 2, the test-taker**, never sees the original list. They answer questions using only Student 1's notes.

The catch: **some facts later get contradicted.** Early on the list says "Roy Rogers is married to Dale Evans"; later it says "Roy Rogers is married to John McVie." The newer fact is the correct one.

**Our question:** does the note-taker update its notes properly when a fact changes, or does it keep outdated information?

| In the picture | In the project |
|---|---|
| Note-taker | **Mem-α** (`YuWangX/Memalpha-4B`), a model trained with reinforcement learning to manage memory |
| Notes | **Memory**, the notes Mem-α saves |
| Test-taker | **Qwen3-4B**, a separate model that answers questions from memory |
| The list of facts | **FactConsolidation**, a test from the MemoryAgentBench benchmark |

---

## 2. Key terms

**Fact.** One numbered sentence in the test data, e.g. `447. Roy Rogers is married to Dale Evans.` The list has 455 facts (#0 to #454). **A higher number means newer.** When two facts contradict each other, the higher-numbered one is the truth.

**Chunk.** A group of facts given to the note-taker at once, like one page of a textbook. The full list is too long to read in one go, so it's split into chunks, and the note-taker processes them one at a time.
- *Week 1:* 7 chunks of about 70 facts each.
- *Week 2:* 28 chunks of about 16 facts each.

**Fact vs. chunk:** a fact is one sentence; a chunk is a batch of facts read together.

**Token.** The unit models use to measure text length, roughly ¾ of a word. Chunk sizes and limits are measured in tokens. 256 tokens is about 16 facts.

**Memory sections.** Mem-α's memory has three parts:
- *Core:* a short summary paragraph
- *Semantic:* individual facts, e.g. "Ada lives in Rome." **This is the part we check.**
- *Episodic:* a log of what happened, e.g. "The user gave me facts about sports."

**Memory operations.** After reading a chunk, the note-taker issues commands: *insert* (add a note), *update* (change a note), or *delete* (remove a note).

**Write limit / cutoff.** The note-taker's reply for each chunk has a maximum length of 2,048 tokens. If it runs out, it stops mid-sentence and the rest of that chunk is never saved. **This was Week 1's main problem.**

**Conflict.** Two facts about the same thing that disagree, e.g. #447 and #452 about Roy Rogers.

**Stale fact.** An old, replaced fact that is still in memory as if it were true.

**Single-hop vs. multi-hop questions.**
- *Single-hop* needs one fact: "Who is Roy Rogers married to?"
- *Multi-hop* chains several: "What music does Roy Rogers' spouse play?" (spouse → John McVie → rock).

**Full-text control.** We also give the test-taker the original fact list instead of memory. If it fails even then, the test-taker is the problem, not the notes.

**Exact match.** The scoring rule: the answer must match the correct answer exactly, ignoring case and punctuation.

---

## 3. How the pipeline works

```
455 facts ──split into──▶ chunks
                            │
         for each chunk:    ▼
    Mem-α reads it ──▶ issues memory operations ──▶ memory saved to a file
                            │
    after the last chunk:   ▼
    Qwen3-4B reads memory + a question ──▶ answer ──▶ scored right/wrong
```

This runs in a **Colab notebook** because it needs a GPU. Every step is saved as files, which we copy into this repo. Analysis scripts then read those files on a normal laptop.

**What's in a run folder** (e.g. `factconsolidation_sh_6k/`):
- `chunk_000.json`, `chunk_001.json`, … are one file per chunk. Each records the chunk's text, what the note-taker wrote, and memory before and after.
- `memory_final.json` is the memory after all chunks.
- `answer_*.json` files hold each question, the test-taker's answer, and whether it was right.

`sh` = single-hop questions, `mh` = multi-hop questions. **Both read the same 455 facts**; only the questions differ.

---

## 4. What we did this week, and what we found

### Step 1: Measured the Week 1 cutoff
[audit_lost_facts.py](scripts/audit_lost_facts.py) checks, for every fact, whether it reached memory. It only reads saved files; no GPU needed.

**Finding:** about 1 in 5 facts never reached memory (353/455 single-hop, 347/455 multi-hop). The missing facts were always **the last ones in each chunk**: the note-taker ran out of writing room before finishing.

### Step 2: Traced why each Week 1 question failed
[question_trace_v1.md](docs/question_trace_v1.md) follows each of the 10 test questions back to the facts it needed.

**Finding:** 4 of 10 questions were **impossible**, because a needed fact was lost to the cutoff. In 4 others, all the facts were in memory, but the test-taker still answered wrong.

### Step 3: Fixed the cutoff and reran
[Week2_Chunking_Fix.ipynb](notebooks/Week2_Chunking_Fix.ipynb) is the Week 1 notebook with these changes:
- **Smaller chunks:** 256 tokens (about 16 facts) instead of 1,024 (about 70).
- **No split facts:** chunks are cut only between facts. Week 1 sometimes cut a fact in half.
- **Same write limit (2,048),** which matches the original Mem-α code.
- Two small bug fixes: missing imports, and a reader input limit raised from 8,192 to 16,384 tokens because the fuller memory no longer fit.

Run once on an L4 GPU. Results are in [chunk256_results_v1.md](docs/chunk256_results_v1.md).

| | Week 1 | Week 2 |
|---|---:|---:|
| Replies cut off | 14 of 14 | **0 of 56** |
| Facts that reached memory | ~350 of 455 | **~450 of 455** |
| Accuracy, single-hop / multi-hop | 1/5, 0/5 | 2/5, 0/5 |

### Step 4: Counted every conflict
[count_conflicts.py](scripts/count_conflicts.py) finds all 161 conflicts in the facts and checks whether memory kept the old version, the new one, or both. Details are in [conflicts_v1.md](docs/conflicts_v1.md).

**Finding:** in Week 2, **160 of 161 conflicts kept the old fact** alongside the new one. Mem-α never removed an outdated fact; the one exception is a fact that was never saved at all.

### What this means
1. **The cutoff is fixed.** Notes are now nearly complete.
2. **Mem-α never removes old facts.** It made 552 inserts and **zero updates or deletes**. When a fact changes, the old and new versions both stay in memory.
3. **The test-taker is the weak link.** It often picks the old fact, and it scores just as badly when given the original list instead of memory.

### Surprises
- **Sometimes Mem-α pasted a whole chunk as one big note** instead of one note per fact. The audit now checks notes line by line to handle this.
- **The single-hop and multi-hop runs behaved differently from chunk 6 onward, despite reading identical facts.** GPU runs aren't perfectly repeatable, so be careful drawing conclusions from one run.

---

## 5. What's next

1. ~~Conflict counter~~ **Done:** stale rate 160/161. This is the number our extension needs to bring down.
2. **Improve the test-taker, in parallel.** Try better instructions or Qwen's "thinking" mode, checked against the full-text control.
3. **Build our extension.** Before saving a new fact, search memory for an older version and replace it. Measure it with the conflict counter.
4. **Run the final comparison.** Plain Qwen3-4B vs. Mem-α vs. Mem-α with our extension, all on the same settings.

**Team decisions needed:**
- Use the new chunk settings for every model we compare.
- Should saved notes keep their fact numbers? That's how the test-taker is supposed to tell which fact is newer.

---

## 6. How to rerun the notebook

1. Upload [Week2_Chunking_Fix.ipynb](notebooks/Week2_Chunking_Fix.ipynb) to Colab (**File → Upload notebook**) and pick a GPU (**Runtime → Change runtime type**).
2. Run the install cell, then **Runtime → Restart session**.
3. Run the remaining sections in order, one at a time. Section 7 (building memory) takes about 45–60 minutes on an L4.
4. Keep your computer awake. If you get disconnected, rerun the setup sections (2–6), then section 7, which resumes from saved chunks.
5. Section 10 downloads a ZIP. Check it with the audit script:
   ```bash
   python week_2/scripts/audit_lost_facts.py <unzipped run>/factconsolidation_sh_6k out.csv
   ```
6. **Change `RUN_NAME`** in section 2 whenever you change a setting, so earlier results aren't overwritten.

---

## 7. Where things are

| Path | What it is |
|---|---|
| `scripts/audit_lost_facts.py` | Checks which facts reached memory (laptop, no GPU) |
| `docs/question_trace_v1.md` | Why each Week 1 question failed |
| `docs/chunk256_results_v1.md` | Week 2 run results |
| `scripts/count_conflicts.py` | Counts conflicts and whether memory kept the old fact (laptop, no GPU) |
| `docs/conflicts_v1.md` | Conflict counter results |
| `results/conflicts_v1/` | One row per conflict, for each run |
| `notebooks/Week2_Chunking_Fix.ipynb` | Colab notebook with the chunking fix |
| `results/lost_facts_v1/` | Audit output for the Week 1 run |
| `results/week2_chunk256_01/` | The Week 2 run: original ZIP, extracted files, audit output |

The original Week 2 plan, written before this work, is in the [Week 1 handoff](../week_1/results/week1_closeout/WEEK2_HANDOFF.md). Week 1 files are unchanged.
