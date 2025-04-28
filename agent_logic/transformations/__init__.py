"""
Logical transformations module.

This module provides tools for logical formula transformations,
including normal forms and logical equivalences.
"""

from agent_logic.transformations.equivalences import EquivalenceRules
from agent_logic.transformations.normal_forms import (
    to_cnf,
    to_dnf
)

__all__ = [
    # Equivalence transformations
    "EquivalenceRules",
    
    # Normal forms
    "to_cnf",
    "to_dnf"
] 