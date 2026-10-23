import unittest
from fractions import Fraction as F
import numpy as np
from innovation.phase1.native_lime import (BACKGROUND,OFFSETS,QueryLedger,generate,explainer,
    probability,weighted_ridge_reference,seed_for)
from innovation.phase1.float_adapter import computational_loss

class NativeLimeTests(unittest.TestCase):
    def setUp(self):
        self.center=np.array([1.,-1.]); self.seed=114
        self.ledger=QueryLedger()
        self.h=generate(self.center,self.seed,self.ledger.callback('generation'))
    def test_capture_is_native_default_not_changed_fit(self):
        e=explainer(self.seed).explain_instance(self.center,probability,labels=(1,),num_features=2,num_samples=128)
        self.assertEqual(e.local_exp,self.h.explanation.local_exp)
        self.assertEqual(e.intercept,self.h.explanation.intercept)
        np.testing.assert_array_equal(e.local_pred,self.h.explanation.local_pred)
        self.assertEqual(e.score,self.h.explanation.score)
    def test_independent_weighted_normal_equation(self):
        ref=weighted_ridge_reference(self.h)
        np.testing.assert_allclose(ref,np.r_[self.h.regressor.intercept_,self.h.regressor.coef_],rtol=0,atol=1e-13)
        r=self.h.regressor; x=r.design_; y=r.responses_; w=r.weights_
        residual=r.predict(x)-y
        self.assertLess(abs(np.sum(w*residual)),1e-12)
        np.testing.assert_allclose(x.T@(w*residual)+r.coef_,[0.,0.],atol=1e-12)
    def test_full_surrogate_matches_native_local_pred(self):
        np.testing.assert_array_equal(self.h.predict(self.center[None,:]),self.h.explanation.local_pred)
        self.assertNotAlmostEqual(float(self.h.predict(self.center[None,:])[0]),float(self.h.regressor.predict(self.center[None,:])[0]),places=6)
    def test_query_rows_and_native_perturbations(self):
        c=self.ledger.rows['generation']
        self.assertEqual((c['calls'],c['model_rows']),(1,128))
        r=self.h.regressor
        np.testing.assert_allclose(r.design_[0],self.center/self.h.scale)
        self.assertEqual(r.weights_[0],1.)
        dist=np.linalg.norm(r.design_-r.design_[0],axis=1)
        expected=np.sqrt(np.exp(-dist**2/(.75*np.sqrt(2))**2))
        np.testing.assert_allclose(r.weights_,expected,atol=1e-14)
    def test_pointwise_evaluation_is_batch_pure(self):
        z=self.center+OFFSETS
        np.testing.assert_array_equal(self.h.predict(z),np.r_[self.h.predict(z[:1]),self.h.predict(z[1:])])
        np.testing.assert_array_equal(probability(z),np.vstack([probability(row[None,:]) for row in z]))
    def test_seed_repeat_preserves_native_object(self):
        other=generate(self.center,self.seed,probability)
        np.testing.assert_array_equal(self.h.regressor.coef_,other.regressor.coef_)
        np.testing.assert_array_equal(self.h.regressor.design_,other.regressor.design_)
    def test_independent_finite_loss_reference(self):
        z=self.center+OFFSETS; p=probability(z); h=self.h.predict(z)
        result=computational_loss(p,h)
        ref=sum((abs(F.from_float(float(a))-F.from_float(float(b))) for a,b in zip(p[:,1],h)),F())/4
        self.assertEqual(result['raw_abs_loss'],ref)
        self.assertEqual(result['invalid_probability_rate'],0)
        self.assertEqual(result['native_loss'],ref)
    def test_fixed_target_probability_and_role_seed(self):
        p=probability(BACKGROUND)
        self.assertTrue(np.all((p>=.2)&(p<=.8)))
        self.assertEqual(float(probability(np.zeros((1,2)))[0,1]),.5)
        seeds={seed_for(2026102304,'calibration',i,role) for i in range(64) for role in ('center','generation','score','loss','random')}
        self.assertEqual(len(seeds),320)

if __name__=='__main__': unittest.main()
