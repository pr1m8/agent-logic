from __future__ import annotations
from pydantic import Field
from typing import Dict, List
from logic.core.base import LogicalExpression
from logic.core.functions import Relation

class UniversalQuantifier(LogicalExpression):
    """∀x P(x): Universal quantification."""
    variable: str
    predicate: Relation

    def evaluate(self, context: Dict[str, List[bool]]) -> bool:
        """Evaluates ∀x P(x) over all values in context[variable]."""
        return all(self.predicate.evaluate({self.variable: v, **context}) for v in context.get(self.variable, []))

    def variables(self) -> List[str]:
        return [self.variable] + self.predicate.variables()

    def depth(self) -> int:
        return 1 + self.predicate.depth()

    def to_dict(self) -> Dict:
        return {"type": "UniversalQuantifier", "variable": self.variable, "predicate": self.predicate.to_dict()}

    @classmethod
    def from_dict(cls, data: Dict) -> UniversalQuantifier:
        return cls(variable=data["variable"], predicate=Relation.from_dict(data["predicate"]))


class ExistentialQuantifier(LogicalExpression):
    """∃x P(x): Existential quantification."""
    variable: str
    predicate: Relation

    def evaluate(self, context: Dict[str, List[bool]]) -> bool:
        """Evaluates ∃x P(x) checking if any value satisfies predicate."""
        return any(self.predicate.evaluate({self.variable: v, **context}) for v in context.get(self.variable, []))

    def variables(self) -> List[str]:
        return [self.variable] + self.predicate.variables()

    def depth(self) -> int:
        return 1 + self.predicate.depth()

    def to_dict(self) -> Dict:
        return {"type": "ExistentialQuantifier", "variable": self.variable, "predicate": self.predicate.to_dict()}

    @classmethod
    def from_dict(cls, data: Dict) -> ExistentialQuantifier:
        return cls(variable=data["variable"], predicate=Relation.from_dict(data["predicate"]))
