from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from logic.core.base import LogicalExpression
from logic.proofs.inference_rules import InferenceRules
from logic.proofs.quantifier_rules import QuantifierRules
from logic.proofs.unification import Unification


class ProofStep(BaseModel):
    """Represents a single step in a structured proof."""

    step_number: int
    statement: LogicalExpression
    justification: str = Field(..., description="Inference rule or equivalence used.")
    dependencies: Optional[List[int]] = Field(
        None, description="Previous step references."
    )


class Proof(BaseModel):
    """Represents a structured proof with step-by-step reasoning."""

    steps: List[ProofStep]

    def is_valid(self) -> bool:
        """Validates the proof by ensuring logical correctness of each step."""
        known_statements: Dict[int, LogicalExpression] = {}

        for step in self.steps:
            print(f"Checking step {step.step_number}: {step.statement}")

            # ✅ If it's a given premise, add it to known statements automatically.
            if step.justification == "Given":
                known_statements[step.step_number] = step.statement
                continue  # Skip inference for given premises

            # Ensure referenced steps exist
            if step.dependencies:
                for dep in step.dependencies:
                    if dep not in known_statements:
                        print(f"Invalid reference to step {dep}")
                        return False  # Invalid reference

            # Apply inference
            derived_statement = self.apply_inference(step, known_statements)

            if derived_statement is None:
                print(
                    f"Failed derivation at step {step.step_number}: No inference applied"
                )
                return False

            if str(derived_statement) != str(
                step.statement
            ):  # Compare by string representation
                print(f"Mismatch at step {step.step_number}:")
                print(f"  Expected: {step.statement}")
                print(f"  Got:      {derived_statement}")
                return False  # Statement mismatch

            known_statements[step.step_number] = step.statement

        return True  # If all steps are logically sound

    def apply_inference(
        self, step: ProofStep, known_statements: Dict[int, LogicalExpression]
    ) -> Optional[LogicalExpression]:
        """Applies inference rules dynamically based on the step's justification."""
        if step.dependencies:
            ref_statements = [
                known_statements[dep]
                for dep in step.dependencies
                if dep in known_statements
            ]

            # ✅ Map rule names to methods dynamically
            inference_methods = {
                "Modus Ponens": InferenceRules.modus_ponens,
                "Modus Tollens": InferenceRules.modus_tollens,
                "Hypothetical Syllogism": InferenceRules.hypothetical_syllogism,
                "Disjunctive Syllogism": InferenceRules.disjunctive_syllogism,
                "Law of Excluded Middle": InferenceRules.law_of_excluded_middle,
                "Proof by Contradiction": InferenceRules.proof_by_contradiction,
                "Absorption": InferenceRules.absorption,
                "Transitivity of Implication": InferenceRules.transitivity_of_implication,
                "Constructive Negation": InferenceRules.constructive_negation,
                "Distributive Rule": InferenceRules.distributive_rule,
                "Associative Rule": InferenceRules.associative_rule,
                "Constructive Dilemma": InferenceRules.constructive_dilemma,
                "Destructive Dilemma": InferenceRules.destructive_dilemma,
                "Conjunction Introduction": InferenceRules.conjunction_introduction,
                "Conjunction Elimination": InferenceRules.conjunction_elimination,
                "Addition": InferenceRules.addition,
                "Biconditional Elimination": InferenceRules.biconditional_elimination,
                "Biconditional Introduction": InferenceRules.biconditional_introduction,
                "Negation Introduction": InferenceRules.negation_introduction,
                "Negation Elimination": InferenceRules.negation_elimination,
                "Universal Elimination": QuantifierRules.universal_elimination,
                "Existential Instantiation": QuantifierRules.existential_instantiation,
                "Existential Generalization": QuantifierRules.existential_generalization,
                "Unification": Unification.unify,
            }

            if step.justification in inference_methods:
                rule_func = inference_methods[step.justification]

                # ✅ Handle different numbers of dependencies (arguments)
                try:
                    if len(ref_statements) == 1:
                        return rule_func(ref_statements[0])
                    elif len(ref_statements) == 2:
                        return rule_func(ref_statements[0], ref_statements[1])
                    elif len(ref_statements) == 3:
                        return rule_func(
                            ref_statements[0], ref_statements[1], ref_statements[2]
                        )
                    else:
                        raise ValueError(
                            f"Invalid number of arguments for {step.justification}"
                        )
                except ValueError as e:
                    print(f"❌ Error at step {step.step_number}: {e}")
                    return None  # Return None on failure

        return None  # If no valid inference is applied

    def to_dict(self) -> Dict:
        """Serializes the proof to a structured dictionary for external usage."""
        return {"steps": [step.dict() for step in self.steps]}

    @classmethod
    def from_dict(cls, data: Dict) -> Proof:
        """Reconstructs a proof from a dictionary representation."""
        steps = [ProofStep(**step) for step in data["steps"]]
        return cls(steps=steps)
