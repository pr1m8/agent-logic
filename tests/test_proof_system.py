import logging
import unittest

from agent_logic.core.operations import BinaryOp, Not, Proposition
from agent_logic.proofs.proof_system import Proof, ProofStep
from agent_logic.utils.logger import set_global_log_level


class TestProofSystem(unittest.TestCase):

    def setUp(self):
        # Set log level to ERROR for tests to minimize output
        set_global_log_level(logging.ERROR)

    def test_proof_validation(self):
        """Test that proof validation correctly follows inference rules."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        step1 = ProofStep(step_number=1, statement=p, justification="Given")
        step2 = ProofStep(step_number=2, statement=p_implies_q, justification="Given")
        step3 = ProofStep(
            step_number=3,
            statement=q,
            justification="Modus Ponens",
            dependencies=[1, 2],
        )

        proof = Proof(steps=[step1, step2, step3], debug=True)
        self.assertTrue(proof.is_valid())

    def test_invalid_proof(self):
        """Test an invalid proof scenario."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        not_q = Not(operand=q)

        step1 = ProofStep(step_number=1, statement=p, justification="Given")
        step2 = ProofStep(
            step_number=2,
            statement=not_q,
            justification="Modus Ponens",
            dependencies=[1],
        )

        proof = Proof(steps=[step1, step2], debug=True)
        self.assertFalse(proof.is_valid())

    def test_multi_step_proof(self):
        """Test a multi-step proof with multiple inference rules."""
        # Proof: P, P→Q, Q→R ⊢ R
        p = Proposition(name="P")
        q = Proposition(name="Q")
        r = Proposition(name="R")

        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")
        q_implies_r = BinaryOp(left=q, right=r, operator="IMPLIES")

        steps = [
            ProofStep(step_number=1, statement=p, justification="Given"),
            ProofStep(step_number=2, statement=p_implies_q, justification="Given"),
            ProofStep(step_number=3, statement=q_implies_r, justification="Given"),
            ProofStep(
                step_number=4,
                statement=q,
                justification="Modus Ponens",
                dependencies=[1, 2],
            ),
            ProofStep(
                step_number=5,
                statement=r,
                justification="Modus Ponens",
                dependencies=[4, 3],
            ),
        ]

        proof = Proof(steps=steps, debug=True)
        self.assertTrue(proof.is_valid())

    def test_complex_proof(self):
        """Test a more complex proof using several inference rules."""
        # Proof: P→Q, ¬Q ⊢ ¬P (Modus Tollens)
        # But we'll derive it using multiple steps
        p = Proposition(name="P")
        q = Proposition(name="Q")

        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")
        not_q = Not(operand=q)
        not_p = Not(operand=p)

        steps = [
            ProofStep(step_number=1, statement=p_implies_q, justification="Given"),
            ProofStep(step_number=2, statement=not_q, justification="Given"),
            ProofStep(
                step_number=3,
                statement=not_p,
                justification="Modus Tollens",
                dependencies=[2, 1],
            ),
        ]

        proof = Proof(steps=steps, debug=True)
        self.assertTrue(proof.is_valid())

    def test_proof_with_law_of_excluded_middle(self):
        """Test a proof that uses the Law of Excluded Middle."""
        # Proof: ⊢ P∨¬P (Law of Excluded Middle)
        p = Proposition(name="P")

        steps = [
            # First create a step to introduce P
            ProofStep(step_number=1, statement=p, justification="Given"),
            # Then apply Law of Excluded Middle using P
            ProofStep(
                step_number=2,
                statement=BinaryOp(left=p, right=Not(operand=p), operator="OR"),
                justification="Law of Excluded Middle",
                dependencies=[1],  # Depends on introducing P first
            ),
        ]

        proof = Proof(steps=steps, debug=True)
        self.assertTrue(proof.is_valid())

    def test_proof_with_dependency_error(self):
        """Test a proof with a missing dependency."""
        p = Proposition(name="P")
        q = Proposition(name="Q")

        steps = [
            ProofStep(step_number=1, statement=p, justification="Given"),
            ProofStep(
                step_number=2,
                statement=q,
                justification="Modus Ponens",
                dependencies=[1, 3],  # Dependency 3 doesn't exist yet
            ),
        ]

        proof = Proof(steps=steps, debug=True)
        self.assertFalse(proof.is_valid())

    def test_proof_with_incorrect_inference(self):
        """Test a proof with an incorrect inference application."""
        p = Proposition(name="P")
        Proposition(name="Q")
        r = Proposition(name="R")  # Unrelated proposition

        steps = [
            ProofStep(step_number=1, statement=p, justification="Given"),
            ProofStep(
                step_number=2,
                statement=r,  # This shouldn't follow from just p
                justification="Modus Ponens",
                dependencies=[1],  # Missing the implication premise
            ),
        ]

        proof = Proof(steps=steps, debug=True)
        self.assertFalse(proof.is_valid())

    def test_to_dict_from_dict(self):
        """Test serialization and deserialization of proofs."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        steps = [
            ProofStep(step_number=1, statement=p, justification="Given"),
            ProofStep(step_number=2, statement=p_implies_q, justification="Given"),
            ProofStep(
                step_number=3,
                statement=q,
                justification="Modus Ponens",
                dependencies=[1, 2],
            ),
        ]

        original_proof = Proof(steps=steps)

        # Convert to dict and back
        proof_dict = original_proof.to_dict()
        reconstructed_proof = Proof.from_dict(proof_dict)

        # Check that the steps match
        self.assertEqual(len(reconstructed_proof.steps), len(original_proof.steps))

        # Check step 3's dependencies
        self.assertEqual(
            reconstructed_proof.steps[2].dependencies,
            original_proof.steps[2].dependencies,
        )
