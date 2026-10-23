# Agent 5 — Independent Audit Immutable Handoff
2026-10-22 | Agent4 controlled synthetic references, not new XAI

## 1. Immutable identities and non-modification rule
**Implementation commit:3327e942f8d3abfe851f9513ba2c4a2a30e29a67** on research/xai-innovation.
Implementation tree:52d429fb8e23ad17fb3e394649bcbed33e47a1a4.
Source snapshot ID:sha256:9c5b2eca9453937c58075fccde067cc764469eae40c0381d36749012f482a6c0, the byte digest of evidence/publication/SOURCE_SNAPSHOT_MANIFEST.csv (127 covered files; manifest excludes itself and publication-safety receipt).
This document is delivered by a later documentation-only commit, NOT the implementation commit. Its enclosing full commit SHA is reported separately in the final delivery; HANDOFF_CONTENT_MANIFEST.json binds this document's byte/Git-blob identity to the implementation SHA. A commit cannot contain its own hash. Use both reported immutable SHAs, not a moving branch tip. Git can resolve the document commit with git log -1 --format=%H -- research/innovation/AGENT5_INDEPENDENT_AUDIT_HANDOFF.md.

**Agent5 MUST NOT modify the implementation commit, source, tests, parameters, frozen result records, or Agent4 branch/worktree.** Inspect by git show or extract a copy into Agent5's own approved workspace. Write independent audit artifacts separately. Do not make a failed source test green or tune settings using final results. No new native/real/hidden runs or novelty claims authorized by this package.

## 2. Exact source/test locations
- src/benchmark + tests/benchmark:23 byte-identical files from A3 implementation51a6915ec8f94cf1779609422bd61e8d6b3911c7. Documentation source d42bec729e9e78ae5387720d29360c5d60f38192. evidence/solve/A3_IMPORT_MANIFEST.csv pins each commit/path/blob/SHA256, patchNONE. Upstream Git objects optional for archive reproduction; byte checks mandatory.
- H1 reference:src/innovation/h1_reference.py, tests/innovation/test_h1_reference.py (8tests).
- H2:src/innovation/h2_reference.py,h2_pilot.py, tests/innovation/test_h2_reference.py (7tests).
- Existing accepted-count LTT:src/innovation/ltt_accepted.py, tests/innovation/test_ltt_accepted.py (7tests); transformed controller unchanged in src/benchmark/ltt.py.
- Native SIS loader/counter:src/innovation/sis_native.py; tests/innovation/test_sis_native.py (7tests).
- third_party/google_sis/sis.py:Google commit0d94f8c4d92678ce5f7a0eacae725f79174cfb03, SHA2562718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079. Apache2 LICENSE/copyright unchanged; UPSTREAM_PROVENANCE/SIS_LICENSE_REVIEW record scope. Author-endorsed port, full paper-experiment equivalence UNVERIFIED.

## 3. Reproduction without touching the frozen source
From Agent5's own workspace inspect git show3327e942...:<path>, or extract a selective archive:
```sh
mkdir -p .cache/agent4-source
 git --no-pager archive --format=tar --output=.cache/agent4-source.tar 3327e942f8d3abfe851f9513ba2c4a2a30e29a67 -- .gitignore .gitattributes LICENSE src tests third_party/google_sis research/innovation
 tar -xf .cache/agent4-source.tar -C .cache/agent4-source
```
Run from that extracted root in an Agent5-owned isolated Python3.13 environment with NumPy2.3.4. Tested wheel is Windows amd64/cp313; other platforms require a separately audited lock, not silent replacement. Only SIS requires NumPy; remaining references stdlib. Package installation is a separate Agent5 authorization/security decision, not automatic in this handoff.
```sh
PYTHONPATH=src python -m unittest discover -s tests/benchmark -v
python -X utf8 research/innovation/evidence/solve/run_validation.py --output-dir ../agent4-audit-results
python -X utf8 research/innovation/evidence/publication/check_sis_scope.py
```
Original56pass. Strict combined validation expected exit1:85tests,84pass,1native SIS failure,0errors/skips. Do NOT treat exit1 as hidden success; failed assertion remains visible. Optional --verify-source-objects requires A3 Git objects; archive default checks local pinned bytes without Git metadata. Source snapshot hashes verified before AND after archive validation, without source/evidence mutation. No cross-platform validation claim.
H1 reproduction PYTHONPATH=src python research/innovation/evidence/solve/H1_run_reference.py writes its result; if replaying use a disposable copy, never replace frozen evidence. H2 replay, only if separately approved, uses python -m innovation.h2_pilot --output research/innovation/evidence/solve/NEW_AUDIT_H2_RESULTS.json with frozen config and new output filename; no rerun required to read first results. Full commands/locks in REPRODUCIBILITY.md.

