"""
Base module for logical expressions.

This module provides the base class for all logical expressions in the logic system.
It defines the common interface that all logical expressions must implement,
including evaluation, variable extraction, and serialization.
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel


class LogicalExpression(BaseModel):
    """
    Recursive base class for logical expressions.

    This abstract class defines the interface for all logical expressions
    in the system. Concrete implementations include Proposition, Not, and BinaryOp.

    Attributes:
        model_config: Pydantic model configuration to allow arbitrary types.
    """

    model_config = {"arbitrary_types_allowed": True}

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """
        Recursively evaluates the expression under a given truth assignment.

        Args:
            context: Dictionary mapping variable names to truth values.
                    Example: {"P": True, "Q": False}

        Returns:
            Boolean result of evaluating the expression.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        raise NotImplementedError

    def variables(self) -> List[str]:
        """
        Recursively extracts all variables in the expression.

        Returns:
            List of variable names used in the expression.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        raise NotImplementedError

    def depth(self) -> int:
        """
        Computes the depth of the logical expression tree.

        Returns:
            Integer representing the depth of the expression tree.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        raise NotImplementedError

    def to_dict(self) -> Dict:
        """
        Recursively converts expression to a dictionary.

        Returns:
            Dictionary representation of the logical expression.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented by subclasses.
        """
        raise NotImplementedError

    @classmethod
    def from_dict(cls, data: Dict) -> LogicalExpression:
        """
        Recursively reconstructs an expression from a dictionary.

        Args:
            data: Dictionary representation of a logical expression.
                 Must include a 'type' field.

        Returns:
            Reconstructed logical expression.

        Raises:
            ValueError: If the data is not a dictionary, doesn't have a type field,
                        or has an unknown expression type.
        """
        if not isinstance(data, dict):
            raise ValueError(f"Expected dictionary but got {type(data)}")

        # Import here to avoid circular imports
        from agent_logic.core.operations import BinaryOp, Not, Proposition

        if "type" not in data:
            raise ValueError(f"Missing 'type' in expression data: {data}")

        exp_type = data["type"]
        if exp_type == "Proposition":
            return Proposition.from_dict(data)
        elif exp_type == "Not":
            return Not.from_dict(data)
        elif exp_type == "BinaryOp":
            return BinaryOp.from_dict(data)
        else:
            raise ValueError(f"Unknown expression type: {exp_type}")
