#!/usr/bin/env python3
"""
Command-line interface for the agent-logic package.

This module provides a command-line interface for interacting with the agent-logic package,
including tools for validating proofs and other logical operations.

Usage:
    python -m agent_logic.cli --help
    python -m agent_logic.cli validate path/to/proof.json
    python -m agent_logic.cli --log-level DEBUG validate path/to/proof.json
"""

import argparse
import json
import logging
import sys

from agent_logic.proofs.proof_system import Proof
from agent_logic.utils.logger import set_global_log_level


def parse_args():
    """
    Parse command-line arguments.

    Returns:
        Parsed command-line arguments as an argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(description="Logic system command-line interface")

    # Global arguments
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set logging level",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (sets log level to DEBUG)",
    )

    # Main command subparsers
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Validate proof command
    validate_parser = subparsers.add_parser("validate", help="Validate a proof")
    validate_parser.add_argument("proof_file", type=str, help="Path to proof JSON file")

    return parser.parse_args()


def validate_proof(proof_file, debug=False):
    """
    Validate a proof from a JSON file.

    Loads a proof from a JSON file and checks if it is valid
    according to the specified inference rules.

    Args:
        proof_file: Path to the JSON file containing the proof.
        debug: Whether to enable debug mode in the proof validation.

    Returns:
        Exit code (0 for success, 1 for invalid proof, 2 for errors).

    Raises:
        FileNotFoundError: If the proof file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    try:
        with open(proof_file, "r") as f:
            data = json.load(f)

        # Create proof object
        proof = Proof.from_dict(data)

        # Set debug mode
        proof.debug = debug

        # Validate proof
        is_valid = proof.is_valid()

        if is_valid:
            print("✅ Proof is valid")
            return 0
        else:
            print("❌ Proof is invalid")
            return 1
    except Exception as e:
        print(f"Error validating proof: {e}")
        return 2


def main():
    """
    Main entry point for the CLI.

    Parses command-line arguments, sets up logging, and
    executes the appropriate command.

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    args = parse_args()

    # Set log level
    log_level = logging.DEBUG if args.debug else getattr(logging, args.log_level)
    set_global_log_level(log_level)

    if args.command == "validate":
        return validate_proof(args.proof_file, debug=args.debug)
    else:
        print("Please specify a command. Use --help for more information.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
