# Accepted-count LTT test log

Run from the isolated xai-innovation worktree, with its src directory on PYTHONPATH:

python -m unittest tests.innovation.test_ltt_accepted -v

Result: 6 tests passed in 0.060s. Tests cover positive power, k=0 behavior, using accepted count rather than n for the risk p-value, separate full-n coverage, unmet-IID / split leakage, target mismatch, and an exact enumeration over all 3^5 IID samples of a uniform three-state law. In that enumeration, the risky all-accepted policy's false rejection occurred for the all-zero-loss sample only: 1/243, below the per-family risk budget 1/2. This narrow numerical result is not a general guarantee.
