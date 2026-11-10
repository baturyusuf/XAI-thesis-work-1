# Q1 r2 E1-E8 independent evidence audit

Implementation `a4e5cb276bc860847c3ae8d056829dfd3f1dd4da`; TEST anchors are under `src/innovation/phase2/test_os_connector_v1/`. Standard: `576283e769a13ae460713cff995ca994b18e9318`, B2_Q1_API_DENIAL_EVIDENCE_STANDARD.md:19-26 and Q1-F01/02/03/07. All four standard documents were independently matched to the copied blobs. No API call or evaluator function was executed.

**API_DENIAL_SOURCE_REVIEW_PASSED**, limited to implementation of the conditional rule. This is not adoption of a broader evidence contract or runtime rejection proof.

## Criterion-by-criterion result

| Gate | Decision | Source argument and limits |
|---|---|---|
| E1 exact native return | **VERIFIED_SOURCE** | os_api.raw_probe_create:218-263 directly invokes frozen B.create_process, takes int BOOL and completed/raw_return/API/origin fields. probe_protocol.creation_outcome:32-39 distinguishes 0/nonzero/unknown. Setup/caught OSError cannot synthesize the record. Actual BOOL is UNVERIFIED. |
| E2 error provenance | **VERIFIED_SOURCE** | os_api:236,244-254 checks use_last_error function flag16, resets private error, calls native API and immediately copies C.get_last_error on FALSE before timing/formatting/query calls. Python thread identity is recorded before/after. Frozen winjob_v4:6,31-32,47 loads kernel32 with ctypes.WinDLL(use_last_error=True), explicit argtypes and BOOL restype. This is a synchronous same-thread ctypes last-error copy, not error.winerror/errno inference. Runtime binding behavior is unexercised. |
| E3 intended valid request | **CONDITIONAL** | os_api:222-229,255-263 fixes the approved direct interpreter, exact six argv elements, mutable Unicode buffer, explicit application path, default security/environment/cwd, no extended attributes/replacement parent, suspended+detached flags12 plus optional0x01000000. Frozen ABI guards require x64/STARTUPINFO104/PROCESS_INFORMATION24; evaluator:108-115 checks [8,104,24], actual image hash, direct Python3.11.9 and equal nominal launch fingerprint. File/security/token/context stability and target-build applicability are assumptions, not proved by a hash or a new positive child. |
| E4 exact combined policy | **CONDITIONAL** | actor._prepare_probe_policy:161-190 and observer._prepare_probe_policy:71-98 query their OWN live inner/outer handles, caller generation and exact nominal member sets. probe_protocol._contexts_ok:54-75 binds attempt, identities, observed times and deadline; active2/96MiB versus active3/2GiB, UI0 and flags0x2208 must match. Source has no policy mutation/inner export; actual nested enforcement and stability through a race remain runtime premises. |
| E5 combined attribution | **CONDITIONAL** | probe_protocol:7-9,117-120 declares conservative codes5/1816 before results and also requires E3/E4, exact variant, competing-context label and no known competing failure. This can classify only the reviewed combined scenario under its assumptions. Codes are not exhaustive OS specifications, proof of sole cause or general denial predictors. |
| E6 complete receipt | **VERIFIED_SOURCE** | plan:15-22, checked_return:25-29 and evaluate_denial:121-124 bind run/epoch/ordinal/image/prepayment/standard/source hash. fixtures:100-140 publishes a complete per-attempt return; IPC:59-78 makes probe frames write-once. Receipt loss, malformed data, payload overflow or producer death cannot be filled from denial bits. Delivery/durability is not guaranteed. |
| E7 no contradiction | **VERIFIED_SOURCE** | evaluate_denial:89-93 rejects non-FALSE before context checks; :125-128 checks absence of a success identity/copy/thread target and later error, unspecified FALSE-output handles and no observed STOP at receipt. fixtures:119-156 retains a reliable nonzero outcome across later identity/delegation failures. Missing reliable result remains unknown, never a fabricated denial. Complete truth/absence of outside competing faults is not measured. |

There is no identified SOURCE_DEFECT in E1-E7 wiring under the declared model. VERIFIED_SOURCE does not mean these gates were satisfied by an actual request. CONDITIONAL is deliberately weaker than proof of target-system validity.

## R2-C01 -- P2 context/attribution qualification

Source: os_api.launch_fingerprint:320-332 and primary_token_identity:292-317; actor:241-243; evaluator:108-120. The nominal fingerprint is captured before the EXISTING worker creation. Probe caller fingerprint includes image/path/cwd hashes, PATH/SYSTEMROOT/WINDIR subset and primary TokenId/AuthId/ModifiedId/restriction state. It is not a full environment/security-policy certificate. Exact token-object statistics may conservatively mismatch a legitimate copied token; mismatch blocks rather than earns a denial/retry.

