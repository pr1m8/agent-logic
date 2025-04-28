from typing import Dict

from agent_logic.core.base import LogicalExpression
from agent_logic.core.functions import Function, Relation
from agent_logic.core.operations import BinaryOp, Not, Proposition
from agent_logic.core.quantifiers import ExistentialQuantifier, UniversalQuantifier


class ASTParser:
    """Parses structured data (JSON/dict) into logical expressions."""

    @staticmethod
    def parse_dict(data: Dict) -> LogicalExpression:
        """Recursively parses a JSON/dict representation into an expression."""

        if data["type"] == "Proposition":
            return Proposition.from_dict(data)

        elif data["type"] == "Not":
            return Not.from_dict(data)

        elif data["type"] == "BinaryOp":
            return BinaryOp.from_dict(data)

        elif data["type"] == "Function":
            return Function.from_dict(data)

        elif data["type"] == "Relation":
            return Relation.from_dict(data)

        elif data["type"] == "UniversalQuantifier":
            return UniversalQuantifier.from_dict(data)

        elif data["type"] == "ExistentialQuantifier":
            return ExistentialQuantifier.from_dict(data)

        raise ValueError(f"Unknown expression type: {data['type']}")
