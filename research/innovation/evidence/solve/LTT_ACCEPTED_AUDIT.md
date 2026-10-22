# Accepted-count conditional-risk LTT audit

## Specification and derivation

For each pre-fixed policy threshold t, let A_t be the deterministic accept decision from the score and independent probe randomness. Under iid base units and independent score/loss probes, the pairs (A_t,L) are iid. Conditional on the total accepted count K_t=k, the accepted losses are iid draws from the conditional law L | A_t=1. Therefore the existing bounded-loss Hoeffding/Bentkus (HB) p-value applied to precisely those k losses tests the unsafe null E[L | A_t=1] > alpha. The conditional p-value remains super-uniform under the null for each fixed policy. Bonferroni at delta_risk/m controls familywise risk rejection across the m fixed thresholds. When k=0 there is no conditional risk estimate or rejection.

Coverage is separately bounded using the original A3 whole-sample Hoeffding lower bound, with n base units and the same fixed-family correction. Policy selection requires risk rejection and the coverage lower bound to exceed the declared floor. The 1e-12 strict numerical guard is conservative.

## Assumption and validity audit

A3 calibrate_ltt is called first for its input, target/loss identity, split, IID-cluster, family-origin, and probe-separation checks; only BLOCKED is used as a guard. Its full-sample risk decision is ignored. The guarantee is conditional on truthful assumptions and metadata: the implementation cannot prove iid sampling, score independence, fixed-family status, stable population, or support/control over shift. With MC loss probes, the observed bounded loss must be conditionally unbiased for the intended latent loss and probe construction must meet A3's guard; if the estimand is not conditionally unbiased, this test cannot certify latent true risk.

Sampling violating the IID assumptions, adaptive policy/threshold selection, leaked fitting, shared probes, unmodeled dependence, or distribution shift invalidate the stated derivation; no replacement guarantee is asserted. The test suite's finite enumeration is only a regression check, not a proof of a general theorem. This is the known accepted-subset construction documented in the A1 LTT guarantee audit, not a methodological innovation. The primary A3 transformed controller remains unchanged and separate.

## H2 predeclaration

Before outcomes: 6 scores x 2 controllers; risk and coverage budgets each 1/240 (global union 1/10); alpha 1/5; minimum coverage 1/20; C=512; thresholds 0..8/16 unchanged. Accepted-count compute is higher when evaluating per-policy subsets.

Parent corrections: materialize input iterators before A3 guard and use A3 rational(score) semantics; regression covers generators and decimal thresholds.1e-12 guard conservatively avoids equality decisions, but is not a formal global floating-error bound. Current targeted tests7pass; initial six-test log retained.
