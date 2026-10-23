# Agent5 independent Phase1 audit handoff

## Custody and fixed identifiers
New source/config/result manifest SHA256: 07e537056c4121fcad23cedcfd06b1fb9ca32549fdea6ac4bdc46a30956f80e1. SOURCE_MANIFEST.csv enumerates25files. SNAPSHOT_ID.json records its identity. No new Phase1 commit/push performed; this is a content-addressed local handoff, NOT remote Git immutability. A published Git artifact needs separate approval.

Base HEAD305fb2f30bdcac1bf852a2f2c9f226346869fdc2; original frozen implementation3327e942f8d3abfe851f9513ba2c4a2a30e29a67; Agent5 audit2992eeee9d6436d62846e8190ed129bd3d9852ea verified on GitHub. Original127file manifest digest9c5b2eca9453937c58075fccde067cc764469eae40c0381d36749012f482a6c0 unchanged.23Agent3files byte-identical to51a6915ec8f94cf1779609422bd61e8d6b3911c7. Do NOT modify frozen implementation/audit/pinned native source/results or this snapshot. Reproduce in auditor-owned copy/new output paths; fixes require new snapshot.

## Source and tests
New source src/innovation/phase1/{h1_reference_v2,float_adapter,native_lime,lime_pilot,bayes_smoke}.py. Tests tests/phase1/test_{h1_counter_v2,float_adapter,lime_native,bayes_native,phase1_records}.py.

Frozen suite rerun in original3.13NumPy2.3.4 environment:85total84pass1SISfailure0errors0skips,exit1. New compatible-minimal3.11:23total23pass; disjoint108total107pass1knownfailure. Do NOT count failed assertion as pass or add prior25/37Agent5checks here. TEST_FINAL.txt/FROZEN85_RERUN.txt are actual logs. REPLAY_CHECK.json confirms actual same-environment replay, not independent statistical replication.

## H1 remediation
Only newv2 returns model_callbacks=None,unique_states=None without ledger. XOR still executes8callbacks/3predicates; supplied counter reports8. Measured0 differs fromNone. Supplied counters remain LIFETIME snapshots, not deltas. Search law/subsets unchanged. Original exact/nonmonotone/local-global examples retained at3327e942 and prior independent audit. No PAXp replication claim.

## Retained SIS counterexample
Google0d94f8c4d92678ce5f7a0eacae725f79174cfb03, source SHA2562718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079, Apache2.0. Unchanged test_constant_score_empty_sufficient_set: x=ones2,fullymasked=zeros2,constant1scorer,threshold1; expected emptySIS/allFalsemask, actual[]/[True,True],4calls5rows. Emptyindices->tuple()->mask[()]=True. Baseline already sufficient, unlike recommended uninformative use. Output-field inconsistency, NOT demonstrated ordinary-use sufficiency failure. Preserve failing test; no patch/skip/xfail/issue.

## Native LIME and numerical adapter
Actual release0.2.0.1 SHA25676960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781, BSD2, NOT current Git API with same version string.19installedpyfiles match archive. Check LIME_SOURCE_AUDIT/SOURCE_INTEGRITY/requirements.lock/WHEEL_AUDIT before execution.

Native Gaussian perturbations around-instanceTrue, no discretization/feature selection,128samples. Documented model_regressor hook captures default Ridge(alpha1,interceptTrue) and scaler; no-hook comparison passes bitwise. Full h is not coefficients alone or native R2/local_pred. Same estimator evaluated rowwise for fixed numerical behavior. No native source patch. Explicitclip(h) supplies bounded LTT loss; raw loss/invalid/clipping gain retained. No normalization of f or fake Fraction-simplex support. Selected scalar float values become exact binary Fractions and means stay Fraction. Analytic-real tanh is not numerical target.

## New H2 native bank and controllers
P1=.5+.18tanh(x0)+.12tanh(x1), output(1-p1,p1), target1. Fixed9point background; B32/C64/T64 augmented IID-design units. Generation128; B labels16; directscore8; Closs16; Tloss32 plus exact four-offset unit average.736role seeds with no collisions,448batches. Score/loss offset indices and seeds serialized. B-only quality Ridge fit. Different seed metadata is not proof of IID; inspect conditional-unbiasedness. Evaluation uniform four offsets(+/- .25 each) deliberately differs from native Gaussian/kernel law.

A_t=1[q<=t], grid{0,1/50,1/20,1/10,1}. Direct/Blearned Ridge/random/reversed all use SAME h_Lbank/loss. Each family risk1/80 and coverage1/80 split among5thresholds; total4*(1/80+1/80)=1/10. Shared losses allowed by Bonferroni; no independent-policy assumption.

