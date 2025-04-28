from agent_logic.core.base import LogicalExpression
from agent_logic.core.operations import BinaryOp, Not


class EquivalenceRules:
    """Defines common logical equivalences for transformations."""

    @staticmethod
    def apply_de_morgan(expression: LogicalExpression) -> LogicalExpression:
        """
        De Morgan’s Laws:
        ¬(A ∧ B) ≡ (¬A ∨ ¬B)
        ¬(A ∨ B) ≡ (¬A ∧ ¬B)
        """
        if isinstance(expression, Not) and isinstance(expression.operand, BinaryOp):
            op = expression.operand
            if op.operator == "AND":
                return BinaryOp(Not(op.left), Not(op.right), "OR")
            elif op.operator == "OR":
                return BinaryOp(Not(op.left), Not(op.right), "AND")
        return expression

    @staticmethod
    def double_negation(expression: LogicalExpression) -> LogicalExpression:
        """
        Double Negation:
        ¬(¬A) ≡ A
        """
        if isinstance(expression, Not) and isinstance(expression.operand, Not):
            return expression.operand.operand  # Return A
        return expression

    @staticmethod
    def contradiction_elimination(expression: LogicalExpression) -> LogicalExpression:
        """
        Proof by Contradiction:
        If (A ∧ ¬A) is true, then ⊥ (false) is reached.
        """
        if isinstance(expression, BinaryOp) and expression.operator == "AND":
            if (
                isinstance(expression.left, Not)
                and expression.left.operand == expression.right
            ):
                return None  # ⊥ (contradiction)
            elif (
                isinstance(expression.right, Not)
                and expression.right.operand == expression.left
            ):
                return None  # ⊥ (contradiction)
        return expression

    @staticmethod
    def distributive_law(expression: LogicalExpression) -> LogicalExpression:
        """
        Distributive Law:
        (A ∧ (B ∨ C)) ≡ ((A ∧ B) ∨ (A ∧ C))
        (A ∨ (B ∧ C)) ≡ ((A ∨ B) ∧ (A ∨ C))
        """
        if isinstance(expression, BinaryOp):
            if (
                expression.operator == "AND"
                and isinstance(expression.right, BinaryOp)
                and expression.right.operator == "OR"
            ):
                return BinaryOp(
                    BinaryOp(expression.left, expression.right.left, "AND"),
                    BinaryOp(expression.left, expression.right.right, "AND"),
                    "OR",
                )
            elif (
                expression.operator == "OR"
                and isinstance(expression.right, BinaryOp)
                and expression.right.operator == "AND"
            ):
                return BinaryOp(
                    BinaryOp(expression.left, expression.right.left, "OR"),
                    BinaryOp(expression.left, expression.right.right, "OR"),
                    "AND",
                )
        return expression
