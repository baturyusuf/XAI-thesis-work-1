# Agent4 cost and probe audit

2026-10-22. Frozen implementation3327e942f8d3abfe851f9513ba2c4a2a30e29a67. A strict replay and B independent seed/ticket/event reconstruction agree; C full matched-cost superiority remains NOT_ESTABLISHED.

## H2 ledger independently reconstructed
| Role | Logical draws | Model callbacks |
|---|---:|---:|
| B256 fit labels,16 each |4096|512|
| C512 direct score,8 each |4096|1020|
| C512 calibration loss,16 each |8192|1024|
| T512 direct score,8 each |4096|1016|
| T512 MC evaluation,32 each |16384|1024|
| T512 exact referee |0 random draws|1024|
| Diagnostics |0 random draws|7|
| Total |36864|5627|

VERIFIED: independent per-batch draw sets recover MC callback counts; exact-referee count follows two support points per unit. Diagnostic7 is source-derived2+2+1+2 and separately confirmed by a fresh runtime counter around the actual primitive, not by replayed random draws. Sampling evaluates a unique drawn state once per batch and weights by frequency. Logical count differs from callbacks; all roles together have only two distinct possible model inputs, but NO global cache was used. Do not interpret two unique states as only two actual calls, or5627 as36864 actual forward calls. A full probability vector counts once. Exact referee1024 calls are not free, and not scorer input. Diagnostic7 includes strict-invalid early exit after one model call.

Learned score has512 B label-generation callbacks; inference on known endpoint cell uses no model queries, but its CPU/time/memory is not zero or independently profiled. Direct C/T scores cost1020/1016. Reversed score explicitly reuses direct values; it is not independently remeasured. Calibration/evaluation losses are common permitted comparison data; shared values do not create new independent repetitions. Do not multiply common loss work by twelve to describe actual physical calls, or hide it in method-level deployment cost.

All1280 unit IDs and2304 MC batch seeds, role assignments and probe counts reconstructed; stream-ID/draw-token construction was source-inspected and the original validator replayed, but batch stream/token records were not serialized and independently compared. This is a provenance-granularity limit, not demonstrated reuse. fit seeds100000+2i, C score200000+2i/loss+1, T score300000+2i/loss+1. Random control score has its separate seed range. B/C/T endpoint banks use801/802/803, fixed scores fit only B, no C/T labels enter cell means. Exact T referee has no RNG. Distinct seeds and IDs are declared separation and reproducible simulation, NOT mathematical proof of independent MT streams or factual real-world IID. The ideal stochastic product-law/conditional-unbiasedness claim remains conditional; no violation-frequency experiment or real-data guarantee.

## H1 and SIS costs
For A4 one subset metric: one base probability-vector callback plus one per positive-mass matching completion. Probability vector is reused for label/scalar, unlike repeatedly querying those separately. Fresh ledgers: uniform deletion2+3+3=8 callbacks/3 predicates; enumeration5+3+3+2=13/4 candidates; wrong-law deletion2+3+5=10/3, enumeration empty5/1. Fixed selected-Q evaluation uses another fresh ledger, never Q_eval re-search. These counters are verified, not a scalability comparison: exact oracle has privileged law/support and solves a different global problem. Extra diagnostic/full-run aggregate callbacks and H1 runtime stay NOT_MEASURED.

Native SIS empty case independently returns4 calls/5 batch rows; ordinary-case counts are preserved by the original tests. Native setup/import/runtime is not a matched method comparison. Original H2 elapsed7.776s is recorded, not a cross-platform or total-cost superiority statistic; replay timing intentionally excluded from equality. Full peak memory, fine-grained explanation/score costs and native real-method costs stay NOT_MEASURED.

## P2 optional measurement availability
Confirmed separate API ambiguity: repeated_deletion(...,callback_counts=None) reports model_callbacks=0 while actual wrapped predictor runs8 times on uniform XOR. Frozen artifacts supply CountingModel and are correct; this is NOT an error in reported8/10 counts or search quality. Missing measurement must be labeled unavailable, not interpreted as zero cost. Minimal test: test_h1_callback_counts_and_missing_ledger_scope in test_agent4_unit_record_audit.py. Recommend an explicit availability flag/None/required ledger in a future approved revision; no patch here.

Evidence: H2_UNIT_RECALCULATION.json and original COST_SUMMARY.json; reproduction logs; test_agent4_unit_record_audit.py. Full cost superiority and real-method efficiency remain BLOCKED/NOT_ESTABLISHED.