## 4. SIS exact negative control and scope
Input np.ones(2), fully_masked_input np.zeros(2), f(batch)=np.ones(len(batch)), threshold1. Native sis_collection returns one SISResult with sis=[],mask[True,True];4callback calls/5input rows. Expected semantic mask[False,False]. test_constant_score_empty_sufficient_set retains that failing assertion; no patch, xfail, skip or repair.
Source trace:_find_sis_from_backselect447-448 explicitly permits empty SIS; _transform_index_array_into_indexer244-246 maps empty list to(); find_sis532-534 assigns mask[()]=True, selecting all positions. SISResult.mask109-113 promises only SIS coordinates retained. Byte-pinned proof:SIS_EDGE_SCOPE.json and check_sis_scope.py.
Recommendation30-38 is an uninformative fully-masked prediction. Constant score at threshold does not establish that practical condition; the code does not hard-reject this input and documents empty SIS. This is an output-field inconsistency, NOT demonstrated normal-use algorithmic/sufficiency failure: every mask still scores1 in this constant model. Ordinary cases6pass. Keep these two claims separate.

## 5. H1 exact/reference calculations
NOT native PAXp. Fixed2-bit XOR probability vector(1-XOR,XOR), x=(0,0), original predicted label0, separately declared numeric target class1; logical groups individual coordinates, eta1/4. Exact conditional V_Q(S)=Pr[f_label(Z)!=f_label(x)|Z_S=x_S], D_Q(S)=E|p1(Z)-p1(x)| under supplied rational finite joint.
Uniform weights1/4: full subset necessary, empty V=D=1/2. Wrong same-support weights(.7,.1,.1,.1): deletion/exact oracle choose empty, own-Q V=D=1/5; evaluate SAME selected subset under uniformQeval gives1/2. No Qeval re-search; law mismatch not search failure.
Nonmonotone weights(.01,.09,.09,.81): full S single-deletion minimal (each singleton V9/10), yet empty globally feasible V9/50. A small heuristic limitation, not native literature-wide failure. Unary/constant/full/random-subset controls and same-label/nonzero-distortion3/20 included. Tests compare all16two-bit truth tables x4subsets atx00 with A3 and exact minima; no global real-data conclusion.
H1_RESULTS/H1_REPORT/H1_run_reference.py: fresh search/enumeration/fixed-evaluation counters. Uniform deletion8callbacks/3predicates, enumeration4candidates/13callbacks; wrong-Q deletion10/3, enumeration1/5. Oracle privileged, no scalable cost claim. Some extra diagnostic/full-run aggregate cost and runtime NOT_MEASURED; don't impute0.

