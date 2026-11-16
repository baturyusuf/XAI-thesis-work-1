# Agent handoffs and Astra oversight

Astra retained the rubric, manuscript score, journal ranking, risk judgments and scope decisions. Agents extracted evidence and mechanically assembled assigned files; none was authorized to commit, push, edit the manuscript, contact outsiders or start experiments. Primary task checkout baseline was research/astra-scie-q4-publication at f23a4b7453adf32e52d8bf6d9115f64148d395dd. Source B metadata reads used c7f7729ff1c944891e66eb2e42b9d1113a179a32.

| Agent/session | Model | Bounded work | Private independent handoff |
|---|---|---|---|
| Springer 68080415-0710-4575-8f10-3dc5b9eda9b5 | GPT-6.1-Terra | Publisher policies, identifiers, final metadata and A/CSV assembly | local/agents/springer_screen.md; final_metadata_check.md |
| Other publishers b3c73860-9806-4b94-847e-2c55cd7803b5 | GPT-6.1-Terra | Publisher screen and five IJAIT abstracts | local/agents/other_publishers_screen.md; ijait_papers.md |
| Rights 36922ec2-dec3-4a07-8962-76a65cec8d00 | GPT-6-Luna | Creator/CC/ethics evidence and unsent drafts | local/agents/rights_ethics_closure.md |
| Applied 2b2b94d8-51aa-49f0-9948-f830f3775773 | GPT-6-Luna | Five full HTML articles; later mechanical25-record assembly using existing notes and Astra scores | local/agents/applied_intelligence_papers.md; local/PAPER_REGISTRY.json |
| NCA ad880432-f13d-403c-8282-d1941d4bcd27 | GPT-6-Luna | Five full HTML articles | local/agents/neural_computing_papers.md |
| Soft 298f96f1-c7b9-4d58-9ffa-baaff99f83f0 | GPT-6-Luna | Five full HTML articles | local/agents/soft_computing_papers.md |
| ESWA 7bde3297-01f4-4364-8cb3-e240cf2e8bd6 | GPT-6-Luna | Five abstract records/policies; bounded10-request lawful full-text follow-up | local/agents/eswa_papers_and_policy.md; eswa_fulltext_followup.md |

Tools: normal publisher/Crossref/OpenAlex/official-source fetches, immutable Git/metadata reading, terminal Python for assigned reports. File tools could not access the sibling Astra checkout; terminal operations used its verified absolute path. No barrier bypass was used for blocked pages or images.

Astra read the current manuscript main text, all relevant extraction memos and direct critical primary sources. Independent primary checks included B2B test-threshold wording, NCA churn article, creator license metadata, CC legalcode, ESWA guide/insights and Springer homepages. The later direct NCA index-list observation superseded a conflicting agent note. Source-to-byte/licence and missing-table caveats remain explicit; agent claims were not automatically treated as facts.

Public outputs are paraphrased evidence/risk reports. Detailed private handoffs remain separated by agent; no simultaneous write ownership was shared. Subsequent corrections to assembly output were by Astra after agents completed. Actual agent hours/token cost were not instrumented and are NR, not a fabricated sum.
