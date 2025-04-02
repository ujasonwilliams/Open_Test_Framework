import unittest
import subprocess
from unittest.mock import patch, MagicMock
from Library.FunctionLibrary import generate_system_report
import os

class TestFunctionLibrary(unittest.TestCase):
    @patch("subprocess.run")
    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_generate_system_report_success(self, mock_exists, mock_makedirs, mock_subprocess_run):
        """
        Test that generate_system_report successfully generates a report.
        """
        # Mock os.path.exists to simulate the directory already exists
        mock_exists.return_value = True

        # Mock subprocess.run to simulate successful execution of the msinfo32 command
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        # Call the function
        file_path = "C:\\Users\\jason\\Desktop\\SystemReport.nfo"
        result = generate_system_report(file_path)

        # Assert that subprocess.run was called with the correct arguments
        mock_subprocess_run.assert_called_once_with(["msinfo32", "/report", file_path], check=True)

        # Assert that the function returns the expected success message
        self.assertEqual(result, f"System information report successfully generated at: {file_path}")

    @patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "msinfo32"))
    def test_generate_system_report_failure(self, mock_subprocess_run):
        """
        Test that generate_system_report handles subprocess errors correctly.
        """
        # Call the function
        file_path = "C:\\Users\\jason\\Desktop\\SystemReport.nfo"
        result = generate_system_report(file_path)

        # Assert that the function returns the expected error message
        self.assertIn("Error generating system information report", result)

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_generate_system_report_create_directory(self, mock_exists, mock_makedirs):
        """
        Test that generate_system_report creates the directory if it does not exist.
        """
        # Mock os.path.exists to simulate the directory does not exist
        mock_exists.return_value = False

        # Call the function
        file_path = "C:\\Users\\jason\\Desktop\\SystemReport.nfo"
        with patch("subprocess.run") as mock_subprocess_run:
            mock_subprocess_run.return_value = MagicMock(returncode=0)
            result = generate_system_report(file_path)

        # Assert that os.makedirs was called to create the directory
        mock_makedirs.assert_called_once_with(os.path.dirname(file_path))

        # Assert that the function returns the expected success message
        self.assertEqual(result, f"System information report successfully generated at: {file_path}")

if __name__ == "__main__":
    unittest.main()