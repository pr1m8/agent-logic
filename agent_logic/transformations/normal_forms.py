from agent_logic.core.base import LogicalExpression
from agent_logic.core.operations import BinaryOp, Not


class NormalForms:
    """Handles logical normal forms like CNF and DNF."""

    @staticmethod
    def to_cnf(expression: LogicalExpression) -> LogicalExpression:
        """Recursively converts an expression to Conjunctive Normal Form (CNF)."""

        # Apply De Morgan’s laws where necessary
        if isinstance(expression, Not) and isinstance(expression.operand, BinaryOp):
            op = expression.operand
            if op.operator == "AND":
                return BinaryOp(Not(op.left), Not(op.right), "OR")
            elif op.operator == "OR":
                return BinaryOp(Not(op.left), Not(op.right), "AND")

        # Recursively simplify left and right subexpressions
        if isinstance(expression, BinaryOp):
            return BinaryOp(
                NormalForms.to_cnf(expression.left),
                NormalForms.to_cnf(expression.right),
                expression.operator,
            )

        return expression  # If already in CNF, return as-is

    @staticmethod
    def to_dnf(expression: LogicalExpression) -> LogicalExpression:
        """Recursively converts an expression to Disjunctive Normal Form (DNF)."""

        # Apply De Morgan’s laws where necessary
        if isinstance(expression, Not) and isinstance(expression.operand, BinaryOp):
            op = expression.operand
            if op.operator == "AND":
                return BinaryOp(Not(op.left), Not(op.right), "OR")
            elif op.operator == "OR":
                return BinaryOp(Not(op.left), Not(op.right), "AND")

        # Recursively simplify left and right subexpressions
        if isinstance(expression, BinaryOp):
            return BinaryOp(
                NormalForms.to_dnf(expression.left),
                NormalForms.to_dnf(expression.right),
                expression.operator,
            )

        return expression  # If already in DNF, return as-is
