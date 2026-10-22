# Native API and source audit

Evidence is from immutable source snapshots listed with SHA-256 in evidence/SOURCE_FETCH_MANIFEST.csv. URLs below pin the exact commits. Snapshots were read, not executed. All native runs: NOT_RUN. Paper-code equivalence: UNVERIFIED.

## Primary adapters

### LIME — BSD-2-Clause
Repo: https://github.com/marcotcr/lime/tree/fd7eb2e6f760619c29fca0187c07b82157601b32
Source: lime/lime_tabular.py and lime_base.py at that SHA.
LimeTabularExplainer.explain_instance(self,data_row,predict_fn,labels=(1,),top_labels=None,num_features=10,num_samples=5000,distance_metric='euclidean',model_regressor=None,sampling_method='gaussian'). Private __data_inverse(self,data_row,num_samples,sampling_method). Base explanation API returns (intercept, exp list, weighted local R², local_pred); local_pred is fitted prediction for first neighborhood row. Base score is weighted R², not absolute functional loss. Default discretized representation is binary bin-match; continuous mode uses scaled features. Store exact representation, intercept, coefficients, and transformation. Gaussian uses explainer random state; LHS path does not forward that RNG to pyDOE2. Setup snapshot supplies dependency declarations; versions must be checked against manifest rather than assumed.

### SHAP Kernel — MIT
Repo: https://github.com/shap/shap/tree/cc2007eedf365e66f4cd7e5d37edef6d463b322b
Source: shap/explainers/_kernel.py. KernelExplainer.__init__(self,model,data,feature_names=None,link='identity',**kwargs); shap_values(self,X,**kwargs); __call__(self,X,l1_reg='num_features(10)',silent=False); explain(self,incoming_instance,**kwargs). Link-space attribution sums to linked model output minus linked background expectation; retain link and output space. Default sample budget is approximately 2*M+2048, with a finite-coalition cap when M<=30; exhaustive only when the selected budget reaches that cap; global NumPy RNG and no seed parameter in these entrypoints. Native compiled _cutils is imported. SHAP dependency environment and native execution not verified.

### Bayes Local Explanations — MIT
Repo: https://github.com/dylan-slack/Modeling-Uncertainty-Local-Explainability/tree/72c4330bc7d29150b55018b0946f85f7df88e107
Sources: bayes/explanations.py, bayes/regression.py, requirements.txt. BayesLocalExplanations.__init__(self,training_data,data='image',kernel='lime',credible_interval=95,mode='classification',categorical_features=[],discretize_continuous=True,save_logs=False,log_file_name='bayes.log',width=0.75,verbose=False). explain(self,data,classifier_f,label,cred_width=1e-2,focus_sample=True,n_samples=None,max_n_samples=10000,focus_sample_batch_size=2500,focus_sample_initial_points=100,ptg_initial_points=200,to_consider=10000,feature_selection=True,n_features=15,tag=None,only_coef=False,only_blr=False,enumerate_initial=True,max_coefs=None,l2=True). BayesianLinearRegression.__init__(self,percent=95,l2=True,prior=None); fit(self,xtrain,ytrain,sample_weight,compute_creds=True); predict(self,data); get_creds(self,percent=95,n_samples=10000,get_intercept=False); draw_posterior_samples(self,num_samples,get_intercept=False). Classifier probabilities are sliced by label. BLR prepends intercept; score and s_2 equal (weighted residual squares plus coefficient-square penalty)/N, a Bayesian scale estimate, not absolute loss or density-at-zero. Posterior radius is percentile absolute deviation; drawing uses global RNG. Default focused route is unimplemented; SHAP feature selection plus focus raises NotImplementedError. Dense N×N weights and matrix inverse; posterior sampling cost. Requirements pin numpy 1.21.6, scipy 1.7.3, sklearn 1.0.2, lime 0.2.0.1, shap 0.41.0, torch 1.12.1, torchvision 0.13.1. Current pinned LIME API requires sampling_method but Bayes private calls omit it; compatibility with declared older LIME has not been run.

## Risk-control references

### LTT — MIT
Repo: https://github.com/aangelopoulos/ltt/tree/3ad7a64adad9f356e29f40e73935a6114f896396
core/bounds.py includes binom_p_value(r_hat,n,alpha), hb_p_value(r_hat,n,alpha), HB_mu_plus(muhat,n,delta,maxiters), clt_p_value(r_hat,sigma_hat,n,alpha), wsr_p_value(losses,alpha,delta=0.1). These implement distinct binomial, Hoeffding/Bentkus, asymptotic CLT, and betting confidence-sequence calculations; assumptions and loss domain must match. pfdr.py get_selective_risk_p_values(score_vector,correct_vector,lambdas,alpha), pfdr_loss_table(score_vector,correct_vector,lambdas,alpha), pfdr_bonferroni_binom(score_vector,correct_vector,lambdas,alpha,delta), pfdr_bonferroni_search_binom(score_vector,correct_vector,lambdas,alpha,delta,downsample_factor=10). Selects score>lambda and minimum accepted count 25 in p-value routine. Source issues to audit: HB boundary log terms; HB_mu_minus contains pdb.set_trace; Bonferroni wrapper loses cut-lambda mapping, search uses shortened indices and downsample_factor appears unused. Do not adopt blindly.

