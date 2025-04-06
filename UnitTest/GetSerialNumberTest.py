from unittest.mock import patch, MagicMock
from Library.FunctionLibrary import get_bios_serial_number
import unittest
import time

class TestFunctionLibrary(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_bios_serial_number(self, mock_subprocess_run):
        """
        Test that get_bios_serial_number returns a non-null value within 1000ms.
        """
        # Mock the subprocess.run to simulate WMIC command output
        mock_result = MagicMock()
        mock_result.stdout = "SerialNumber\nABC123XYZ\n"
        mock_result.returncode = 0
        mock_subprocess_run.return_value = mock_result

        # Start the timer
        start_time = time.time()

        # Call the function
        serial_number = get_bios_serial_number()

        # End the timer
        end_time = time.time()

        # Assert that the serial number is not null
        self.assertIsNotNone(serial_number, "The BIOS serial number should not be null.")
        self.assertNotEqual(serial_number.strip(), "", "The BIOS serial number should not be empty.")

        # Assert that the function completes within 1000ms
        elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
        self.assertLessEqual(elapsed_time, 1000, f"The function took too long to execute: {elapsed_time}ms")

        # Assert that the serial number matches the mocked value
        self.assertEqual(serial_number, "ABC123XYZ", "The BIOS serial number does not match the expected value.")

if __name__ == "__main__":
    unittest.main()
