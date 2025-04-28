from typing import Dict, Optional

from agent_logic.core.functions import Relation


class Unification:
    """Handles unification for first-order logic terms."""

    @staticmethod
    def unify(term1: Relation, term2: Relation) -> Optional[Dict[str, str]]:
        """
        Unifies two predicates by finding a substitution θ such that term1(θ) = term2(θ).
        Example:
            P(x) and P(f(y)) → {x → f(y)}
        """
        if term1.name != term2.name or len(term1.parameters) != len(term2.parameters):
            return None  # Cannot unify if predicate names or arity differ

        substitution = {}
        for p1, p2 in zip(term1.parameters, term2.parameters, strict=False):
            if p1 == p2:
                continue  # Already matching
            elif p1.islower() and p2.isupper():  # Variable → Constant
                substitution[p1] = p2
            elif p1.isupper() and p2.islower():  # Constant → Variable
                substitution[p2] = p1
            else:
                return None  # Cannot unify

        return substitution
