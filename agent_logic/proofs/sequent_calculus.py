from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel

from agent_logic.core.base import LogicalExpression
from agent_logic.core.operations import BinaryOp, Not


class Sequent(BaseModel):
    """
    Represents a sequent in sequent calculus:
    Γ ⊢ Δ (Hypotheses imply conclusions)
    """

    hypotheses: List[LogicalExpression]
    conclusions: List[LogicalExpression]

    def __str__(self):
        hyp_str = ", ".join(str(h) for h in self.hypotheses)
        concl_str = ", ".join(str(c) for c in self.conclusions)
        return f"{hyp_str} ⊢ {concl_str}"


class SequentCalculus:
    """Implements sequent calculus inference rules for formal proofs."""

    @staticmethod
    def and_left(seq: Sequent) -> List[Sequent]:
        """
        ∧-Left Rule:
        If (A ∧ B) appears in the hypotheses, split into two sequents:
        (A ∧ B), Γ ⊢ Δ  ⟹  (A, B, Γ ⊢ Δ)
        """
        new_sequents = []
        for hyp in seq.hypotheses:
            if isinstance(hyp, BinaryOp) and hyp.operator == "AND":
                new_hypotheses = seq.hypotheses.copy()
                new_hypotheses.remove(hyp)
                new_hypotheses.extend([hyp.left, hyp.right])
                new_sequents.append(
                    Sequent(hypotheses=new_hypotheses, conclusions=seq.conclusions)
                )
        return new_sequents if new_sequents else [seq]

    @staticmethod
    def and_right(seq: Sequent) -> Optional[Sequent]:
        """
        ∧-Right Rule:
        If both A and B appear in the conclusions, merge them into (A ∧ B):
        Γ ⊢ A, B  ⟹  Γ ⊢ (A ∧ B)
        """
        if len(seq.conclusions) >= 2:
            new_conclusions = seq.conclusions.copy()
            a, b = new_conclusions.pop(0), new_conclusions.pop(0)
            new_conclusions.insert(0, BinaryOp(a, b, "AND"))
            return Sequent(hypotheses=seq.hypotheses, conclusions=new_conclusions)
        return None

    @staticmethod
    def or_left(seq: Sequent) -> List[Sequent]:
        """
        ∨-Left Rule:
        If (A ∨ B) is in the hypotheses, generate two cases:
        (A ∨ B), Γ ⊢ Δ  ⟹  (A, Γ ⊢ Δ)  and  (B, Γ ⊢ Δ)
        """
        new_sequents = []
        for hyp in seq.hypotheses:
            if isinstance(hyp, BinaryOp) and hyp.operator == "OR":
                new_hyp1 = seq.hypotheses.copy()
                new_hyp2 = seq.hypotheses.copy()
                new_hyp1.remove(hyp)
                new_hyp2.remove(hyp)
                new_hyp1.append(hyp.left)
                new_hyp2.append(hyp.right)
                new_sequents.append(
                    Sequent(hypotheses=new_hyp1, conclusions=seq.conclusions)
                )
                new_sequents.append(
                    Sequent(hypotheses=new_hyp2, conclusions=seq.conclusions)
                )
        return new_sequents if new_sequents else [seq]

    @staticmethod
    def or_right(seq: Sequent) -> Optional[Sequent]:
        """
        ∨-Right Rule:
        If A is in the conclusions, we can infer (A ∨ B):
        Γ ⊢ A  ⟹  Γ ⊢ (A ∨ B)
        """
        if len(seq.conclusions) >= 1:
            new_conclusions = seq.conclusions.copy()
            a = new_conclusions.pop(0)
            new_conclusions.insert(0, BinaryOp(a, a, "OR"))
            return Sequent(hypotheses=seq.hypotheses, conclusions=new_conclusions)
        return None

    @staticmethod
    def implies_left(seq: Sequent) -> Optional[Sequent]:
        """
        →-Left Rule:
        If (A → B) is in the hypotheses, transform into two sequents:
        (A → B), Γ ⊢ Δ  ⟹  (Γ ⊢ A)  and  (B, Γ ⊢ Δ)
        """
        new_sequents = []
        for hyp in seq.hypotheses:
            if isinstance(hyp, BinaryOp) and hyp.operator == "IMPLIES":
                new_hyp = seq.hypotheses.copy()
                new_hyp.remove(hyp)
                new_sequents.append(Sequent(hypotheses=new_hyp, conclusions=[hyp.left]))
                new_sequents.append(
                    Sequent(
                        hypotheses=[hyp.right] + new_hyp, conclusions=seq.conclusions
                    )
                )
                return new_sequents
        return [seq]

    @staticmethod
    def implies_right(seq: Sequent) -> Optional[Sequent]:
        """
        →-Right Rule:
        If B appears in the conclusions, infer (A → B):
        Γ, A ⊢ B  ⟹  Γ ⊢ (A → B)
        """
        if len(seq.conclusions) >= 1:
            new_conclusions = seq.conclusions.copy()
            a, b = seq.hypotheses[0], new_conclusions.pop(0)
            new_conclusions.insert(0, BinaryOp(a, b, "IMPLIES"))
            return Sequent(hypotheses=seq.hypotheses, conclusions=new_conclusions)
        return None

    @staticmethod
    def not_left(seq: Sequent) -> Optional[Sequent]:
        """
        ¬-Left Rule:
        If ¬A is in the hypotheses, transform into:
        (¬A), Γ ⊢ Δ  ⟹  Γ ⊢ A, Δ
        """
        for hyp in seq.hypotheses:
            if isinstance(hyp, Not):
                new_hypotheses = seq.hypotheses.copy()
                new_hypotheses.remove(hyp)
                new_conclusions = seq.conclusions.copy()
                new_conclusions.append(hyp.operand)
                return Sequent(hypotheses=new_hypotheses, conclusions=new_conclusions)
        return None

    @staticmethod
    def not_right(seq: Sequent) -> Optional[Sequent]:
        """
        ¬-Right Rule:
        If A is in the conclusions, infer ¬A:
        Γ ⊢ A  ⟹  Γ, ¬A ⊢ ⊥
        """
        if len(seq.conclusions) >= 1:
            new_conclusions = seq.conclusions.copy()
            a = new_conclusions.pop(0)
            return Sequent(
                hypotheses=seq.hypotheses + [Not(a)], conclusions=[None]
            )  # ⊥ represented as None
        return None