Minimum action: retain the stable reviewed launch/security-context premise and disclose fingerprint coverage. Do not tune allowed errors/fingerprint rules after observing results. Any broader causal claim requires a separately justified contract, not a code silently converting unrelated failures to success. Future actual fingerprint/ABI/context observations remain UNVERIFIED; no extra positive child/control is allocated.

## E8 -- E8_SOURCE_REVIEW_PASSED

1. Each attempt plan binds run/epoch/ordinal/kind/image/precharge to a distinct write-once probe0/probe1 frame. fixtures:94 claims each ordinal only by 0->1; raw_probe_create:230-243 advances 1->2 or cancellation5, never resets. After raw return, 2->3->4 is bookkeeping. There is no retry/replacement path.
2. Observer:126-146 obtains checked_return and evaluate_denial, requires accepted API_REJECTED, a non-stopped channel and live normal pair, then performs gate._swap(IDLE,IDLE) before marking the matching probe_acceptN. It caches acceptance only as historical evidence. The ACK is not a blanket permission.
3. Worker fixtures:141-148 waits for that ordinal ACK under the original deadline, then rechecks STOP/fixture_error. Before probe2, admit:108-114 re-reads/evaluates the first immutable receipt, requires probe_accept0 and issues a NEW IDLE-to-IDLE CAS. Second attempt also has its own exact inner/outer context, not the first context reused.
4. Frozen guard_remediation_v2/gate.py:82-107 exchanges STOP on the SAME authoritative word and uses InterlockedCompareExchange for _swap. If S wins first, CAS returns STOP and raises GateStopped; it cannot reopen IDLE. This word belongs to the original Channel mapping, not the separate TEST metadata claim/ACK flags.
5. If the acceptance CAS wins before S but the ACK write happens physically after S, it is still only historical acceptance. A post-ACK STOP check or probe2 CAS rejects further logical admission. If probe2 CAS wins BEFORE S, its physical call can start/return later; raw_probe_create:239-245 adds a final observed cancellation check but does not claim I1/I3 exclusion.
6. campaign.complete:81-96 and probe_protocol.next_case_admissible:144-148 require both accepted immutable receipts, claims[4,4], ACKs[1,1], no pending probe/fixture error, plus normal pair exit/S checks. Two prepaid attempts are never post-S permission. Unaccepted/unknown first outcome cannot start probe2 or another lifecycle.

No stale-ACK/reset/replay counterexample was identified in the trusted single-producer graph. No physical Win32-entry ordering, malicious actor resistance, scheduler fairness or actual atomic/IPC observation was established. Wrong/missing context from a runtime failure blocks receipt acceptance; owner queries and source immutability, not arbitrary metadata assertions, support the source argument.

The worker preflight waits for both matching attempt contexts and the nominal fingerprint. It does not atomically re-run every E4 field check inside the final native-call boundary: valid policy values rely on the independently checked owner-emitter paths and their no-mutation premise; complete E4 receipt validation also occurs after return. Missing/wrong attempt or fingerprint blocks the source path, but this is not a guarantee against forged metadata, unreviewed policy mutation or all runtime query failures. No concrete wrong-context emission was identified in the pinned trusted-role graph. This boundary is part of R2-C01, not evidence that CAS alone proves policy validity.

## Creation, interpretation and exit are separate axes

| Evidence | Correct classification / consequence |
|---|---|
| Reliable native FALSE | API_REJECTED; no returned child object or fabricated EXIT_CONFIRMED. E1-E7 must additionally hold for conditional API-level negative-control acceptance |
| Reliable FALSE but bad/missing context/error | API_REJECTED + DENIAL_OBSERVED_CAUSE_UNVERIFIED; no second probe/pass. Attribution uncertainty is not evidence that a child was created |
| Reliable nonzero | UNEXPECTED_CREATED + TEST_FAILED, regardless of later initialization/cleanup/query result. Exact probe exit remains separately required |
| Missing trustworthy outcome / interrupted call | UNKNOWN_OR_INTERRUPTED, EXIT_UNVERIFIED; stop known scope, no later admission. Expected OS denial does not fill the receipt |
| Kill request or API return only | EXIT_UNVERIFIED until the exact retained object provides signal/identity/exit-time/code evidence |
| Exact retained object satisfies all exit checks | EXIT_CONFIRMED_RETAINED_OBJECT for that probe only; a previously unexpected creation remains a failed TEST |

When a complete raw-result object survives, later retention/context failure cannot erase its TRUE. If the producer dies inside the native wrapper or while returning a record, no complete result may survive at all; this is UNKNOWN, not a manufactured FALSE. Pre-custody handling remains [blocked](Q1_R2_PRE_CUSTODY_SAFETY_AUDIT.md) under the current full custody contract.

Primary error contract: https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror -- last error is thread-local, must be captured immediately, and per-function error lists are not complete fixed API specifications. The ctypes private same-thread copy is supported by the pinned use_last_error binding; no ctypes or project binding was imported/executed here.
