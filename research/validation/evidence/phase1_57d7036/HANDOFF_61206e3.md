# Agent 5 - immutable Phase 1 audit handoff

## 1. Fixed identities and custody

- Phase 1 implementation commit: 57d703699e7c7d1c323c251c4cac9bd0ca163634
- Immutable handoff payload: Git blob deb4b5675ccce459f81d6ed69b81edea4986d098
- Payload SHA-256: 33c55a2d1fa12c644e75c0caada68f68d599e1bc7cef47afeef5b777a0102e8b
- Payload path in that implementation: research/innovation/phase1/publication/AUDIT_PAYLOAD.json
- Implementation manifest SHA-256: 59642059961c67734e1bfc1ff5ab90b3bdc14ffd23c8fd845a7096ed43361552
- Original Phase 1 source/config/result manifest SHA-256: 07e537056c4121fcad23cedcfd06b1fb9ca32549fdea6ac4bdc46a30956f80e1

This final document is delivered in a separate documentation-only commit. Its exact commit SHA is supplied in the delivery; the immutable payload identity above avoids a self-referential commit hash inside the document. Read the final handoff using that documentation SHA, but obtain and execute ALL application/source/config/test/results from the implementation SHA above, never a moving branch.

Do NOT modify the implementation commit, frozen code/results, pinned upstream sources or audited files. Audit in an auditor-owned snapshot copy. Remediations need a new version/commit and re-review, not edits to this evidence. The implementation includes the initial local draft of this handoff; only this later document supersedes that draft. Historical51file DELIVERABLE_MANIFEST and65file publication IMPLEMENTATION_FILE_MANIFEST apply to the implementation commit, not the later changed handoff file.

Prior identities remain immutable: frozen implementation3327e942f8d3abfe851f9513ba2c4a2a30e29a67; prior handoff305fb2f30bdcac1bf852a2f2c9f226346869fdc2; Agent5 audit2992eeee9d6436d62846e8190ed129bd3d9852ea. Agent3 source51a6915ec8f94cf1779609422bd61e8d6b3911c7 remains23byte-identical imported files. All127old frozen manifest files unchanged (manifest digest9c5b2eca9453937c58075fccde067cc764469eae40c0381d36749012f482a6c0). Old Phase1 no-commit/push status documents are historical; current human authorization permits only this freeze and normal publication.

## 2. Source, dependency and license pins

LIME actual PyPI release0.2.0.1 archive SHA25676960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781, BSD-2-Clause.19installedPythonfiles byte-match. Do NOT substitute current GitHub code with the same version string: its private sampler API differs. Bayes author repo dylan-slack/Modeling-Uncertainty-Local-Explainability commit72c4330bc7d29150b55018b0946f85f7df88e107, MIT;6source/provenance-file hashes verified. Google SIS pin0d94f8c4d92678ce5f7a0eacae725f79174cfb03 remains original Apache2source.

Native environment Python3.11.9, NumPy1.26.4, SciPy1.11.4, sklearn1.3.2, LIME0.2.0.1, with all remaining pins in ENVIRONMENT_FREEZE.txt and25hashed binary wheels in requirements.lock/WHEEL_AUDIT.json. publication/SOURCE_ENV_LICENSE_QC.json verifies hashes, package versions, license notices and pipcheck. This compatible-minimal stack is NOT the authors full historical Bayes environment. No NEW external source, wheel, archive or venv is distributed; downloads remain ignored. Root project Apache2license does not relabel dependency licenses.

## 3. H1 v2 and retained SIS failure

src/innovation/phase1/h1_reference_v2.py changes only availability of cost metadata. Search/predicate AST identical to original; uniformXOR selects(0,1), executes8callbacks/3predicates with or without a supplied ledger. V2 missing ledger reportsNone; measuredzero differs fromunknown; supplied counters are lifetime snapshots, not deltas. Original h1_reference.py and exact/reference results untouched. Four unit tests in test_h1_counter_v2.py plus standalone publication/verify_h1_counter.py and H1_COUNTER_QC.json establish the scoped check; standalone checks do not inflate unittest count.

Native SIS test_constant_score_empty_sufficient_set remains a failing assertion, not skip/xfail. x=ones2,fullymasked=zeros2,constant1batchscorer,threshold1 => SIS[]/mask[True,True] instead of empty/allFalse. Emptyindices->tuple()->mask[()]=True. Fourcalls/fiverows. Fullymasked score already sufficient: output-field inconsistency demonstrated, ordinary-use sufficiency failure INCONCLUSIVE. Source SHA2562718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079 unchanged. No patch or external issue.

## 4. Native versus adapter contracts

Native LIME bank:160explanations,128native samples each, all continuous, no discretization, feature_selection=none, sample_around_instance=True. Full native Ridge retains intercept/scaler/featureorder. Captured model_regressor matches unhooked default fit bitwise; weighted normal-equation/reconstruction and native local_pred checks pass. R2 is not functional fidelity loss. Rowwise calls to that same fitted estimator fix numerical evaluation shape; no refit or coefficient repair.

