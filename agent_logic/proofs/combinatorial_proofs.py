from itertools import permutations
from typing import List, Optional

from agent_logic.core.base import LogicalExpression
from agent_logic.proofs.inference_rules import InferenceRules
from agent_logic.proofs.proof_system import Proof, ProofStep
from agent_logic.transformations.equivalences import EquivalenceRules


class CombinatorialProofs:
    """Automates proof verification by searching for valid proof sequences."""

    @staticmethod
    def brute_force_proof(
        goal: LogicalExpression, premises: List[LogicalExpression], max_depth: int = 5
    ) -> Optional[Proof]:
        """
        Tries all possible proof sequences up to `max_depth` steps.
        Returns the shortest valid proof if found, else None.
        """
        known_statements = {i + 1: premise for i, premise in enumerate(premises)}
        proof_steps = [
            ProofStep(step_number=i + 1, statement=premise, justification="Given")
            for i, premise in enumerate(premises)
        ]

        for _depth in range(1, max_depth + 1):
            for perm in permutations(
                list(known_statements.keys()), 2
            ):  # Try all 2-combinations of premises
                p, q = known_statements[perm[0]], known_statements[perm[1]]

                # Try all inference rules
                derived_statements = [
                    InferenceRules.modus_ponens(p, q),
                    InferenceRules.modus_tollens(p, q),
                    InferenceRules.hypothetical_syllogism(p, q),
                    InferenceRules.disjunctive_syllogism(p, q),
                    EquivalenceRules.apply_de_morgan(p),
                    EquivalenceRules.double_negation(p),
                ]

                for new_statement in derived_statements:
                    if new_statement and new_statement not in known_statements.values():
                        step_number = len(known_statements) + 1
                        known_statements[step_number] = new_statement
                        proof_steps.append(
                            ProofStep(
                                step_number=step_number,
                                statement=new_statement,
                                justification="Derived",
                                dependencies=[perm[0], perm[1]],
                            )
                        )

                        if new_statement == goal:
                            return Proof(
                                steps=proof_steps
                            )  # Return proof if goal is reached

        return None  # No proof found within max depth

    @staticmethod
    def validate_proof(proof: Proof) -> bool:
        """Validates whether a given proof follows logical derivation rules."""
        return proof.is_valid()
