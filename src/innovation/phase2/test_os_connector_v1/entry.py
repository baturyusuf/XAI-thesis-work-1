# Minimal unreleased TEST entry; no OS/project backend import until false brakes pass.
import sys
import time
from .config import ROOT, require_test_execution


def argv_for(role, run, epoch, approval):
    require_test_execution()
    if role not in ('controller', 'worker'):
        raise ValueError('No arbitrary TEST process role')
    code = ('import sys,runpy; sys.path.insert(0,'+repr(str(ROOT/'src'))+
            '); sys.argv='+repr(['B2_TEST', role, run, epoch, approval])+
            '; runpy.run_module('+repr('innovation.phase2.test_os_connector_v1.entry')+
            ',run_name='+repr('__main__')+')')
    return [sys.executable, '-I', '-S', '-B', '-c', code]


def main(arguments):
    require_test_execution()  # Entry brake, before imports that bind Windows APIs.
    role = arguments[0]
    if role == 'observer' and len(arguments) == 2:
        from .observer import run
        return run(arguments[1])
    if role in ('controller', 'worker') and len(arguments) == 4:
        from .roles import controller_main, worker_main
        function = controller_main if role == 'controller' else worker_main
        return function(*arguments[1:])
    raise ValueError('Fixed TEST roles only')


if __name__ == '__main__':
    main(sys.argv[1:])
