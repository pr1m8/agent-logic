"""
Proof system module for logical reasoning.

This module provides classes for representing and validating logical proofs.
It includes:
- ProofStep: Represents a single step in a logical proof
- Proof: Represents a complete proof with multiple steps and validation logic

The proof system supports various inference rules and validates
the logical correctness of each step in the proof.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from agent_logic.core.base import LogicalExpression
from agent_logic.core.operations import BinaryOp, Proposition
from agent_logic.proofs.inference_rules import InferenceRules
from agent_logic.proofs.quantifier_rules import QuantifierRules
from agent_logic.proofs.unification import Unification
from agent_logic.utils.logger import get_logger

# Create module-level logger
logger = get_logger(__name__)


class ProofStep(BaseModel):
    """
    Represents a single step in a structured proof.

    Each step consists of a logical statement, a justification for that statement,
    and optional references to previous steps that support the justification.

    Attributes:
        step_number: Sequential number identifying this step in the proof.
        statement: The logical expression being asserted at this step.
        justification: Name of the inference rule or justification for this step.
        dependencies: List of step numbers that this step depends on, or None if this is a premise.
    """

    step_number: int
    statement: LogicalExpression
    justification: str = Field(..., description="Inference rule or equivalence used.")
    dependencies: Optional[List[int]] = Field(
        None, description="Previous step references."
    )


class Proof(BaseModel):
    """
    Represents a structured proof with step-by-step reasoning.

    A proof consists of a sequence of steps, each building on previous steps
    according to valid rules of inference. The proof is valid if each step
    follows logically from the steps it depends on.

    Attributes:
        steps: List of ProofStep objects making up the proof.
        debug: Boolean flag to enable or disable debug output during validation.
    """

    steps: List[ProofStep]
    debug: bool = False  # Control debug output

    def is_valid(self) -> bool:
        """
        Validates the proof by ensuring logical correctness of each step.

        The validation process checks that:
        1. All referenced dependencies exist
        2. Each step follows logically from its dependencies using the specified rule
        3. The derived statement matches the claimed statement

        Returns:
            Boolean indicating whether the proof is valid.
        """
        known_statements: Dict[int, LogicalExpression] = {}

        for step in self.steps:
            if self.debug:
                logger.debug(f"Checking step {step.step_number}: {step.statement}")

            # ✅ If it's a given premise, add it to known statements automatically.
            if step.justification == "Given":
                known_statements[step.step_number] = step.statement
                continue  # Skip inference for given premises

            # Ensure referenced steps exist
            if step.dependencies:
                for dep in step.dependencies:
                    if dep not in known_statements:
                        if self.debug:
                            logger.warning(f"Invalid reference to step {dep}")
                        return False  # Invalid reference

            # Apply inference
            derived_statement = self.apply_inference(step, known_statements)

            if derived_statement is None:
                if self.debug:
                    logger.warning(
                        f"Failed derivation at step {step.step_number}: No inference applied"
                    )
                return False

            if str(derived_statement) != str(
                step.statement
            ):  # Compare by string representation
                if self.debug:
                    logger.warning(f"Mismatch at step {step.step_number}:")
                    logger.warning(f"  Expected: {step.statement}")
                    logger.warning(f"  Got:      {derived_statement}")
                return False  # Statement mismatch

            known_statements[step.step_number] = step.statement

        return True  # If all steps are logically sound

    def apply_inference(
        self, step: ProofStep, known_statements: Dict[int, LogicalExpression]
    ) -> Optional[LogicalExpression]:
        """
        Applies inference rules dynamically based on the step's justification.

        Extracts the referenced statements from previous steps,
        and applies the appropriate inference rule to derive the current step.

        Args:
            step: The current proof step being validated.
            known_statements: Dictionary mapping step numbers to their logical expressions.

        Returns:
            The derived logical expression, or None if inference failed.
        """
        if step.dependencies:
            ref_statements = [
                known_statements[dep]
                for dep in step.dependencies
                if dep in known_statements
            ]

            # Map rule names to methods dynamically
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

                # Handle different numbers of dependencies (arguments)
                try:
                    if (
                        step.justification == "Modus Ponens"
                        and len(ref_statements) == 2
                    ):
                        # For Modus Ponens, ensure correct parameter order
                        for i in range(2):
                            if (
                                isinstance(ref_statements[i], Proposition)
                                and isinstance(ref_statements[1 - i], BinaryOp)
                                and ref_statements[1 - i].operator == "IMPLIES"
                            ):
                                return rule_func(
                                    ref_statements[i], ref_statements[1 - i]
                                )
                        # If no valid combination found
                        return None
                    elif (
                        step.justification == "Modus Ponens"
                        and len(ref_statements) != 2
                    ):
                        # Silently fail for Modus Ponens with wrong number of dependencies
                        if self.debug:
                            logger.warning(
                                f"Failed at step {step.step_number}: Modus Ponens requires exactly 2 dependencies"
                            )
                        return None
                    elif len(ref_statements) == 1:
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
                except (ValueError, TypeError) as e:
                    if self.debug:
                        logger.error(f"Error at step {step.step_number}: {e}")
                    return None  # Return None on failure

        return None  # If no valid inference is applied

    def to_dict(self) -> Dict:
        """
        Serializes the proof to a structured dictionary for external usage.

        Returns:
            Dictionary representation of the proof with all steps.
        """
        # Convert each step to a dictionary, ensuring statement is also converted to dict
        steps_data = []
        for step in self.steps:
            step_dict = step.model_dump()  # Use model_dump instead of dict
            # Ensure statement is serialized as a dict with type information
            step_dict["statement"] = step.statement.to_dict()
            steps_data.append(step_dict)

        return {"steps": steps_data}

    @classmethod
    def from_dict(cls, data: Dict) -> Proof:
        """
        Reconstructs a proof from a dictionary representation.

        Args:
            data: Dictionary containing a "steps" list with proof step data.

        Returns:
            Reconstructed Proof object.
        """
        steps_data = data.get("steps", [])

        # Create ProofStep objects with properly reconstructed statements
        steps = []
        for step_data in steps_data:
            # If step_data["statement"] is itself a dictionary, reconstruct it as a LogicalExpression
            if isinstance(step_data.get("statement"), dict):
                from agent_logic.core.base import LogicalExpression

                step_data["statement"] = LogicalExpression.from_dict(
                    step_data["statement"]
                )

            # Create the ProofStep
            steps.append(ProofStep(**step_data))

        return cls(steps=steps)
