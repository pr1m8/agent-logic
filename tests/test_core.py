import unittest

from agent_logic.core.base import LogicalExpression
from agent_logic.core.operations import BinaryOp, Not, Proposition


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

    def test_evaluate_missing_variable(self):
        """Test error handling when a variable is missing from the context."""
        p = Proposition(name="P")
        context = {"Q": True}  # P is missing
        with self.assertRaises(ValueError):
            p.evaluate(context)

    def test_variables_proposition(self):
        """Test variables() method for Proposition."""
        p = Proposition(name="P")
        self.assertEqual(p.variables(), ["P"])

    def test_variables_not(self):
        """Test variables() method for Not."""
        p = Proposition(name="P")
        not_p = Not(operand=p)
        self.assertEqual(not_p.variables(), ["P"])

    def test_variables_binary_op(self):
        """Test variables() method for BinaryOp."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        r = Proposition(name="R")

        # Test binary operation with two different variables
        and_expr = BinaryOp(left=p, right=q, operator="AND")
        vars_set = set(and_expr.variables())
        self.assertEqual(vars_set, {"P", "Q"})

        # Test with a more complex expression
        complex_expr = BinaryOp(
            left=BinaryOp(left=p, right=q, operator="AND"), right=r, operator="OR"
        )
        vars_set = set(complex_expr.variables())
        self.assertEqual(vars_set, {"P", "Q", "R"})

        # Test with duplicate variables
        dup_expr = BinaryOp(left=p, right=p, operator="OR")
        self.assertEqual(set(dup_expr.variables()), {"P"})

    def test_depth_proposition(self):
        """Test depth() method for Proposition."""
        p = Proposition(name="P")
        self.assertEqual(p.depth(), 0)

    def test_depth_not(self):
        """Test depth() method for Not."""
        p = Proposition(name="P")
        not_p = Not(operand=p)
        self.assertEqual(not_p.depth(), 1)

        # Nested NOT
        not_not_p = Not(operand=not_p)
        self.assertEqual(not_not_p.depth(), 2)

    def test_depth_binary_op(self):
        """Test depth() method for BinaryOp."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        r = Proposition(name="R")

        # Simple binary operation
        and_expr = BinaryOp(left=p, right=q, operator="AND")
        self.assertEqual(and_expr.depth(), 1)

        # Complex nested expression
        complex_expr = BinaryOp(
            left=BinaryOp(left=p, right=q, operator="AND"), right=r, operator="OR"
        )
        self.assertEqual(complex_expr.depth(), 2)

        # Even more complex with negation
        very_complex = BinaryOp(
            left=Not(operand=p),
            right=BinaryOp(left=q, right=r, operator="IMPLIES"),
            operator="AND",
        )
        self.assertEqual(very_complex.depth(), 2)

    def test_to_dict_proposition(self):
        """Test to_dict() method for Proposition."""
        p = Proposition(name="P")
        expected = {"type": "Proposition", "name": "P"}
        self.assertEqual(p.to_dict(), expected)

    def test_to_dict_not(self):
        """Test to_dict() method for Not."""
        p = Proposition(name="P")
        not_p = Not(operand=p)
        expected = {"type": "Not", "operand": {"type": "Proposition", "name": "P"}}
        self.assertEqual(not_p.to_dict(), expected)

    def test_to_dict_binary_op(self):
        """Test to_dict() method for BinaryOp."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        and_expr = BinaryOp(left=p, right=q, operator="AND")

        expected = {
            "type": "BinaryOp",
            "left": {"type": "Proposition", "name": "P"},
            "right": {"type": "Proposition", "name": "Q"},
            "operator": "AND",
        }

        self.assertEqual(and_expr.to_dict(), expected)

    def test_from_dict_proposition(self):
        """Test from_dict() method for Proposition."""
        data = {"type": "Proposition", "name": "P"}
        p = LogicalExpression.from_dict(data)

        self.assertIsInstance(p, Proposition)
        self.assertEqual(p.name, "P")

    def test_from_dict_not(self):
        """Test from_dict() method for Not."""
        data = {"type": "Not", "operand": {"type": "Proposition", "name": "P"}}

        not_p = LogicalExpression.from_dict(data)

        self.assertIsInstance(not_p, Not)
        self.assertIsInstance(not_p.operand, Proposition)
        self.assertEqual(not_p.operand.name, "P")

    def test_from_dict_binary_op(self):
        """Test from_dict() method for BinaryOp."""
        data = {
            "type": "BinaryOp",
            "left": {"type": "Proposition", "name": "P"},
            "right": {"type": "Proposition", "name": "Q"},
            "operator": "AND",
        }

        and_expr = LogicalExpression.from_dict(data)

        self.assertIsInstance(and_expr, BinaryOp)
        self.assertIsInstance(and_expr.left, Proposition)
        self.assertIsInstance(and_expr.right, Proposition)
        self.assertEqual(and_expr.left.name, "P")
        self.assertEqual(and_expr.right.name, "Q")
        self.assertEqual(and_expr.operator, "AND")

    def test_from_dict_complex(self):
        """Test from_dict() with a complex nested expression."""
        data = {
            "type": "BinaryOp",
            "left": {"type": "Not", "operand": {"type": "Proposition", "name": "P"}},
            "right": {
                "type": "BinaryOp",
                "left": {"type": "Proposition", "name": "Q"},
                "right": {"type": "Proposition", "name": "R"},
                "operator": "OR",
            },
            "operator": "IMPLIES",
        }

        expr = LogicalExpression.from_dict(data)

        self.assertIsInstance(expr, BinaryOp)
        self.assertEqual(expr.operator, "IMPLIES")

        self.assertIsInstance(expr.left, Not)
        self.assertIsInstance(expr.left.operand, Proposition)
        self.assertEqual(expr.left.operand.name, "P")

        self.assertIsInstance(expr.right, BinaryOp)
        self.assertEqual(expr.right.operator, "OR")
        self.assertEqual(expr.right.left.name, "Q")
        self.assertEqual(expr.right.right.name, "R")

    def test_from_dict_error_handling(self):
        """Test error handling in from_dict() method."""
        # Missing type field
        with self.assertRaises(ValueError):
            LogicalExpression.from_dict({"name": "P"})

        # Unknown type
        with self.assertRaises(ValueError):
            LogicalExpression.from_dict({"type": "UnknownType"})

        # Not a dictionary
        with self.assertRaises(ValueError):
            LogicalExpression.from_dict("not a dict")
