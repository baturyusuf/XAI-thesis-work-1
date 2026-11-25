# Reproducibility guide

This guide accompanies the manuscript "Which metric should choose the model? Selection criteria, class weighting and endpoint recall in tabular ordinal classification".

It explains how every result in the paper can be regenerated from the original data sources. Raw data, identifiers and row-level predictions are not distributed. Two providers forbid redistribution, and the others are cited at their source.

## What is in the study

All code is in one place: the repository `https://github.com/baturyusuf/XAI-thesis-work-1`, tag `compstat-v2`, directory `research/ordinal_selection_y1/`. Paths below are relative to that directory. The stages were developed on separate branches; their histories were merged without changing any frozen file.

| Stage | Tasks | Fits | Protocol and runner |
|---|---|---:|---|
| 1 | wine red, wine white, SkillCraft (8 leagues, superseded), TAE (control) | 576 | `Y1_PILOT_PROTOCOL.md`, `pilot_config.json`, `PROTOCOL_FREEZE.json`, `run_pilot.py`, `y1/` |
| 2 | Restaurant, Sushi, MovieLens-100k, SkillCraft (7 survey leagues) | 576 | `gate_v2/real_extension/`, `gate_v2/skillcraft_survey/` |
| simulation | latent Gaussian model, 6 cells × 10 replications | 480 | `gate_v2/mechanism/` |
| 3 | CTG, HCV, Cirrhosis, SUPPORT2; Diabetes130, Student, NPHA (controls) | 1,008 | `m1_extension/` (pre-fit freeze commit `2f5533e`) |
| 4 (pre-specified) | the 14 tasks above (not the superseded one) with 24 candidates; simulation with 6 shares × 3 signals × 10 replications | 6,048 + 1,440 | `robustness_m2/{PROTOCOL.md, config.json, FREEZE.json, run.py}` |
| 5 (pre-registered) | 4 new sources (Drug Consumption alcohol, Entrance Exam, NHANES 2017–18 and NHIS 2019 self-rated health) and the 14 earlier tasks; 32 candidates incl. a Frank–Hall ordinal family; median decoding | 10,368 | `validation_m5/{PROTOCOL.md, config.json, FREEZE.json, fetch.py, data.py, run.py}` (pushed before any fit, commit `66e426e`) |
| analysis | cross-task analysis, tables, figures, manuscript | 0 | `manuscript_compstat/` |

## Getting the code and the environment

```
git clone https://github.com/baturyusuf/XAI-thesis-work-1.git
cd XAI-thesis-work-1
git checkout compstat-v2
cd research/ordinal_selection_y1
python -m venv local/.venv
local/.venv/Scripts/python -m pip install -r requirements.txt                          # fitting (Windows path; use local/.venv/bin/python elsewhere)
local/.venv/Scripts/python -m pip install -r manuscript_compstat/requirements-analysis.txt  # figures and tables
```

All analyses used Python 3.13. `ENVIRONMENT.txt` lists the full package set of the fitting environment.

**Proportional-odds code.** The proportional-odds estimator, the shared preprocessor and the RPS function are read from the authors' earlier public repository, `https://github.com/baturyusuf/employee-performance-with-XAI`, at commit `c7f7729`. They are not copied into this repository. To fetch them:

```
git clone https://github.com/baturyusuf/employee-performance-with-XAI.git ../../../employee-performance-with-XAI
python bootstrap_source.py --source-repo ../../../employee-performance-with-XAI
```

`bootstrap_source.py` copies the five files of that commit into the ignored `local/source/` folder. `y1/source.py` checks them against the SHA-256 hashes in `SOURCE_MANIFEST.json` before every fit and stops if any file differs.

Every stage has a `PROTOCOL.md`, a `config.json` and a `FREEZE.json`.

`FREEZE.json` holds SHA-256 hashes of the code, the configuration, the prepared tables and the exact split assignments. These were recorded before any model was fitted in that stage. The freezes are local, not external registrations.

The runners refuse to overwrite an existing freeze or run directory.

## Stage 4 (pre-specified robustness)

`robustness_m2/PROTOCOL.md` states hypotheses H1–H5 (expanded pool) and S1–S3 (simulation) with their exact decision rules. It was frozen with the configuration, the runner and the hashes of the reused split assignments before any stage-4 fit (`FREEZE.json`, UTC time stamp; local, not an external registration).

- **Candidates (24).** Proportional odds with C ∈ {0.01, 0.1, 1, 10}; random forest with depth ∈ {3, 6, 12, unlimited}; histogram gradient boosting with (learning rate, depth) ∈ {(0.05, 3), (0.05, unlimited), (0.1, 3), (0.1, unlimited)}, 200 iterations, no early stopping. Each with and without balanced weights; selection within family.
- **Splits.** The frozen assignments of stages 1–3, unchanged, so the results are paired with the earlier runs.
- **Run.** From `research/ordinal_selection_y1/`:

