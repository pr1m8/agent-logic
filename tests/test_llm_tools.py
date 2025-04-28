import unittest

from logic.core.operations import BinaryOp, Not, Proposition
from logic.evaluation.truth_table import TruthTable


class TestTruthTable(unittest.TestCase):

    def test_truth_table(self):
        """Test the truth table generation for an AND expression."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        and_expr = BinaryOp(left=p, right=q, operator="AND")

        truth_table = TruthTable(and_expr).generate()
        expected_table = [
            {"P": False, "Q": False, "Result": False},
            {"P": False, "Q": True, "Result": False},
            {"P": True, "Q": False, "Result": False},
            {"P": True, "Q": True, "Result": True},
        ]

        self.assertEqual(truth_table, expected_table)

    def test_tautology_check(self):
        """Test whether a tautology is correctly identified."""
        p = Proposition(name="P")
        or_expr = BinaryOp(left=p, right=Not(operand=p), operator="OR")  # P ∨ ¬P

        truth_table = TruthTable(or_expr)
        self.assertTrue(truth_table.is_tautology())

    def test_contradiction_check(self):
        """Test whether a contradiction is correctly identified."""
        p = Proposition(name="P")
        and_expr = BinaryOp(left=p, right=Not(operand=p), operator="AND")  # P ∧ ¬P

        truth_table = TruthTable(and_expr)
        self.assertTrue(truth_table.is_contradiction())
