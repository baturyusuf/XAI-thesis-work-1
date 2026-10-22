"""Read only pinned Git blobs; write a whitelisted audit copy in Agent5 worktree."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess

W = Path(__file__).resolve().parents[3]
A1 = '27bc1a7fb731bbf1f13787038e4d3a123233fa61'
A2 = '2a3cc1abc29c823fb6eda26ebf1ed29b064da63c'
A3 = '51a6915ec8f94cf1779609422bd61e8d6b3911c7'
DELIVERY = 'd42bec729e9e78ae5387720d29360c5d60f38192'

def git(*args):
    return subprocess.check_output(['git', '-C', str(W), '--no-pager', *args])

def guard():
    assert git('branch', '--show-current').decode().strip() == 'research/independent-validation'
    assert Path(git('rev-parse', '--show-toplevel').decode().strip()).resolve() == W

def main():
    guard()
    specs = {
        A1: ['AGENTS.md'] + ['research/literature/' + p for p in ('AGENT3_BENCHMARK_REQUIREMENTS.md', 'AGENT4_BASELINE_INTEGRATION.md', 'AGENT4_INTEGRATION_MATRIX.csv', 'LTT_GUARANTEE_AUDIT.md', 'PAXP_PSEUDOCODE_AUDIT.md', 'H1_COMPLETION_LAW_REVIEW.md', 'H2_SELECTIVE_QUALITY_REVIEW.md', 'REVIEW_REPORT_02.md')],
        A2: ['research/datasets/' + p for p in ('DATASET_HANDOFF.md', 'REVIEW_REPORT.md', 'SPLIT_STRATEGY.md', 'DATASET_DEPENDENCE_AUDIT.md', 'LEAKAGE_AND_TEMPORALITY_AUDIT.md', 'HIDDEN_DATASET_POLICY.md', 'XAI_METRIC_DATA_REQUIREMENTS.md')],
        DELIVERY: ['research/benchmark/' + p for p in ('AGENT4_PUBLISHED_HANDOFF.md', 'IMPLEMENTED_API.md', 'FINAL_METHOD_QC.md', 'SOLVE_TEST_REPORT.md', 'RE_REVIEW_REPORT.md', 'METRIC_DEFINITIONS.md', 'STATISTICAL_ANALYSIS_PLAN.md', 'HELDOUT_EVALUATION_REQUIREMENTS.md', 'AGENT5_HANDOFF.md', 'BASELINE_ELIGIBILITY.md', 'COST_AND_QUERY_BUDGET.md', 'evidence/solve/REFERENCE_RESULTS.json')],
    }
    paths = git('ls-tree', '-r', '--name-only', A3, 'src/benchmark', 'tests/benchmark').decode().splitlines()
    paths = ['LICENSE'] + [p for p in paths if p.endswith('.py')]
    specs[A3] = paths
    rows = []
    snapshot = W / 'research/validation/evidence/source_copy/agent3_51a6915'
    for sha, names in specs.items():
        assert git('cat-file', '-t', sha).strip() == b'commit'
        for name in names:
            blob = git('rev-parse', sha + ':' + name).decode().strip()
            data = git('show', sha + ':' + name)
            copied = ''
            if sha == A3:
                dest = snapshot / name
                assert dest.resolve().is_relative_to(snapshot)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if dest.exists():
                    assert dest.read_bytes() == data, 'Never overwrite altered source copy'
                else:
                    dest.write_bytes(data)
                copied = dest.relative_to(W).as_posix()
            rows.append(dict(commit=sha, path=name, blob=blob, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), copy_path=copied, access='pinned_git_blob'))
    out = W / 'research/validation/evidence/SOURCE_MANIFEST.csv'
    with out.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator=chr(10))
        writer.writeheader(); writer.writerows(rows)
    parity = git('diff', '--name-only', A3, DELIVERY, '--', 'src/benchmark', 'tests/benchmark').decode().splitlines()
    result = dict(status='VERIFIED', source_entries=len(rows), copied_files=len(paths), source_test_delivery_diff=parity, base=git('rev-parse', 'main').decode().strip(), branch=git('branch', '--show-current').decode().strip(), worktree="verified-linked-audit-worktree", source_scope='No raw data or other worktree files; source copy not independently authored tests')
    (W / 'research/validation/evidence/SOURCE_VERIFICATION.json').write_text(json.dumps(result, indent=2) + chr(10), encoding='utf-8', newline=chr(10))
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
