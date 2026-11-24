# Y1 post-v1 exploratory real-source extension

## Boundary
New prospective local freeze AFTER v1 and the separate mechanism experiment, not
untouched confirmation. No v1 or mechanism refits. Prepare/test/freeze only before
parent review. Three eligible source tasks/families do not meet the original minimum
four-task criterion: no full Y1 GO, no automatic scientific decision. Blocked sources
are explicitly marked and never replaced silently.

## Sources and labels
PROVENANCE.json records primary URLs, citations, archive and member SHA256 hashes,
license evidence and machine UTC inspection/download times. Existing parent evidence
has no invented original access date. No full source READMEs are republished.
Restaurant: UCI232 DOI10.24432/C5DP41 CC-BY4. Overall rating only, raw/ranks0,1,2.
The 2011 primary paper says 0 dislike and 2 high preference; it lists 1 but does not
call it intermediate. UCI release1161 ratings/138 users differs from paper1251
ratings/111 users/237 restaurants. These are not claimed to be the same version.
Sushi2016: Kamishima KDD2003, any research use, no redistribution without permission.
2016 corrects the pre-Dec-29-2015 reversed score coding as well as the README
user-ID issue. The older score file used 0 most preferred; this 2016 release uses
0 most disliked and 4 most preferred. 5000 users/50000 observed scores.
Raw/ranks0..4: 0 most disliked, 4 most preferred; drop only -1 unrated. User rows
align score rows; item IDs align columns. Do not publish known author identities.
MovieLens100k: GroupLens100000 ratings/943 users/1682 movies. Research permitted,
cite Harper/Konstan2015 DOI10.1145/2827872; no endorsement or redistribution; no
commercial/revenue-bearing use without permission. Parent confirmed academic study.
Raw1..5 map ranks0..4. u.user/u.item actually pipe-separated despite README tab claim.

## Frozen feature allowlists and sampling
Restaurant: all rows, group userID; validate many-to-one user/place joins with no
loss or unmatched records; '?' missing. Restaurant alcohol,dress_code,accessibility,
price,Rambience,franchise,area,other_services; user budget,dress_preference,ambience,
transport, all categorical. No food/service rating, IDs, names, locations, demographics,
religion, marital status, weight, or any nonallowlisted input.
Sushi: select500 users by lowest SHA256('Y1-real-extension-v1|sushi|'+groupID),
without outcomes, retaining all selected users' observed scores. Categorical age band,
item style,major/minor group only. No questionnaire-derived oiliness/eating frequency/
normalized price/shop frequency, time,gender,geography, IDs or author identities.
MovieLens: select400 users by same hash scheme, dataset='movielens100k', retain all
ratings. Numeric user age, release year,19 genre flags only. No IDs,gender,occupation,
ZIP,title,URL,timestamp or rating-derived aggregates. Exact dictionaries and machine
feature names are in data.py and audit.json. Missing features remain for train-only
preprocessor imputation; no outcome-based row deletion or group selection.

## Evaluation
Reuse make_nested: grouped user splits,3 outer/2 inner folds, seeds20261124/20261125,
existing100 support-valid split attempts; save effective seeds and assignments.
Endpoint distinct users >=20 in selected full task; all classes in every inner/outer
train/test; no user overlap. Quantify item overlap for outer and inner splits.
Estimand is held-out users conditional on observed item pool and historical ratings,
not new-item/known-item-only performance or prospective future outcomes.
Reuse fit_prediction,candidates,pipeline,score,choose; train preprocessor on fitting
partition only. Eight candidates: PO C=.1,1; RF depths4,None; each none/balanced;
RF100 trees, PO max_iter1000, one thread. 8x(2 inner+1 outer)x3 folds x2 seeds=144
fits/source;432 total. Zero fits during prepare/tests/freeze.
Seven within-family selectors: QWK,MAE,AMAE,MMAE,macro-F1,RPS,endpoint constrained
QWK (floor.2; existing AMAE fallback), tolerance1e-12/order ties. Inner OOF metrics
only select; outer test never selects. Save inner candidate scores, selected schedule,
weights,infeasible/fallback flags, all candidate/selected repeated OOF probabilities,
and full metric dictionaries including QWK observed/expected components.
Keep fixed-h balanced-minus-none controls and policy-minus-QWK endpoint contrasts,
all nulls/reversals/costs. Reuse paired bootstrap only for aggregate fixed-prediction
user-resampling conditional on fitted models, not independent folds/repeats. No
cross-source significance claim or automatic expansion.

## Privacy, failure and freeze
All source/subset rows,splits,IDs,schedules,OOF predictions and outcomes stay ignored
under local/gate_v2/real_extension. Public artifacts contain aggregate metadata only.
Freeze hashes code/tests,protocol/config/provenance, imported existing helpers/source,
archive/license evidence,prepared tables and exact nested splits; check package
versions before each model run. Existing prepared artifacts/freeze/output dirs cannot
be overwritten; reviewed amendments required. First fit error records failure and
stops, with no candidate dropping, effect-driven reseeding or source replacement.

## Commands from authorized worktree root
Interpreter: research/ordinal_selection_y1/local/.venv/Scripts/python.exe -B
Runner: research/ordinal_selection_y1/gate_v2/real_extension/run.py
Actions: prepare; freeze; verify; run --dataset NAME.
Tests: interpreter -m pytest -p no:cacheprovider research/ordinal_selection_y1/gate_v2/real_extension/tests -v
NAME: restaurant, sushi, movielens100k. Parent alone runs models after review.
Preparation and freeze are already completed; repeat verification, not overwrite.
