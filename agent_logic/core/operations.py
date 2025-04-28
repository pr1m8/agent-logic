"""
Core logical operations module.

This module implements the fundamental logical operations:
- Proposition: Represents atomic propositions (variables)
- Not: Represents logical negation (¬)
- BinaryOp: Represents binary operations (AND, OR, IMPLIES, IFF)

These classes form the building blocks of logical expressions and formulas.
"""

from typing import Dict, List, Literal

from pydantic import Field

from agent_logic.core.base import LogicalExpression


class Proposition(LogicalExpression):
    """
    Represents an atomic proposition (logical variable).

    An atomic proposition is the most basic unit in propositional logic,
    representing a statement that can be either true or false.

    Attributes:
        name: The name of the proposition (e.g., "P", "Q").
    """

    name: str = Field(..., description="The name of the proposition.")

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """
        Evaluates the proposition given a truth assignment.

        Args:
            context: Dictionary mapping variable names to truth values.
                    Example: {"P": True, "Q": False}

        Returns:
            Boolean value of the proposition in the given context.

        Raises:
            ValueError: If the proposition name is not in the context.
        """
        if self.name not in context:
            raise ValueError(f"No truth value provided for proposition {self.name}")
        return context[self.name]

    def variables(self) -> List[str]:
        """
        Returns the list of variables in the proposition.

        Returns:
            A list containing only the name of this proposition.
        """
        return [self.name]

    def depth(self) -> int:
        """
        Returns the depth of the expression tree.

        For an atomic proposition, the depth is always 0.

        Returns:
            0, as atomic propositions have no depth.
        """
        return 0

    def to_dict(self) -> Dict:
        """
        Converts the proposition to a dictionary.

        Returns:
            Dictionary representation of the proposition.
            Example: {"type": "Proposition", "name": "P"}
        """
        return {"type": "Proposition", "name": self.name}

    @classmethod
    def from_dict(cls, data: Dict) -> "Proposition":
        """
        Reconstructs a proposition from a dictionary.

        Args:
            data: Dictionary representation of a proposition.
                 Must contain a "name" field.

        Returns:
            Reconstructed Proposition object.
        """
        if "type" in data and data["type"] == "Proposition":
            return cls(name=data["name"])
        return cls(name=data["name"])


class Not(LogicalExpression):
    """
    Represents logical negation (¬).

    The NOT operation negates the truth value of its operand.

    Attributes:
        operand: The logical expression being negated.
    """

    operand: LogicalExpression = Field(..., description="Operand being negated.")

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """
        Evaluates the NOT expression given a truth assignment.

        Args:
            context: Dictionary mapping variable names to truth values.
                    Example: {"P": True, "Q": False}

        Returns:
            Boolean result of negating the operand's evaluation.
        """
        return not self.operand.evaluate(context)

    def variables(self) -> List[str]:
        """
        Returns the list of variables in the NOT expression.

        Returns:
            List of variable names used in the operand.
        """
        return self.operand.variables()

    def depth(self) -> int:
        """
        Returns the depth of the expression tree.

        Returns:
            The depth of the operand plus 1.
        """
        return 1 + self.operand.depth()

    def to_dict(self) -> Dict:
        """
        Converts the NOT expression to a dictionary.

        Returns:
            Dictionary representation of the NOT expression.
            Example: {"type": "Not", "operand": {"type": "Proposition", "name": "P"}}
        """
        return {"type": "Not", "operand": self.operand.to_dict()}

    @classmethod
    def from_dict(cls, data: Dict) -> "Not":
        """
        Reconstructs a NOT expression from a dictionary.

        Args:
            data: Dictionary representation of a NOT expression.
                 Must contain an "operand" field.

        Returns:
            Reconstructed Not object.

        Raises:
            ValueError: If the data is invalid or contains an unknown operand type.
        """
        if "operand" in data:
            # Get the operand type from the operand data
            if "type" in data["operand"]:
                operand_type_name = data["operand"]["type"]
                if operand_type_name == "Proposition":
                    operand = Proposition.from_dict(data["operand"])
                elif operand_type_name == "Not":
                    operand = Not.from_dict(data["operand"])
                elif operand_type_name == "BinaryOp":
                    operand = BinaryOp.from_dict(data["operand"])
                else:
                    raise ValueError(f"Unknown operand type: {operand_type_name}")
                return cls(operand=operand)

        raise ValueError("Invalid NOT expression data")


