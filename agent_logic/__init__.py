"""
Agent Logic Package.

This package provides tools for propositional logic, proof validation, and logical reasoning.
It includes components for defining logical expressions, evaluating truth values,
constructing and validating proofs, and working with logical inference rules.

Modules:
    core: Core logical expressions and operations
    proofs: Tools for constructing and validating logical proofs
    evaluation: Truth table generation and evaluation
    utils: Utility functions and logging tools
"""

__version__ = "1.0.0"

# Define public API
__all__ = [
    # Core logic expressions
    "LogicalExpression",
    "Proposition",
    "Not",
    "BinaryOp",
    # Inference rules and proof system
    "InferenceRules",
    "Proof",
    "ProofStep",
    # Truth table evaluation
    "TruthTable",
    # Utilities
    "get_logger",
    "set_global_log_level",
]

# Import key classes and functions for easier access
from agent_logic.core.base import LogicalExpression
from agent_logic.core.operations import BinaryOp, Not, Proposition

# Evaluation tools
from agent_logic.evaluation.truth_table import TruthTable

# Proof system imports
from agent_logic.proofs.inference_rules import InferenceRules
from agent_logic.proofs.proof_system import Proof, ProofStep

# Utility functions
from agent_logic.utils.logger import get_logger, set_global_log_level
