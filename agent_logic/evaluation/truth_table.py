from itertools import product
from typing import Dict, List, Union

from agent_logic.core.base import LogicalExpression


class TruthTable:
    """Generates a truth table for a given logical expression."""

    def __init__(self, expression: LogicalExpression):
        if not isinstance(expression, LogicalExpression):
            raise TypeError("TruthTable requires a LogicalExpression instance.")
        self.expression = expression

    def generate(self) -> List[Dict[str, Union[bool, str]]]:
        """
        Generates all possible truth values for the logical expression.

        Returns:
            List of dictionaries, where each dictionary represents a row in the truth table.
        """
        variables = sorted(
            self.expression.variables()
        )  # Ensure sorted order of variables
        table = []

        for values in product([False, True], repeat=len(variables)):
            context = dict(
                zip(variables, values, strict=False)
            )  # Maintain consistent order
            try:
                result = self.expression.evaluate(context)
            except Exception as e:
                result = f"Error: {e}"  # Store error message for debugging

            row = {var: context[var] for var in variables}  # Preserve variable order
            row["Result"] = result
            table.append(row)

        return table

    def is_tautology(self) -> bool:
        """
        Checks if the expression is always true.

        Returns:
            True if the expression evaluates to True for all assignments, otherwise False.
        """
        return all(row["Result"] is True for row in self.generate())

    def is_contradiction(self) -> bool:
        """
        Checks if the expression is always false.

        Returns:
            True if the expression evaluates to False for all assignments, otherwise False.
        """
        return all(row["Result"] is False for row in self.generate())

    def is_satisfiable(self) -> bool:
        """
        Checks if there exists a truth assignment that makes the expression true.

        Returns:
            True if at least one assignment makes the expression True, otherwise False.
        """
        return any(row["Result"] is True for row in self.generate())
