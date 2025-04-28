from __future__ import annotations

from typing import Dict, List, Literal, Any, TYPE_CHECKING

from pydantic import BaseModel

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from agent_logic.core.predicates import Predicate  # noqa: F401


class UniversalQuantifier(BaseModel):
    """Represents Universal Quantification: ∀x P(x)"""

    type: Literal["FORALL"] = "FORALL"
    variable: str
    predicate: Any  # Predicate

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
        from agent_logic.core.predicates import Predicate
        return cls(
            variable=data["variable"], predicate=Predicate.from_dict(data["predicate"])
        )


class ExistentialQuantifier(BaseModel):
    """Represents Existential Quantification: ∃x P(x)"""

    type: Literal["EXISTS"] = "EXISTS"
    variable: str
    predicate: Any  # Predicate

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
        from agent_logic.core.predicates import Predicate
        return cls(
            variable=data["variable"], predicate=Predicate.from_dict(data["predicate"])
        )


# Define aliases for better naming in imports
ForAll = UniversalQuantifier
Exists = ExistentialQuantifier

# Add a base Quantifier type for type hints
Quantifier = UniversalQuantifier | ExistentialQuantifier
