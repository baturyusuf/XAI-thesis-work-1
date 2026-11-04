# G04 source review and API provenance

## Scope

Current human instruction:G04 source only. No generated-module import/execution, dynamic state/scheduling model, thread/process/Job test, worker, native science import/fit/predictor, commit or push. Ten files only parsed as Python3.11 grammar and compiled to unexecuted code objects. Syntax consistency is not runtime safety or all-interleavings proof.

## Read-only consultation

GPT6Luna openai-subscribed/gpt-6-luna, session2e7a0f16-8312-49d5-aa8e-e335ca4b0ddf. Conceptual/static review of controller/channel/worker/OS source. No writes/imports/tests/OS or worker execution. It could not locate B2 document copies on its first pass; parent read the pinned contract/admission/handoff objects and retained responsibility. No reasoning selector or local/Rumeli model used.

Initial conclusion under separate nontransactional APIs, arbitrary preemption and no finite syscall bound:strict physical I1 and STOP independent of a lock held over OS resume are not jointly established. A token claim cannot be renamed physical syscall invocation. Same distinction applies to actual Python-call entry for I2.

Follow-up inspected the atomic gate integration and supported only conditional logical admission ordering, assuming fresh shared/aligned word, intended peers, correct interlocked ABI and no reset. It raised reference-counter writes and gate/ledger ordinal binding. Parent added explicit ticket.sequence==unit ordinal checks at both peers and documented reference writes as bookkeeping inside an admitted unit, not new node-call authorization. If stronger per-node physical admission is required, that remains unproved. Final small create-claim/central fatal-path refinements were parent-reviewed, not a separate full independent source acceptance. Decision remains SOURCE_REMEDIATION_REQUIRED.

## Primary API text actually read

https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread
ResumeThread takes a thread HANDLE, decrements suspend count and reports the prior count. -1 fails;0 means not suspended;1 resumes;>1 remains suspended. Its interface has no transaction with a user-memory STOP word. No finite completion bound was established.

https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedcompareexchange
Atomic32bit compare/exchange, original value returned,32bit alignment required, full barrier and atomicity relative to other interlocked calls documented.

https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedexchange
Atomic32bit exchange, original value returned, full barrier and atomicity relative to other interlocked calls documented.

Generic authorization banners were present but substantive text was accessible. These live documentation reads are NOT immutable target-machine execution evidence or proof that no stronger API could ever exist. Parent makes the LIMITED incompatibility argument for the supplied API pair/assumptions, not a global Windows impossibility theorem.

## Preservation/preparation

Pre-G0432-file packet plus original-path/hash map was copied before edits. Old23-file source identity7338a018695665960cc41a2b57632421954b9678fef26e6a3c86284190c43809 is reconstructible through archive mapping and unchanged frozen dependencies. v1 evidence/failures untouched.

One oversized documentation-writing terminal invocation failed shell parsing with exit2, unexpected EOF looking for matching double quote. Python/document writes did not execute; split file-writing commands succeeded. This was preparation, not a guard test or model failure; no process/Job test budget was consumed. No failed runtime records were removed or replaced.

A later documentation-only update initially failed because Windows default cp1254 decoding was applied to UTF8 text (UnicodeDecodeError). Explicit UTF8 reads and targeted typographic repair were used for current generated reports only; frozen source/contracts/archive bytes were not changed. No generated module executed and source-manifest identity was unaffected.
