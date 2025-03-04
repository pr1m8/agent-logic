from __future__ import annotations
from pydantic import Field
from typing import List, Dict
from logic.core.base import LogicalExpression

# Define logical operations
LOGIC_OPERATORS = {
    "AND": lambda x, y: x and y,
    "OR": lambda x, y: x or y,
    "NOT": lambda x: not x,
    "IMPLIES": lambda p, q: (not p) or q,
    "IFF": lambda p, q: p == q,
}


class Proposition(LogicalExpression):
    """Atomic proposition (e.g., P, Q, R)."""
    name: str = Field(..., description="Atomic proposition name (e.g., P, Q, R).")

    def evaluate(self, context: Dict[str, bool]) -> bool:
        return context.get(self.name, False)

    def variables(self) -> List[str]:
        return [self.name]

    def depth(self) -> int:
        return 1  # A single proposition has depth 1

    def to_dict(self) -> Dict:
        return {"type": "Proposition", "name": self.name}

    @classmethod
    def from_dict(cls, data: Dict) -> Proposition:
        return cls(name=data["name"])


class Not(LogicalExpression):
    """Logical NOT operation (¬A)."""
    operand: LogicalExpression

    def evaluate(self, context: Dict[str, bool]) -> bool:
        return LOGIC_OPERATORS["NOT"](self.operand.evaluate(context))

    def variables(self) -> List[str]:
        return self.operand.variables()

    def depth(self) -> int:
        return 1 + self.operand.depth()

    def to_dict(self) -> Dict:
        return {"type": "Not", "operand": self.operand.to_dict()}

    @classmethod
    def from_dict(cls, data: Dict) -> Not:
        return cls(operand=LogicalExpression.from_dict(data["operand"]))


class BinaryOp(LogicalExpression):
    """Binary logical operations (AND, OR, IMPLIES, IFF)."""
    left: LogicalExpression
    right: LogicalExpression
    operator: str = Field(..., regex="^(AND|OR|IMPLIES|IFF)$")

    def evaluate(self, context: Dict[str, bool]) -> bool:
        return LOGIC_OPERATORS[self.operator](
            self.left.evaluate(context), self.right.evaluate(context)
        )

    def variables(self) -> List[str]:
        return list(set(self.left.variables() + self.right.variables()))

    def depth(self) -> int:
        return 1 + max(self.left.depth(), self.right.depth())

    def to_dict(self) -> Dict:
        return {
            "type": "BinaryOp",
            "operator": self.operator,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> BinaryOp:
        return cls(
            operator=data["operator"],
            left=LogicalExpression.from_dict(data["left"]),
            right=LogicalExpression.from_dict(data["right"]),
        )
