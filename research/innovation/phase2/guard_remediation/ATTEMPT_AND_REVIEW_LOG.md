# Bounded attempt and source-review log

Before launch:DIAGNOSTIC_PLAN.json fixed14 named cases, maximum16 invocations including2 explicitly justified corrections. No automatic retry. At completion16/16; no further process probe authorized. The fixed native D1a caps were not consumed because there were0 fits/calls.

-01 memory_causal96: successful16MiB, rejected32MiB, free parent40MiB, separate successful32MiB. Source revision01.
-02 memory_preassignment96: same fixed sequence, parent allocation before job assignment.
-03 containment_natural: thirdchild1816, breakaway5, natural worker exit, kill-on-close controller exit.
-04 setup_deadline;05 rational_deadline;06 native_dummy_deadline;07 postfit_deadline;08 global_deadline:intended short watchdog stop reasons observed. No scientific operation.
-After08:preserved source snapshot b72b3ee14c607e742cdca036e7fdb377454efc668cbca9053aac8a132ecf0e65. Revision02 adds lifecycle-tail evidence, independently queried worker exit code and attempted release of completed Python Thread object. That release did NOT eliminate residual count differences; no success claim.
-09 worker_exception;10 controller_exception;11 whole-job termination93;12 stalled shutdown/lifecycle kill92;13 preflight failure with no worker;14 injected monitor error. Case12 lifecycle overshoot is a resource violation. Per-case raw records retained.
-After14:independent source review found a dead-monitor/failed-kill path and old initial interval omission. Preserved revision02 source snapshot40db2254a8ce42fd74ee089102262344e80d8eca1fac2f5145ca6d54fae33c77. Revision03 adds initial pre-job sample/initial-gap admission check and immediate whole-job/owner-exit escalation. No cap/architecture change.
-15 correction_containment_natural:one planned corrective launch; maximum gap43.8939ms including initial sample; containment denials preserved.
-16 correction_monitor_failure:second and FINAL corrective launch. Controller98, worker90, retained-handle exit proof, no external rescue. Missing monitor-tail data remains NOT_MEASURED; direct termination-failure branches not injected.
-Offline:19/19 narrow software regressions,0 Job Object launches. Compile checks use stdlib only. No full old scientific suite run.
-One documentation-writing shell invocation failed with exit2, bash unexpected EOF looking for matching double quote, because the oversized command was truncated. No Python/controller/worker job ran in that invocation and no document write occurred; split commands succeeded. This preparation error is not a native/scientific failure. It is not counted as a controlled probe or hidden from the record.

Prior raw failures, v2 syntax-error evidence and misleading SELFTEST_PASSED were not removed. Four old manifests verify byte-for-byte. Runtime source hashes in every launch resolve to current source or archived revision snapshots.

## Subagent record and critical review

Policy delegation from the earlier context used GPT6Luna session af22c59f-4adb-4696-8fa2-06b685a6a8fd. Main reviewer corrected unbounded short profiles, initial namespace and transition-after-deadline issues;8 pure policy tests passed before OS tests. Those8 are included in current19, not added separately.

Independent source review here:session695909dd-4b74-4030-9c3b-a6c35c282173, model openai-subscribed/gpt-6-luna. Read-only API/worker/policy review, then controller/probe follow-up. No delegate OS probes or scientific imports. No task-level reasoning selector was available/claimed. No local/Rumeli model used.

Accepted findings:explicit path bootstrap needed under -I -S (implemented in launcher), monitor must actually enforce policy (controller thread implemented), non-atomic sample scopes, uncertain cleanup, initial-gap omission and monitor-exception fail-open possibility. Main reviewer rejected the claim that GetSystemTimePreciseAsFileTime needs a BOOL error check:it returns VOID. Killing the controller at FINAL lifecycle is expected for same-job whole-tree enforcement; status must be durably recorded BEFORE that kill, not after. A third production supervisor was not introduced in response to review. Review cannot promote tested dummy code to native admission.

Ledger null/blank fields mean NOT_MEASURED or no applicable worker; they are never measured zero. Raw schema scopes distinguish current private commit, current WS and OS historical peaks.19 test passes are guard tests only; admission stays BLOCKED.
