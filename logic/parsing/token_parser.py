import re
from typing import List


class Tokenizer:
    """Lexical analyzer for tokenizing logical expressions."""

    TOKEN_MAP = {
        "AND": r"\∧|\bAND\b",
        "OR": r"\∨|\bOR\b",
        "IMPLIES": r"→|\bIMPLIES\b",
        "IFF": r"↔|\bIFF\b",
        "NOT": r"¬|\bNOT\b",
        "FORALL": r"∀|\bFORALL\b",
        "EXISTS": r"∃|\bEXISTS\b",
        "LPAREN": r"\(",
        "RPAREN": r"\)",
        "VAR": r"[a-zA-Z][a-zA-Z0-9_]*",
    }

    @staticmethod
    def tokenize(expression: str) -> List[str]:
        """Tokenizes a logical expression into components."""
        token_regex = "|".join(
            f"(?P<{key}>{value})" for key, value in Tokenizer.TOKEN_MAP.items()
        )
        tokens = []
        for match in re.finditer(token_regex, expression):
            tokens.append((match.lastgroup, match.group()))
        return tokens

    @staticmethod
    def validate_syntax(tokens: List[str]) -> bool:
        """Performs basic syntax validation."""
        if not tokens:
            return False
        balance = 0  # Track parenthesis balance
        last_token = None
        for token_type, _token_value in tokens:
            if token_type == "LPAREN":
                balance += 1
            elif token_type == "RPAREN":
                balance -= 1
                if balance < 0:
                    return False
            if (
                last_token and last_token == token_type
            ):  # No two same token types in sequence (except VAR)
                return False
            last_token = token_type
        return balance == 0  # Ensure all parentheses are closed
