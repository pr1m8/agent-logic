from logic.core.base import LogicalExpression
from logic.core.operations import Not, BinaryOp
from logic.core.base import LogicalExpression
from logic.core.operations import Not, BinaryOp
from typing import List
class InferenceRules:
    """Extends formal rules of inference for proofs with additional logical principles."""
    

    @staticmethod
    def modus_ponens(p: LogicalExpression, p_implies_q: LogicalExpression) -> LogicalExpression:
        """
        Modus Ponens: If P is true and (P → Q) is true, then Q must be true.
        P, (P → Q) ⊢ Q
        """
        if isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES":
            if p == p_implies_q.left:
                return p_implies_q.right  # Return Q
        raise ValueError("Invalid Modus Ponens application.")

    @staticmethod
    def modus_tollens(not_q: LogicalExpression, p_implies_q: LogicalExpression) -> LogicalExpression:
        """
        Modus Tollens: If ¬Q is true and (P → Q) is true, then ¬P must be true.
        ¬Q, (P → Q) ⊢ ¬P
        """
        if isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES":
            if isinstance(not_q, Not) and not_q.operand == p_implies_q.right:
                return Not(p_implies_q.left)  # Return ¬P
        raise ValueError("Invalid Modus Tollens application.")

    @staticmethod
    def hypothetical_syllogism(p_implies_q: LogicalExpression, q_implies_r: LogicalExpression) -> LogicalExpression:
        """
        Hypothetical Syllogism: If (P → Q) is true and (Q → R) is true, then (P → R) must be true.
        (P → Q), (Q → R) ⊢ (P → R)
        """
        if isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES":
            if isinstance(q_implies_r, BinaryOp) and q_implies_r.operator == "IMPLIES":
                if p_implies_q.right == q_implies_r.left:
                    return BinaryOp(p_implies_q.left, q_implies_r.right, "IMPLIES")  # Return (P → R)
        raise ValueError("Invalid Hypothetical Syllogism application.")

    @staticmethod
    def disjunctive_syllogism(p_or_q: LogicalExpression, not_p: LogicalExpression) -> LogicalExpression:
        """
        Disjunctive Syllogism: If (P ∨ Q) is true and ¬P is true, then Q must be true.
        (P ∨ Q), ¬P ⊢ Q
        """
        if isinstance(p_or_q, BinaryOp) and p_or_q.operator == "OR":
            if isinstance(not_p, Not):
                if not_p.operand == p_or_q.left:
                    return p_or_q.right  # Return Q
                elif not_p.operand == p_or_q.right:
                    return p_or_q.left  # Return P
        raise ValueError("Invalid Disjunctive Syllogism application.")

    @staticmethod
    def law_of_excluded_middle(p: LogicalExpression) -> BinaryOp:
        """
        Law of Excluded Middle: P ∨ ¬P is always true.
        ⊢ (P ∨ ¬P)
        """
        return BinaryOp(p, Not(p), "OR")

    @staticmethod
    def proof_by_contradiction(assumption: LogicalExpression, contradiction: LogicalExpression) -> Not:
        """
        Reductio ad Absurdum (Proof by Contradiction): If assuming P leads to ⊥, then ¬P must be true.
        P ⊢ ⊥ ⟹ ¬P
        """
        if contradiction is None:  # ⊥ is represented as None
            return Not(assumption)
        raise ValueError("Invalid Proof by Contradiction application.")

    @staticmethod
    def absorption(p: LogicalExpression, p_implies_q: LogicalExpression) -> LogicalExpression:
        """
        Absorption Rule: (P → Q) implies (P → (P ∧ Q)).
        P → Q ⊢ P → (P ∧ Q)
        """
        if isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES":
            return BinaryOp(p_implies_q.left, BinaryOp(p_implies_q.left, p_implies_q.right, "AND"), "IMPLIES")
        raise ValueError("Invalid Absorption Rule application.")

    @staticmethod
    def transitivity_of_implication(p_implies_q: LogicalExpression, q_implies_r: LogicalExpression) -> LogicalExpression:
        """
        Transitivity of Implication: If (P → Q) and (Q → R) hold, then (P → R) holds.
        (P → Q), (Q → R) ⊢ (P → R)
        """
        if isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES":
            if isinstance(q_implies_r, BinaryOp) and q_implies_r.operator == "IMPLIES":
                if p_implies_q.right == q_implies_r.left:
                    return BinaryOp(p_implies_q.left, q_implies_r.right, "IMPLIES")
        raise ValueError("Invalid Transitivity of Implication application.")

    @staticmethod
    def constructive_negation(p_implies_false: LogicalExpression) -> Not:
        """
        Constructive Negation: If (P → ⊥) is true, then ¬P must be true.
        (P → ⊥) ⊢ ¬P
        """
        if isinstance(p_implies_false, BinaryOp) and p_implies_false.operator == "IMPLIES":
            if p_implies_false.right is None:  # ⊥ is represented as None
                return Not(p_implies_false.left)
        raise ValueError("Invalid Constructive Negation application.")

    @staticmethod
    def distributive_rule(expression: LogicalExpression) -> LogicalExpression:
        """
        Distributive Law:
        (P ∧ (Q ∨ R)) ≡ ((P ∧ Q) ∨ (P ∧ R))
        (P ∨ (Q ∧ R)) ≡ ((P ∨ Q) ∧ (P ∨ R))
        """
        if isinstance(expression, BinaryOp):
            if expression.operator == "AND" and isinstance(expression.right, BinaryOp) and expression.right.operator == "OR":
                return BinaryOp(
                    BinaryOp(expression.left, expression.right.left, "AND"),
                    BinaryOp(expression.left, expression.right.right, "AND"),
                    "OR",
                )
            elif expression.operator == "OR" and isinstance(expression.right, BinaryOp) and expression.right.operator == "AND":
                return BinaryOp(
                    BinaryOp(expression.left, expression.right.left, "OR"),
                    BinaryOp(expression.left, expression.right.right, "OR"),
                    "AND",
                )
        return expression

    @staticmethod
    def associative_rule(expression: LogicalExpression) -> LogicalExpression:
        """
        Associative Law:
        (P ∨ (Q ∨ R)) ≡ ((P ∨ Q) ∨ R)
        (P ∧ (Q ∧ R)) ≡ ((P ∧ Q) ∧ R)
        """
        if isinstance(expression, BinaryOp):
            if expression.operator in {"AND", "OR"} and isinstance(expression.right, BinaryOp) and expression.right.operator == expression.operator:
                return BinaryOp(
                    BinaryOp(expression.left, expression.right.left, expression.operator),
                    expression.right.right,
                    expression.operator,
                )
        return expression

    @staticmethod
    def constructive_dilemma(p_implies_q: LogicalExpression, r_implies_s: LogicalExpression, p_or_r: LogicalExpression) -> LogicalExpression:
        """
        Constructive Dilemma: If (P → Q) is true, (R → S) is true, and (P ∨ R) is true, then (Q ∨ S) must be true.
        (P → Q), (R → S), (P ∨ R) ⊢ (Q ∨ S)
        """
        if (
            isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES" and
            isinstance(r_implies_s, BinaryOp) and r_implies_s.operator == "IMPLIES" and
            isinstance(p_or_r, BinaryOp) and p_or_r.operator == "OR"
        ):
            if p_or_r.left == p_implies_q.left and p_or_r.right == r_implies_s.left:
                return BinaryOp(p_implies_q.right, r_implies_s.right, "OR")  # Return (Q ∨ S)
        raise ValueError("Invalid Constructive Dilemma application.")

    @staticmethod
    def destructive_dilemma(p_implies_q: LogicalExpression, r_implies_s: LogicalExpression, not_q_or_not_s: LogicalExpression) -> LogicalExpression:
        """
        Destructive Dilemma: If (P → Q) is true, (R → S) is true, and (¬Q ∨ ¬S) is true, then (¬P ∨ ¬R) must be true.
        (P → Q), (R → S), (¬Q ∨ ¬S) ⊢ (¬P ∨ ¬R)
        """
        if (
            isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES" and
            isinstance(r_implies_s, BinaryOp) and r_implies_s.operator == "IMPLIES" and
            isinstance(not_q_or_not_s, BinaryOp) and not_q_or_not_s.operator == "OR"
        ):
            if isinstance(not_q_or_not_s.left, Not) and isinstance(not_q_or_not_s.right, Not):
                if not_q_or_not_s.left.operand == p_implies_q.right and not_q_or_not_s.right.operand == r_implies_s.right:
                    return BinaryOp(Not(p_implies_q.left), Not(r_implies_s.left), "OR")  # Return (¬P ∨ ¬R)
        raise ValueError("Invalid Destructive Dilemma application.")

    @staticmethod
    def conjunction_introduction(p: LogicalExpression, q: LogicalExpression) -> LogicalExpression:
        """
        Conjunction Introduction: If P is true and Q is true, then (P ∧ Q) is true.
        P, Q ⊢ (P ∧ Q)
        """
        return BinaryOp(p, q, "AND")

    @staticmethod
    def conjunction_elimination(p_and_q: LogicalExpression) -> List[LogicalExpression]:
        """
        Conjunction Elimination: If (P ∧ Q) is true, then P and Q must be true separately.
        (P ∧ Q) ⊢ P, Q
        """
        if isinstance(p_and_q, BinaryOp) and p_and_q.operator == "AND":
            return [p_and_q.left, p_and_q.right]
        raise ValueError("Invalid Conjunction Elimination application.")

    @staticmethod
    def addition(p: LogicalExpression, q: LogicalExpression) -> LogicalExpression:
        """
        Addition: If P is true, then (P ∨ Q) must be true.
        P ⊢ (P ∨ Q)
        """
        return BinaryOp(p, q, "OR")

    @staticmethod
    def biconditional_elimination(p_iff_q: LogicalExpression) -> List[LogicalExpression]:
        """
        Biconditional Elimination: If (P ↔ Q) is true, then (P → Q) and (Q → P) must be true.
        (P ↔ Q) ⊢ (P → Q), (Q → P)
        """
        if isinstance(p_iff_q, BinaryOp) and p_iff_q.operator == "IFF":
            return [
                BinaryOp(p_iff_q.left, p_iff_q.right, "IMPLIES"),
                BinaryOp(p_iff_q.right, p_iff_q.left, "IMPLIES"),
            ]
        raise ValueError("Invalid Biconditional Elimination application.")

    @staticmethod
    def biconditional_introduction(p_implies_q: LogicalExpression, q_implies_p: LogicalExpression) -> LogicalExpression:
        """
        Biconditional Introduction: If (P → Q) is true and (Q → P) is true, then (P ↔ Q) must be true.
        (P → Q), (Q → P) ⊢ (P ↔ Q)
        """
        if (
            isinstance(p_implies_q, BinaryOp) and p_implies_q.operator == "IMPLIES" and
            isinstance(q_implies_p, BinaryOp) and q_implies_p.operator == "IMPLIES"
        ):
            if p_implies_q.left == q_implies_p.right and p_implies_q.right == q_implies_p.left:
                return BinaryOp(p_implies_q.left, p_implies_q.right, "IFF")  # Return (P ↔ Q)
        raise ValueError("Invalid Biconditional Introduction application.")

    @staticmethod
    def negation_introduction(p_implies_false: LogicalExpression) -> LogicalExpression:
        """
        Negation Introduction: If (P → ⊥) is true, then ¬P must be true.
        (P → ⊥) ⊢ ¬P
        """
        if isinstance(p_implies_false, BinaryOp) and p_implies_false.operator == "IMPLIES":
            if p_implies_false.right is None:  # ⊥ is represented as None
                return Not(p_implies_false.left)
        raise ValueError("Invalid Negation Introduction application.")

    @staticmethod
    def negation_elimination(not_not_p: LogicalExpression) -> LogicalExpression:
        """
        Negation Elimination: If ¬(¬P) is true, then P must be true.
        ¬(¬P) ⊢ P
        """
        if isinstance(not_not_p, Not) and isinstance(not_not_p.operand, Not):
            return not_not_p.operand.operand
        raise ValueError("Invalid Negation Elimination application.")