LIME Gaussian/kernel generation law deliberately differs from uniform four-offset(+/- .25 each) evaluation law. Predictor fixed p1=.5+.18tanh(x0)+.12tanh(x1), vector(1-p1,p1), targetclass1, probability scale. No silent normalization. Selected-class float values are represented as exact binary Fractions; calibration means remain Fraction. This is the computational float target, NOT analytic-real tanh or full-vector exact Fraction-simplex validation.

Native LIME h is globally unbounded, so bounded-loss LTT explicitly evaluates clip(h,0,1). Raw/clipped loss, invalid-output rate and clipping gain remain separate in final JSON unit records. Zero observed invalid batches/gain is not proof of global raw-native boundedness. See float_adapter.py/EVALUATION_CONTRACT.md/test_float_adapter.py.

Bayes smoke:threecenters128samples each, focus_sample=False, native default training-mean-centered sampler. BLR fits original coordinates with penalized intercept; LIME's h uses scaled coordinates/unpenalized intercept. h_B and h_L are different banks, not interchangeable. Native posterior radii/s2/predict diagnostics retained. Native predict second output sqrt(s2*(1+xVx)) is Student-t scale under its IG sampler, not full marginal standard deviation. No Bayes fidelity guarantee, fullpaper benchmark replication, posterior transfer to h_L or BayesSHAP surrogate-loss assumption. Bayes LTT calibration NOT_MEASURED.

## 5. Splits, scores, controller and evaluation

Frozen bank IDs: fit-0..31(B32),calibration-0..63(C64),evaluation-0..63(T64); full IDs/centers/native coefficients/seeds/probeindices in LIME_PILOT_RESULTS.json. Deterministic9pointbackground, synthetic only. No real/private/hidden data or otherworktree writes. Every augmented base observation includes its own explanation/score randomness.448probe batches,736unique role seeds; IDs/seeds alone do not prove IID.

B quality labels16independent probes/unit. Directscore8; Closs16; Tloss32 plus exact fourpoint unitloss referee. Separate generation/score/calibrationloss/evaluationloss draws, B-only standardRidge score fit. Four score families direct/BlearnedRidge/random/reversed share the SAME explanationbank/target/loss. Reversed deliberately reuses direct computation, not an independent budget run. Final evaluation never feeds fitting/calibration.

Accepted-count HB+Bonferroni: alpha1/5; thresholds{0,1/50,1/20,1/10,1}; each family risk1/80 plus coverage1/80; total4*(1/80+1/80)=1/10. Minimumcoverage1/20 separately. A_t=1[q<=t]; K=sumA. For k>0 HB uses accepted bounded losses, p=min(1,exp(-k*KL(mean,alpha)),e*BinomCDF(k,alpha,ceil(sumlosses))) if mean<alpha, else1. K0=>p1,riskNone. Coverage lower=max(0,K/64-sqrt(log(5/delta_coverage)/(2*64))). Choose maximum calibration coverage within eligible set. Shared records do not invalidate Bonferroni if each test valid.

Validity requires independent fittedB/fixedfamily, augmentedIIDunits, stable population and loss probes conditionally unbiased given explanation/score/acceptance randomness. Perturbations do not add to calibrationn64. Metadata does not establish theorem assumptions. Inherited float HB/1e-12guard is not all-range intervalproof.20policies independently cross-checked using65digitDecimal and exact sums/counts.

All four score families accept same64TIDs,coverage1,common exact empirical unitloss107486909779412685/9223372036854775808 (~0.0116537541). Random/reversed success makes this mechanism nondiscriminating for strong selectivequality, not broad adequacy/necessity/superiority. Samecoverage/prefixAURC descriptive only. Exact fourpoint UNIT loss and finiteT empirical risk are NOT integrated population risk or a fidelity guarantee event. Earlier audited synthetic-reference direct/learned and transformed-controller results stay unchanged, with their own different model/bank/budgets; not pooled into new leaderboard.

## 6. Costs, tests, known failures and attempts

FinalLIME pilot512batchcallbacks/25344modelrows:20480generation,512Blabels,1024directscores,1024Closs,2048Tloss,256exactreferee. Each exactreferee1call4rows despite sampledprobe_count0. Charge learned-only Bgeneration4096+labels512+fit/inference; standalone direct does not needB. COST_LEDGER/JSON separate modelcalls/rows/walltime; nested fit/generation timings must not be doublecounted. Each Bayescenter1x128generation+1x4evaluation; combinedwalltime includes posterior work. Peakmemory/setup/isolatedposterior timings NOT_MEASURED; matchedtotalcost NOT_ESTABLISHED.

Latest distinct suites: frozen85=84pass+1KNOWN_TEST_FAILURE,0errors/skips,exit1; Phase1=23pass/23,0errors/skips,exit0; total108/107pass/1knownfailure. Replay repeats are not extra tests; olderAgent5audit25/37tests are not included. Current logs under publication/{FROZEN85_RERUN,FROZEN85_SUMMARY,PHASE1_23_RERUN,NATIVE_REPLAY_RERUN}; RESULT_REPRODUCTION_QC confirms ALL nontiming fields match, environment not excluded. Tests are in tests/phase1/ and original tests/{benchmark,innovation}/.