## 6. H2 bank, scores, split and probe records
Synthetic local-surrogate reference, NOT LIME. Frozen p1(z)=1/4+z/2 for z0/1, M uniform, ordered classes(0,1), target1. Each iid-design base unit has a frozen linear h_E with endpoints independently uniform in{1/4,1/2,3/4}; all main outputs naturally bounded probabilities. Same E/f/M/target per unit across ALL scorers/controllers.
Direct:8fresh score draws, mean abs residual. Learned:existing fixed-cell mean regression on endpoint pair, fitted ONLY to B256 independent units with16MC loss-label draws each; no C/T fit. C512calibration, T512evaluation; loss-probe budgets16/32 plus separate exact T referee. Probe counts NEVER increase n. Base seedsB801/C802/T803, probe seed bases100000/200000/300000; per-unit score/loss streams separated. Full config H2_PRESPECIFIED_CONFIG.json; H2_RESULTS_UNIT_RECORDS.json holds safe synthetic IDs/endpoints/seeded scores/MC/exact losses. V1 unexecuted retained; V2 expanded controller multiplicity before first pilot, no n/alpha/grid/seed tuning. No independent preregistration timestamp claim.
Random/reverse/always/zero controls retained; reverse reuses direct score and is not separate inference cost. Strict raw invalid h rejected; explicit clipping control raw5/8/clipped1/8/invalid1/2/gain1/2 is a DIFFERENT h, never main native-probability gain.

## 7. Controllers and exact guarantee boundary
For each fixed t, A_t=1[q<=t]. Independent bounded MC loss Lhat must satisfy E[Lhat|base unit,E,score randomness]=L_exact. Conditional on independent B fit and IID augmented units, accepted losses given K_t=k are IID from Lhat|A=1, with conditional mean equal latent accepted explanation risk. Accepted-count uses bounded HB test on k accepted losses; k0 gives riskNone/no rejection. This is existing LTT machinery, not novel algorithm.
Transformed: Y_i=alpha+A_i*(Lhat_i-alpha) in[0,1]; E[Y]-alpha=C_t*(R_t-alpha) for C_t>0; bounded HB on all n512. Same declared loss/target/grid/C records/FWER/coverage budget for BOTH controllers; different statistics/power, not forced same p-value.
HB logp=min(0,-n*KL(min(mean,alpha)||alpha),1+log BinCDF(ceil(sum losses);n,alpha)); accepted substitutes k/accepted inputs. Conservative unsafe null R>=alpha, hence covers R>alpha. Exact rational ceiling, floating KL/CDF; not interval-certified. Reject logp<log(1/2160)-1e-12. m9thresholds0,1/16,...,8/16, alpha1/5, per score/controller dr=dc1/240. Full-n coverage lower=max(0,c_hat-sqrt(log(m/dc)/(2n))); require positive lower>=1/20+1e-12. Sixscores x2controllers x(risk+coverage)=1/10 union budget, no independence between policies/controllers needed for Bonferroni. Perfect-bank controls are separate deterministic known-truth correctness checks, not selected pilot families.
Source flags/IDs/seeds cannot PROVE genuine IID, independence, conditional unbiasedness, model stability or fixed policy provenance. At most conditional mathematical guarantee under assumptions, NOT validated statistical theorem/real-world safety. Same C/T units/loss draws acrosscontrollers are paired, not extra independent replicates.

## 8. Preserved outcomes and cost
Accepted-count direct/learned t3/16 certify conditionally; transformed all6NO_POLICY_CERTIFIED. Main12 rows total2eligible/10none, null test points retained. Direct Tcoverage51/128,risk91/816; learned Tcoverage171/512,risk14/171. DIFFERENT coverages, no superiority. Exact known-population referee given fit/selected threshold: direct C13/32,R433/3744; learned C1/3,R1/12. These integrate score noise, not B/C selection uncertainty or empirical violation-frequency validation. Outer probability over calibration, conditional accepted population risk and finite empirical T risk are distinct.
At50% hypothetical rank coverage both risks141/1024. Partial ties may be unreachable by fixed thresholds; not certified deployment risk. Zero policy retains riskNone regardless of hypothetical prefix metrics. No-policy is not loss1 or safe risk0.
H2 logical draws36,864, actual callbacks5,627 including1,024exact-referee/7diagnostic. Two-state within-batch dedup explains draw/call difference; no global cache advantage claimed. Learned labels512calls; direct C/Tscore1020/1016; shared C-loss1024,T-MC1024,T-exact1024. Pilot elapsed7.776s on recorded environment; subcomponent runtime/memory/full-cost matching NOT_MEASURED/NOT_ESTABLISHED. COST_SUMMARY and H2_RESULTS query ledgers, H1 counters, SIS per-case callbacks/rows are preserved.

