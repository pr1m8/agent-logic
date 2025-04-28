from typing import Literal

from pydantic import Field

from logic.core.base import LogicalExpression


class Proposition(LogicalExpression):
    """Represents an atomic proposition."""

    name: str = Field(..., description="The name of the proposition.")


class Not(LogicalExpression):
    """Represents logical negation."""

    operand: LogicalExpression = Field(..., description="Operand being negated.")


class BinaryOp(LogicalExpression):
    """Represents binary logical operations (AND, OR, IMPLIES, IFF)."""

    left: LogicalExpression
    right: LogicalExpression
    operator: Literal["AND", "OR", "IMPLIES", "IFF"]
