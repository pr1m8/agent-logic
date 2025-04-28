import unittest

from logic.core.operations import BinaryOp, Not, Proposition


class TestCoreLogicalExpressions(unittest.TestCase):

    def test_proposition(self):
        """Test atomic proposition evaluation."""
        p = Proposition(name="P")
        context = {"P": True}
        self.assertTrue(p.evaluate(context))
        context = {"P": False}
        self.assertFalse(p.evaluate(context))

    def test_negation(self):
        """Test NOT operation."""
        p = Proposition(name="P")
        not_p = Not(operand=p)
        context = {"P": True}
        self.assertFalse(not_p.evaluate(context))
        context = {"P": False}
        self.assertTrue(not_p.evaluate(context))

    def test_binary_operations(self):
        """Test AND, OR, IMPLIES, IFF operations."""
        p = Proposition(name="P")
        q = Proposition(name="Q")

        and_expr = BinaryOp(left=p, right=q, operator="AND")
        or_expr = BinaryOp(left=p, right=q, operator="OR")
        implies_expr = BinaryOp(left=p, right=q, operator="IMPLIES")
        iff_expr = BinaryOp(left=p, right=q, operator="IFF")

        context = {"P": True, "Q": False}
        self.assertFalse(and_expr.evaluate(context))
        self.assertTrue(or_expr.evaluate(context))
        self.assertFalse(implies_expr.evaluate(context))
        self.assertFalse(iff_expr.evaluate(context))
