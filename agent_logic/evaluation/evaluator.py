from typing import Any, Dict

from agent_logic.core.base import LogicalExpression
from agent_logic.core.functions import Function, Relation
from agent_logic.core.operations import BinaryOp, Not, Proposition
from agent_logic.core.predicates import ExistentialQuantifier, UniversalQuantifier


class Evaluator:
    """Evaluates logical expressions recursively with variable assignments."""

    @staticmethod
    def evaluate(expression: LogicalExpression, context: Dict[str, Any]) -> bool:
        """Evaluates a logical expression under a given context of truth values."""

        if isinstance(expression, Proposition):
            return expression.evaluate(context)

        elif isinstance(expression, Not):
            return expression.evaluate(context)

        elif isinstance(expression, BinaryOp):
            return expression.evaluate(context)

        elif isinstance(expression, Function):
            return expression.evaluate(context)

        elif isinstance(expression, Relation):
            return expression.evaluate(context)

        elif isinstance(expression, UniversalQuantifier):
            return expression.evaluate(context)

        elif isinstance(expression, ExistentialQuantifier):
            return expression.evaluate(context)

        raise ValueError(f"Unknown expression type: {expression}")

    @staticmethod
    def expression_depth(expression: LogicalExpression) -> int:
        """Computes the depth of a logical expression."""
        return expression.depth()
