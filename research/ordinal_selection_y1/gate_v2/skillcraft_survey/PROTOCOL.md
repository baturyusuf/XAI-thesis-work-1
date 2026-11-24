# SkillCraft survey-league bounded fourth-source pilot

## Post-v1 source-audit amendment
Astra authorizes a bounded pilot, NOT full benchmark/automatic confirmation. Restrict
UCI272 to LeagueIndex1..7; drop8(professional) for heterogeneous acquisition provenance,
not prediction performance. No merging, favorable-outcome selection or feature change.
This is a new prospective freeze AFTER v1/source audit, not untouched confirmation.
No restricted-task model outcomes seen. Original8-class pilot/data/freezes untouched;
no rerun. Final Astra eligibility must qualify the person-independence assumption.

## Primary evidence and uncertainty
Thompson, Blair, Chen & Henrey2013, Video Game Telemetry as a Critical Tool in the
Study of Complex Skill Learning, DOI10.1371/journal.pone.0075129: Data Collection
reports survey replay files/player codes for league checks, but professional games
from gaming websites. Exclusions list Grandmaster35 and professional55 games;
Discussion reports a single game per participant. Thompson, Blair & Henrey2014,
Over the Hill at24, DOI10.1371/journal.pone.0094215, Method/Overview reports exactly
one replay per survey participant, analyzes3305 amateurs. UCI3395 includes3340
leagues1..7 including35 Grandmasters omitted from paper analyses. Exact UCI-paper
cohort mapping is NOT authenticated; neither paper is claimed to analyze all3340.
PROVENANCE.json records primary URLs, machine UTC access dates, evidence hashes,
original source table/manifest hashes and UCI CC-BY4 attribution metadata.

Raw1..7 -> ranks0..6: Bronze,Silver,Gold,Platinum,Diamond,Master,Grandmaster,
intrinsic league order, no empirical binning. Retain Grandmasters irrespective of
possible professional occupation: league defines task, not verified amateur status.
Historical survey gamers/recorded league is the narrower estimand, conditional on
observed game predictors/source collection. Not future skill/outcomes, new-account
guarantees, causal effects or population expertise. GameID is not person ID; unique
GameID does not prove independence. Source protocol supports one game per participant,
but multiple accounts, shared matches/opponents and latent dependencies may remain.
Excluding8 closes major endpoint acquisition ambiguity, not all person dependencies.

## Immutable adapter and support gates
Reuse y1.data.load('skillcraft'): original source hash verified via DATA_MANIFEST;
existing exact-predictor duplicate groups (including missing sentinel) preserved.
Subset x,y,groups only by raw1..7, preserve original row order and18 numeric features,
values/missingness; exclude GameID/LeagueIndex from x. No deduplication, imputation,
scaling or feature regeneration in preparation. Retain originalGameID uniqueness
check as technical assertion, not person-independence evidence. Freeze local NPZ of
selected original rows/ranks/groups; load features from immutable original source.
Expected3395 counts167,347,553,811,806,621,35,55 ->3340 retained and55 excluded.
Measure total/class-level predictor groups. Endpoint groups>=20 and all7 classes in
every inner/outer train/test or BLOCK/stop. Reuse make_nested3outer/2inner, seeds
20261124/20261125,100 predefined support-valid attempts; save effective seeds/exact
splits. No effect-driven reseeding. Group disjointness and complete OOF coverage tested.

## Models and selection
Reuse candidates,pipeline,fit_prediction,score,choose,paired_endpoint_ci directly;
no new algorithms or blind monkeypatching. Eight candidates: PO C=.1,1; RF depth4,None;
each none/balanced; RF100trees, POmax_iter1000, one thread. 3x2x8x(2inner+1outer)=144
fits total. Preprocessor/model fit on fitting partition only. Seven within-family
selectors: QWK,MAE,AMAE,MMAE,macro-F1,RPS, constrainedQWK(endpoint floor.2, AMAE
fallback), tolerance1e-12/order ties. ONLY inner OOF scores select, never outer test.
First fit error stops/records traceback; no candidate dropping or effect reseeding.
No refits of original8-class task, other sources, old pilot or mechanism.
Save local allcandidate/selected repeated OOF probabilities, inner scores, schedule,
weights,infeasible/fallback. Metrics: endpoint recalls,QWK,nMAE,nAMAE,nMMAE,macro-F1,
RPS,ECE,cumulativeECE,QWK observed/expected. Preserve fixed-h balanced-minus-none
and policy-minus-QWK contrasts, all costs/nulls/reversals. Existing paired bootstrap
is aggregate-only group resampling of fixed predictions conditional on models and
independence assumption; folds/repeats are not independent scientific units. No
cross-source significance or automatic scientific/full Y1 GO.

## Freeze and execution
Writes ONLY gate_v2/skillcraft_survey and local/gate_v2/skillcraft_survey. Data/splits/
identity/predictions stay ignored locally; public summaries aggregate only. Freeze
code/tests,protocol/config/provenance/audit, original table/manifests/evidence,
imported helpers/source, selection NPZ and exact splits BEFORE new fits. Verify
SHA256/file set/runtime versions each run. Existing preparation/freeze/run dirs
cannot be overwritten; reviewed amendments require transparent history.
Zero fits during tests/preparation/freeze. Parent reviews and executes144fits later.
From authorized root, interpreter research/ordinal_selection_y1/local/.venv/Scripts/python.exe -B
Runner research/ordinal_selection_y1/gate_v2/skillcraft_survey/run.py actions:
prepare (already done), freeze (already done), verify, run (parent only).
Tests: interpreter -m pytest -p no:cacheprovider research/ordinal_selection_y1/gate_v2/skillcraft_survey/tests -v
