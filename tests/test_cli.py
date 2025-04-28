import json
import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from agent_logic.cli import main, validate_proof
from agent_logic.core.operations import BinaryOp, Proposition
from agent_logic.proofs.proof_system import Proof, ProofStep


class TestCLI(unittest.TestCase):

    def test_validate_proof_valid(self):
        """Test validating a valid proof file."""
        # Create a valid proof
        p = Proposition(name="P")
        q = Proposition(name="Q")
        p_implies_q = BinaryOp(left=p, right=q, operator="IMPLIES")

        steps = [
            ProofStep(step_number=1, statement=p, justification="Given"),
            ProofStep(step_number=2, statement=p_implies_q, justification="Given"),
            ProofStep(
                step_number=3,
                statement=q,
                justification="Modus Ponens",
                dependencies=[1, 2],
            ),
        ]

        proof = Proof(steps=steps)

        # Get the dict directly using model_dump with custom handling
        proof_dict = {"steps": []}
        for step in proof.steps:
            step_dict = step.model_dump()
            step_dict["statement"] = step.statement.to_dict()
            proof_dict["steps"].append(step_dict)

        # Write to a temporary file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            json.dump(proof_dict, temp_file)
            temp_file_path = temp_file.name

        try:
            # Test the validate_proof function with proper error handling
            with patch("builtins.print"):  # Suppress print output
                result = validate_proof(temp_file_path, debug=False)
                self.assertEqual(result, 0)  # Success
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_validate_proof_invalid(self):
        """Test validating an invalid proof file."""
        # Create an invalid proof
        p = Proposition(name="P")
        r = Proposition(name="R")  # Unrelated proposition

        steps = [
            ProofStep(step_number=1, statement=p, justification="Given"),
            ProofStep(
                step_number=2,
                statement=r,  # This doesn't follow from p
                justification="Modus Ponens",
                dependencies=[1],
            ),
        ]

        proof = Proof(steps=steps)

        # Get the dict directly using model_dump with custom handling
        proof_dict = {"steps": []}
        for step in proof.steps:
            step_dict = step.model_dump()
            step_dict["statement"] = step.statement.to_dict()
            proof_dict["steps"].append(step_dict)

        # Write to a temporary file
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
            json.dump(proof_dict, temp_file)
            temp_file_path = temp_file.name

        try:
            # Test the validate_proof function with proper error handling
            with patch("builtins.print"):  # Suppress print output
                result = validate_proof(temp_file_path, debug=False)
                self.assertEqual(result, 1)  # Failure
        finally:
            # Clean up
            os.unlink(temp_file_path)

    def test_validate_proof_error(self):
        """Test error handling with a non-existent file."""
        # Use a path that doesn't exist
        non_existent_path = "/path/to/nonexistent/file.json"

        # Test the validate_proof function
        result = validate_proof(non_existent_path, debug=False)
        self.assertEqual(result, 2)  # Error

    def test_cli_help(self):
        """Test CLI help command."""
        with patch("sys.argv", ["logic.cli", "--help"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                with self.assertRaises(SystemExit) as context:
                    main()

                # Help should exit with code 0
                self.assertEqual(context.exception.code, 0)

                # Check that help output contains expected content
                output = mock_stdout.getvalue()
                self.assertIn("usage:", output)
                self.assertIn("validate", output)

    @patch("logic.cli.validate_proof")
    def test_cli_validate_command(self, mock_validate):
        """Test the 'validate' command in the CLI."""
        mock_validate.return_value = 0  # Simulate success

        with patch("sys.argv", ["logic.cli", "validate", "test.json"]):
            result = main()

            # Check that validate_proof was called with the correct arguments
            mock_validate.assert_called_once_with("test.json", debug=False)
            self.assertEqual(result, 0)

    @patch("logic.cli.validate_proof")
    def test_cli_validate_with_debug(self, mock_validate):
        """Test the 'validate' command with debug flag."""
        mock_validate.return_value = 0  # Simulate success

        with patch("sys.argv", ["logic.cli", "--debug", "validate", "test.json"]):
            result = main()

            # Check that validate_proof was called with debug=True
            mock_validate.assert_called_once_with("test.json", debug=True)
            self.assertEqual(result, 0)

    def test_cli_no_command(self):
        """Test CLI with no command."""
        with patch("sys.argv", ["logic.cli"]):
            with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
                result = main()

                # Should return an error code
                self.assertEqual(result, 1)

                # Check error message
                output = mock_stdout.getvalue()
                self.assertIn("Please specify a command", output)
