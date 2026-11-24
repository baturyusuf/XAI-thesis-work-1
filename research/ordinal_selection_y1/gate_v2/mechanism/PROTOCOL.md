# Y1 bounded controlled mechanism experiment

## Status and scope
Implement/test/freeze only pending parent review. No real mechanism fits before review.
The local SHA freeze is prospective for this experiment, after an earlier real pilot;
it is not entire-study preregistration. No scientific GO is automated. Only fixed
algorithmic interventions under the specified DGP are supported, not real-world causality.

## DGP and budget
Five independent standard Gaussian covariates. beta = [1,.7,-.4,0,0] / norm(beta).
z = (signal X beta + independent N(0,1)) / sqrt(signal^2+1).
Five classes use fixed population norm.ppf(cumulative priors) thresholds, never sample
quantiles. Priors: balanced [.2,.2,.2,.2,.2], symrare [.04,.16,.6,.16,.04],
asym [.45,.25,.15,.1,.05]. Signals .5 and 2. Seeds 20261201 through 20261210.
Within each seed identical underlying X, noise, and partition membership across all
six cells. Train/validation/test are independent disjoint draws of 1000/1000/4000;
no nested CV or row reuse. Missing classes in any partition cause a hard stop.

Exactly 6 cells x 10 independent replications x 8 candidates = 480 fits (240 PO,
240 RF), sequential and one thread. Existing y1.models candidates/pipeline are reused:
PO C=.1,1; RF depth=4,None; each weight=None,balanced; RF=100 trees;
PO max_iter=1000. Same seed for candidate random states within replicate.
Preprocessing and model are fit on train once; no refit after selection.
Toy unit fits are permitted and excluded from this budget. No new algorithms.

## Selection and reporting
Existing y1.metrics score/choose are reused, separately per family. Validation-only
policies: QWK, MAE, AMAE, MMAE, macro-F1, RPS, and endpoint-recall-constrained QWK
(floor .2, existing AMAE fallback); tolerance 1e-12, existing candidate order ties.
Test scores are never passed to selection. Replay needs only saved validation scores,
config, and ordered candidate identities. Test metrics, support counts, confusion
matrices and QWK observed/expected components are saved; no row data or predictions.
Constraint infeasible/fallback flags and weighting frequencies/counts are retained.
Cheap baselines are train-mode one-hot and known population prior probabilities;
no fitting or use of test labels to set baseline predictions.

Fixed-hyperparameter balanced-minus-none test contrasts are separate from validation
policy contrasts. Primary: AMAE-selected minus QWK-selected mean endpoint recall.
Secondary: macro-F1-selected minus QWK-selected mean endpoint recall. All low/high/mean
endpoint recalls, QWK, nMAE, nAMAE, nMMAE, macro-F1, RPS, ECE, cumulative ECE,
and QWK components are retained in contrasts, including nulls, reversals and costs.
Ten independent replicate contrasts, not folds or candidates, form each Monte Carlo
mean and t95 interval (df=9). Intervals are MC under this fixed DGP, NOT real-world
inference. All pairwise cross-cell interactions first subtract same-seed contrasts.
Secondary metrics and cross-cell intervals are descriptive, without multiplicity-adjusted
confirmatory claims. No favorable-effect filter, reseeding, dropping candidates,
or recovery after first fit error. A failed run records the traceback and stops.

## Freeze and execution
FREEZE.json hashes protocol, config, experiment code/tests, existing y1 Python helpers,
requirements, source manifest and all local source Python files; package versions are
recorded and checked. Verification precedes every real run. Existing freeze cannot be
overwritten. A reviewed amendment is needed for changes. Output directory is created
exclusively, never overwritten or resumed. Only local/gate_v2/mechanism holds outputs.
run.py freeze and run.py verify do not run the experiment. Parent alone executes
run.py run after review. Summary is generated only after all 480 fits complete;
RESULTS.md initially records the intentionally unexecuted status.
