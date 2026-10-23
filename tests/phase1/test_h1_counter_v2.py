import unittest
from fractions import Fraction as F
from types import SimpleNamespace
from benchmark.h1 import SubsetResult
from innovation.h1_reference import repeated_deletion as legacy
from innovation.phase1.h1_reference_v2 import repeated_deletion

class H1CounterV2Tests(unittest.TestCase):
    def test_missing_counter_is_unknown_despite_eight_executions(self):
        calls = []
        def result(groups):
            calls.extend((1, 1))
            return SubsetResult(F(0), F(0), len(groups))
        selected, counts = repeated_deletion(result, (0, 1, 2))
        self.assertEqual(selected, ())
        self.assertEqual(len(calls), 8)
        self.assertIsNone(counts.model_callbacks)
        self.assertIsNone(counts.unique_states)
        self.assertEqual(counts.predicate_calls, 4)

    def test_supplied_counts_are_lifetime_snapshot(self):
        counter = SimpleNamespace(calls=8, states={(0,), (1,)})
        _, counts = repeated_deletion(lambda g: SubsetResult(F(0), F(0), len(g)), (0, 1), callback_counts=counter)
        self.assertEqual((counts.model_callbacks, counts.unique_states), (8, 2))

    def test_measured_zero_differs_from_unknown(self):
        counter = SimpleNamespace(calls=0, states=set())
        _, measured = repeated_deletion(lambda g: SubsetResult(F(0), F(0), len(g)), (), callback_counts=counter)
        _, unknown = repeated_deletion(lambda g: SubsetResult(F(0), F(0), len(g)), ())
        self.assertEqual((measured.model_callbacks, measured.unique_states), (0, 0))
        self.assertIsNone(unknown.model_callbacks)
        self.assertIsNone(unknown.unique_states)

    def test_search_and_predicate_count_match_frozen_reference(self):
        result = lambda g: SubsetResult(F(0), F(0), len(g))
        old_selected, old_counts = legacy(result, (0, 1))
        new_selected, new_counts = repeated_deletion(result, (0, 1))
        self.assertEqual(new_selected, old_selected)
        self.assertEqual(new_counts.predicate_calls, old_counts.predicate_calls)
        self.assertEqual((new_counts.model_callbacks, new_counts.unique_states), (None, None))

if __name__ == "__main__":
    unittest.main()
