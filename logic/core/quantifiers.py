from __future__ import annotations

from typing import Dict, List, Literal

from pydantic import BaseModel

from logic.core.predicates import Predicate


class UniversalQuantifier(BaseModel):
    """Represents Universal Quantification: ∀x P(x)"""

    type: Literal["FORALL"] = "FORALL"
    variable: str
    predicate: Predicate

    def evaluate(self, context: Dict[str, List[bool]]) -> bool:
        """Evaluates ∀x P(x) over all values in context[variable]."""
        return all(
            self.predicate.evaluate({self.variable: v, **context})
            for v in context.get(self.variable, [])
        )

    def variables(self) -> List[str]:
        return [self.variable] + self.predicate.variables()

    def depth(self) -> int:
        return 1 + self.predicate.depth()

    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "variable": self.variable,
            "predicate": self.predicate.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> UniversalQuantifier:
        return cls(
            variable=data["variable"], predicate=Predicate.from_dict(data["predicate"])
        )


class ExistentialQuantifier(BaseModel):
    """Represents Existential Quantification: ∃x P(x)"""

    type: Literal["EXISTS"] = "EXISTS"
    variable: str
    predicate: Predicate

    def evaluate(self, context: Dict[str, List[bool]]) -> bool:
        """Evaluates ∃x P(x), checking if any value satisfies predicate."""
        return any(
            self.predicate.evaluate({self.variable: v, **context})
            for v in context.get(self.variable, [])
        )

    def variables(self) -> List[str]:
        return [self.variable] + self.predicate.variables()

    def depth(self) -> int:
        return 1 + self.predicate.depth()

    def to_dict(self) -> Dict:
        return {
            "type": self.type,
            "variable": self.variable,
            "predicate": self.predicate.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: Dict) -> ExistentialQuantifier:
        return cls(
            variable=data["variable"], predicate=Predicate.from_dict(data["predicate"])
        )
