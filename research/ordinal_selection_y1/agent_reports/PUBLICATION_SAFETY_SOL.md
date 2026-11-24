Audit UTC: 2026-11-23T11:44:50.494064+00:00

# SOL publication-safety / provenance audit

## Decision and scope

**Selected local-only checkpoint: conditionally suitable. Public push/release: HOLD for rights and disclosure review.** This is not legal advice or scientific GO. No training, tests, validation-runner execution, staging, commit, push, deletion or history rewrite occurred. Only this new report was written; no current/frozen files were edited.

Authorized branch: `research/ordinal-selection-y1`.
HEAD: `1b71d4c45ae1aba771e7c499f87f197f44b3112c`.
The editor root is a different sibling; all reads and this write used the authorized Y1 worktree explicitly. Account/absolute workstation path values are omitted here.

ALL **96 nonignored untracked Y1 files** were read for content/structure screening: **992,800 bytes**, comprising 27 Python,33 JSON,21 Markdown,10 TXT,4 CSV and one `.gitignore`. Full per-file SHA256 inventory follows. Python was AST-inspected; JSON recursively inspected; CSV schemas and observation units checked. Large result artifacts were assessed structurally rather than printed as records.

Tools: terminal Python standard library (`pathlib`, `subprocess`, `json`, `csv`, `ast`, `re`, `hashlib`, `difflib`, `collections`); read-only Git `branch --show-current`, `rev-parse HEAD`, `ls-files` (tracked, nonignored-untracked and ignored variants), `check-ignore -v`, `diff --cached --name-only`, `diff --name-only`. No project modules executed, packages installed, or external services contacted for this audit. No actual subject records or secret values reproduced.

Y1 tracked files: **0**. Whole repository current index: **9** configuration/license/editor entries; no tracked raw table, prediction archive, PDF/DOCX/TEX/XLSX was found. Staged and tracked working-tree diffs were empty when checked. This does not certify historical objects, remotes, other worktrees, employee-repository history, backups or cloud copies. Parallel parent/reviewer activity makes this a point-in-time inventory, not a filesystem lock or approval of later files.

## Findings

### 1. Employee-source redistribution remains unresolved — public-release gate

`SOURCE_MANIFEST.json` explicitly records user-authorized local use and public redistribution not cleared, at upstream commit `c7f7729ff1c944891e66eb2e42b9d1113a179a32`. All five ignored source snapshot hashes match. No license/copyright/SPDX notice was found in those five Python files; a compatible upstream license is not established by the inspected evidence. This does not prove no license exists elsewhere upstream.

Actual reuse: `y1/source.py` verifies hashes, activates `local/source`, imports `ProportionalOddsClassifier`, `build_common_preprocessor`, `ranked_probability_score`; `y1/models.py` uses model/preprocessor and `y1/metrics.py` uses RPS. The runners inherit these dependencies. Upstream ordinal evaluation also imports `evaluate.py` and `task_schema.py`. This is real algorithm/metric reuse, not just inspiration.

`bootstrap_source.py` retrieves pinned Git objects into ignored storage; it does not embed upstream bodies in the public bootstrap. No nonignored copy with the five snapshot basenames was found. A normalized-line heuristic found no contiguous match of >=8 nonempty lines between public Python and the five upstream files. This does not certify independent authorship or exclude smaller/adapted derivatives.

The root Apache-2.0 license does **not** automatically license employee source from another repository. Public visibility, attribution, a commit hash and local-use permission are not redistribution permission. Before release, obtain authorized-rightsholder clearance/compatible licensing or review an explicitly external, separately authorized dependency plan. Do not vendor snapshots, claim all dependencies are Apache-licensed, or imply an ordinary public clone supplies that source. Employment/third-party ownership may require owner review. Local checkpointing does not grant rights or make cloud storage private.

### 2. Raw/row-level material excluded at this checkpoint

`research/ordinal_selection_y1/.gitignore` line1 is `local/`. Git probes confirm exclusion of raw tables, private-source snapshots, virtualenv, original and extension OOF NPZ paths, and Restaurant/Sushi/MovieLens archives. Ignored inventory: **12,257 entries**, including **12,064 virtualenv entries**. Non-venv/cache ignored metadata includes archives, source/data/splits, full source-page/PDF evidence and prediction NPZs; no subject records were opened for this audit.

