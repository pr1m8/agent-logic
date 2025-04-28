"""
Logical proofs module.

This module provides tools for constructing and validating logical proofs,
including inference rules and proof verification systems.
"""

from agent_logic.proofs.inference_rules import InferenceRules
from agent_logic.proofs.proof_system import Proof, ProofStep
from agent_logic.proofs.quantifier_rules import QuantifierRules
from agent_logic.proofs.unification import Unification

__all__ = [
    "InferenceRules",
    "Proof",
    "ProofStep",
    "QuantifierRules",
    "Unification"
]
