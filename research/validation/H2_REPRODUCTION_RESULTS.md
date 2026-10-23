# H2 independent unit-record reconstruction (B)

2026-10-22. Same immutable pins as AGENT4_SOURCE_REPRODUCTION.md. Independent recalculate_h2.py imports no benchmark/innovation function: Fraction event sums, independent PRNG ticket loop, cell aggregation, binomial score-noise enumeration and own Decimal HB calculator. Original replay (A) and this reference reconstruction (B) are separate.

## Contract and records
VERIFIED: p1(z)=1/4+z/2, ordered classes(0,1),target1; uniform two-state law; nine equally likely endpoint pairs from{1/4,1/2,3/4} squared, naturally bounded surrogate loss. Fixed E/f/law/target/calibration losses/scores/grid/budgets/T records are shared by both controllers. Only test statistic differs. All1280 unit endpoint/label/seed/score/loss records independently rebuilt: B256,C512,T512; nine learned cells/fallback match B labels only. All108 policy risk/coverage/count/p-value/decision records match.

| Accepted-count selected policy | Calibration threshold | T accepted | Empirical T exact-loss coverage | Empirical T exact-loss risk | Exact known-population coverage | Exact population risk |
|---|---|---|---|---|---|---|
| Direct independent probe |3/16|204|51/128|91/816|13/32|433/3744|
| Learned cell mean |3/16|171|171/512|14/171|1/3|1/12|

Independent T probe-loss means are2911/26112 and1823/21888 respectively: yet another measurement, not the exact T-loss means. Exact population values integrate nine endpoint types and score-probe binomial noise conditional on fitted B and chosen threshold; they do not integrate calibration selection or establish empirical violation-frequency reliability.

Accepted-count has2 eligible score families and4 no-certification; transformed has6 no-certification. Both selected policies are ELIGIBLE_CONDITIONAL, not unconditional safety. Five individual threshold policies pass both gates across the12rows; highest empirical C coverage selects3/16 in each eligible family. Null test points retained. No same-coverage superiority follows from171 versus204 accepted units.

## Risk-Coverage
All six seeded prefix AURC, uniform-tie expected AURC, and54 population-grid points independently match. At hypothetical half-rank coverage, direct and learned both have risk141/1024; **256 is not a score-block endpoint for either**, so this is randomized partial-tie descriptive membership, not the certified fixed-threshold policy. Different tie estimands remain separate. No new primary metric selected.

Numerics: max saved-logp difference1.841e-13; all decisions unchanged. See H2_CONTROLLER_NUMERICAL_AUDIT.md for thresholds/margins/guard limitations and H2_ACCEPTED_COUNT_THEOREM_AUDIT.md for random K/FWER proof. Independent record results: evidence/agent4_3327e942/H2_UNIT_RECALCULATION.json. Finite T means, exact toy population risks and the outer calibration guarantee are NOT interchangeable. No theorem validity claim is established merely by matching these results.
