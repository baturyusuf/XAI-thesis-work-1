# Independent H2 audit

**Disposition: no P0 defect found; proceed only with conditional-synthetic wording.** Audit was read-only apart from this report and INDEPENDENT_H2_CHECK.json. No pilot rerun, production edits, private data, or upstream edits.

## Independent reconstruction

I parsed H2_RESULTS_UNIT_RECORDS.json and independently replayed the seeded two-state draws and Fraction sums; I did not call the H2 calibration or metric helpers. All 256 fit, 512 calibration, and 512 evaluation rows were present. All nine endpoint pairs occurred in fit, and rebuilt cell means matched the exported existing fixed-cell mean regression. Direct/reversed scores, random scores, fit labels, MC loss means, exact evaluation losses, role callback counts, and logical draw counts replayed. The 2,304 expected probe batches are accounted for; all role/base seed values and unit IDs were unique.

From C rows I separately recalculated both accepted-only and transformed bounded-loss HB log-p values, Bonferroni threshold multiplicity, coverage lower bounds, eligible threshold selection, and the chosen T point sums. All 12 score/controller threshold outcomes and reported exact/MC test point metrics matched. Every result retains all nine threshold rows. Ten result rows correctly have no selected policy and null T points; these are not dropped observations. C deliberately uses 512 MC loss records and no exact C losses; T preserves all 512 exact loss rows.

The exact selected-population diagnostics also independently reproduce by enumerating the nine endpoint pairs and integrating the eight-probe binomial score noise: direct probe coverage/risk = 13/32 and 433/3744; learned fixed-cell mean = 1/3 and 1/12. These are conditional exact synthetic-population calculations: they hold the realized B fit and selected threshold fixed and integrate score-probe noise only, not B/C selection uncertainty. They are not empirical validation. Full check values are in INDEPENDENT_H2_CHECK.json.

## Source / design review

- src/innovation/h2_reference.py:14-17 freezes the same target, two-state law and endpoint support; :24-30 defines the shared unit/surrogate; :45-47 routes each role through the same functional loss and records its logical draws; :58-66 is a fixed-cell mean fit on B (not LIME); :68-84 integrates finite population and direct-score probe noise; :86-98 keeps strict rejection and explicit clipping diagnostics separate.
- src/innovation/h2_pilot.py:31-37 fits score labels on B; :39-57 builds disjoint C/T banks with one score stream and a separate loss stream per unit; :58-62 validates probe separation and split roles; :63-74 selects thresholds from C only and evaluates chosen thresholds on T; :75-85 records descriptive metrics, controls, and explicit cost limitations. All six scores share the same unit endpoint pairs, frozen target, surrogate rule, and law. Reverse derives from the direct score rather than receiving independent inference cost.
- src/innovation/ltt_accepted.py:20-55 first reuses A3 calibration guards, then tests only accepted calibration losses for conditional risk and uses all calibration units for coverage. For a fixed threshold and IID base units, acceptance independent of its loss probe makes accepted losses IID from the conditional accepted-loss law; its risk p-value is therefore an accepted-count conditional test. The threshold family is Bonferroni-adjusted.
- src/benchmark/ltt.py:80-150 contains the reused guard and existing transformed-HB controller. In particular :97-126 checks declared assumptions, split membership, repeated units, target/loss IDs, probe separation and MC probe counts; these metadata checks cannot prove scientific assumptions. src/benchmark/provenance.py:52-63 validates declared stream/seed/token separation. A3 source hashes embedded in H2_RESULTS match the recorded files.

V1 is labeled PREDECLARED_NOT_RUN; V2 adds a second controller and positive control and changes each risk/coverage allocation from 1/120 to 1/240, maintaining total union budget 1/10 over six scores x two controllers x risk and coverage. Scores, thresholds, alpha, minimum coverage, sample sizes, and seeds are unchanged. The result config hash matches V2. This is an accounting change needed for the expanded multiplicity, not outcome-driven scientific retuning. Artifact contents support the stated version sequence, but I cannot independently attest chronology from untrusted file timestamps.

The saved query ledger distinguishes logical draws from unique-state predictor callbacks. Independent replay matched 36,864 logical draws and 5,627 actual callbacks including 1,024 exact-referee callbacks and seven diagnostics. Each role touched two unique support states. Runtime for the native method, peak memory, and matched total cost are explicitly NOT_MEASURED / NOT_ESTABLISHED; there is no matched-cost superiority result.

## Findings

### P0 — none

No unsafe implementation defect found in the reviewed accepted-count calculation or its A3 guard reuse. The result is conditional, not an unconditional certification.

### P1 — qualification required

1. Validity depends on genuine IID base units, fixed score/policy family, independent B/C/T, score/loss probe independence, and bounded unbiased MC loss. The pilot sets all Assumptions flags true and checks declared provenance only; the code cannot establish these conditions outside this synthetic generator.
2. Neither seeded finite-sample success nor exact finite-population integration proves empirical reliability, transport, subgroup safety, shift robustness, efficacy, or a practical advantage. Preserve “conditional synthetic reference” language.
3. No native LIME is implemented or assessed. The learned reference is fixed-cell mean regression, not LIME. Matched total cost is not established.

### P2 — interpretation / provenance

1. V2’s changed multiplicity allocation is appropriate for adding a second controller, but pre-outcome chronology is a declared artifact fact rather than independently timestamped custody.
2. The accepted-count and transformed controllers use different valid test statistics, so their differing synthetic power is not a like-for-like method superiority finding. The deterministic-perfect-bank positive control establishes only that the references can certify an ideal bank; it is not efficacy evidence.
3. The explicit clipping control changes the surrogate: invalid raw output is rejected, while an explicitly clipped adapter reports raw absolute loss 5/8 and clipped loss 1/8. This must not be presented as algorithmic improvement. Primary pilot records are native probability-valued with zero invalid rate.

## Confidence / independence limits

High confidence in artifact arithmetic and saved-record consistency; moderate confidence in the conditional theorem/code reading; no claim of formal proof or external provenance. This audit author previously contributed H1, so it is independent of H2 implementation at source/reconstruction level but is not independent Agent5 external custody. No SIS/H1/H2 code or other evidence was modified.
