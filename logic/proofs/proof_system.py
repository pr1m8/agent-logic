from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from logic.core.base import LogicalExpression
from logic.proofs.inference_rules import InferenceRules
from logic.transformations.equivalences import EquivalenceRules
from logic.evaluation.evaluator import Evaluator


class ProofStep(BaseModel):
    """Represents a single step in a structured proof."""
    step_number: int
    statement: LogicalExpression
    justification: str = Field(..., description="Inference rule or equivalence used.")
    dependencies: Optional[List[int]] = Field(None, description="Previous step references.")


class Proof(BaseModel):
    """Represents a structured proof with step-by-step reasoning."""
    steps: List[ProofStep]

    def is_valid(self) -> bool:
        """Validates the proof by ensuring logical correctness of each step."""
        known_statements: Dict[int, LogicalExpression] = {}

        for step in self.steps:
            # Ensure referenced steps exist
            if step.dependencies:
                for dep in step.dependencies:
                    if dep not in known_statements:
                        return False  # Invalid reference

            # Validate the statement based on justification
            derived_statement = self.apply_inference(step, known_statements)
            if derived_statement is None or derived_statement != step.statement:
                return False  # Invalid inference or incorrect statement

            # Store step statement
            known_statements[step.step_number] = step.statement

        return True  # If all steps are logically sound

    def apply_inference(self, step: ProofStep, known_statements: Dict[int, LogicalExpression]) -> Optional[LogicalExpression]:
        """Applies inference rules or equivalence transformations to derive the expected statement."""
        if step.dependencies:
            # Fetch referenced statements
            ref_statements = [known_statements[dep] for dep in step.dependencies]

            # Apply corresponding inference rule
            if step.justification == "Modus Ponens":
                return InferenceRules.modus_ponens(ref_statements[0], ref_statements[1])
            elif step.justification == "Modus Tollens":
                return InferenceRules.modus_tollens(ref_statements[0], ref_statements[1])
            elif step.justification == "Hypothetical Syllogism":
                return InferenceRules.hypothetical_syllogism(ref_statements[0], ref_statements[1])
            elif step.justification == "Disjunctive Syllogism":
                return InferenceRules.disjunctive_syllogism(ref_statements[0], ref_statements[1])
            elif step.justification == "Constructive Dilemma":
                return InferenceRules.constructive_dilemma(ref_statements[0], ref_statements[1], ref_statements[2])
            elif step.justification == "Distributive Law":
                return EquivalenceRules.distributive_law(ref_statements[0])
            elif step.justification == "De Morgan’s Law":
                return EquivalenceRules.apply_de_morgan(ref_statements[0])
            elif step.justification == "Double Negation":
                return EquivalenceRules.double_negation(ref_statements[0])
            elif step.justification == "Proof by Contradiction":
                return EquivalenceRules.contradiction_elimination(ref_statements[0])

        return None  # No valid derivation found

    def to_dict(self) -> Dict:
        """Serializes the proof to a structured dictionary for external usage."""
        return {"steps": [step.dict() for step in self.steps]}

    @classmethod
    def from_dict(cls, data: Dict) -> Proof:
        """Reconstructs a proof from a dictionary representation."""
        steps = [ProofStep(**step) for step in data["steps"]]
        return cls(steps=steps)
