# Re-review and native admission

Decision: RESOURCE_GUARD_BLOCKED. No native experiment may start.

## P0 execution gates

Mandatory monitoring/lifecycle/fail-closed coverage is not fully qualified; a narrow memory success cannot promote the aggregate decision to READY. The scientific job remains0 native imports/fits/predictor callbacks and16 unattempted slots. This is NOT an XAI failure. Source snapshot is guard-only and cannot be used as native launch authorization.

## P1 findings

1. Old summaries excluded startup interval. Several reconstructed initial gaps exceed50ms. New pre-job initial sample and fail-closed check were tested only in corrective15/16;16 loses final sample trace under deliberate termination. Whole lifecycle monitoring, including tail, is not universally verified.
2. Scaled shutdown-stall lifetime.4139134s exceeds.40s by.0139134s. Record violation; no full600/605s empirical test or scheduler guarantee. Production phase constants are unit-checked, not physically established by short timers.
3. Dead monitor + failed TerminateProcess was a source-level fail-open possibility. Revision03 escalates; monitor-error test passes actual termination98/90. Direct termination/job-termination failure branches remain source-reviewed only, not exercised. No completeness claim.
4. All explicit retained process/thread/query handles close, but before/after handle counts differ: observer126->128; controller pre-close includes unexplained additional handles. Their types/ownership are unresolved. Process exit evidence does not identify handle types, and count growth alone does not establish a leak.
5. The final harness always selects a diagnostic profile. Production constants are immutable and tested, but native production admission wiring remains unqualified. No new production supervisor/third process was introduced.

## P2 limitations

- Class28 is undocumented build diagnosis, not supported enforcement evidence.
- Sampled sums and historical peaks are distinct, non-atomic scopes.
- Last-job-close/whole-job termination kills controller too; final counter tails can be NOT_MEASURED. Durable pre-action records plus independent exit evidence are preserved.
- Dynamic source changed after08 and14 for narrow defects. Launch hashes resolve to preserved snapshots/current files. Old tests were not reclassified as final-revision tests.
- Short dummy tests and19 passing regressions are not scientific validation or native-readiness proof. Prior7/7, raw SELFTEST_PASSED and old failures stay unchanged.

## Options requiring another decision

Preferred: renew a SMALL, prebounded guard-only budget to classify residual handle types, audit initial/tail monitoring and force termination-API failure branches, after Agent5 source review. No cap change is requested or implemented. A staged pre-deadline shutdown margin could be proposed while retaining600/605 as ceilings; its semantics require explicit methodological approval before use. A separate production supervisor, third process or external runner would change the two-process/accounting architecture and requires HUMAN approval; not an automatic workaround. VM/container execution does not remove the same caps or validation requirements.

READY is withheld. No further process probe, native import or scientific calculation follows this report.

## Additional production enforcement gap (P1)

The watchdog uses process creation time, so delayed bootstrap is charged, but the watchdog thread itself starts AFTER Python imports/API setup and some synchronous durable writes. Backdating a deadline is not active enforcement while bootstrap is hung. Long blocking fsync/ack writes under the watchdog lock could likewise delay timer action. The short dummy tests do not prove these paths bounded. The external six-second test observer is NOT an approved production remedy. A leaner bootstrap/shorter locked sections might retain the same two-process architecture but need source review and a renewed bounded guard-only test plan. Replacing the controller or adding a supervisor is not implemented automatically.
