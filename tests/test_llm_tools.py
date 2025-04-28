import unittest

from agent_logic.core.operations import BinaryOp, Not, Proposition
from agent_logic.evaluation.truth_table import TruthTable


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

    def test_truth_table_or(self):
        """Test the truth table generation for an OR expression."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        or_expr = BinaryOp(left=p, right=q, operator="OR")

        truth_table = TruthTable(or_expr).generate()
        expected_table = [
            {"P": False, "Q": False, "Result": False},
            {"P": False, "Q": True, "Result": True},
            {"P": True, "Q": False, "Result": True},
            {"P": True, "Q": True, "Result": True},
        ]

        self.assertEqual(truth_table, expected_table)

    def test_truth_table_implies(self):
        """Test the truth table generation for an IMPLIES expression."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        implies_expr = BinaryOp(left=p, right=q, operator="IMPLIES")

        truth_table = TruthTable(implies_expr).generate()
        expected_table = [
            {"P": False, "Q": False, "Result": True},  # F → F is True
            {"P": False, "Q": True, "Result": True},  # F → T is True
            {"P": True, "Q": False, "Result": False},  # T → F is False
            {"P": True, "Q": True, "Result": True},  # T → T is True
        ]

        self.assertEqual(truth_table, expected_table)

    def test_truth_table_not(self):
        """Test the truth table generation for a NOT expression."""
        p = Proposition(name="P")
        not_expr = Not(operand=p)

        truth_table = TruthTable(not_expr).generate()
        expected_table = [
            {"P": False, "Result": True},
            {"P": True, "Result": False},
        ]

        self.assertEqual(truth_table, expected_table)

    def test_truth_table_complex(self):
        """Test the truth table for a complex expression (P ∧ (Q → R))."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        r = Proposition(name="R")

        q_implies_r = BinaryOp(left=q, right=r, operator="IMPLIES")
        complex_expr = BinaryOp(left=p, right=q_implies_r, operator="AND")

        truth_table = TruthTable(complex_expr).generate()

        # With 3 variables, we should have 2^3 = 8 rows
        self.assertEqual(len(truth_table), 8)

        # Check a few specific cases
        # Find row where P=True, Q=True, R=False - should have Result=False
        row = next(row for row in truth_table if row["P"] and row["Q"] and not row["R"])
        self.assertFalse(row["Result"])

        # Find row where P=True, Q=True, R=True - should have Result=True
        row = next(row for row in truth_table if row["P"] and row["Q"] and row["R"])
        self.assertTrue(row["Result"])

    def test_tautology_check(self):
        """Test whether a tautology is correctly identified."""
        p = Proposition(name="P")
        or_expr = BinaryOp(left=p, right=Not(operand=p), operator="OR")  # P ∨ ¬P

        truth_table = TruthTable(or_expr)
        self.assertTrue(truth_table.is_tautology())

        # Test a non-tautology
        q = Proposition(name="Q")
        and_expr = BinaryOp(left=p, right=q, operator="AND")
        truth_table = TruthTable(and_expr)
        self.assertFalse(truth_table.is_tautology())

    def test_contradiction_check(self):
        """Test whether a contradiction is correctly identified."""
        p = Proposition(name="P")
        and_expr = BinaryOp(left=p, right=Not(operand=p), operator="AND")  # P ∧ ¬P

        truth_table = TruthTable(and_expr)
        self.assertTrue(truth_table.is_contradiction())

        # Test a non-contradiction
        q = Proposition(name="Q")
        or_expr = BinaryOp(left=p, right=q, operator="OR")
        truth_table = TruthTable(or_expr)
        self.assertFalse(truth_table.is_contradiction())

    def test_satisfiable_check(self):
        """Test whether an expression is satisfiable."""
        p = Proposition(name="P")
        q = Proposition(name="Q")

        # Satisfiable but not a tautology
        and_expr = BinaryOp(left=p, right=q, operator="AND")
        truth_table = TruthTable(and_expr)
        self.assertTrue(truth_table.is_satisfiable())

        # Contradiction is not satisfiable
        contradiction = BinaryOp(left=p, right=Not(operand=p), operator="AND")
        truth_table = TruthTable(contradiction)
        self.assertFalse(truth_table.is_satisfiable())

        # Tautology is satisfiable
        tautology = BinaryOp(left=p, right=Not(operand=p), operator="OR")
        truth_table = TruthTable(tautology)
        self.assertTrue(truth_table.is_satisfiable())

    def test_truth_table_error_handling(self):
        """Test error handling in TruthTable."""
        # Test with a non-LogicalExpression
        with self.assertRaises(TypeError):
            TruthTable("not an expression").generate()
