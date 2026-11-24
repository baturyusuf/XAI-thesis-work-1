# Reproducibility guide

This guide accompanies the manuscript "Which metric should choose the model? Selection criteria, class weighting and endpoint recall in tabular ordinal classification".

It explains how every result in the paper can be regenerated from the original data sources. Raw data, identifiers and row-level predictions are not distributed. Two providers forbid redistribution, and the others are cited at their source.

## What is in the study

| Stage | Tasks | Fits | Protocol and runner (branch / path) |
|---|---|---:|---|
| 1 | wine red, wine white, SkillCraft (8 leagues, superseded), TAE (control) | 576 | `research/ordinal-selection-y1`: `research/ordinal_selection_y1/{Y1_PILOT_PROTOCOL.md, pilot_config.json, run_pilot.py, y1/}` |
| 2 | Restaurant, Sushi, MovieLens-100k, SkillCraft (7 survey leagues) | 576 | same branch: `research/ordinal_selection_y1/gate_v2/{real_extension, skillcraft_survey}/` |
| simulation | latent Gaussian model, 6 cells × 10 replications | 480 | same branch: `research/ordinal_selection_y1/gate_v2/mechanism/` |
| 3 | CTG, HCV, Cirrhosis, SUPPORT2; Diabetes130, Student, NPHA (controls) | 1,008 | `research/ordinal-y1-m1-extension`: `research/ordinal_selection_y1/m1_extension/` (pre-fit freeze commit `2f5533e`) |
| analysis | cross-task analysis, tables, figures, manuscript | 0 | `research/q3-journal-selection`: `research/ordinal_selection_y1/manuscript_compstat/` |

Every stage has a `PROTOCOL.md`, a `config.json` and a `FREEZE.json`.

`FREEZE.json` holds SHA-256 hashes of the code, the configuration, the prepared tables and the exact split assignments. These were recorded before any model was fitted in that stage. The freezes are local, not external registrations.

The runners refuse to overwrite an existing freeze or run directory.

## Design shared by all stages

- **Candidates (8).** Proportional odds with C ∈ {0.1, 1} and random forest with depth ∈ {4, unlimited} (100 trees, minimum leaf 2). Each configuration is trained with class weights none and balanced. Selection happens within each model family.
- **Cross-validation.** Grouped nested CV with 3 outer and 2 inner folds and two seeds.
  - For each seed, the first support-valid assignment among seed offsets 0–99 is used.
  - All preprocessing and weights are fitted on training partitions only.
- **Selection.** Seven criteria select from pooled inner out-of-fold scores: QWK, MAE, AMAE, MMAE, macro-F1, RPS, and QWK with an endpoint-recall floor of 0.2 that falls back to AMAE.
- **No per-criterion refits.** Every candidate's outer predictions are computed once, so nothing is refitted per criterion. This makes 144 fits per task.
- **Software.** Python 3.13, NumPy 2.5.5, pandas 3.1.1, SciPy 1.18.1, scikit-learn 1.9.1, one thread per fit.

## Data

`DATA_SOURCES.csv` lists, for every task:
- the provider URL, DOI and terms;
- whether redistribution is allowed;
- the SHA-256 of the downloaded archive and, where available, of the prepared table;
- the file that defines the task: target coding, excluded variables, grouping and outcome-blind subsampling.

To reproduce, obtain each archive from its provider and check its hash. The stage's `prepare` command then rebuilds the tables and splits, and `verify` checks them against the freeze before any fit.

Restricted sources:
- **Sushi (Kamishima) and MovieLens-100k (GroupLens):** research use only, no redistribution. Download them from the providers.
- **SUPPORT2:** used under the distributor's general permission (hbiostat.org/data). No redistribution right is claimed.

## From saved predictions to the paper (no fitting)

Run these from `research/ordinal_selection_y1/manuscript_compstat/`:

```
python -B analysis/m3_cross_task.py <stage 1-2 local dir> <stage 3 local dir> analysis/out
python analysis/make_figures.py analysis/out figures
python analysis/make_tables.py analysis/out ../gate_v2/MECHANISM_CONTRASTS.csv .
python analysis/check_and_package.py .
```

What each step does:
- **`m3_cross_task.py`** reads the saved out-of-fold probabilities, recomputes every metric with an independent implementation, and checks the results against the stored run summaries (2,100 comparisons; largest difference 2.2e-16). It writes aggregate tables only.
- **`make_tables.py`** writes `numbers.tex` (every number in the text) and `tables/`. It also enforces claim guards: if a re-analysis changed any qualitative statement in the text, the script stops instead of producing an inconsistent manuscript.
- **`check_and_package.py`** checks the LaTeX sources and builds flat upload folders.
- **`analysis/word/build_word.ps1`** builds the Word versions from the same sources.

## Code dependency to settle before public release

The proportional-odds estimator, the shared preprocessor and the RPS function come from the authors' earlier code base (`employee-performance-with-XAI`, commit `c7f7729`).

That code is snapshotted locally and verified by hash (`SOURCE_MANIFEST.json`). Its public licence must be decided by its owner before the code is released together with this study.

All other code in the repository is under the repository's Apache-2.0 licence.
