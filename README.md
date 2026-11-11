# CLMM final project

Conflict resolution in an adapted, quantized Mem-alpha memory agent. Three-person project; all inference uses open-source models with no paid APIs. GPU code is provided as Colab notebooks.

## Weekly folders

| Folder | Purpose | Status |
|---|---|---|
| [week_1](week_1/README.md) | Colab setup, feasibility pilot, saved run and completed report | Complete; limitations documented |
| [week_2](week_2/README.md) | Repair truncated writes, calibrate reader, establish matched baselines | In progress: cutoff fixed; reader and conflict analysis next |
| [week_3](week_3/README.md) | Writer diagnostics, reader calibration and conflict-checking prototype | Implemented; Colab runs pending |
| [week_4](week_4/README.md) | Frozen extension evaluation and final comparisons | Planned |
| [week_5](week_5/README.md) | Final report, presentation and reproducibility | Planned |

The [original proposal](proposal/COMS6998%20CLMM%20Project%20Proposal.pdf) is preserved separately. The implemented plan removes the paid GPT-4.1-mini baseline and documents quantization and other adaptations.

## Start here

1. Read the [Week 1 completion report](week_1/results/week1_closeout/WEEK1_REPORT.md).
2. Assign the three roles in the [Week 2 handoff](week_2/README.md).
3. Use the [maintained Week 1 Colab notebook](week_1/notebooks/Week1_Colab_Feasibility.ipynb) as the starting point for Week 2 fixes. Create a version in `week_2/notebooks/` and a new run name rather than overwriting Week 1 evidence.

Each week has folders for notebooks, CPU-only scripts, documentation and results. Empty folders are intentional; later-week code has not been implemented yet. Put all GPU-dependent Python work in `.ipynb` notebooks. Do not commit model weights, credentials or caches.

The original executed notebook and run archive are retained together under `week_1/results/week1_closeout/evidence/`. Redundant handoff ZIPs and an identical extracted copy are preserved locally under `archives/local_copies/` and excluded from GitHub. Colab output locations in Drive are unchanged by this repository reorganization.
