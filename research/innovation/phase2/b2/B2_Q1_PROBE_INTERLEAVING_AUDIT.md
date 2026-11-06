# Q1 r2 interleaving audit -- source reasoning only

Agent3 evidence standard 576283e769a13ae460713cff995ca994b18e9318; Agent5 audit 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19. TEST baseline 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184, parent 7087da0b3d3e2bdc4093a6a6f4def749998a8799; frozen L01 d51652e340fd99f533cc07cef910f90acd660baa and G04 8325d9911556855ea7966e112e91a80d786a393d unchanged.

API evidence integration PASS (static, conditional); unexpected-success SOURCE_BLOCKED; Q1_SOURCE_REMEDIATION_REQUIRED. No runtime interleaving is proven. All rows NOT_RUN; both flags False; TEST_PLAN_FEASIBILITY_BLOCKED and native RESOURCE_GUARD_BLOCKED.

All source anchors below are in src/innovation/phase2/test_os_connector_v1; exact AST spans are in B2_Q1_SOURCE_CROSSWALK.csv.

| History | Source/function/line | Interpretation and failure behavior |
|---|---|---|
| STOP before context/API admission | fixtures.py:65-118 _probe_context / q1_denied_creations; os_api.py:230-243 raw_probe_create | Bounded positive waits abort; no accepted denial. A demonstrably unissued call is cancelled, prepaid quota never refunded. |
| STOP wins against logical probe CAS | fixtures.py:104-114 admit; unchanged gate.py:89-107 _swap | Same authoritative word cannot change from STOP to IDLE; no new logical admission. |
| Probe CAS wins, STOP observed before API | os_api.py:237-243 raw_probe_create | Phase5 cancellation; no native receipt or physical-start claim fabricated. |
| STOP after final check but before physical API | os_api.py:244-250 raw_probe_create | Pre-S admitted call may physically start/return later; I3 NOT_CLAIMED. Missing/late outcome is terminal; no post-S probe2. |
| Completed native FALSE with E1-E7 | probe_protocol.py:89-131 evaluate_denial; observer.py:128-146 _q1_probe_cleanup | Conditional API-only acceptance, exit N/A; no unique cause or physical no-child-ever assertion. |
| FALSE with bad context/error/ABI/image | probe_protocol.py:95-131 evaluate_denial | API_REJECTED retained, attribution unverified; terminal, second slot NOT_STARTED, no next case. Generic OSError never supplies native FALSE. |
| First denial accepted; second requested | fixtures.py:104-148 admit / q1_denied_creations | First complete receipt plus observer ACK, fresh context/time/quota and fresh same-word CAS required. Cached ACK alone never grants authority. |
| ACK or STOP race | observer.py:132-145 _q1_probe_cleanup; fixtures.py:141-148 | ACK may be physically written after S if acceptance CAS preceded S. It is historical evidence only. Worker STOP check and fresh probe2 CAS still reject new post-S admission. No I1/I3 claim. |
| Historical accepted receipt after normal S | observer.py:129-131; campaign.py:81-96 complete | Keep historical acceptance; this does not authorize new work. Only both accepted receipts plus unchanged other oracles and real pair exits may complete Q1. |
| TRUE followed by identity/query exception | fixtures.py:119-156; probe_protocol.py:89-93 | UNEXPECTED_CREATED is preserved. Original handles stay retained; cleanup is failed TEST, not a denial. |
| TRUE with both memberships confirmed | actor.py:192-223 _probe_memberships; observer.py:155-208 | Memberships checked through exact owners; S/direct retained kill and separate real exit. Cleanup never upgrades failed probe to pass. |
| Successful breakaway outside outer Job | observer.py:170-199; fixtures.py:18-62 _creator_cleanup | Hard containment failure; do not assume outer termination covers probe. Use available original/copy PROCESS kill; uncertain exit remains EXIT_UNVERIFIED. |
| Producer dies during create/before transfer | observer.py:107-125 _q1_probe_cleanup | Pending/claimed receipt is unknown, not expected denial. No next case; potentially escaped live child is an OPEN P1 physical gap. |
| Remote duplicate succeeds, publication interrupted | os_api.py:266-277 delegate_probe_process; ipc.py:59-78 publish | Destination may hold an undiscoverable reference. No PID/handle invention; terminal unverified. Source cannot guarantee cleanup of that target. |
| Return/custody arrives after S | observer.py:230-367 one | Existing cutoff bounds cleanup-only late-result routing; no accepted new probe or retry. Reliable late TRUE still fails. |
| Kill API fails or handle not signaled | os_api.py:280-289 kill_probe; observer.py:201-208 | Request/return/error separate from actual exit. No automatic retry/replacement; unresolved proof stays unverified. |
| Logging/ACK blocks or controller dies | fixtures.py:18-62; observer.py:211-228; actor.py:161-223 | STOP/direct known-probe kill precedes optional cleanup persistence. Existing independent L01 and outer enforcers do not await policy witness/ACK/log/actor. Evidence may remain PARTIAL. |
| Normal pair exits but probe unresolved | campaign.py:81-96; probe_protocol.py:144-148 | Pair exits never discharge pending/unknown/unaccepted probe. Campaign cannot continue. |

## Ordering and resource premises

I2 STOP remains the unchanged atomic terminal exchange (guard_remediation_v2/gate.py:82-87). IDLE-to-IDLE CAS is TEST logical admission; claim fields in the separate TEST mapping prevent replay. No science ISSUE/CONSUME transition is changed. No lock is held over create, membership, telemetry or kill. Neither API return nor Python scheduling gives a physical deadline/I1/I3 theorem.

Seven independent terminal identities, one observer, 15 nominal instances plus two prepaid attempts (17<=18), concurrent3, outer2GiB/active3, inneractive2/Q1 96MiB, shared nominal120s and zero retry remain. No extra positive trial or JOB_LIST. A possibly broken active3 assumption fails qualification; post-hoc counts cannot certify a peak. Token/context stability and actual API progress remain runtime assumptions.

Prior r1 failed reasoning is preserved in q1_denial_integration_history/r1_eb05053d; prior QC syntax failure remains historical. Adoption of the conditional API standard does not cure the pre-custody P1. Source manifest SHA-256 in B2_Q1_REMEDIATION_SNAPSHOT_ID.txt is not a Git commit.
