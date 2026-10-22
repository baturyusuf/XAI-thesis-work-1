# Dependency/runtime plan — NOT INSTALLED
2026-10-22 | REVIEW, all effort estimates static inference

Host Python3.13.15/Windows11/MSYS; py launcher lists3.11/3.13/3.14, not3.10/3.7. No interpreter/env installed. Propose own .venv-reference/.venv-sis/.venv-lime only after local ignore/lock review. Legacy env/container/WSL separate approval; global Python unchanged.

| Artifact | Observed manifest/source | Strategy/blocker |
|---|---|---|
| A3 | Stdlib, >=3.10 syntax, reported tested3.13.15 |3.13 isolated env, no pip needed for56 |
| Google SIS | absl-py>=0.5.0/numpy>=1.12.1; sis.py NumPy+collections | Only subdir, not entire Google monorepo; resolve compatible wheel/hash lock after approval |
| LIME pin | NumPy/SciPy/sklearn>=0.18/skimage>=0.12/matplotlib/tqdm/pyDOE2==1.3.0 | Source SHA vs PyPI0.2.0.1 not same-source assumption; build/install hooks audit then compatible lock |
| Bayes pin | NumPy1.21.6/SciPy1.7.3/sklearn1.0.2/LIME0.2.0.1/SHAP0.41.0/torch1.12.1/vision0.13.1 +2022 full stack |3.10 candidate absent; do not force3.13. Exact dependency/source check; minimal stack/upgrade extraction separate reviewed patch |
| RDE README | Python3.7.8/TF-GPU1.15/Keras2.2.4/NumPy1.17/CUDA10.0.130/cudnn7.6.5/keras-adf19.1.0/statstream19.1.0 | HIGH legacy/security/hardware gate, missing pretrained weights; defer, no data/model download |
| VeriX | Marabou/ONNX Runtime/NumPy/skimage/matplotlib, default solve300s | Compiler/platform/ops/tie and model conversion audit; supported synthetic NN only |
| LTT original | Python3.7.7/NumPy1.18.1/SciPy1.4.1 +large experiment stack | A3 stdlib reference first; original helpers source crosschecks distinct from native replication |
| CRC | NumPy/SciPy import in helper | Separate marginal controller semantics |
| Anchors | NumPy/SciPy/spacy/LIME/sklearn>=0.22 | Separate rule/sampler arm |
| ReCalX/CE/SST/FRI | Metadata-only recheck this round | Dependency/actual API audit UNVERIFIED |

Inspect package build hooks, transitive licenses, wheels/compilers, network/model/data downloads and compatibility before execution. No vulnerability/transitive-license approval claimed. Public GETs disclose normal IP/request metadata, no private files/secrets transmitted, no paid API or key used.
After approval record full lock/hash/index, Python/hardware/OS/BLAS/threads, seeds/framework determinism and patch diff. Old environment vulnerabilities/platform feasibility may require deferral; a port is not exact historical reimplementation. No measured install/runtime cost fabricated.
