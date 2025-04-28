from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from agent_logic.core.base import LogicalExpression
from agent_logic.proofs.proof_system import ProofStep


class LLMProofRequest(BaseModel):
    """Defines the structure for LLMs to request a proof verification."""

    premises: List[LogicalExpression] = Field(
        ..., description="Premises for the logical proof."
    )
    goal: LogicalExpression = Field(..., description="Goal to be proven.")
    max_depth: Optional[int] = Field(
        5, description="Max steps allowed for proof derivation."
    )


class LLMProofResponse(BaseModel):
    """Defines the structure of the response for LLM-driven proof validation."""

    is_valid: bool = Field(..., description="Indicates whether the proof is valid.")
    proof_steps: Optional[List[ProofStep]] = Field(
        None, description="Proof steps if a valid proof is found."
    )
    error_message: Optional[str] = Field(
        None, description="Error message in case of failure."
    )


class LLMTruthTableRequest(BaseModel):
    """Defines the structure for requesting a truth table generation."""

    expression: LogicalExpression = Field(
        ..., description="Logical expression for truth table analysis."
    )


class LLMTruthTableResponse(BaseModel):
    """Defines the response structure for an LLM-generated truth table."""

    truth_table: List[Dict[str, bool]] = Field(
        ..., description="Generated truth table."
    )
    is_tautology: bool = Field(
        ..., description="Indicates if the expression is a tautology."
    )
    is_contradiction: bool = Field(
        ..., description="Indicates if the expression is a contradiction."
    )
    is_satisfiable: bool = Field(
        ..., description="Indicates if the expression is satisfiable."
    )


class LLMEquivalenceRequest(BaseModel):
    """Defines the structure for equivalence transformation requests."""

    expression: LogicalExpression = Field(..., description="Expression to transform.")
    transformation: str = Field(
        ...,
        description="Type of transformation (e.g., 'De Morgan', 'Double Negation').",
    )


class LLMEquivalenceResponse(BaseModel):
    """Defines the structure of the response for equivalence transformations."""

    transformed_expression: LogicalExpression = Field(
        ..., description="Transformed logical expression."
    )