ATTEMPT_LOG plus all namedATTEMPT artifacts retain failed serialization, prior float-return adapter defect, coverage/cost metadata clarification and Bayes internal sampler override. Exclude these attempts from final native/exact conclusions, not from research history. No nativealgorithm failure or novelty inferred from wrapper mistakes.

## 7. Exact reproduction commands

Run only in an auditor-owned checkout/archive of implementation57d703699e7c7d1c323c251c4cac9bd0ca163634. Read the later handoff separately; never execute from a moving branch or edit Agent4's worktree. Inspect pinned source/build/license metadata first; no global install, credentials or data uploads. Windows Bash commands:

    git --no-pager show --stat 57d703699e7c7d1c323c251c4cac9bd0ca163634
    py -3.11 research/innovation/phase1/publication/verify_snapshot.py --commit 57d703699e7c7d1c323c251c4cac9bd0ca163634
    py -3.11 research/innovation/phase1/publication/verify_snapshot.py

First verification reads immutable Git blobs; second verifies actual files in the exact implementation snapshot. Historical handoff digest WILL differ if the second command is incorrectly applied to the later documentation tree. Do not rewrite manifests to hide this expected documentation-only difference.

    py -3.11 research/innovation/phase1/reproduce.py --prepare
    PYTHONPATH=src .cache/innovation/phase1/venv/Scripts/python.exe -m unittest discover -s tests/phase1 -v
    PYTHONPATH=src .cache/innovation/phase1/venv/Scripts/python.exe research/innovation/phase1/publication/verify_h1_counter.py
    .cache/innovation/phase1/venv/Scripts/python.exe research/innovation/phase1/reproduce.py --replay agent5_phase1_replay_01

The exact packages are downloaded/verified in ignored.cache; only audited small LIME archive uses standard setup.py build, no Bayes installscript or fulllegacy stack. Combined --prepare was not run end-to-end during integration: individual audit/install stages were executed and pipcheck/version/sourcebyte checks passed. Agent5 should explicitly test pristine bootstrap compatibility rather than assume it. Preparation can refresh provenance metadata in the auditor's disposable copy; compare/record any differences, never alter frozen evidence. Fresh replay directory/output required; no overwrite. Same scientific fields expected; walltimes may differ. No source/dependency version fallback or source patch without reporting BLOCKED.

Original frozen environment is distinct, Windowsamd64CPython3.13 with NumPy2.3.4 hashedwheel:

    py -3.13 -m venv .venv-sis
    .venv-sis/Scripts/python.exe -m pip install --only-binary=:all: --no-deps --require-hashes -r research/innovation/evidence/solve/SIS_REQUIREMENTS_HASHED.txt
    .venv-sis/Scripts/python.exe -X utf8 research/innovation/evidence/solve/run_validation.py --output-dir .cache/innovation/phase1/agent5_frozen85

Expected exit1 for85tests due solely to retained SISmask failure, not an installation failure. Other platforms require separately audited wheel/environment, not silent pin changes. Full command/pin details in REPRODUCIBILITY.md and publication/AUDIT_PAYLOAD.json.

## 8. Independent-review priorities and decision boundaries

- P0: independently seek any false certification, corrupted target/native semantics or leaked evaluation; none newly demonstrated in scoped checks. Parent/subagent success messages are not independent validation.
- P1: validate augmentedIID/conditionalMCunbiasedness, B/C/T independence, fixedfamily/multiplicity, clipping target, fullrange numerical limits and distinction between certified population target and empiricalT risk. Reassess easy-mechanism null, unmatched costs, Bayes coordinate/posterior-scale semantics and freshenvironment portability. No fullpaper replication or general quality claim.
- P2: confirm missing-counterNone versus measuredzero without changed search; preserve original SISedgecase; distinguish exactprobe_count0 from4rowquerycost. Parent-corrected wrapper errors remain visible.

Main inputs: REPORT.md; RE_REVIEW_REPORT.md; SCIENTIFIC_COMPATIBILITY.md/.csv; EVALUATION_CONTRACT.md; H1_REMEDIATION.md; BAYESLIME_SOURCE_ENV_AUDIT.md; LIME_PILOT_RESULTS.json; BAYES_SMOKE_RESULTS.json; COST_LEDGER.csv; ATTEMPT_LOG.md; publication/AUDIT_PAYLOAD.json; publication/PUBLICATION_QC.md; publication/RESULT_REPRODUCTION_QC.json; publication/SOURCE_ENV_LICENSE_QC.json and manifest/whitelist.

No new experiment arm, harder synthetic mechanism, native RDE/VeriX expansion, real/hidden data, final benchmark freeze, new XAI algorithm or novelty claim is authorized. Return independent audit and human decision before any such continuation. Publication authorization does not promote conditional technical evidence to scientific superiority.
