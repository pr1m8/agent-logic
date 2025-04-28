import unittest

from logic.core.operations import BinaryOp, Not, Proposition
from logic.proofs.inference_rules import InferenceRules


class TestInferenceRules(unittest.TestCase):

    def test_modus_ponens(self):
        """Test Modus Ponens: P, (P → Q) ⊢ Q."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        result = InferenceRules.modus_ponens(p, p_implies_q)
        self.assertEqual(result, q)

    def test_modus_tollens(self):
        """Test Modus Tollens: ¬Q, (P → Q) ⊢ ¬P."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        not_q = Not(q)
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        result = InferenceRules.modus_tollens(not_q, p_implies_q)
        self.assertEqual(result, Not(p))

    def test_disjunctive_syllogism(self):
        """Test Disjunctive Syllogism: (P ∨ Q), ¬P ⊢ Q."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_or_q = BinaryOp(left=p, right=q, operator="OR")
        not_p = Not(p)

        result = InferenceRules.disjunctive_syllogism(p_or_q, not_p)
        self.assertEqual(result, q)

    def test_biconditional_elimination(self):
        """Test Biconditional Elimination: (P ↔ Q) ⊢ (P → Q), (Q → P)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_iff_q = BinaryOp(left=p, right=q, operator="IFF")

        result = InferenceRules.biconditional_elimination(p_iff_q)
        self.assertEqual(result[0], BinaryOp(left=p, right=q, operator="IMPLIES"))
        self.assertEqual(result[1], BinaryOp(left=q, right=p, operator="IMPLIES"))
