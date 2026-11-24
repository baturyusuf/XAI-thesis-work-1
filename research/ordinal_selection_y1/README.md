# Y1 — Ordinal Selection Pilot

Current status: see [CURRENT_PROGRESS.md](CURRENT_PROGRESS.md) and [Gate-v2 decision](gate_v2/Y1_GATE_V2_DECISION.md). The v1 reports below remain historical evidence.
Own branch: research/ordinal-selection-y1. Research and technical pilot, NOT submission-ready or a completed confirmatory benchmark.

Start with Y1_PROGRESS.md, then Y1_RESEARCH_PROTOCOL.md / Y1_PILOT_PROTOCOL.md. Required audits: Y1_DATASET_AUDIT.csv, Y1_CODE_REUSE_AUDIT.md, Y1_LITERATURE_NOVELTY.md, Y1_WORKLOAD_AND_AUTOMATION.md. Journal screen and post-pilot corrections separate.

## Existing results (no training needed)
Open this directory as your terminal working directory:

    local/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
    local/.venv/Scripts/python.exe validate_results.py
    local/.venv/Scripts/python.exe analyze_pilot.py

These verify/recompute summaries without model refitting, except tiny synthetic estimator unit tests. Existing runner intentionally refuses to overwrite a run directory. Original protocol freeze and prediction hashes retained.

## Reproduce without overwriting existing evidence
First create a template-only isolated replay (no fits or raw copies):

    local/.venv/Scripts/python.exe make_replay.py --name replicate_01

The new directory local/replays/replicate_01 contains code/config/protocol only, no old freezes or outputs. Open a terminal there and use the existing parent virtualenv interpreter or create its own environment as below. A newly generated freeze belongs to that replay, not the original external preregistration (there is none).

## Commands inside the new clean replay
1. python -m venv local/.venv
2. local/.venv/Scripts/python.exe -m pip install -r requirements.txt
3. local/.venv/Scripts/python.exe bootstrap_source.py --source-repo PATH_TO_AUTHORIZED_EMPLOYEE_REPOSITORY
4. local/.venv/Scripts/python.exe prepare_data.py
5. local/.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider
6. local/.venv/Scripts/python.exe run_pilot.py --prepare
7. local/.venv/Scripts/python.exe run_pilot.py --dataset wine_red
Repeat step7 for wine_white, skillcraft, tae only. No automatic22dataset run. Do NOT replace an existing freeze or delete previous runs to hide an amendment. For a genuinely new protocol/version use a separate named working copy/run design and preserve old receipts.
After the four fits, run seal_results.py, then analyze_pilot.py, then validate_results.py. A new run needs its own matching RUN_ARTIFACTS.json, never copy the original receipt. Freeze timestamps are local, not external preregistration. New downloaded source versions/hashes need review before comparing runs.

## Safety and rights
local/ holds raw UCI archives/tables, upstream source snapshots, row folds/predictions and the virtualenv; all ignored. Public artifacts contain only aggregate metrics, protocols and hashes. New glue sits in the thesis Apache2 repository; that does not grant a licence to upstream Employee code. Local reuse authorized by user; public source distribution still requires owner review. No source repository or original manuscript changed. No remote push/submission/OSF action performed.

## Data citations
Wine: Cortez et al.(2009), UCI DOI10.24432/C56S3T.
SkillCraft: Blair, Thompson, Henrey, Chen(2013), UCI DOI10.24432/C5161N.
TAE: Loh(1997), UCI DOI10.24432/C55P6M.
All three official UCI pages state CC-BY4. Grouping/rank encoding and source-binned controls described in protocol; data NOT redistributed here. Institutional ethics/author decisions not delegated toAI.

## Byte-preserving research checkpoint
This directory disables Git text normalization in its own .gitattributes so existing SHA-256 seals retain exact archived bytes across operating systems. Historical files are not normalized or re-sealed. Raw/local files remain excluded by .gitignore.