## 9. Evidence/status inventory
All paths below relative to research/innovation:
- evidence/publication/FINAL_FREEZE_TEST_SUMMARY.json,A3_FREEZE_LOG.txt,A4_FREEZE_LOG.txt:85/84/1, failure untouched.
- evidence/publication/ARCHIVE_VALIDATION_RECEIPT.json:tested implementation tree, no .git metadata, local hash verification before/after, same85/84/1 on same platform.
- evidence/publication/SIS_EDGE_SCOPE.json,H2_FINAL_AUDIT.json,SCIENTIFIC_STATUS_MATRIX.csv:scoped last checks and claim classification.
- evidence/solve/H1_RESULTS.json,H2_RESULTS.json,H2_RESULTS_UNIT_RECORDS.json,INDEPENDENT_H2_CHECK.json,INDEPENDENT_H2_AUDIT.md:raw safe synthetic outcomes/reference reconstruction. Peer independent of H2 implementation, not formal external Agent5 custody.
- evidence/solve/OUTCOME_ARTIFACTS.json,COST_SUMMARY.json:all outcome types, separate costs/missing measurements.
- evidence/publication/IMPLEMENTATION_WHITELIST.txt,SOURCE_SNAPSHOT_MANIFEST.csv,REDACTION_MANIFEST.csv,EXCLUSION_MANIFEST.csv,PUBLICATION_SAFETY.json:publication provenance. Display metadata paths/hostnames normalized; raw originals local only. Scientific result/config/source bytes unchanged. No caches/venvs/packages/other raw third-party source snapshots included; redistribution only unmodified Apache2 SIS with attribution.
Statuses are CLAIM-SCOPED:REPRODUCED means specified implementation/fixture behavior, not whole-paper replication; INDEPENDENT_REFERENCE_CHECKED means source/arithmetic crosscheck, not a theorem; REPORTED applies source paper claims; INCONCLUSIVE to broad algorithm failure/unconditional guarantee; BLOCKED to deferred native methods; KNOWN_TEST_FAILURE to SIS mask assertion; NOT_MEASURED to missing full profiling/replicate reliability. Do not collapse these into scalar scores or count the failed test as successful.

## 10. Agent5 P0/P1 audit priorities
P0 forbidden conclusions:do not infer novelty, literature-wide failure, certified instance/subgroup/shift safety, real-world generalization or native LIME replication from toy results. No source/data/final protocol changes in this audit.
P1:independently prove per-policy bounded-test validity under random accepted count, conditional unbiasedness and fitting/probe separation; review full family/covariance/budget accounting. Source metadata cannot authenticate factual IID. Challenge HB KL/log-binomial-CDF/ceil/float endpoints and coverage rounding;1e-12 guard not global numerical proof.
P1:confirm SIS source-path/output metadata inconsistency vs fully-masked-input recommendation; no normal-use failure claim from this constant control. Preserve known failure, source pin and no-patch distinction.
P1:validate same E/f/law/object/target and raw-vs-clip semantics, local-vs-global minima and support scope; never class a sampler/evaluator/interface issue as explanation failure. Costs incomplete and different coverages; no superiority assertion.
P2:pre-outcome sequence recorded but not independent timestamped custody; synthetic two-state/nine-type model deliberately tractable; original/earlier draft logs are historical, current freeze receipts authoritative. No hidden-dataset labels/manifests/person records in this handoff.
Native Bayes/RDE/VeriX and new XAI development remain deferred pending separate human approval. Agent5 should report independent findings, not silently patch this immutable implementation or overwrite its outcomes.
