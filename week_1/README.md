# Week 1 — feasibility and setup

**Complete as a feasibility milestone.** The 4B pilot ran on an A100. Generated-write truncation and reader limitations must be addressed in Week 2 before the main experiment.

## Code

- [Maintained Colab notebook](notebooks/Week1_Colab_Feasibility.ipynb): setup, quantization preflight, memory construction, reader controls, scoring and export. Upload to Colab and select a GPU runtime.
- [Executed notebook](results/week1_closeout/evidence/Week1_Colab_Feasibility_EXECUTED.ipynb): unchanged historical execution evidence with outputs. This differs from the maintained notebook, which includes subsequent compatibility checks.
- `scripts/`: reserved for CPU-only utilities; none are needed for Week 1.

## Documentation and results

- [Completed report](results/week1_closeout/WEEK1_REPORT.md)
- [Five-event memory review](results/week1_closeout/MANUAL_REVIEW.md)
- [Evidence index](results/week1_closeout/README.md), including original ZIP and extracted logs
- [Original checklist](docs/WEEK1_CHECKLIST.md) and [blank report template](docs/WEEK1_REPORT_TEMPLATE.md)
- [Initial analysis of the run](results/week1_review/REVIEW.md)
- [Final-report starter](results/week1_closeout/FINAL_REPORT_STARTER.md)

Week 1 results are frozen pilot evidence, not final benchmark findings. Start a new run directory when changing settings for Week 2. The blank review CSV remains a reusable template; the completed five-event review is the Markdown document above.
