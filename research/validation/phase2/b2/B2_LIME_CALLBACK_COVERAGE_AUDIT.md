# B2 native LIME callback coverage audit

Immutable source1bd1210a6601f5d82a5b288fe995a63aaada552a. Code paths below are under src/innovation/phase2/guard_remediation_v2/. Contract:8325d9911556855ea7966e112e91a80d786a393d, amendment sections3/5; revised requirements lines10-14,69-73. No native import, fit, predictor, reference calculation or test was executed.

## Official release independently verified

**VERIFIED_RECORD:** official PyPI metadata and in-memory sdist bytes identify lime==0.2.0.1,275719 bytes, SHA25676960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781. All19 package Python-file sizes/hashes and LICENSE match NATIVE_LIME_RELEASE_MANIFEST.json; license text is BSD-2-Clause. No extraction to disk, setup, install, package import or source execution. This closes the consultants archive-access limitation, not a runtime gate. Installed private-site bytes and actually loaded modules were NOT inspected; prospective verify_bound_run checks do not constitute observed runtime evidence. Current Git branch API is not substituted for the historical release.

Metadata:https://pypi.org/pypi/lime/0.2.0.1/json . Exact archive URL/hash is in B2_SOURCE_VERIFICATION.json.

## Complete reviewed callback chain

Generation: controller parent unit -> worker.run_frozen_roles:217-249 -> gate.enter_unit -> NativeOperations._generation:70-127 -> public explain_instance(callback):107-109 -> RELEASE lime_tabular.py:340 inverse generation and :355 predict_fn(inverse) -> connector callback:100-105 -> permit.predict -> worker.OperationPermit._callback:76-105 -> gate.issue_callback:215-219 -> gate.consume_callback:220-221 -> NativeOperations.predict:35-53.

Q4/QJ4/QJ16: each has a SEPARATE parent role; _evaluation:140-167 calls the same permit.predict on4/64/1024 fixed rows. Only worker._callback invokes the stored frozen predictor in this reviewed source. Native Ridge.predict/score are surrogate computations, not classifier callbacks. No alternate connector source caller bypass was found. This is coverage of cooperative pinned code, not a sandbox against arbitrary replacement plugins.

| User question | Source assessment / limit |
|---|---|
| Public predict_fn path | VERIFIED_SOURCE in the actual pinned release, not an inferred modern API |
| Every generation predictor callback wrapped | One public callback under these dense classification options; unexpected additional call/size is rejected before new predictor work |
| Q4/QJ same I2 | Yes, separate role and the common callback wrapper |
| Separate child admission | Each predictor callback independently ISSUEs and CONSUMEs on the STOP word; parent fit is not authority |
| STOP while library work is underway | A callback not consumed before S cannot enter; errors commit STOP before optional partial-record persistence |
| Already consumed, not yet entered | ADMITTED_PENDING_START, physical_entry unknown; final check cancels observed STOP but leaves the accepted scheduling gap |
| Native versus dummy | Same runner, permit, gate and ledger. Dummy simulated callbacks use no actual predictor/native work |
| Runtime behavior | UNVERIFIED: imports, actual callback execution, Windows interleavings, dtype/shape conformance and actual solver/fit behavior |

## One native Ridge fit, not two

CapturedRidge:83-99 records saved scaled design/weights/target and delegates to the same Ridge super.fit ONCE; a second fit is rejected. Params alpha1, fit_interceptTrue, random_state=explainer.random_state match RELEASE lime_base.py:188-193 defaults. Public model_regressor is supplied, labels=(1,), top_labels=None and feature_selection=none. RELEASE feature_selection at lime_base.py:73-74 returns all feature indices without its other branches fitting a selector; lime_tabular.py:452 calls the base explainer in the selected-label path. This single-fit conclusion is specific to these options. RELEASE score/predict calls :194-198 use the fitted surrogate; they do not query the frozen predictor. Source supports unchanged optimization intent with capture overhead, not bit-identical runtime/performance without execution. The saved-design exact3x3 solve is reference arithmetic, not another native fit.

## Budget and measurement distinctions

budget.py:32-37 fixes16 generation/fit reservations,8/context,64 callbacks and19520 logical predictor rows; per-slot row sum128+4+64+1024=1220. Every callback unit has exact size and max1 child callback, with no refund/replacement. Reservations, gate-consumed units, wrapper observations, returned calls/rows and unknown physical entry are different fields. Callback result or counters written after S are bookkeeping, not post-S authority. Unknown call results remain null/partial, not measured0.

Reference reserves1092 nodes/1088 cells/1 solve per slot. Current source ACTUALLY implements only a saved weighted normal-equation solve, with0 real-proxy node/cell evaluations and1 solve on completion; reserved ceilings are not measured work. Dummy cost is SIMULATED_UNITS_NOT_MODEL_QUERIES; it cannot validate native runtime. Production verify_bound_run rejects a dummy backend: a future TEST connector is still missing, not a reason to weaken production validation.

## Scientific scope, separate from guard gates

| Target | Present source / evidence status |
|---|---|
| M1/M4 rational anchors | reference_arithmetic.py:53-112 contains Fraction definitions/assertions; NOT calculated in this audit |
| W+one-event | B2-N01/P2: placeholder SOURCE_DEFINITION_UNRESOLVED at:106-110; no full M4 replication claim |
| Native M2 Q4/QJ | Frozen context/class1 predictor and fixed grids present; no native results produced |
| Raw/clipped/invalid/gain | _evaluation:147-165 and stored_loss_diagnostics:170-182 separate stored-float rational grid statistics |
| Numerical uncertainty | QJ is a deterministic grid, not continuous risk; [0,1]/NUMERICAL_UNRESOLVED is honest but not precision success |
| Real-proxy/transfer | B2-N02/P2: independent_reference:149-242 has no reviewed directed integration/transfer certificate; real_proxy NOT_MEASURED |
| Strong context/direct nulls | Saved Q4 outputs and c0 node diagnostics support source hooks, not uniform context safety or population policy certification |

Generation is native Gaussian perturbation plus the fixed original row, not Q4/QJ evaluation law. The weighted3x3 reference penalizes slopes by1 and not the intercept; it uses saved scaled design/class1 responses and invokes no predictor. Rational differences from native coefficients are not bit-exact-solver expectations or a continuous error bound.

B2-N01/N02 minimum: preserve unresolved statuses, bind any later W+event definition and reviewed directed enclosure separately; no guard-source failure should be called mathematical-method failure. Dynamic evidence is needed for native conformance, not authorized now. Continuous scientific readiness remains blocked independently of the lifecycle blocker in B2-L01.
