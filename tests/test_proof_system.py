import unittest

from logic.core.operations import BinaryOp, Not, Proposition
from logic.proofs.proof_system import Proof, ProofStep


class TestProofSystem(unittest.TestCase):

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

        proof = Proof(steps=[step1, step2, step3])
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

        proof = Proof(steps=[step1, step2])
        self.assertFalse(proof.is_valid())
