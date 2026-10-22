# Agent 4 — controlled SOLVE handoff

2026-10-22 | Reference interfaces implemented; scientific protocol not frozen.

## Ready now
[IMPLEMENTED_API.md](IMPLEMENTED_API.md) documents actual signatures and entry commands; code lives under src/benchmark in Agent3 worktree. Core H1: exact finite conditioning, V_cls/D_Q, logical group size, finite-U property, single-deletion checks, all minimum-cardinality optima. Core H2: native bounded/clip-adapted surrogate loss with invalid/raw/clipped/gain diagnostics, independent fixed-budget sampling, unit-level risk/coverage/prefix AURC/exact-count risk. LTT reference offers Hoeffding/HB plus Bonferroni/fixed-sequence and separate minimum-coverage bound. Split/probe metadata audits reject known misuse.

Use TargetSpec(predictor_id, ordered classes, chosen class, probability scale) consistently. Supply finite normalized joint and explicit support/group schema, tagged SubsetExplanation or LocalSurrogate. Lower q predicts better functional loss. No empty-coverage zero risk. Clip adapter is another explanation object; never hide raw invalidity. Same-support and within-U support relations differ. Unit records, not perturbations, define n.

## Integration prerequisites retained
Read [SOLVE_TEST_REPORT.md](SOLVE_TEST_REPORT.md) and [RE_REVIEW_REPORT.md](RE_REVIEW_REPORT.md). Known-function fixtures and positive/negative branch tests are not native baseline executions. Missing code remains visible in BASELINE_ELIGIBILITY.md; author artifact or separately named faithful reference still required. Bayes/learned-functional-loss/direct independent probing + strong existing LTT remain mandatory candidates. Only direct probing/control-score path is exercised here; Bayes/learned score fitting not implemented.

A4 must pin/hash/version real model and method artifacts, establish callable stability and exact target/game/group/law equivalence, account for native/adapter differences and offline/online/evaluator costs. No native RDE/SIS/PAXp/VeriX/Selective package/API equivalence claimed by this reference kernel. Solver UNKNOWN is not counterexample. Simple exhaustive oracle is a privileged referee, not scalable cheap competitor.

## Pending / forbidden
Human approves next integration scope. No new XAI, novelty, real/large/hidden benchmark, primary/effect freeze or final test access authorized. A2 development allowlist/source/as-of/unit/family evidence still required for any future real branch. H3 preliminary. Attribution/subset H2 loss contracts must be separate; rejecting them from surrogate loss does not reject their methods.

This handoff contains no hidden data links/locations or row manifests. Reference records use synthetic tokens only. Separate executor/provenance artifact binding, full cost ledger/timeouts, real samplers and independent Agent5 audit are not delivered by this minimal API.
