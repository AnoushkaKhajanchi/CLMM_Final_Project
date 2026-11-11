# Why did the Week 1 pilot get its 10 questions wrong?

Each of the 10 pilot questions is traced back to the facts needed to answer it. Using [the lost-facts audit](../results/lost_facts_v1/), we check whether each needed fact reached memory. Source: Week 1 run `week1_memalpha_4bit_01` (read-only). No new model runs.

- **In memory** = the fact is in semantic memory after its chunk (see `stored_verbatim` in the CSVs).
- **Correct chain** = the newest version of every fact the question needs. In FactConsolidation, the higher fact number wins.

## Result

| Outcome | Count | Questions |
|---|---:|---|
| Correct | 1 | SH-Q3 |
| Correct, but scored wrong due to formatting | 1 | SH-Q1 |
| **Impossible: a needed fact was lost to the write cutoff** | **4** | SH-Q2, SH-Q4, MH-Q0, MH-Q2 |
| Facts all in memory, test-taker still wrong | 4 | SH-Q0, MH-Q1, MH-Q3, MH-Q4 |

The pilot scored 1/10 on exact match. That number mostly measures the setup, not Mem-α's conflict handling:

1. **4 of 10 questions could not be answered from memory**, because the cutoff dropped a needed fact (see the [Week 1 report](../../week_1/results/week1_closeout/WEEK1_REPORT.md), finding 1).
2. **When old and new facts were both stored, the test-taker could not tell which was newer.** Mem-α kept both versions with no fact numbers (e.g. `goaltender ... ice hockey` and `goaltender ... pesäpallo`). The test-taker's instructions say to pick the higher number, but the numbers aren't there. In SH-Q0 and MH-Q4 it picked the old fact.
3. **The test-taker is weak even with perfect input.** Given the full original fact list instead of memory, it scored 2/10.

## Per-question evidence

`✅` = in memory, `❌` = lost to the cutoff (end of its chunk). Fact numbers point to rows in the audit CSVs.

### Single-hop

| Q | Question → correct answer | Facts (old → **new**) | Memory answer | Outcome |
|---|---|---|---|---|
| 0 | goaltender's sport → pesäpallo | #223 ice hockey ✅ → **#310 pesäpallo ✅** | ice hockey | Both kept, no numbers; picked old |
| 1 | Nobuhiro Watsuki famous for → The Fairly OddParents | #91 Rurouni Kenshin ✅ → **#259 Fairly OddParents ✅** | "The author of The Fairly OddParents." | Right content, fails exact match |
| 2 | rugby union created in → India | #100 England ✅ → **#186 India ❌** | England | Impossible (cutoff) |
| 3 | Ferdowsi famous for → Shahnameh | **#86 Shahnameh ✅** (no conflict) | Shahnameh | Correct |
| 4 | Joan Didion's university → UC Berkeley | **#63 UC Berkeley ❌** (no conflict) | Bowdoin College | Impossible (cutoff) |

### Multi-hop

| Q | Question → correct answer | Correct chain | Memory answer | Outcome |
|---|---|---|---|---|
| 0 | citizenship of spouse of author of *Our Mutual Friend* → Belgium | **#146** Darwin ✅ → **#335** married Amala Paul ❌ → **#322** Belgium ✅ | United Kingdom | Impossible (cutoff) |
| 1 | where Igor of Kiev's spouse died → Rodez | **#175** Olga ✅ → **#450** Rodez ✅ (old #125 Kyiv was lost) | Rome | All facts present; wrong |
| 2 | birthplace country of Steve Sax's sport → Italy | **#417** association football ✅ → **#389** Italy ❌ | baseball | Impossible (cutoff); also used old #35 |
| 3 | capital of origin country of Tunisia team's sport → Russellville | **#418** basketball ✅ → **#348** Soviet Union ✅ → **#179** Russellville ✅ | (long explanation, no answer) | All facts present; wrong |
| 4 | Blair Walsh's sport → rugby | **#419** placekicker ✅ → **#321** rugby ✅ (old #78 American football also kept) | American football | Both kept, no numbers; picked old |

## What this means for next steps

- **Fix the cutoff before measuring anything else.** Rerun [the audit script](../scripts/audit_lost_facts.py) on any new run; missing facts should be near 0%.
- **Decide how memory records which fact is newer.** Either keep fact numbers in stored notes or have the writer replace old facts. Without one of these, the test-taker can't resolve conflicts even when both facts are present. Whatever we choose must be the same for every compared writer.
- **Test the test-taker separately.** It failed MH-Q1 and MH-Q3 with every needed fact present, and scored 2/10 on the full text.
- **Early sign for research question 1:** in every conflict above where both versions reached memory, Mem-α kept both and never updated or deleted the old one. This is consistent with Week 1's count of zero semantic updates or deletes. Step 3 (the conflict finder) will measure this across all conflicts, not just these 10 questions.

Caveat: 10 questions from a single run. These explain pilot failures; they are not benchmark rates.
