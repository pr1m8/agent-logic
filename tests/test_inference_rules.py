import unittest

from agent_logic.core.operations import BinaryOp, Not, Proposition
from agent_logic.proofs.inference_rules import InferenceRules


class TestInferenceRules(unittest.TestCase):

    def test_modus_ponens(self):
        """Test Modus Ponens: P, (P → Q) ⊢ Q."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        result = InferenceRules.modus_ponens(p, p_implies_q)
        self.assertEqual(result, q)

        # Test with non-matching proposition
        r = Proposition(name="R")
        result = InferenceRules.modus_ponens(r, p_implies_q)
        self.assertIsNone(result)

    def test_modus_tollens(self):
        """Test Modus Tollens: ¬Q, (P → Q) ⊢ ¬P."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        not_q = Not(operand=q)
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        result = InferenceRules.modus_tollens(not_q, p_implies_q)
        self.assertEqual(result, Not(operand=p))

        # Test error case with invalid input
        r = Proposition(name="R")
        with self.assertRaises(ValueError):
            InferenceRules.modus_tollens(r, p_implies_q)

    def test_disjunctive_syllogism(self):
        """Test Disjunctive Syllogism: (P ∨ Q), ¬P ⊢ Q."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_or_q = BinaryOp(left=p, right=q, operator="OR")
        not_p = Not(operand=p)

        result = InferenceRules.disjunctive_syllogism(p_or_q, not_p)
        self.assertEqual(result, q)

        # Test with negated right operand
        not_q = Not(operand=q)
        p_or_q = BinaryOp(left=p, right=q, operator="OR")
        result = InferenceRules.disjunctive_syllogism(p_or_q, not_q)
        self.assertEqual(result, p)

        # Test error case
        r = Proposition(name="R")
        with self.assertRaises(ValueError):
            InferenceRules.disjunctive_syllogism(p_or_q, r)

    def test_biconditional_elimination(self):
        """Test Biconditional Elimination: (P ↔ Q) ⊢ (P → Q), (Q → P)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_iff_q = BinaryOp(left=p, right=q, operator="IFF")

        result = InferenceRules.biconditional_elimination(p_iff_q)
        self.assertEqual(result[0], BinaryOp(left=p, right=q, operator="IMPLIES"))
        self.assertEqual(result[1], BinaryOp(left=q, right=p, operator="IMPLIES"))

        # Test error case
        p_and_q = BinaryOp(left=p, right=q, operator="AND")
        with self.assertRaises(ValueError):
            InferenceRules.biconditional_elimination(p_and_q)

    def test_hypothetical_syllogism(self):
        """Test Hypothetical Syllogism: (P → Q), (Q → R) ⊢ (P → R)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        r = Proposition(name="R")

        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")
        q_implies_r = BinaryOp(left=q, right=r, operator="IMPLIES")

        result = InferenceRules.hypothetical_syllogism(p_implies_q, q_implies_r)
        expected = BinaryOp(left=p, right=r, operator="IMPLIES")

        self.assertEqual(result.left, expected.left)
        self.assertEqual(result.right, expected.right)
        self.assertEqual(result.operator, expected.operator)

        # Test error case with non-matching middle term
        s = Proposition(name="S")
        s_implies_r = BinaryOp(left=s, right=r, operator="IMPLIES")

        with self.assertRaises(ValueError):
            InferenceRules.hypothetical_syllogism(p_implies_q, s_implies_r)

    def test_law_of_excluded_middle(self):
        """Test Law of Excluded Middle: ⊢ (P ∨ ¬P)."""
        p = Proposition(name="P")

        result = InferenceRules.law_of_excluded_middle(p)
        expected = BinaryOp(left=p, right=Not(operand=p), operator="OR")

        self.assertEqual(result.left, expected.left)
        self.assertEqual(result.right.operand, expected.right.operand)
        self.assertEqual(result.operator, expected.operator)

    def test_proof_by_contradiction(self):
        """Test Proof by Contradiction: P ⊢ ⊥ ⟹ ¬P."""
        p = Proposition(name="P")

        result = InferenceRules.proof_by_contradiction(p, None)
        expected = Not(operand=p)

        self.assertEqual(result.operand, expected.operand)

        # Test error case
        q = Proposition(name="Q")
        with self.assertRaises(ValueError):
            InferenceRules.proof_by_contradiction(p, q)

    def test_constructive_dilemma(self):
        """Test Constructive Dilemma: (P → Q), (R → S), (P ∨ R) ⊢ (Q ∨ S)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        r = Proposition(name="R")
        s = Proposition(name="S")

        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")
        r_implies_s = BinaryOp(left=r, right=s, operator="IMPLIES")
        p_or_r = BinaryOp(left=p, right=r, operator="OR")

        result = InferenceRules.constructive_dilemma(p_implies_q, r_implies_s, p_or_r)
        expected = BinaryOp(left=q, right=s, operator="OR")

        self.assertEqual(result.left, expected.left)
        self.assertEqual(result.right, expected.right)
        self.assertEqual(result.operator, expected.operator)

        # Test error case
        wrong_or = BinaryOp(left=p, right=q, operator="OR")
        with self.assertRaises(ValueError):
            InferenceRules.constructive_dilemma(p_implies_q, r_implies_s, wrong_or)

    def test_conjunction_introduction(self):
        """Test Conjunction Introduction: P, Q ⊢ (P ∧ Q)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")

        result = InferenceRules.conjunction_introduction(p, q)
        expected = BinaryOp(left=p, right=q, operator="AND")

        self.assertEqual(result.left, expected.left)
        self.assertEqual(result.right, expected.right)
        self.assertEqual(result.operator, expected.operator)

    def test_conjunction_elimination(self):
        """Test Conjunction Elimination: (P ∧ Q) ⊢ P, Q."""
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_and_q = BinaryOp(left=p, right=q, operator="AND")

        result = InferenceRules.conjunction_elimination(p_and_q)

        self.assertEqual(result[0], p)
        self.assertEqual(result[1], q)

        # Test error case
        p_or_q = BinaryOp(left=p, right=q, operator="OR")
        with self.assertRaises(ValueError):
            InferenceRules.conjunction_elimination(p_or_q)

    def test_addition(self):
        """Test Addition: P ⊢ (P ∨ Q)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")

        result = InferenceRules.addition(p, q)
        expected = BinaryOp(left=p, right=q, operator="OR")

        self.assertEqual(result.left, expected.left)
        self.assertEqual(result.right, expected.right)
        self.assertEqual(result.operator, expected.operator)

    def test_biconditional_introduction(self):
        """Test Biconditional Introduction: (P → Q), (Q → P) ⊢ (P ↔ Q)."""
        p = Proposition(name="P")
        q = Proposition(name="Q")

        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")
        q_implies_p = BinaryOp(left=q, right=p, operator="IMPLIES")

        result = InferenceRules.biconditional_introduction(p_implies_q, q_implies_p)
        expected = BinaryOp(left=p, right=q, operator="IFF")

        self.assertEqual(result.left, expected.left)
        self.assertEqual(result.right, expected.right)
        self.assertEqual(result.operator, expected.operator)

        # Test error case with non-matching terms
        r = Proposition(name="R")
        q_implies_r = BinaryOp(left=q, right=r, operator="IMPLIES")

        with self.assertRaises(ValueError):
            InferenceRules.biconditional_introduction(p_implies_q, q_implies_r)