### CRC — license/source snapshot
Repo: https://github.com/aangelopoulos/conformal-risk/tree/3eff946390a8f188b1e5ab700fce21a66a215e7c
core/get_lhat.py get_lhat(calib_loss_table,lambdas,alpha,B=1). Uses column means, corrected risks, and chooses max(argmax(corrected risk >= alpha)-1,0). Ordering is assumed small-to-large loss. All-pass/no-feasible behavior needs explicit audit; guarantee is marginal expected risk and is not equivalent to LTT conditional-risk/FWER. Only core helper verified; experiment entrypoint not verified.

## Other source checks

SIS Google snapshot https://github.com/google-research/google-research/tree/0d94f8c4d92678ce5f7a0eacae725f79174cfb03; find_sis(f,threshold,current_input,current_mask,fully_masked_input), sis_collection(f,threshold,initial_input,fully_masked_input,initial_mask), produce_masked_inputs(input_to_mask,fully_masked_input,batch_of_masks). Batched scalar f; True mask means unmasked; greedy backward search, fixed baseline, not global all-subset optimality. Apache license. Author implementation is a distinct MIT artifact; equivalence unverified.

RDE snapshot https://github.com/jmaces/rde/tree/d71169d697c322695901653fedd2ccf97413f018; source stl10/rde.py. ProjectedGD(fun,x0,jac,maxiter,eta,ftol,xtol,c,tau,maxls,momentum), get_distortion(x,node,target,mean,covariance,model,mode), get_sparsity_regularizer(), adf_rde_lagrangian(x,node,target,s0,mean,covariance,model,mu,mode). Optimization-based distortion/sparsity, not a probability-vector quality selector; dependency/cost and model object compatibility require adapter review.

VeriX snapshot https://github.com/NeuralNetworkVerification/VeriX/tree/fd2041ec304767d1e233f72d41c70b2701c3b647; VeriX.py class signatures: __init__(self,dataset,image,model_path,plot_original,labels,directory), traversal_order(self,traverse,plot_sensitivity,seed), get_explanation(self,epsilon,plot_explanation,plot_counterfactual,plot_timeout). Verification/sensitivity workflow, not native acceptance-risk score; status/timeout semantics must not be converted to probability without a designed adapter.

ReCalX (thomdeck/recalx, 222807cbcebb19603b3ae9150675a94ebc8b871b), CE/FCE (Moffran/calibrated_explanations, 7fd6bf1bb75683ebd6f5ca6d193e6831444eaa8f), SST (IBM/SAX, e296e3c721852cc43ce60d5dfceaae379515b1cc), and FRI (lpfann/fri, 58aa2b33a9fa5ffb306f5125d4ba0b8c223e3c6d) have commit metadata only in this evidence set. No API, license, source, or compatibility claims are verified for them.

## Exact optional defaults from pinned AST (static parsing only)

Source snapshot: sis_google__sufficient_input_subsets__sis.py.txt

```python
def find_sis(f, threshold, current_input, current_mask, fully_masked_input):
def sis_collection(f, threshold, initial_input, fully_masked_input, initial_mask=None):
```

Source snapshot: rde__stl10__rde.py.txt

```python
def ProjectedGD(fun, x0, jac, maxiter=1500, eta=1.0, ftol=1e-18, xtol=1e-18, c=0.65, tau=0.7, maxls=30, momentum=0.0):
def get_distortion(x, node, target, mean, covariance, model, mode='diag'):
def adf_rde_lagrangian(x, node, target, s0, mean, covariance, model, mu, mode='diag'):
```

Source snapshot: verix__VeriX.py.txt

```python
def __init__(self, dataset, image, model_path, plot_original=True, labels=None, directory=''):
def traversal_order(self, traverse='heuristic', plot_sensitivity=True, seed=42):
def get_explanation(self, epsilon, plot_explanation=True, plot_counterfactual=False, plot_timeout=False):
```

Source snapshot: anchors__anchor__anchor_tabular.py.txt

```python
def __init__(self, class_names, feature_names, train_data, categorical_names={}, discretizer='quartile', encoder_fn=None):
def explain_instance(self, data_row, classifier_fn, threshold=0.95, delta=0.1, tau=0.15, batch_size=100, max_anchor_size=None, desired_label=None, beam_size=4, **kwargs):
```