Public CSV units: dataset audit28 rows; original policy summary56; mechanism contrasts24; real policy summary42. The large original results JSON contains metric/configuration/fold summaries (including2016 empirical-oracle-regret entries), not2016 participant predictions. Public preparation logs are counts/missingness/feature dictionaries/item-overlap aggregates. Freeze/run receipts expose hashes and relative paths, not embedded rows/split memberships. Fixtures are synthetic.

No actual raw feature table, scientific-person identifier table, observation-level probability/prediction array, selected-user membership list, row split list, private source body, full dataset README, full article/manuscript or binary archive was detected in the reviewed nonignored set. This is a bounded content/schema check, not proof against every encoding or reidentification risk. Sparse aggregate cells still require ordinary ethics/disclosure review.

The Y1 ignore file itself is untracked and must accompany a later selected checkpoint. Ignores do not protect already tracked files, force-adds, raw files copied outside `local/`, or uploads outside Git. Review the exact selected index before any eventual commit; do not broadly force-add research/local artifacts.

### 3. Publisher excerpts need public-release review

`JOURNAL_GUIDELINE_EXCERPTS.json` contains snippets from three publisher guideline pages, including redundant prose and incidental analytics JavaScript. It is not a whole website/manuscript, but a publication license/permission or applicable exception is not established. Short quotation is not automatically unrestricted reuse. Tracking IDs in those snippets are not evidence of leaked credentials.

`LITERATURE_METADATA.json` and `LITERATURE_VERIFIED_DOIS.json` contain citation metadata, author names/ORCIDs and source links, not article bodies or abstract collections. Those are public bibliographic identities, not subject IDs. Source-paper evidence and full data-license READMEs remain local. Public provenance contains citations, short evidence descriptions and hashes. Preserve attribution and have the owner review excerpt necessity/terms. Do not silently alter frozen originals: use an authorized, traceable publication export or amendment if sanitization is needed.

### 4. Machine paths differ from scientific identifiers

Absolute workstation/account paths occur in three files: `gate_v2/mechanism/TEST_LOG.txt`, `gate_v2/real_extension/TEST_LOG.txt`, `gate_v2/skillcraft_survey/TEST_LOG.txt`. They are environment metadata, not participant records or grouping identifiers. They nevertheless disclose researcher/machine context and may defeat anonymous review. Values are intentionally not repeated here. Redact an authorized publication export, not historical frozen evidence silently.

Real user/item/GameID values or membership/OOF linkages would be scientific identifiers even if pseudonymous. Merely mentioning those field names in code or contracts is not disclosure of record values. DOIs, hashes, model candidate IDs, folds, source filenames and bibliographic ORCIDs are not access credentials or participant IDs merely because they resemble identifiers.

### 5. Secrets screening found no hits, with limited assurance

All96 candidates were checked for private-key blocks, common provider-token/access-key formats, credential-bearing URLs, quoted password/API-token/secret assignments and email-address shapes. **Zero matches for each screen**. Content/schema review found no secret store. SHA256,DOIs and publisher analytics identifiers were not classified as secrets. This was not a comprehensive entropy/malware scan or proof against unfamiliar credential formats. Do not publish actual values if future review finds one.

## Integrity observations and checkpoint/publication conditions

Read-only SHA comparisons found no missing/changed listed files in the current v1 protocol freeze or current mechanism, real_extension and skillcraft_survey freezes. The superseded real-extension freeze differs from four amended current files as documented; it is not the active freeze. Its archived bytes match recorded SHA256 `d0d4a40185579cd5b5ee8d77c89f4e631b26c11d468fed0260c6c7c4a71c5c11`. Hashes certify bytes, not ethical clearance, external preregistration or scientific correctness. No scientific validation scripts/tests were rerun for this audit.

A selected local-only checkpoint of nonraw protocols, glue/code, aggregate results and hash receipts is reasonable under stated local-use authorization, retaining these qualifications. This report does not authorize staging/committing. Keep raw/private/row-OOF/venv excluded and inspect the exact selected diff/index first. No broad add/force-add, arbitrary deletion, freeze replacement or history rewrite is warranted.

Public push/release remains a separate owner gate: resolve employee-source rights/distribution plan; review publisher excerpts; review workstation disclosure/anonymity; retain dataset citations/use restrictions (Sushi/MovieLens no redistribution; MovieLens research/noncommercial limits); obtain the parent's scientific/ethics decision. Technical source/prediction validation and scientific eligibility are separate from this safety audit. No external messages, manuscript upload or public-service submission occurred.

## Full inspected-file inventory

Paths relative to `research/ordinal_selection_y1/`. This is evidence of inspected bytes, not redistribution permission. Inventory excludes this report because it resides at root `agent_reports/`, outside the audited Y1 subtree.

