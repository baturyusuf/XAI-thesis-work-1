"""Explicit prospective entry; no CLI, automatic execution or current release."""

def execute_approved(approval_relative, evidence_relative):
    """Own isolated controller ONLY; normal termination exits this process.

    This function is NOT invoked by this source-only task. Authority fields are
    auditable human-governance declarations, not an adversarial security token.
    Native execution still needs independent source/qualification/human release.
    """
    from . import EXECUTION_AUTHORIZED
    if EXECUTION_AUTHORIZED is not True:
        raise PermissionError('B2 is SOURCE ONLY; no dynamic release')
    import os
    import sys
    from pathlib import Path
    from .config import authority_only, inside, verify_bound_run
    authority_only(approval_relative)  # Denial blueprint fails before Win32 imports.
    if sys.version_info[:3] != (3, 11, 9) or not (sys.flags.isolated and sys.flags.no_site):
        raise PermissionError('Isolated Python3.11.9 -I -S controller required')
    if Path(sys.executable).resolve() != Path(sys._base_executable).resolve():
        raise PermissionError('Use direct base interpreter; no venv redirector process')
    job = actor = None
    try:
        from . import os_api as O
        from .config import PRODUCTION, ROOT
        launch = O.A.process_start_clock()
        job = O.OwnedJob(PRODUCTION)
        job.attach_controller()
        # No worker or science exists yet. No log/fsync precedes enforcer arming.
        from .telemetry import EvidenceBus
        from .controller import Controller
        bus = EvidenceBus()
        actor = Controller(job, launch, bus)
        actor.thread.start()
        actor.armed.wait()  # Enforcer failure calls fatal owner exit, never silent return.
        if actor.channel.stopped():
            raise PermissionError('STOP before full source/config admission')
        # All potentially blocking source/package/durable work is AFTER t_arm.
        approved = verify_bound_run(approval_relative)
        import json
        from .budget import Slot
        registry = json.loads((ROOT/'research/innovation/phase2/evidence/D1A_PLANNED_SLOT_REGISTRY.json').read_text())
        slots = tuple(Slot(r['context'], r['slot'], r['seed']) for r in registry['slots'])
        output = inside(evidence_relative)
        if output.exists():
            raise FileExistsError('Evidence output may not overwrite old records')
        output.parent.mkdir(parents=True, exist_ok=True)
        bus.start_writer(output)
        bus.start_sampler(job, actor, launch)
        actor.submit(approved, slots)
        actor.worker_exited.wait()
        # Enforcer remains armed while this normal-cleanup record can block.
        summary = output.with_name(output.name+'.summary.json')
        with summary.open('x', encoding='utf-8') as f:
            json.dump(dict(status='PARTIAL_UNTIL_EXIT_PROVEN', worker_exit=actor.exit_evidence,
                           ledger=actor.snapshot, boundaries=actor.boundaries,
                           telemetry_tail=bus.tail(__import__('time').perf_counter()),
                           actual_controller_exit=None), f, default=str, allow_nan=False)
            f.flush()
            os.fsync(f.fileno())
        actor.cleanup_done()
        # Nothing with side effects follows this wait. Owner enforcer closes job/exits.
        actor.thread.join()
        job.fatal_owner(99)  # Unexpected enforcer return is a control fault.
    except BaseException:
        if actor is not None:
            actor.request_stop('CONTROLLER_MAIN_ERROR')  # NO writer/lock/ACK first.
            if not actor.thread.is_alive():
                job.fatal_owner(99)
        elif job is not None:
            job.fatal_owner(99)
        else:
            os._exit(99)  # Closes any partially constructed unnamed job handles.
        actor.thread.join()
        job.fatal_owner(99)
