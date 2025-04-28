"""
Logic models module.

This module provides AI model interfaces for logical reasoning and proof generation.
"""

from agent_logic.models.llm_proof_model import (
    LLMProofRequest,
    LLMProofResponse,
    LLMTruthTableRequest,
    LLMTruthTableResponse,
    LLMEquivalenceRequest,
    LLMEquivalenceResponse
)

__all__ = [
    "LLMProofRequest",
    "LLMProofResponse",
    "LLMTruthTableRequest",
    "LLMTruthTableResponse",
    "LLMEquivalenceRequest",
    "LLMEquivalenceResponse"
] 