Snapshot file-count/size recheck: 96 files,992800 bytes. Inventory SHA256 (sorted path, size, content hash): `f47d7c0632235d6ee30d51c81b0b9621195445feae70df640589284b3a6cec39`.

| File | Bytes | SHA256 |
|---|---:|---|
| `.gitignore` | 45 | `e51afbcce3460cbc4e56c200c9591e4f06c8650a035daf62ed0c1654cfdbfc07` |
| `ANALYSIS_IMPLEMENTATION.json` | 561 | `70a5c407456e874c674e200babcb3cd23b2ac599f8e3e011cc6fc21163d78646` |
| `DATA_MANIFEST.json` | 5245 | `c6e8851e0dd495a4f9e710716a6baf204bbc7ea33958bf06d929395e68a4b780` |
| `ENVIRONMENT.txt` | 374 | `23096bfbbe28bf8c43259657c46c95e7c1f8597fcc8b77243c73ee2598151a3c` |
| `FINAL_CHECKS.json` | 616 | `4a7c3b70a5717a05b81bd67ba77416d989395c30729616336e68de592dc1cdfa` |
| `JOURNAL_GUIDELINE_EXCERPTS.json` | 8658 | `92780fd327917123d6d395efccef77c2e0c3745baaf0031efca504f8a118e3fe` |
| `LITERATURE_METADATA.json` | 18893 | `12c64ab4c0715bdb9533c2f5b5ae3868a0e07c41a704ce96cb7b386a9e409ab6` |
| `LITERATURE_VERIFIED_DOIS.json` | 8399 | `8619cf5d068a8c75202662c08daa1b2e82866daef17da515fe11dbdf4cbe14dd` |
| `PROTOCOL_FREEZE.json` | 2733 | `069564744276ddeaa0921b029be595c52cab243f8800fe16de15aa81f8fe8e03` |
| `README.md` | 3452 | `69202d22983b67ca343c0dda1513970650e51533ad32040696460d19f077019e` |
| `RUNTIME_GROUP_CONTRACT.json` | 1754 | `e074907ec7592cf3985a0a2425874a0826090103cd0c6523df9009e7a169f9a2` |
| `RUN_ARTIFACTS.json` | 2102 | `744724404c2486c0c2f273f3332171d320d53155dab28f3c429ef69f3c9f31bf` |
| `SOURCE_MANIFEST.json` | 962 | `9042c1173eab3ddacc0dbadfbf73ca37520ebb577058fa548b581edaddc3f8e4` |
| `TOCUCO_SPLIT_CHECK.json` | 457 | `6069a5ff62a0b5f69f1812c7a1c556eeba4201f31b092cf738d32be570db0ef4` |
| `Y1_CODE_REUSE_AUDIT.md` | 4144 | `e14233cbcddd27ff8cd5aeca9ceb16093c1d8f7a657b20a7c8a940f686aa4dc4` |
| `Y1_DATASET_AUDIT.csv` | 16683 | `fdd4cd7d84f70665e7cb9c5c3bb367877ba2fd9e3c8d7ed2aec95a7ad209ab08` |
| `Y1_JOURNAL_SCREEN.md` | 4892 | `43f1e706cd70d0e35be3ae9e010aa0961eef6bac4fde4e0cdd5951bb6d73da18` |
| `Y1_LITERATURE_NOVELTY.md` | 4804 | `367fbe06f895f79725bd86c6a9220ec005cc011246f6ec621050711ba6b7f263` |
| `Y1_PILOT_PROTOCOL.md` | 3421 | `ad515a2b4728fc58da544cc22ec9f887f3780259d32a6d8ba1e73f0b9d87de04` |
| `Y1_PILOT_RESULTS.json` | 565517 | `250a9f205c3322f46dc8532e6d7682a9034792b92557dcd93fb73bdc89e9aa75` |
| `Y1_PILOT_SUMMARY.csv` | 25898 | `1c031f794cc136dc9caaa2fb58cb7385d44d06fa939a98d46f96aaa135250ccd` |
| `Y1_POSTPILOT_AUDIT.md` | 2559 | `c9b721f2381fe6001bfda0457b4ce0491757024b942e276d53f8c46b2b3856b5` |
| `Y1_PROGRESS.md` | 6661 | `a6ea5b5490a7ea86aec7c056bef63c81f29702fde5579d6fa0a14a8272a79030` |
| `Y1_RESEARCH_PROTOCOL.md` | 5948 | `5dc8f16e1704714d59e80fcc2fc20096df84e89539315d4f70396058c74675f1` |
| `Y1_VALIDATION.json` | 1105 | `d8c51f6fa24a0764ced0b852f23cce811d91899e59af2be60fdc7dedfa429e04` |
| `Y1_WORKLOAD_AND_AUTOMATION.md` | 3046 | `f2dadb32f908131b6431866f5ecf02934193848ad5da97d97ed4a7d39b22d295` |
| `agent_reports/CODE_LUNA.md` | 568 | `3387c14b38e43ab67b44070cfd0cccab38b81956e1f6178cf59a6f21a352f743` |
| `agent_reports/DATA_TERRA.md` | 3920 | `50e2ae41f0c5d3a89111b3119acacbb862d862fa81bdf32530847a0c0cda6978` |
| `agent_reports/LITERATURE_LUNA.md` | 442 | `4f556a53ffbcc2f13daf7d3cc1f25ccfbe59074439c0ad67c9fd43218bb263f8` |
| `agent_reports/MECHANISM_REVIEW_TERRA.md` | 6986 | `b4fa7b6f39f384f6aa25a4e6b36bcb35e6c63d60dc4d23edf6bc84cc7a5fc580` |
| `agent_reports/NOVELTY_GATE_TERRA.md` | 7880 | `a4a924497ab89b0859f38057a33cbea6c40dd2e17c9c2131e3d7180f86f88757` |
| `agent_reports/REAL_EXTENSION_REVIEW_TERRA.md` | 5495 | `f8caab31e0e0116bd9e4a72586f0ab2ff5dec08b334c117fa929bfb82d95eec2` |
| `agent_reports/REVIEW_TERRA.md` | 532 | `c44622f392d04f4c990f10638cf2656e841ae4dafe8c357913c4116ec5c114fe` |
| `agent_reports/SKILLCRAFT_REVIEW_TERRA.md` | 4973 | `d0cb7082453c50def07b72c86842c4f430e957d2326380aa3e0ed411be1841ff` |
| `analyze_pilot.py` | 8721 | `ac621b0f415fd3a5e1ba32b3fc516e6a754ea7c44db54cb15cef126a60228aeb` |
| `bootstrap_source.py` | 1724 | `21cfae769e84e0c63df603828f373a1c1b8b5c29be8101693ce0246c27eb07b0` |
| `build_progress.py` | 7605 | `f7c6a6e4a515f76f88a3d066804760eee192d0f6bbe9a3cba5636fb244269bb1` |
| `gate_v2/FIXED_WEIGHT_CONTROLS.json` | 14984 | `aaea257ff4df22f4cf9dbf4df8234f4662a745087344abb3485a39ef5e2f39d7` |
| `gate_v2/MECHANISM_CONTRASTS.csv` | 9350 | `c774f1a56eac743922f7350506038f9481f904a4451d8a3425e8beeb478516fc` |
| `gate_v2/MECHANISM_POSTRUN_HASHES.json` | 8001 | `9f7c178a953540274dac4f8da3b05f70c8d81bf186ac71b0646683135810f725` |
| `gate_v2/REAL_SELECTION_SUMMARY.csv` | 10525 | `a192caa53158d901f8466a824b44827dfddb0cf0f32393f0a65931df712a4151` |
| `gate_v2/SESSION_EVIDENCE.json` | 650 | `a2e52a392bfea1ad55d22ae967d615c8df3ab7590119abdd9931a0970a8f788e` |
| `gate_v2/build_report.py` | 5111 | `17226c0098811f5237fd0f8dc84799a9258fefa6d0fe9f795e9267b01175f4ec` |
| `gate_v2/mechanism/FREEZE.json` | 2235 | `8d6f3b8f910126ca9a0321ca0f243d25ed65233de857c4314196eb56e4bd536a` |
| `gate_v2/mechanism/FREEZE_VERIFY_LOG.txt` | 66 | `f345456a35c62f3e972d5bd6d5532052d1d35ce5a71d18ff3b909d1febe4bc20` |
| `gate_v2/mechanism/PROTOCOL.md` | 3949 | `1cc5d1a3c22403cd48195e603bfd62889dc678ea24606e2e44608311a299f145` |
| `gate_v2/mechanism/RESULTS.md` | 333 | `ca92638248c374e74204cc8747fc820e378d611313082b3638fb0745b283aedd` |
| `gate_v2/mechanism/TEST_LOG.txt` | 1398 | `6dbd6633c6e007d2fabe5f3d625254d7a31513eccee596e8948091e4438b6b37` |
| `gate_v2/mechanism/config.json` | 871 | `979ffaf4b25af186ae9e2559a43fa36e2a3fab29f1b8b5b59d859c298c167016` |
| `gate_v2/mechanism/run.py` | 8737 | `b398497944203bd52d100c6c19de6fdf64f50bb706fbb6f5b1b69af0a4592096` |
| `gate_v2/mechanism/tests/test_mechanism.py` | 3235 | `e0f68c27bad46edb65b322f43dba1f06ab6551758890bc55a0638bccd5c9e604` |
| `gate_v2/real_extension/AMENDMENT_PRE_RUN.json` | 2024 | `2f9d160c05d71860a92b776d1b86f414d4bab491f16ba9a8c7f07021b225046b` |
| `gate_v2/real_extension/AUDIT_SUMMARY.json` | 4687 | `5e503071f7d24a48fee34840dc39ba2797308e66f9f7b8e77e3182e698a81db4` |
| `gate_v2/real_extension/FREEZE.json` | 4662 | `1afac2702c7d72a4a234fce10c6c4136bffb4a737bc1163ec046fdfe0f782f7f` |
| `gate_v2/real_extension/FREEZE_PRE_REVIEW.json` | 4418 | `d0d4a40185579cd5b5ee8d77c89f4e631b26c11d468fed0260c6c7c4a71c5c11` |
| `gate_v2/real_extension/FREEZE_VERIFY_LOG.txt` | 66 | `5d04010c7f05ff8e32ea4e06a8c5322f1404ffc9ab9670259c25f579498719c0` |
| `gate_v2/real_extension/PREPARE_LOG.txt` | 15603 | `f9f2a6dea4c3c8295aca95cde19f54c118dd1fcfc02002a751e6de8c63dd1e04` |
| `gate_v2/real_extension/PROTOCOL.md` | 5807 | `d8f2175d847bcb6832c71bf9bd81eb51ab98330b9e1c0923c9f2591120a7e13c` |
| `gate_v2/real_extension/PROVENANCE.json` | 7604 | `301c76aa24c02ed88015bbf3ae1e543007d7d0dc3eca871eb3bd21bc1c79238f` |
| `gate_v2/real_extension/TEST_LOG.txt` | 2062 | `868b8f39e507f92ea6076b6b53cce2272898dffb53bede9c7c2f1865f6fa19bc` |
| `gate_v2/real_extension/config.json` | 714 | `1f372a6d0f292431ae29fd76374b07cc9aaaa1240bfa053641f573023b26cfa8` |
| `gate_v2/real_extension/data.py` | 5494 | `d1e1d6133215655447d4306b0bbab0a5f2e50d7b100e5e58709f0c9e2acdcf11` |
| `gate_v2/real_extension/run.py` | 10057 | `662916b18dc873499af39f7243aa94b912042f34eea5de77672b76d1b36f3293` |
| `gate_v2/real_extension/tests/test_real_extension.py` | 6331 | `a2731d3c43bb4eb7faf7975dc4d5ce9db87db3073ed7add36cb2b998ea77e3ba` |
| `gate_v2/skillcraft_survey/AUDIT_SUMMARY.json` | 1778 | `d5680fc97dd5df6f20ee67fa1d1b9ea0ab647f34a719e11693ce5ae9b7554527` |
| `gate_v2/skillcraft_survey/FREEZE.json` | 3729 | `10d319c723ceca6d1d9ee644122cff1f88e78f91676d7f4058682329fa7beabc` |
| `gate_v2/skillcraft_survey/FREEZE_VERIFY_LOG.txt` | 66 | `f8dcf37b1b40244badb77cec99d617640928699cac3bd0068fb48b339b25bc59` |
| `gate_v2/skillcraft_survey/PREPARE_LOG.txt` | 1780 | `b13f9a75850da9e836c5c1e0f2644aec24e22f367d694f6e633dd28d0dfa549b` |
| `gate_v2/skillcraft_survey/PROTOCOL.md` | 5612 | `b247665f7e52e18d78a266a3c8616d4505193af9a0a48d0661d2a13ff9ff4c43` |
| `gate_v2/skillcraft_survey/PROVENANCE.json` | 3878 | `44ea39c749ed6a82e4d263e9af79eba6a5285544e2604271858fd342c1051c97` |
| `gate_v2/skillcraft_survey/TEST_LOG.txt` | 1799 | `4700077badf65b2cd30b0031e93a18bcedafd3b14f447bbaded5db9d05de5a70` |
| `gate_v2/skillcraft_survey/adapter.py` | 2052 | `7aaf0a3fe5562b21e7779c923e23bd5fadc337fc6ab5a757890d8ba3880301ba` |
| `gate_v2/skillcraft_survey/config.json` | 929 | `a0310073a7e4727bf19148a8a081efb62076f22567437de0a125cd84b18aa4d8` |
| `gate_v2/skillcraft_survey/run.py` | 9965 | `86012e8effe30a81e7ca14ef7da387779ede804bd305f3c3e38f52dca9f00359` |
| `gate_v2/skillcraft_survey/tests/test_survey.py` | 5049 | `f8693aab784f81340cef19d4f75bc73aa1e1cd3a514035c1ff4e90a1b3f64f18` |
| `gate_v2/validation/CHECK_REPORT.json` | 3431 | `ff417ccccecee44d338cf78e655bc67d21c85885d57daabaccbca4de1310b4f6` |
| `gate_v2/validation/CHECK_SKILLCRAFT.json` | 3610 | `ef951d78f3efb4ec458799956993d2be9cc4465b0aedf657a18334b3d7fb6519` |
| `gate_v2/validation/RUN_HASH_RECEIPT.json` | 1731 | `90038239b95d67f46c22a0d3d0c45895a75551f8d50e318bfce430fac1ffae5e` |
| `gate_v2/validation/SKILLCRAFT_RUN_HASH_RECEIPT.json` | 674 | `21b4e3ade12558893e5a223d078f0edc9f0d58abcbc34787ad79fa3ee2f1d7ee` |
| `gate_v2/validation/check_results.py` | 11152 | `1639ffcccf29ed72ddbfabde1a4429a6bb47f365fe3e5aac9588c8af015b19ea` |
| `gate_v2/validation/check_skillcraft.py` | 10783 | `d739e44e15a40575d82e7d1c258bdca59aadaf39fcae74611bc60f5d61cb2da1` |
| `make_replay.py` | 1274 | `8f8f417d4e1e8935f7eeedd8c4bbf2bab1d9d89c9c11d7050d987e7d7b083ffd` |
| `pilot_config.json` | 945 | `a5d191c078ebc37eb1a3d2e79530af2a92c01db9d0b867f71420be96e4708525` |
| `prepare_data.py` | 4265 | `7592b0bd5a937c77af1f8f3628870e13c9494f07d7ceef751ac31fba12c1b4d7` |
| `refresh_dataset_audit.py` | 4441 | `408a4d329f07747d9a80784da20b7afdd6c165da89b74f5df5d24359d462eb9d` |
| `requirements.txt` | 98 | `b6f9c775a8a316aebf0d82283f3f8846974d75063b4e2a5cda27bbad67335608` |
| `run_pilot.py` | 7626 | `13dbe0d96000c01b10f8f4b3e5102cfe7603ef7f53a79ee52efee8787efdbd2f` |
| `seal_results.py` | 1028 | `62fb97ee17fa85fea88123f75ae221909571b6b513b8c3a701d1b82becdc114b` |
| `tests/test_analysis.py` | 1301 | `4c9385e05a8fbdea680eca6c9d93f89d2b02e9654ec32f897768f5ab73e36a73` |
| `tests/test_contracts.py` | 3851 | `1f33a5c409df4ab14226a017ab1051e2df53a4cd698fd4f1be7088b579472aa4` |
| `validate_results.py` | 4718 | `39dc1fc587fb4f28a2b524cc6c67d998e853029c64bb956b502b5517fcd346fb` |
| `y1/__init__.py` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `y1/data.py` | 2768 | `c1f1028c1495fafbd837710fb7055267967484e5bda1a219230a90d78bcb0c1b` |
| `y1/metrics.py` | 3813 | `b381b521453aa5b9a6dcb5f792b27cdfd3311fe2911854771472ba5a152a5ea3` |
| `y1/models.py` | 1140 | `f873f557a07f4852393969f739022336523ea7679d8f345f1e0e6d22f65ea6bb` |
| `y1/source.py` | 765 | `e7cc35f93a8f6f3b957742f06b191f9ec8f524a353eb638df6114d4db7f52351` |


Location addendum: the report initially resided in the authorized Y1 root agent_reports directory. Its own bytes were subsequently moved to research/ordinal_selection_y1/agent_reports; the old inventory exclusion explains the historical location, not its current path. No other worktree was used.