class BinaryOp(LogicalExpression):
    """
    Represents binary logical operations (AND, OR, IMPLIES, IFF).

    Binary operations take two logical expressions as operands and combine
    them according to the specified operator.

    Attributes:
        left: The left operand of the binary operation.
        right: The right operand of the binary operation.
        operator: The type of binary operation, one of:
                 - "AND": logical conjunction (∧)
                 - "OR": logical disjunction (∨)
                 - "IMPLIES": logical implication (→)
                 - "IFF": logical biconditional (↔)
    """

    left: LogicalExpression
    right: LogicalExpression
    operator: Literal["AND", "OR", "IMPLIES", "IFF"]

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """
        Evaluates the binary operation given a truth assignment.

        Args:
            context: Dictionary mapping variable names to truth values.
                    Example: {"P": True, "Q": False}

        Returns:
            Boolean result of applying the binary operation to the operands.

        Raises:
            ValueError: If the operator is unknown.
        """
        left_val = self.left.evaluate(context)
        right_val = self.right.evaluate(context)

        if self.operator == "AND":
            return left_val and right_val
        elif self.operator == "OR":
            return left_val or right_val
        elif self.operator == "IMPLIES":
            return (not left_val) or right_val
        elif self.operator == "IFF":
            return left_val == right_val
        else:
            raise ValueError(f"Unknown operator: {self.operator}")

    def variables(self) -> List[str]:
        """
        Returns the list of variables in the binary operation.

        Returns:
            List of unique variable names from both operands.
        """
        return list(set(self.left.variables() + self.right.variables()))

    def depth(self) -> int:
        """
        Returns the depth of the expression tree.

        Returns:
            The maximum depth of either operand plus 1.
        """
        return 1 + max(self.left.depth(), self.right.depth())

    def to_dict(self) -> Dict:
        """
        Converts the binary operation to a dictionary.

        Returns:
            Dictionary representation of the binary operation.
            Example: {"type": "BinaryOp", "left": {"type": "Proposition", "name": "P"},
            "right": {"type": "Proposition", "name": "Q"}, "operator": "AND"}
        """
        return {
            "type": "BinaryOp",
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
            "operator": self.operator,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BinaryOp":
        """
        Reconstructs a binary operation from a dictionary.

        Args:
            data: Dictionary representation of a binary operation.
                 Must contain "left", "right", and "operator" fields.

        Returns:
            Reconstructed BinaryOp object.

        Raises:
            ValueError: If the data is invalid or contains unknown operand types.
        """
        if all(k in data for k in ["left", "right", "operator"]):
            # Parse left operand
            if "type" in data["left"]:
                left_type_name = data["left"]["type"]
                if left_type_name == "Proposition":
                    left = Proposition.from_dict(data["left"])
                elif left_type_name == "Not":
                    left = Not.from_dict(data["left"])
                elif left_type_name == "BinaryOp":
                    left = BinaryOp.from_dict(data["left"])
                else:
                    raise ValueError(f"Unknown left operand type: {left_type_name}")
            else:
                raise ValueError("Missing left operand type")

            # Parse right operand
            if "type" in data["right"]:
                right_type_name = data["right"]["type"]
                if right_type_name == "Proposition":
                    right = Proposition.from_dict(data["right"])
                elif right_type_name == "Not":
                    right = Not.from_dict(data["right"])
                elif right_type_name == "BinaryOp":
                    right = BinaryOp.from_dict(data["right"])
                else:
                    raise ValueError(f"Unknown right operand type: {right_type_name}")
            else:
                raise ValueError("Missing right operand type")

            # Create BinaryOp
            return cls(left=left, right=right, operator=data["operator"])

        raise ValueError("Invalid binary operation data")


class And(BinaryOp):
    """
    Represents logical conjunction (AND, ∧).

    Returns True if and only if both operands are True.
    """

    def __init__(self, left: LogicalExpression, right: LogicalExpression):
        """Initialize an AND operation with left and right operands."""
        super().__init__(left=left, right=right, operator="AND")


class Or(BinaryOp):
    """
    Represents logical disjunction (OR, ∨).

    Returns True if at least one operand is True.
    """

    def __init__(self, left: LogicalExpression, right: LogicalExpression):
        """Initialize an OR operation with left and right operands."""
        super().__init__(left=left, right=right, operator="OR")


class Implies(BinaryOp):
    """
    Represents logical implication (IMPLIES, →).

    Returns True if the left operand is False or the right operand is True.
    """

    def __init__(self, left: LogicalExpression, right: LogicalExpression):
        """Initialize an IMPLIES operation with left and right operands."""
        super().__init__(left=left, right=right, operator="IMPLIES")


class Iff(BinaryOp):
    """
    Represents logical biconditional (IFF, ↔).

    Returns True if both operands have the same truth value.
    """

    def __init__(self, left: LogicalExpression, right: LogicalExpression):
        """Initialize an IFF operation with left and right operands."""
        super().__init__(left=left, right=right, operator="IFF")


class Xor(BinaryOp):
    """
    Represents logical exclusive disjunction (XOR, ⊕).

    Returns True if exactly one operand is True.
    """

    def __init__(self, left: LogicalExpression, right: LogicalExpression):
        """Initialize a XOR operation with left and right operands."""
        super().__init__(left=left, right=right, operator="XOR")

    def evaluate(self, context: Dict[str, bool]) -> bool:
        """
        Evaluates the XOR operation given a truth assignment.

        Args:
            context: Dictionary mapping variable names to truth values.

        Returns:
            Boolean result of XOR operation (True if exactly one operand is True).
        """
        left_val = self.left.evaluate(context)
        right_val = self.right.evaluate(context)
        return left_val != right_val
