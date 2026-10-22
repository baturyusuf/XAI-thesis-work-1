# Agent 4 — Controlled SOLVE report
2026-10-22 | Complete with one documented native SIS conformance failure

## Scope and disposition
D1-D5 used only for small synthetic integration. No new XAI method/novelty, real/private/hidden data, final protocol, commit/merge/push. H1b/H2 remain hypotheses. **Existing H2 null mechanisms certify policies on this toy DGP**; no new mechanism is justified. No practical-adequacy margin approved, so broader formal BASELINE_ADEQUATE is NOT_ASSESSED.

## 1. A3 transfer and original tests
23 files copied byte-identically from51a6915ec8f94cf1779609422bd61e8d6b3911c7:10source/11test Python files+2 subtree ignore files. No cherry-pick/merge/helpers. Manifest evidence/solve/A3_IMPORT_MANIFEST.csv binds commit/path/blob/SHA256/patchNONE. Handoffd42bec729e9e78ae5387720d29360c5d60f38192 source/test bytes same.
Original56 passed before adapters and in final validation. Final: **85tests,84pass,1native SIS failure,0errors/skips**. All-tests-pass FALSE; strict runner exit1, no assertion/upstream API weakened. FINAL_TEST_SUMMARY/A3_ORIGINAL_FINAL_LOG/A4_INTEGRATION_FINAL_LOG.

## 2. H1-P exact/reference
src/innovation/h1_reference.py independently sums Fraction metrics and repeated-deletion, NOT native PAXp. Fixed f/target/groups and eta1/4. Exact oracle privileged, cost separate.
| Case | Deletion | Exact/independent result |
|---|---|---|
| Uniform XOR |full{0,1}|minimum size2; empty violation1/2 |
| Wrong masses(.7,.1,.1,.1)|empty|own-Q optimum/violation1/5; SAME subset under uniformQeval1/2 |
| Nonmonotone(.01,.09,.09,.81)|full locally minimal|empty globally feasible9/50; singletons9/10 |
| Unary3-bit / constant|{0} / empty|known-sufficient controls |
| Random subset seed90210|{0,2}|size2/XOR violation1/2, chosen before evaluation |
| Same-label p1=.6/.9|label violation0|mean abs distortion3/20 |
Uniform deletion8callbacks/3predicates; enumeration4candidates/13callbacks. Wrong-Q deletion10/3; enumeration1candidate/5callbacks. Qeval never reruns search.8 tests include16 truth tables x4subsets against A3 metrics/cardinality. H1_RESULTS/H1_REPORT contain counts; runtime NOT_MEASURED. Early draft metric/threshold/cost errors corrected with attempts retained; not final evidence. No scalability/native-rival failure inference.

## 3. H1-M Google SIS native
Google0d94f8c4d92678ce5f7a0eacae725f79174cfb03, Apache2, source unchanged/hash checked. Author-endorsed NumPy port; exact experiment-version equivalence UNVERIFIED. Loader/counting adapter does not transform outputs. Native fixed replacement/score threshold, NOT H1-P.
Isolated .venv-sis Python3.13.15/NumPy2.3.4 binary wheel only, no system-site/global changes. Wheel inspected/hash+canonical URL verified.7tests:6pass/1retained failure. Full/sparse/no-SIS/tie/nonlinear/broadcast cases match independent enumeration. Constant scorer already sufficient at fully masked baseline: sis=[] but mask=[True,True] instead of[False,False]. Pinned-source empty-index edge, NOT general SIS/paper failure. No patch/mask repair;4calls/5rows retained. SIS_REPORT/RESULTS/ENV/PROVENANCE detail source/costs.

## 4. H2 strong null
**Synthetic local-surrogate reference, NOT LIME.** p1(z)=1/4+z/2; z uniform0/1. Each iid-design unit has frozen h endpoints independently uniform{1/4,1/2,3/4}. Same h/f/target/law for all scorers; natural bounded probabilities. B256/C512/T512; fit-label16/direct-score8/C-loss16/T-loss32 probes plus exact referee.
Fixed-cell mean regression fits labels only onB. Independent score/loss draws, observation-level n, fixed threshold family beforeC.6scores x2existing controllers; alpha1/5,c_min1/20, risk/coverage each1/240, union1/10. V2 added accepted-count reference/multiplicity BEFORE outcomes; original unexecutedV1 retained. No sample/threshold/seed retuning.
| Accepted-count score |Threshold|T coverage|T exact risk|Exact population C/R given fit |
|---|---|---|---|---|
| Direct probe|3/16|51/128=.39844|91/816=.11152|13/32;433/3744=.11565 |
| Learned cell mean|3/16|171/512=.33398|14/171=.08187|1/3;1/12=.08333 |
Transformed A3:6 NO_POLICY_CERTIFIED. Accepted-count:2 ELIGIBLE_CONDITIONAL/4 NO_POLICY_CERTIFIED. Random/reverse/always/zero never certified; null test points retained. Perfect-bank control certifies under BOTH controllers. Accepted-count construction is existing LTT, not new algorithm; A3 unchanged. Guarantee depends on genuine IID/fixed-family/bounded unbiased loss/independence/numerics, not IDs/seeds. One fit/C realization, no empirical violation-frequency study.
At descriptive50% rank coverage both direct/learned risk141/1024=.13770. Partial-tie rank diagnostic, not necessarily achievable/certified threshold policy. Zero-accept risk stays undefined; hypothetical prefix curves do not override it. H2_RESULTS/UNIT_RECORDS preserve all12 outcomes; independent reconstruction matched arithmetic.

## 5. Cost, adapters and deferred methods
36,864 logical draws,5,627 actual model callbacks including1,024 exact-referee/7diagnostic callbacks. A3 aggregates duplicate draws per tiny2-state batch, so probes!=model rows. Learned labels512calls; direct C/T scoring1020/1016; common C-loss1024/T-MC1024/T-exact1024 separately. Pilot7.776s; some component runtimes/memory NOT_MEASURED; matched-total-cost NOT_ESTABLISHED. No superiority from different coverage/cost.
Clipping diagnostic raw5/8/clipped1/8/invalid1/2/gain1/2; native strict rejects. Changes h, not fidelity innovation. Rational fixtures needed no general float bridge; invalid exact-sum float rejected without normalization.
Bayes/RDE/VeriX retained and not run; DEFERRED_NATIVE_PLAN.md. Historical LIME0.2.0.1 private API has no required sampling_method, so currentHEAD mismatch is not proven declared-release incompatibility. No extra install.

## 6. Independent review and next gate
RE_REVIEW_REPORT.md P0/P1/P2; independent source/arithmetic reconstruction INDEPENDENT_H2_AUDIT.md is not formal Agent5 custody. OUTCOME_ARTIFACTS/COST_SUMMARY/SOLVE_METHOD_STATUS and SOLVE_AGENT1/3/5_HANDOFF records ready. REPRODUCIBILITY.md commands reproduce tests/results; validator keeps native failure nonzero.
Next human decisions: external A5 numeric/theorem review; native LIME/Bayes priority; SIS upstream-edge policy; full cost profiling/richer synthetic mechanisms; separate RDE/verifier environment. New algorithm phase neither authorized nor supported by these outcomes. All work remains uncommitted in own worktree; main/other agents unchanged.
