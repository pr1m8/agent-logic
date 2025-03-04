from __future__ import annotations
from pydantic import BaseModel
from typing import List, Dict, Optional, Union

class LogicalExpression(BaseModel):
    """Recursive base class for logical expressions."""

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """Recursively evaluates the expression under a given truth assignment."""
        raise NotImplementedError
    
    def variables(self) -> List[str]:
        """Recursively extracts all variables in the expression."""
        raise NotImplementedError

    def depth(self) -> int:
        """Computes the depth of the logical expression tree."""
        raise NotImplementedError

    def to_dict(self) -> Dict:
        """Recursively converts expression to a dictionary."""
        raise NotImplementedError

    def from_dict(cls, data: Dict) -> LogicalExpression:
        """Recursively reconstructs an expression from a dictionary."""
        raise NotImplementedError
