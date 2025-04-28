"""
Expression evaluator module.

This module provides utilities for evaluating logical expressions with different truth assignments.
"""

from typing import Dict

from agent_logic.core.base import LogicalExpression
from agent_logic.core.functions import Function, Relation
from agent_logic.core.operations import BinaryOp, Not, Proposition
from agent_logic.core.quantifiers import ExistentialQuantifier, UniversalQuantifier


class Evaluator:
    """
    Evaluates logical expressions with different truth assignments.

    This class provides methods to evaluate expressions and determine logical properties
    such as consistency, validity, and equivalence.
    """

    @staticmethod
    def evaluate_with_assignment(expression: LogicalExpression, assignment: Dict[str, bool]) -> bool:
        """
        Evaluates a logical expression under a specific truth assignment.

        Args:
            expression: The logical expression to evaluate
            assignment: Dictionary mapping variable names to boolean values

        Returns:
            Boolean result of evaluating the expression
        """
        return expression.evaluate(assignment)

    @staticmethod
    def are_equivalent(expr1: LogicalExpression, expr2: LogicalExpression) -> bool:
        """
        Determines if two expressions are logically equivalent.

        Expressions are equivalent if they have the same truth value
        for all possible truth assignments to their variables.

        Args:
            expr1: First logical expression
            expr2: Second logical expression

        Returns:
            True if the expressions are equivalent, False otherwise
        """
        # Get all variables from both expressions
        variables = set(expr1.variables() + expr2.variables())

        # Generate all possible truth assignments
        from agent_logic.evaluation.truth_table import TruthTable
        assignments = TruthTable._generate_assignments(list(variables))

        # Check if the expressions have the same value for all assignments
        for assignment in assignments:
            if expr1.evaluate(assignment) != expr2.evaluate(assignment):
                return False

        return True

    @staticmethod
    def is_satisfiable(expression: LogicalExpression) -> bool:
        """
        Determines if an expression is satisfiable (true for at least one assignment).

        Args:
            expression: The logical expression to check

        Returns:
            True if the expression is satisfiable, False otherwise
        """
        from agent_logic.evaluation.truth_table import TruthTable
        return TruthTable(expression).is_satisfiable()

    @staticmethod
    def is_valid(expression: LogicalExpression) -> bool:
        """
        Determines if an expression is valid (true for all assignments).

        Args:
            expression: The logical expression to check

        Returns:
            True if the expression is valid, False otherwise
        """
        from agent_logic.evaluation.truth_table import TruthTable
        return TruthTable(expression).is_tautology()

    @staticmethod
    def evaluate(expression: LogicalExpression, context: Dict[str, bool]) -> bool:
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