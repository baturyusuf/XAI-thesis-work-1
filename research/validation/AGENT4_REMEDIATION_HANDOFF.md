# Remediation handoff — proposals, no source patch

2026-10-22. Responsible implementation pin3327e942f8d3abfe851f9513ba2c4a2a30e29a67; handoff305fb2f30bdcac1bf852a2f2c9f226346869fdc2. No Agent4 source/test/config/result changed. Original85 outcome remains84pass/1knownfailure.

## R1: empty SIS mask conformance (P2, confirmed)
Minimal unchanged native fixture: x=ones(2), baseline=zeros(2), constant-one batch function, threshold1. Empty SIS coordinate sequence becomes index(), then mask[()]=True changes every position. Returned[]/[True,True] conflicts with retained-coordinate semantics; expected empty mask allFalse. Source pins/upstream bytes and independent tests are in GOOGLE_SIS_EDGE_CASE_AUDIT.md, including an issue draft. No external issue/message sent.

Human may authorize a separate upstream fix or explicitly named adapter/patch later, with diff and native-versus-patched records. Alternatively constrain/reject the empty branch with a clearly revised contract. Preserve this immutable original and the failing conformance test; do not skip/xfail/delete it to claim all-green. Source only recommends an uninformative fully masked input; the constant fixture is not ordinary-use sufficiency evidence.

## R2: missing callback measurement (P2, confirmed API limitation)
For uniform XOR, repeated_deletion with omitted callback_counts returns model_callbacks0 while predictor executes8 calls. Counter-supplied frozen outcomes are unaffected. Future approved revision should use None/NOT_MEASURED/availability flag or require instrumentation, with regression preserving no-measurement versus measured-zero distinction. Reproducer is the parent H1 callback test. No source change applied here.

## No numerical controller fix justified by this audit
Random-K accepted-loss derivation, conditional MC target, bounded HB arithmetic, exact ceiling and108 frozen policy decisions agree. Do not adjust alpha/delta/grid/n or choose a controller after seeing calibration without multiplicity. Current sixscore/twocontroller family allocation is valid under assumptions and sums to1/10.1e-12 is a heuristic conservative boundary buffer, not formal interval arithmetic; broader numerical/large-n/near-endpoint claims need a separately approved error policy or certified implementation.

## Reporting requirements before broader claims
Keep conditional certification, finite T estimates, exact population referee and hypothetical rank points distinct. Preserve all no-certification/missing outcomes and NOT_MEASURED costs. Native/frozen-target compatibility, total cost, practical margins and genuinely independent source validation must precede superiority/gap claims. Current accepted-count success weakens an H2 new-method-necessity inference; no new algorithm is authorized.

Any fix requires responsible-agent new immutable SHA plus safe diff/handoff and unchanged-counterexample A5 re-review. Real/hidden/final access, new native installations and novelty decisions require separate human approval. This turn authorizes local audit deliverables only; no push or merge.
