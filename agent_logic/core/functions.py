from __future__ import annotations

from typing import Any, Callable, Dict, List

from pydantic import BaseModel, Field

from agent_logic.core.base import LogicalExpression


class Function(BaseModel):
    """Represents a function f(x) in predicate logic."""

    name: str = Field(..., description="Function name (e.g., f, g, h).")
    parameters: List[str] = Field(..., description="List of parameter variable names.")
    function: Callable[..., Any]

    def evaluate(self, context: Dict[str, Any]) -> Any:
        """Evaluate the function using context for parameter values."""
        args = [context[param] for param in self.parameters]
        return self.function(*args)

    def variables(self) -> List[str]:
        return self.parameters

    def depth(self) -> int:
        return 1  # Functions do not nest deeper (unless higher-order)

    def to_dict(self) -> Dict:
        return {"type": "Function", "name": self.name, "parameters": self.parameters}

    @classmethod
    def from_dict(cls, data: Dict) -> Function:
        return cls(
            name=data["name"],
            parameters=data["parameters"],
            function=lambda *args: None,
        )


class Relation(LogicalExpression):
    """Represents a predicate relation R(x, y, ...)."""

    name: str = Field(..., description="Relation name (e.g., P, Q, R).")
    parameters: List[str] = Field(..., description="List of parameter variable names.")

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """Evaluates a predicate relation based on the truth values in context."""
        key = f"{self.name}({', '.join(self.parameters)})"
        return context.get(key, False)

    def variables(self) -> List[str]:
        return self.parameters

    def depth(self) -> int:
        return 1  # A relation is atomic

    def to_dict(self) -> Dict:
        return {"type": "Relation", "name": self.name, "parameters": self.parameters}

    @classmethod
    def from_dict(cls, data: Dict) -> Relation:
        return cls(name=data["name"], parameters=data["parameters"])