Conditional accepted-count test: given independent fittedB/fixedfamily and K=k>0, selected augmented-unit losses must be IID from accepted law, bounded and conditionally unbiased for clipped computational loss given explanation/score/acceptance randomness. HB p=min(1,exp(-k*KL(mean,alpha)),e*BinomCDF(k,alpha,ceil(sumlosses))) if mean<alpha, else1; K0=>p1,riskNone. Alpha1/5. Coverage lower=max(0,K/64-sqrt(log(5/delta_coverage)/(2*64))); positivecoverage/floor1/20 separately. Choose maximum calibration coverage among eligible policies, not afterT. Inherited floating HB uses1e-12guard, NOT intervalproof.20policies independently checked with65digitDecimal/exactcounts.

Original transformed test uses T_i=alpha+A_i*(Lhat_i-alpha), E[T]-alpha=C*(R-alpha), fulln rather than acceptedk. NOT newly selected/rerun on nativebank; frozen6score2controller1/240budgets remain unchanged. Do not conflate old/new allocations, predictors, banks or population claims. No perturbation inflation of n64.

All four newfamilies certify conditionally, at differentCthresholds but same64acceptedT,coverage1 and exact empirical UNIT-risk0.0116537541. Random/reverse success is a null against necessity in this easy setting. Same-halfcoverage/prefixAURC descriptive only; no superiority or matchedcost conclusion. Four-point exact unitloss is NOT population integration over centers/native generation randomness. No individual/shift guarantee or observed population-certification frequency.

## Native Bayes separate arm
Modeling-Uncertainty-Local-Explainability@72c4330bc7d29150b55018b0946f85f7df88e107,MIT; rawsourcehashes in BAYES_SMOKE_RESULTS match pin. Threecenters128samples,focusFalse,native mean-centered sampler,original-coordinateBLR,penalizedintercept. No internal/source patch in final. Default10000posterior draws. h_Bbank distinct from h_L; no posteriortransfer/BayesSHAPfidelity substitution. s2/radii/native predictive output not fidelity certificates. Native sqrt(s2*(1+xVx)) is Student-t scale under code's IG sampler, not full marginalSD. BayesLTT/calibration NOT_MEASURED.

## Costs and preserved attempts
LIME512batchcalls25344modelrows: generation20480,Blabels512,directscores1024,Closs1024,Tloss2048,referee256. Exact LossObservation.probe_count0 means noMCsampling, NOT zeroqueries: explicit cost1call4rows perreferee. Charge Bgeneration4096+labels512+scorefit to learned; standalone direct needs noB. Fit/generation times nested, do not doublecount. Peakmemory/setup/isolatedBayesposterior timing NOT_MEASURED, matchedtotalcost NOT_ESTABLISHED. Bayes percenter1x128generation+1x4evaluation combinedwalltime, not comparable toLIME160fits.

ATTEMPT_LOG retains serialization error, former float-mean adapter problem, coverage/costmetadata clarification and Bayes internal-sampler override. Only final non-ATTEMPT JSON supports current native/exactclaims. No nativealgorithmfailure inferred from wrappermistakes.

## Reproduce and priorities
Use REPRODUCIBILITY.md in auditor-owned snapshot copy. Preparation py -3.11 research/innovation/phase1/reproduce.py --prepare downloads/audits exact packages then local .cache install only. Combined prepare entry was not rerun end-to-end; individual stages were executed. Actual replay command .cache/innovation/phase1/venv/Scripts/python.exe research/innovation/phase1/reproduce.py --replay independent_audit_01 runs both nativeoutputs and23tests. Originalstrict suite requires originalSISenv/freshoutput, expectedexit1.

P0: independently seek falsecertification or semantic corruption; none newly demonstrated here. P1: IID/conditionalMCunbiasedness, fullrange numeric soundness,clip-vs-native target,easy-null adequacy,Bayes scale and unmatchedcosts. P2: missingcounterNone,retainedSISedgecase,exactreferee cost. Verify manifest before/after. Do not adopt parent/subagent success messages as evidence. Agent1/3 can use REPORT,SCIENTIFIC_COMPATIBILITY,OUTCOME_ARTIFACTS,COST_LEDGER without private data.

No new algorithm/novelty, real/hidden data, heavyRDE/VeriX, protocolfreeze, mainmerge, automaticcommit/push or externalissue. Return independent review before next human decision.
