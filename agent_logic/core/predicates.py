from __future__ import annotations

from typing import Dict, List, Union

from pydantic import BaseModel


class Term(BaseModel):
    """Represents a term in predicate logic (constants, variables, functions)."""

    value: Union[str, List["Term"]]  # Supports functions like f(x, y)


class Predicate(BaseModel):
    """Represents a predicate in first-order logic."""

    name: str
    terms: List[Term]

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """Evaluates the predicate given a context mapping variables to truth values."""
        term_values = tuple(context.get(term.value, False) for term in self.terms)
        return context.get(self.name, lambda *args: False)(*term_values)

    def variables(self) -> List[str]:
        """Returns a list of variable names used in the predicate."""
        return [term.value for term in self.terms]

    def depth(self) -> int:
        return 1

    def to_dict(self) -> Dict:
        return {"name": self.name, "terms": [term.value for term in self.terms]}

    @classmethod
    def from_dict(cls, data: Dict) -> Predicate:
        return cls(name=data["name"], terms=[Term(value=val) for val in data["terms"]])
