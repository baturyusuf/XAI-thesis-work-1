# Guard counterexamples and remediation record

## CEX-G1: console helper breaks strict2process scope
v3 rawrecord: assigned3/listed3/accounting_active3. Samejob live controllerpython2888, workerpython14304, conhost16208. Worker had not written its entry sentinel. This invalidates the tested launch configuration BEFORE any scientific import/fit. v1 did not save executable names, so do not retroactively label its unidentifiedPID with certainty. The venv-only hypothesis was a hypothesis, not a finding. API process-list source inspected: https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_process_id_list .

Guard-only v4 replaces CREATE_NO_WINDOW by DETACHED_PROCESS, still suspended, samejob, activecap2, nobreakaway, killonclose, jobmemory flag. Observed containment passes and child/breakaway calls denied1816/5; no thirdmember ignored and no processcap increase. Originalv1/v2/v3 and failed records preserved. This is a launcher fix, not a LIME patch or general guard qualification.

## CEX-G2: raw pass is not hard-memory admission
v4memory record saysSELFTEST_PASSED after a request denial, yet configuredJobMemoryLimit100663296B and OSpeak111931392B disagree. Sampled private sum78311424B is not OS jobpeak and cannot validate the missing instantaneous bound. Both controller40MiB and child16MiB commit succeeded; next32MiB denied1455. No correlated job-limit event/current-commit evidence excludes another commit constraint or establishes how rejected/transient charges enter the peak. Do not call this a demonstrated OS defect or silently discard the peak. New guard_qualification_v1 explicitly BLOCKS this record even if other gates are declared true; regression includes it.

Needed before another admission proposal: documented counter/current/peak/limit semantics, correlated job-memory-limit notification/violation and system-commit diagnostics, independent aggregate private-commit checks without treating polling as enforcement, and handling of transient/failed charges under the unchanged2GiB cap. No new numerical/native experiment is warranted to resolve an OS accounting question.

## CEX-G3: harness syntax failure
v2 source edit replaced the wrong suspended-call line and produced IndentationError atline24 before controller entry. Full failing source is preserved. Narrow correction targets only the controller launch; v2fixed then still failed the process-count gate. No native execution/retry was involved. The retained parse-invalidsource is itself checked by a logging regression.

## Other mandatory unclosed prerequisites
Implement/selftest perphase60/30/60/20 and global600/shutdown-only5/lifecycle605 with durable phase transitions, exact kill/workerexit/overshoot timestamps and no science after stop. A one-second sleeping-worker test is not that implementation. Validate direct-base -I -S plus ONLY pinned isolated packages/thread settings before native import, without patching the oldenv. Pre-call attempted-fit/row/callback reservations and first-hard-error stopping must be part of any future scientific runner. No such runner is enabled now. Repeat guard-only checks under explicit direction; do not automatically retry science or raise caps. Current qualification remains RESOURCE_GUARD_BLOCKED.
