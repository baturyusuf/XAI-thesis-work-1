# Bayes score identity correction — future eligibility only

2026-10-26. Published as part of the conditionally approved D1a source bundle; static primary/source review and algebra, not fitting or comparative validation. Publication does not activate a Bayes implementation or new algorithm. **All Bayes routes are EXCLUDED from D1a.** This corrects the future B09 identity in the e5 design; it does not silently activate additional scorers or rewrite historical sources.

## 1. Verified primary and source
- Slack et al., *Reliable Post hoc Explanations: Modeling Uncertainty in Explainability*, [arXiv2008.05030v4](https://arxiv.org/html/2008.05030v4), §3.1 Eqs5-8, §3.3 Eq11 and AppendixA read directly. The paper's weak-prior example is not identical numerically to a native zero-hyperparameter limit.
- Author `dylan-slack/Modeling-Uncertainty-Local-Explainability` commit **72c4330bc7d29150b55018b0946f85f7df88e107**, [bayes/regression.py](https://raw.githubusercontent.com/dylan-slack/Modeling-Uncertainty-Local-Explainability/72c4330bc7d29150b55018b0946f85f7df88e107/bayes/regression.py). Retrieved text SHA256 **f451ee33398175e6c6662fde3990975b6b53712d4b8ff86d42b80f4b8671773e**, independently matched the A1 pinned record; no import/execution.
- A1 handoff/source requirements at6a010862cc4cbf97886b19095a030e3db077a638 confirm this distinction; published A5 eligibility at a96ec5315de98b57848a659083b2fd3028775ba3 leaves B09 quality/native frontier pending. These are not new performance results.

## 2. Three different mathematical objects
Let X include the intercept, W be native proximity weights and phi_hat the fitted coefficient vector; v denotes the stored field `s_2`, NOT its square again.

**Native statistic (paper Eq7):**
`v = ((y-X phi_hat)' W (y-X phi_hat) + phi_hat'phi_hat)/N`.
`fit` lines48-57 assign BOTH `self.score=v` and `self.s_2=v`, plus `self.N=N`. This is penalized weighted residual scale, not ordinary unpenalized MSE, a PDF, R2 or actual clipped-Q loss. Default native l2=True/zero-centered coefficient prior penalizes the intercept too. The constructor rejects a supplied informative prior; do not silently replace the native path by a general-prior derivation.

**Paper error-density at zero (Eq8):** for fixed noise-prior n0,sigma0^2,
`nu=N+n0`, `b=(n0*sigma0^2+N*v)/(n0+N)` is the Student-t SCALE SQUARED.
`d0 = Gamma((nu+1)/2)/(Gamma(nu/2)*sqrt(nu*pi*b))`, for b>0,nu>0.
This is the density f_epsilon(0), NOT P(epsilon=0), which is0 for a continuous nondegenerate law. Density can exceed1 and has inverse-output units. Eq8's scalar error law is not the z-indexed posterior predictive; do not insert changing spatial/proximity normalization and call it the same score. No dedicated density-at-zero API was found in this pinned regression module; a reconstruction is PAPER_DERIVED, not a shipped native field.

**Proposed Q-integrated predictive adapter:** native `predict` lines79-99 returns h_B(z) and scale `sqrt(v*(1+a_z' V a_z))` with augmented original-coordinate a_z. With the native IG(N/2,N*v/2) route, `Y_post-h_B(z)` is modeled t_N with that scale. For N>1,
`A_Q = c_N*sqrt(v)*E_Q sqrt(1+a_z' V a_z)`,
`c_N = 2*sqrt(N)*Gamma((N+1)/2)/((N-1)*sqrt(pi)*Gamma(N/2))`.
This is a DERIVED posterior predictive expected absolute residual, including observation-noise AND coefficient uncertainty, not native s2/Eq8. Native predictive SD additionally multiplies scale by sqrt(N/(N-2)) for N>2. The adapter is not an unbiased estimate of E_Q|f(z)-clip(h_B(z))| and need not be bounded1; clipping either h or posterior variables changes its formula/target. A fixed proxy could later be calibrated against independent actual bounded losses, but no calibration is performed or approved here.

## 3. Ordering equivalence — conditional algebra, not new methods
For fixed N>0 and common fixed valid prior, b increases strictly with v; d0 decreases strictly. Under the native limit b=v, `d0=c_density(N)/sqrt(v)`. Thus lower positive finite v and higher d0 produce the SAME ordering/ties in opposite directions. These are aliases of one native-error proxy, not independent algorithms. To compare threshold policies, map thresholds AND acceptance orientation exactly; independently interpolated quantile grids/nonlinear transforms need not give identical policies on unseen units. Numerical overflow, collapse or unmapped extra grids can create extra tested policy variants requiring multiplicity accounting, not extra algorithmic novelty.

For the predictive adapter write `K_i=E_Qi sqrt(1+a_z'V_i a_z)`. At fixed N>1, `A_Qi=c_N*sqrt(v_i)*K_i`. A common finite positive K (e.g. common design V, coordinate map and Q) suffices for the same lower-is-better ranking as v. Fixed N/prior ALONE does not fix K: different native random designs, weights, scalers or Q may change it and reverse the products. Pairwise ordering needs `v_i*K_i^2 <= v_j*K_j^2` when comparing a proposed v_i<=v_j ordering; no unconditional equivalence theorem is claimed. If K is proved common, count the adapter as a more expensive alias/ablation, not a third algorithm.

Varying N/prior changes density/moment factors; the fixed-N equivalence need not survive. v0 is degenerate: no ordinary finite continuous density, and native sampling/prediction may need a separate validity policy. Negative/nonfinite v is invalid, never silently clipped. N<=1 lacks finite absolute t moment; N<=2 lacks finite t variance. Heavy-tailed Q can make K infinite even at N>1. No posterior is transferred to h_L or supplied M4. One independent GPT6-Luna read-only algebra consultation (session4c4adead-cc9a-4b08-af4e-c23a55a40b67) was checked against the paper/source by the parent; this is not Agent5/author-independent signoff.

## 4. Corrected FUTURE eligibility matrix — no active registry expansion
| Identity | Object / source status | Future admission / family accounting |
|---|---|---|
| Native v (`self.score`, `self.s_2`) | h_B only; VERIFIED_FIELD, quality unvalidated | Cheap fixed scalar read once a native fit exists; full native generation/CI/posterior costs still charged. Canonical native-error candidate, not D1a. |
| Eq8 d0 | h_B scalar noise posterior; PAPER_DERIVED, not dedicated source API | Fixed-N/prior rank alias of v. Same family if policies are exactly mapped; extra nonmapped variants require pre-C allocation, not a fake new algorithm. |
| A_Q predictive-absolute adapter | h_B only; DERIVED_ADAPTER, no implementation/quality claim | Separate proposal unless common-K equivalence shown. Charge integration/covariance/error work; independently approve identity/grid/budget later. It is NOT paper-faithful native error density. |
| BayLIME / BMB-LIME / native PTG-focus | Different methods or changed generation/banks | No source/posterior/guarantee transfer; separate future eligibility, none in D1a. |

The old B09 cannot simultaneously mean v, d0 and A_Q. Future human/A1/A4/A5 registry review must choose a canonical native proxy and explicitly name any adapter, drop duplicate ranking aliases and budget genuinely different policies BEFORE C. Earlier17 slots are not silently enlarged or treated as17 validated algorithms. Sequential fixed-h error estimators remain existing strong-null options, outside D1a; stopped score estimation does not automatically supply unbiased C loss.

## 5. Names checked, not conflated
| Name | Verified bibliographic identity | Difference / evidence limit |
|---|---|---|
| Slack BayesLIME | Slack/Hilgard/Singh/Lakkaraju,2008.05030v4(2021 version), primary above | Local Bayesian linear explanation/noise model; the pinned native score in this note. |
| BayLIME | Zhao et al., *BayLIME: Bayesian Local Interpretable Model-Agnostic Explanations*, [2012.03058v5](https://arxiv.org/html/2012.03058v5),2021 version | Primary §§5/7 read: explicit informative-prior retrofit, distinct from Slack's independently developed method. No shared source pin assumed. |
| BMB-LIME | Yu-Hsin Hung/Chia-Yen Lee, *BMB-LIME: LIME with modeling local nonlinearity and uncertainty in explainability*, Knowledge-Based Systems294(2024),111732; [DOI](https://doi.org/10.1016/j.knosys.2024.111732) | Identity verified with publisher-deposited [Crossref record](https://api.crossref.org/works/10.1016/j.knosys.2024.111732). Publisher full text was inaccessible in this check; detailed mechanism/API/license remain UNVERIFIED. Not Slack or Zhao. |

A1's pinned Phase2 handoff substantiates Slack's score; it does NOT supply a completed BMB-LIME/BayLIME identity/code audit. The latter identities are supplementary primary/metadata checks here, not attributed to A1. Ask A1 to extend future eligibility if needed, not block LIME-only correctness for full adjacent-method integration. No bibliographic identity establishes comparative performance or novelty.
