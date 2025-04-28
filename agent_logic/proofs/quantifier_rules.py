from agent_logic.core.functions import Relation
from agent_logic.core.quantifiers import ExistentialQuantifier, UniversalQuantifier


class QuantifierRules:
    """Inference rules for quantifiers (∀, ∃)."""

    @staticmethod
    def universal_elimination(
        quantifier: UniversalQuantifier, constant: str
    ) -> Relation:
        """
        ∀x P(x) ⊢ P(a)
        Replace variable x with constant a.
        """
        if isinstance(quantifier, UniversalQuantifier):
            new_predicate = quantifier.predicate.model_copy()
            new_predicate.parameters = [
                constant if p == quantifier.variable else p
                for p in new_predicate.parameters
            ]
            return new_predicate
        raise ValueError("Invalid application of Universal Elimination.")

    @staticmethod
    def existential_instantiation(
        quantifier: ExistentialQuantifier, constant: str
    ) -> Relation:
        """
        ∃x P(x) ⊢ P(a)
        Introduce a fresh constant.
        """
        if isinstance(quantifier, ExistentialQuantifier):
            new_predicate = quantifier.predicate.model_copy()
            new_predicate.parameters = [
                constant if p == quantifier.variable else p
                for p in new_predicate.parameters
            ]
            return new_predicate
        raise ValueError("Invalid application of Existential Instantiation.")

    @staticmethod
    def existential_generalization(
        predicate: Relation, variable: str
    ) -> ExistentialQuantifier:
        """
        P(a) ⊢ ∃x P(x)
        Replace a constant with a quantified variable.
        """
        if isinstance(predicate, Relation):
            new_predicate = predicate.model_copy()
            new_predicate.parameters = [
                variable if p not in predicate.parameters else p
                for p in new_predicate.parameters
            ]
            return ExistentialQuantifier(variable=variable, predicate=new_predicate)
        raise ValueError("Invalid application of Existential Generalization.")
