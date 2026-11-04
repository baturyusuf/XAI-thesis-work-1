# Guard-only simulated units: no NumPy, native LIME, predictor or M1/M2/M4 math.
VERSION = 'B2-guard-dummy-source-r1'


def create_operations(identity):
    if identity.get('backend_mode') != 'guard_dummy':
        raise ValueError('Explicit TEST-only simulated identity required')
    return DummyOperations(dict(identity))


class DummyOperations:
    mode = 'guard_dummy'
    def __init__(self, identity):
        self.identity = identity

    def predict(self, context, rows):
        raise AssertionError('Dummy has no actual predictor')

    def rational_references(self, permit):
        permit.check()
        permit.record_check('M1')
        permit.record_check('M4')
        return dict(scope='SIMULATED_GUARD_HANDSHAKE_NOT_M1_M4_CORRECTNESS')

    def execute(self, ticket, permit):
        permit.check()
        permit.observe_precall('SIMULATED_'+ticket.role.upper())
        if ticket.callbacks:
            rows = [(0.0, 0.0)]*ticket.logical_rows
            permit.simulated_callback(rows)
        else:
            permit.reference(nodes=0, cells=0, solves=0)
            permit.reference_complete(nodes=0, cells=0, solves=0)
        return dict(version=VERSION, role=ticket.role,
            scope='SIMULATED_ADMISSION_UNITS_NOT_SCIENTIFIC_WORK',
            actual_model_rows=0, actual_model_callbacks=0, native_fits=0,
            reference_math='NOT_APPLICABLE')
