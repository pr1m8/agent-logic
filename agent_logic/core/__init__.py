"""
Core logical expressions and operations.

This module provides the fundamental building blocks for creating and manipulating
logical expressions in propositional and predicate logic.

Classes:
    LogicalExpression: Abstract base class for all logical expressions
    Proposition: A basic propositional variable
    Not: Logical negation operation
    BinaryOp: Base class for binary logical operations (And, Or, Implies, etc.)
    Quantifier: Base class for quantified expressions
    Predicate: Representation of predicate expressions
    Function: Representation of function terms
"""

from agent_logic.core.base import LogicalExpression
from agent_logic.core.functions import Function
from agent_logic.core.operations import (
    And,
    BinaryOp,
    Iff,
    Implies,
    Not,
    Or,
    Proposition,
    Xor,
)
from agent_logic.core.predicates import Predicate, Term
from agent_logic.core.quantifiers import Exists, ForAll, Quantifier

__all__ = [
    # Base classes
    "LogicalExpression",
    # Propositional logic
    "Proposition",
    "Not",
    "BinaryOp",
    "And",
    "Or",
    "Implies",
    "Iff",
    "Xor",
    # Predicate logic
    "Quantifier",
    "ForAll",
    "Exists",
    "Predicate",
    "Function",
    "Term",
]
