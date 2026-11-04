# Pinned public LIME connector; source only until admitted worker import.
# No internal patch, sampler override, retry, second fit, cache or model bypass.
from fractions import Fraction
from itertools import product
from .reference_arithmetic import rational_references, independent_reference

PREDICTOR_ID = 'A3-D1A-M2-numpy64-ordered-v1'
VERSION = 'B2-native-lime-0.2.0.1-source-r1'


def create_operations(identity):
    if (identity.get('frozen_predictor_id') != PREDICTOR_ID or
            identity.get('target_class') != 1 or identity.get('output_scale') != 'probability' or
            identity.get('num_samples') != 128):
        raise ValueError('Wrong frozen native scientific identity')
    # Worker consumes IMPORT before importing this module/calling here.
    import numpy as np
    from lime.lime_tabular import LimeTabularExplainer
    from sklearn.linear_model import Ridge
    return NativeOperations(dict(identity), np, LimeTabularExplainer, Ridge)


class NativeOperations:
    mode = 'native'
    def __init__(self, identity, np, explainer_type, ridge_type):
        self.identity, self.np = identity, np
        self.explainer_type, self.ridge_type = explainer_type, ridge_type
        self.saved = None
        self.slot_key = None
        self.background = None

    def rational_references(self, permit):
        return rational_references(permit)

    def predict(self, context, rows):
        np = self.np
        if type(context) is not int or context not in (0, 1):
            raise ValueError('Context is a fixed closure, not a feature')
        z = np.asarray(rows)
        if z.dtype != np.dtype('float64') or z.ndim != 2 or z.shape[1] != 2 or not np.isfinite(z).all():
            raise ValueError('Expected finite float64 Nx2 input, without coercion')
        if context == 0:
            p = np.full(z.shape[0], np.float64(.25), dtype=np.float64)
        else:
            omega = np.float64(float.fromhex('0x1.921fb54442d18p+0'))
            amplitude = np.float64(9) / np.float64(20)
            p = np.float64(.5) + ((amplitude * np.sin(omega*z[:, 0])) * np.sin(omega*z[:, 1]))
        out = np.column_stack((np.float64(1)-p, p))
        if (out.shape != (len(z), 2) or not np.isfinite(out).all() or
                (out < 0).any() or (out > 1).any() or
                (np.abs(out.sum(axis=1)-1) > 1e-12).any()):
            raise ValueError('Invalid probabilities; no normalization')
        return out

    def execute(self, ticket, permit):
        permit.check()
        if ticket.role == 'generation':
            return self._generation(ticket, permit)
        if self.slot_key != (ticket.slot.context, ticket.slot.index):
            raise ValueError('No matching saved native explanation')
        if ticket.role in ('q4', 'qj4', 'qj16'):
            return self._evaluation(ticket, permit)
        if ticket.role == 'reference':
            result = independent_reference(self.saved, permit)
            self.saved = None
            self.slot_key = None
            return result
        raise ValueError('No extra role or default work')

    def _generation(self, ticket, permit):
        np = self.np
        if self.saved is not None:
            raise ValueError('No replacement or concurrent fit')
        if self.background is None:
            r = np.sqrt(np.float64(3)/np.float64(2))
            self.background = np.asarray(list(product((-r, np.float64(0), r), repeat=2)), dtype=np.float64)
        explainer = self.explainer_type(self.background, mode='classification',
            feature_names=['z1', 'z2'], class_names=['0', '1'], categorical_features=[],
            discretize_continuous=False, sample_around_instance=True,
            feature_selection='none', random_state=ticket.slot.seed)
        capture = {}
        ridge_type = self.ridge_type
        class CapturedRidge(ridge_type):
            # Public model_regressor hook: record, then exactly one super.fit.
            def fit(regressor, X, y, sample_weight=None):
                permit.check()
                permit.observe_native_fit_stage('WRAPPER_ENTRY_OBSERVED')
                if 'design' in capture:
                    raise ValueError('Second native fit forbidden')
                if X.shape != (128, 2) or y.shape != (128,) or sample_weight.shape != (128,):
                    raise ValueError('Native design/weight/target mismatch')
                capture.update(design=X.copy().tolist(), weights=sample_weight.copy().tolist(),
                               fit_target=y.copy().tolist())
                permit.observe_precall('RIDGE_FIT_WITHIN_CONSUMED_GENERATION')
                permit.observe_native_fit_stage('SUPER_FIT_PRECALL_OBSERVED')
                result = super(CapturedRidge, regressor).fit(X, y, sample_weight=sample_weight)
                permit.observe_native_fit_stage('RETURN_OBSERVED')
                return result
        model = CapturedRidge(alpha=1, fit_intercept=True, random_state=explainer.random_state)
        def callback(rows):
            # Only public LIME -> frozen-predictor path.
            values = permit.predict(rows)
            capture['generation_nodes'] = rows.copy().tolist()
            capture['responses'] = values.copy().tolist()
            return values
        permit.observe_precall('NATIVE_EXPLAIN_INSTANCE')
        explanation = explainer.explain_instance(np.zeros(2, dtype=np.float64), callback,
            labels=(1,), top_labels=None, num_features=2, num_samples=128,
            distance_metric='euclidean', model_regressor=model)
        permit.check()
        if not all(k in capture for k in ('design', 'weights', 'fit_target', 'generation_nodes', 'responses')):
            raise ValueError('Native capture incomplete')
        if set(i for i, _ in explanation.local_exp[1]) != {0, 1}:
            raise ValueError('Native feature identity/order mismatch')
        self.model, self.explainer = model, explainer
        self.slot_key = (ticket.slot.context, ticket.slot.index)
        self.saved = dict(capture, model=dict(intercept=float(model.intercept_),
            coef2=model.coef_.tolist(), mean2=explainer.scaler.mean_.tolist(),
            scale2=explainer.scaler.scale_.tolist()), evaluations={})
        state = [model.intercept_, *model.coef_, *explainer.scaler.mean_, *explainer.scaler.scale_]
        if not np.isfinite(np.asarray(state)).all() or (explainer.scaler.scale_ <= 0).any():
            raise ValueError('Nonfinite/degenerate native affine state')
        return dict(version=VERSION, context=ticket.slot.context, seed=ticket.slot.seed,
            background=self.background.tolist(), saved_generation=self.saved,
            native_weighted_r2=float(explanation.score), local_exp=[[int(i), float(v)] for i, v in explanation.local_exp[1]],
            target_class=1, scale='probability', generation_law='Gaussian plus fixed original row',
            capture='PUBLIC_MODEL_REGRESSOR_RECORD_THEN_SAME_RIDGE_ONCE')

    def _nodes(self, role):
        if role == 'q4':
            points = list(product((-1, 1), repeat=2))
        else:
            m = {'qj4': 4, 'qj16': 16}[role]
            points = [(Fraction(s)-Fraction(1, 6)+Fraction(2*i+1, 6*m),
                       Fraction(t)-Fraction(1, 6)+Fraction(2*j+1, 6*m))
                      for s, t in product((-1, 1), repeat=2)
                      for i in range(m) for j in range(m)]
        return self.np.asarray([[float(x), float(y)] for x, y in points], dtype=self.np.float64)

    def _evaluation(self, ticket, permit):
        np = self.np
        if ticket.role in self.saved['evaluations']:
            raise ValueError('No evaluation replay')
        nodes = self._nodes(ticket.role)
        if nodes.shape != (ticket.logical_rows, 2):
            raise ValueError('Predetermined grid size mismatch')
        probabilities = permit.predict(nodes)
        permit.observe_precall('SAVED_AFFINE_EVALUATION')
        scaled = (nodes-self.explainer.scaler.mean_)/self.explainer.scaler.scale_
        raw = self.model.predict(scaled)
        proxy = self.model.intercept_ + scaled @ self.model.coef_
        if (not np.isfinite(raw).all() or
                (np.abs(raw-proxy) > 1e-10*np.maximum(1, np.maximum(np.abs(raw), np.abs(proxy)))).any()):
            raise ValueError('Complete affine point conformance failed')
        if ticket.slot.context == 0 and (np.abs(raw-.25) > 1e-10).any():
            raise ValueError('Constant-context node conformance failed; no repair')
        permit.check()
        clipped = np.clip(raw, 0, 1)  # Explicit diagnostic adapter; never replace raw.
        item = dict(nodes=nodes.tolist(), probabilities=probabilities.tolist(),
                    raw=raw.tolist(), clipped=clipped.tolist())
        item['diagnostics'] = stored_loss_diagnostics(item)
        item['law'] = 'Q4' if ticket.role == 'q4' else 'QJ_FIXED_MIDPOINT_GRID_NOT_CONTINUOUS_RISK'
        item['computational_continuous_interval'] = None if ticket.role == 'q4' else ['0/1', '1/1']
        item['numerical_status'] = 'EXACT_STORED_FLOAT_AGGREGATION' if ticket.role == 'q4' else 'NUMERICAL_UNRESOLVED'
        item['context_null'] = 'NODE_RESIDUAL_ONLY_NOT_UNIFORM_PROOF' if ticket.slot.context == 0 else 'NOT_APPLICABLE'
        self.saved['evaluations'][ticket.role] = item
        return item


def stored_loss_diagnostics(item):
    # Exact aggregation of stored binary floats; not an ideal-real sine proof.
    f = lambda x: Fraction.from_float(float(x))
    p = [f(row[1]) for row in item['probabilities']]
    h = [f(x) for x in item['raw']]
    g = [f(x) for x in item['clipped']]
    n = len(p)
    raw = sum((abs(a-b) for a, b in zip(h, p)), Fraction())/n
    clipped = sum((abs(a-b) for a, b in zip(g, p)), Fraction())/n
    invalid = Fraction(sum(x < 0 or x > 1 for x in h), n)
    return dict(raw_loss=str(raw), clipped_loss=str(clipped),
                invalid_output_rate=str(invalid), clipping_gain=str(raw-clipped),
                aggregation='STORED_FLOAT_RATIONAL_ABSOLUTE_PROBABILITY_LOSS')
