# M1 amendment: hypotheses H-M1a/b/c added AFTER fitting (not pre-specified)

## Timeline (machine records)
- 2026-11-24T09:54:31Z: FREEZE.json created (digest 83814c61bdfd75f7c7d4f043cd8eae85462aaf7893e0ad2d247e7ee072ee26c0); pre-fit commit 2f5533e (09:55:05Z).
- 2026-11-24T09:55:16Z to 09:55:49Z: all 1,008 M1 fits ran.
- 10:01:07Z: results commit b5b249b. The M1 outcomes had been inspected and reported in M1_RESULTS_TR.md,
  including a descriptive remark that endpoint classes are sometimes majority classes (related to H-M1a).
- After 10:01Z: the manuscript session (branch research/q3-journal-selection) asked for H-M1a/b/c to be frozen
  before any M1 fit. Fitting had already finished, so this was not possible.

## Consequence
H-M1a/b/c are NOT pre-specified for M1 and M1 is NOT a prospective test of them. PROTOCOL.md and FREEZE.json are
deliberately left unchanged: adding the hypotheses there would misdate them and break freeze verification. The
results below are post-hoc analyses of saved outputs (no new fits) and are labelled as such everywhere. The analyst
had seen the M1 outcomes before the hypotheses arrived. The analysis follows the requested definitions exactly and
reports failures to replicate. One element was fixed before fitting: the moderator for H-M1a. Endpoint class counts,
rows and endpoint group counts per task are part of the frozen AUDIT_SUMMARY.json (listed in FREEZE.json), and
prevalence = count / rows of the prepared table.

## Hypotheses as received (definitions used unchanged)
- H-M1a: contrast = AMAE-selected minus QWK-selected mean endpoint recall. The contrast is larger when the rarer
  endpoint is rare. Primary: one-sided Spearman correlation (expected negative) between the contrast and
  min(endpoint prevalence) over the new task x family cells. Secondary: mean contrast for cells with min prevalence
  < 0.05 versus >= 0.05.
- H-M1b: constrained QWK minus QWK has mean endpoint recall >= 0 and QWK <= 0. Sign test / exact Wilcoxon over
  source-family x model-family blocks (each M1 source is its own source family, so 7 x 2 = 14 blocks).
- H-M1c: the fraction of balanced-weight selections is lower under MAE and RPS than under MMAE and constrained QWK;
  the fraction is reported per policy.

## Analysis choices made here (after outcomes were seen; reported as sensitivities, not as alternatives to pick from)
- Primary H-M1a uses all 14 M1 cells, as requested. Sensitivities: the 8 primary-task cells only, and 7 task-level
  means (the two families share data, so the 14 cells are not independent). The p-value is scipy's one-sided
  Spearman test plus a Monte Carlo permutation p (100,000 permutations, seed 20261124).
- H-M1b drops zero differences (identical selections) in the sign test and the Wilcoxon test (zero_method='wilcox'),
  and reports how many blocks were zero.
- Code: validation/posthoc_hypotheses.py -> POSTHOC_HYPOTHESES_M1.json. No cross-task claim beyond these post-hoc
  descriptions is made here.
