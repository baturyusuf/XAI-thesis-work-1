# Independent replication protocol and executed scope

2026-10-22. Distinguish A source reproduction, B independent numerical answers, C scientific validation throughout. No inference that a matching toy answer validates a broad claim.

## Executed tiny-only workflow
1. Verify root/branch and pinned commits. Read shared rules and whitelisted public handoffs; never traverse private directories.
2. prepare_sources.py resolves 50 Git entries and copies only A3-I ten modules/eleven tests/LICENSE into evidence/source_copy/agent3_51a6915, with source SHA, blob and byte SHA256. No automatic merge/cherry-pick.
3. Standalone tests derive finite conditioning/truth-table, clipping, tie permutation and bounded-transform answers independently. They import no benchmark internals.
4. test_pinned_implementation.py compares new direct-event sums/Decimal calculations with pinned actual calls: 256 binary-model subset cases; weighted XOR; clipping/native modes; 64 tie/loss configurations; zero coverage; 240 HB grid values; a weighted 243-sample LTT population for two controllers and eligible zero-loss control.
5. Run unchanged A3 tests in copied root and tiny benchmark.synthetic with stdout captured in audit evidence only. Compare semantic fixture/pilot/source-hash fields with immutable published JSON, excluding timestamp/environment/elapsed timing. Recheck source copy digests.

## Commands from Agent5 worktree
- python -B research/validation/evidence/prepare_sources.py
- python -B research/validation/evidence/run_review_checks.py
- Standalone only: python -B -m unittest discover -s tests/independent_validation -p test_h1_reference.py -v (likewise h2/ltt).

run_review_checks.py uses subprocess with explicit cwd/PYTHONPATH, 60-second per-command timeouts and no dependency install. It runs 56 original tests, 23 new checks (15 standalone +8 differential), then the existing tiny pilot (64 calibration +64 evaluation). It writes CHECK_RESULTS.json and text logs; source copy remains byte-identical. This is a tiny diagnostic, not a large benchmark or new method.

## Actual results and limits
All commands completed successfully on Python 3.13.15/Windows. Six pilot statuses and all reasons matched pinned evidence: NO_POLICY_CERTIFIED / NO_RISK_NULL_REJECTED. No selected-policy final risk exists; no null replaced by zero. Exact reference_cases, selective_pilot and source_sha256 fields matched.

Independent unsafe test differs from A3 published 1/243 example: reject/good/bad states with probabilities 1/4,1/4,1/2; C=3/4,R=2/3,alpha=1/2; n=5, two fixed policies. False risk rejection has exact weighted mass 0 for Hoeffding+Bonferroni and 1/1024 for fixed sequence, each <=1/10. This one population is not a general theorem or HB/FWER proof. HB grid uses exact binomial probabilities and 70-digit Decimal formulas (absolute comparison tolerance 2e-13), not certified interval arithmetic.

Not run: real/hidden data, native methods, large simulations, real imputer fitting, cross-platform reproduction or universal numerical/formal verification. Future method replication requires immutable Agent4 artifact and human-approved scope. Any original-code defect would be delivered as minimal unchanged-source repro and handoff, not silently fixed by A5.

## Preparation extension (separate from original Phase0)
Human conditionally accepted the 56+(15+8) evidence and approved a future Agent4 scope, not current native execution. Three new standalone modules prepare accepted-count (3 tests), generic SIS (7, optional existing NumPy) and repeated-deletion (4). Run python -B research/validation/evidence/run_preparation_checks.py for separate preparation evidence; original runner explicitly selects the original four modules and preserves the 23-test boundary. New tests are not Agent4 reproduction. Wait for immutable SHA/handoff; see AGENT4_AUDIT_REQUIREMENTS.md.
