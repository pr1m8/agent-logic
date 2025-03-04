from itertools import product
from typing import Dict, List, Union
from logic.core.base import LogicalExpression

class TruthTable:
    """Generates a truth table for a given logical expression."""

    def __init__(self, expression: LogicalExpression):
        self.expression = expression

    def generate(self) -> List[Dict[str, Union[bool, str]]]:
        """Generates all possible truth values for the logical expression."""
        variables = self.expression.variables()
        table = []

        for values in product([False, True], repeat=len(variables)):
            context = dict(zip(variables, values))
            result = self.expression.evaluate(context)
            row = {**context, "Result": result}
            table.append(row)

        return table

    def is_tautology(self) -> bool:
        """Checks if the expression is always true."""
        return all(row["Result"] for row in self.generate())

    def is_contradiction(self) -> bool:
        """Checks if the expression is always false."""
        return all(not row["Result"] for row in self.generate())

    def is_satisfiable(self) -> bool:
        """Checks if there exists a truth assignment that makes the expression true."""
        return any(row["Result"] for row in self.generate())
