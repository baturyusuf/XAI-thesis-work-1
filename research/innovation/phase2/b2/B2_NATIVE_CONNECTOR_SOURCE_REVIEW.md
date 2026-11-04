# B2 native LIME connector source review

Authority: amendment8325d9911556855ea7966e112e91a80d786a393d + B2 base841ded9c3544e259fd638003350d31e7cae23686; older auditf32686c2c7e08bdf872a8469609120ee3dfc5441 concerns implementationbf040de8c567aeed5cd2c30470414a297cba8014. No dynamic/native release.

Overall SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED; native RESOURCE_GUARD_BLOCKED. P1-A concrete native source coverage is supplied for independent review; P1-B actual TEST OS connector remains absent. I1/I3 not required or claimed.

## Native identity and behavior

Pinned lime==0.2.0.1 sdist SHA-25676960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781, BSD-2-Clause. All19 package Python files matched archive/installed raw bytes without importing them. NATIVE_LIME_RELEASE_MANIFEST.json identifies each; config requires its exact reviewed digest15dfda532bedc7fbdfee75ad418b634c82f2d62469c33181872368a477ba70fb,19 distinct entries and callback/base files. No native source or wheel was copied/patched/installed.

Worker consumes IMPORT before native module/create_operations imports NumPy/LIME/sklearn. Production binds exactly native_lime_connector and native mode, not a generic plugin or dummy. Python3.11.9/environment metadata/base interpreter/source checks remain. The example approval remains purpose=implementation_only, release flags false, no immutable review commit. It is deliberately not runnable authority.

Frozen class1 uses context closure c0=.25 or c1 float64 sine interaction in prescribed order and omega hex constant; ordered(1-p,p), no normalization. Generation uses center0, nine-row prescribed background, saved actual scaler, two numeric features, no discretization/categories, feature_selection none, instance-centered Gaussian, fixed seed and explicit num_samples128. Native generation is not Q4/QJ and includes original row.

Public explain_instance callback at release lime_tabular.py:355 calls the wrapper once with inverse128x2. That wrapper delegates only to OperationPermit.predict. Public model_regressor is a record-only CapturedRidge subclass: same alpha1/unpenalized intercept/random-state/solver and exactly one super.fit; no monkeypatch, feature-selection replay or second fit. Native lime_base.py:181-198 computes weights, selects both features and performs fit/score/local surrogate prediction. Those last two are surrogate calculations, NOT new frozen-predictor callbacks.

## Finite in-flight boundary

One generation grant covers finite native sampling/preprocessing,128-row callback, one Ridge fit and native explanation construction. Every predictor callback still needs a separate child ISSUE and CONSUME. Internal NumPy/BLAS/sklearn steps are not individually gated; STOP may interrupt the consumed bundle and physical effects may lag. Observed STOP checks precede callback/native fit, but final-check scheduling gaps remain; no I3 proof.

Q4 and fixed QJ m4/m16 use separate unit grants and4/64/1024-row child callbacks. Complete fitted Ridge/scaler/feature order is retained; raw outputs are saved alongside explicit diagnostic clipping and exact binary-rational absolute-loss aggregation. Point reconstruction/c0 checks use declared tolerances; no coefficient repair. QJ is a grid statistic, computational continuous interval[0,1]/NUMERICAL_UNRESOLVED, no false certificate. Reference uses saved data, one exact Ridge normal-equation solve, zero predictor calls; real-proxy nodes/cells NOT_MEASURED. M1/M4 helper contains finite exact definitions; the unspecified W+one-event anchor remains SOURCE_DEFINITION_UNRESOLVED, not full M4 replication.

P0 preventive: no I1/I3/readiness/novelty claim. P1-A is a source candidate, not tested callback behavior; P1-B actual observer/outer/nested TEST/injection source absent. P2 numerical transfer/directed enclosure and complete M4 optional-anchor rule unresolved. All seven cases NOT_RUN;0 imports/fits/predictor calls. Runtime qualification and separate human permission still required.


## Exact current source anchors
- config.py:verify_bound_run: src/innovation/phase2/guard_remediation_v2/config.py:110-187
- worker.py:main: src/innovation/phase2/guard_remediation_v2/worker.py:254-297
- native_lime_connector.py:create_operations: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:11-20
- native_lime_connector.py:NativeOperations.predict: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:35-53
- native_lime_connector.py:NativeOperations._generation: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:70-127
- native_lime_connector.py:NativeOperations._generation.CapturedRidge.fit: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:85-98
- native_lime_connector.py:NativeOperations._generation.callback: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:100-105
- native_lime_connector.py:NativeOperations._evaluation: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:140-167
- reference_arithmetic.py:independent_reference: src/innovation/phase2/guard_remediation_v2/reference_arithmetic.py:149-242
