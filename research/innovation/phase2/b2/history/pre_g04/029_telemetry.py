"""Disposable telemetry; NEVER called by the stop/kill path."""
from collections import deque
import json
import os
import threading
import time

class EvidenceBus:
    def __init__(self, maximum=16384):
        self.items = deque(maxlen=maximum)
        self.dropped = 0
        self.degraded = False
        self.writer_error = None
        self.samples = deque(maxlen=maximum)

    def offer(self, kind, **values):
        """CPython deque append only; no queue/log lock and no durable operation."""
        try:
            if len(self.items) == self.items.maxlen:
                self.dropped += 1
                self.degraded = True
            self.items.append(dict(kind=kind, qpc=time.perf_counter(), **values))
        except BaseException:
            self.degraded = True

    def start_writer(self, output):
        def writer():
            try:
                with output.open('x', encoding='utf-8') as f:
                    while True:
                        try:
                            record = self.items.popleft()
                        except IndexError:
                            time.sleep(.02)
                            continue
                        f.write(json.dumps(record, default=str, allow_nan=False)+chr(10))
                        f.flush()
                        os.fsync(f.fileno())
            except BaseException as exc:
                self.writer_error = type(exc).__name__
                self.degraded = True
        thread = threading.Thread(target=writer, daemon=True, name='optional-evidence-writer')
        thread.start()
        return thread

    def start_sampler(self, job, worker_getter, launch):
        """Sampler is NOT enforcer; query failures degrade only this channel."""
        from . import os_api as O
        def sampler():
            previous_completion = launch
            try:
                while True:
                    start = time.perf_counter()
                    rows = [dict(pid=os.getpid(), **O.A.process_memory(O.B.current()))]
                    worker = worker_getter()
                    if worker is not None and not O.signaled(worker.hProcess):
                        rows.append(dict(pid=int(worker.pid), **O.A.process_memory(worker.hProcess)))
                    end = time.perf_counter()
                    private = sum(x['private_commit'] for x in rows)
                    working_set = sum(x['working_set'] for x in rows)
                    gap = start-previous_completion
                    if gap > .05 or end-start > .05:
                        self.degraded = True
                    self.samples.append(dict(start_qpc=start, completion_qpc=end,
                        preceding_gap_seconds=gap, processes=rows, current_private_sum=private,
                        current_WS_sum=working_set, sequential_not_atomic=True))
                    if len(self.samples) == self.samples.maxlen:
                        self.degraded = True
                    self.offer('sample', start=start, completion=end, gap=gap,
                               private_commit=private, working_set=working_set)
                    if working_set >= 2147483648:
                        worker_getter.request_stop('OBSERVED_WS_RESOURCE_LIMIT')
                    previous_completion = end
                    time.sleep(.05)
            except BaseException as exc:
                self.degraded = True
                self.offer('telemetry_error', scope='TELEMETRY_DEGRADED', error=type(exc).__name__)
        thread = threading.Thread(target=sampler, daemon=True, name='optional-WS-sampler')
        thread.start()
        return thread

    def tail(self, boundary):
        last = self.samples[-1]['completion_qpc'] if self.samples else None
        return dict(last_completed_sample=last, boundary_qpc=boundary,
                    tail_gap=None if last is None else boundary-last,
                    actual_process_exit_tail='NOT_MEASURED_WITHOUT_INDEPENDENT_EXIT_EVIDENCE',
                    status='TELEMETRY_DEGRADED' if self.degraded else 'PARTIAL',
                    dropped=self.dropped)
