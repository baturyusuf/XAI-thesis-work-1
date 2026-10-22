import unittest
from benchmark.contracts import FeatureSchema, FrozenPredictor, SubsetExplanation, TargetSpec
from benchmark.finite import FiniteLaw
from benchmark.provenance import SplitManifest, ProbeBatch

class FrozenMetadataTests(unittest.TestCase):
    def test_mutable_constructor_inputs_are_snapshotted(self):
        labels=[0,1]; groups=[[0],[1]]
        target=TargetSpec("f",labels,1); schema=FeatureSchema(2,groups)
        chosen=[0]; explanation=SubsetExplanation(chosen,target)
        labels.reverse(); groups[0].append(1); chosen.append(1)
        self.assertEqual(target.class_labels,(0,1)); self.assertEqual(schema.groups,((0,),(1,)))
        self.assertEqual(explanation.groups,(0,))
        weights={(0,):1}; law=FiniteLaw(weights,"l","exact");weights[(0,)]=0
        self.assertEqual(law.weights[(0,)],1)
        ids=["c"]; split=SplitManifest((),ids,("t",));ids.append("t");split.validate()
        draws=["d"]; batch=ProbeBatch("u","evaluation_loss","e",draws,3);draws.append("d")
        self.assertEqual(batch.draw_ids,("d",))

if __name__=="__main__": unittest.main()