```
python -B robustness_m2/run.py verify --y1 <stage 1-2 dir> --m1 <stage 3 dir>
python -B robustness_m2/run.py tasks  --y1 <stage 1-2 dir> --m1 <stage 3 dir> --workers 12
python -B robustness_m2/run.py sim    --y1 <stage 1-2 dir> --m1 <stage 3 dir> --workers 12
```

The runs took about 10 minutes on 12 cores. Outputs go to `local/robustness_m2/` (not in Git) and are never overwritten.

## Stage 5 (pre-registered validation)

`validation_m5/PROTOCOL.md` states predictions V1–V5 (new sources), F1–F2 (Frank–Hall ordinal family) and D1–D2 (median decoding), with their decision rules. Before any stage-5 fit, the protocol, code, data hashes (`PROVENANCE.json`), the eligibility audit (`AUDIT_SUMMARY.json`) and `FREEZE.json` were committed and pushed to the public repository (commit `66e426e`).

- **Data.** `fetch.py` downloads the approved files into `local/validation_m5/raw/<source>/` and records their SHA-256 hashes.
  - NHANES and NHIS files are used under the NCHS Data User Agreement: statistical analysis only, no re-identification, no linkage with identifiable data.
- **Run.** From `research/ordinal_selection_y1/`:

```
python -I -B validation_m5/fetch.py
python -B validation_m5/run.py prepare --y1 <stage 1-2 dir> --m1 <stage 3 dir>
python -B validation_m5/run.py verify  --y1 <stage 1-2 dir> --m1 <stage 3 dir>
python -B validation_m5/run.py tasks   --y1 <stage 1-2 dir> --m1 <stage 3 dir> --workers 12
```

- **Outputs.** Inner out-of-fold probabilities are saved, so `m5_validation.py` can repeat every selection with median decoding and with the max–min floor fallback without refitting.
- **Check.** Rerunning the 14 earlier tasks reproduces the stage-4 predictions of the 24 shared candidates exactly.

## Design shared by stages 1–3

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
python -B analysis/m4_robustness.py ../local/robustness_m2 ../robustness_m2 analysis/out
python -B analysis/m5_validation.py ../local/validation_m5 ../local/robustness_m2 ../validation_m5 analysis/out
python -B analysis/source_level.py analysis/out
python -B analysis/make_figures.py analysis/out figures
python -B analysis/make_tables.py analysis/out ../gate_v2/MECHANISM_CONTRASTS.csv .
python -B analysis/check_and_package.py .
```

The first three steps need the saved predictions in the ignored `local/` folders, which are produced by the runs above and are not distributed. The last four steps need only the aggregate files in `analysis/out/`, which are in the repository. In a fresh clone they regenerate every table, figure and number of the paper.

What each step does:
- **`m3_cross_task.py`** reads the saved out-of-fold probabilities, recomputes every metric with an independent implementation, and checks the results against the stored run summaries (2,100 comparisons; largest difference 2.2e-16). It writes aggregate tables only.
- **`m4_robustness.py`** evaluates H1–H5 and S1–S3 exactly as written in the stage-4 protocol (task-cluster bootstrap with 2,000 resamples; Monte Carlo t intervals with 9 df) and writes `m4_hypotheses.json` with a supported / not supported verdict for each.
- **`source_level.py`** repeats the cross-task tests with the nine primary sources as independent units. It runs Friedman tests with source blocks and Wilcoxon tests with the two model families averaged within each source. It also recomputes the bootstrap intervals of the endpoint-share rule with source clusters. Inputs are aggregate outputs only.
- **`make_tables.py`** writes `numbers.tex` (every number in the text) and `tables/`. It also enforces claim guards: if a re-analysis changed any qualitative statement in the text, the script stops instead of producing an inconsistent manuscript.
- **`check_and_package.py`** checks the LaTeX sources and builds flat upload folders.
- **`analysis/word/build_word.ps1`** builds the Word versions from the same sources.

## Code dependency and licences

The proportional-odds estimator, the shared preprocessor and the RPS function come from the authors' earlier repository, `employee-performance-with-XAI`, at commit `c7f7729`. That repository is public, but on 2026-11-25 it had no licence file. Readers can therefore inspect and download the code, but no reuse licence is granted yet. Choosing a licence is the owner's decision. The code is not copied into this repository; `bootstrap_source.py` fetches it from a local clone.

All other code in this repository is under the repository's Apache-2.0 licence. Data are not redistributed; see `DATA_SOURCES.csv` for each provider's terms.
