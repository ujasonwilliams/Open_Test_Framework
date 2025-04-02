
import unittest
from unittest.mock import patch
from Library.FunctionLibrary import get_hostname

class TestFunctionLibrary(unittest.TestCase):
    @patch("socket.gethostname")
    def test_get_hostname(self, mock_gethostname):
        """
        Test that get_hostname returns a valid hostname.
        """
        # Mock the hostname to simulate a valid return value
        mock_gethostname.return_value = "TestMachine"

        # Call the function
        hostname = get_hostname()

        # Assert that the hostname is not null or empty
        self.assertIsNotNone(hostname, "The hostname should not be null.")
        self.assertNotEqual(hostname.strip(), "", "The hostname should not be empty.")

        # Assert that the hostname matches the mocked value
        self.assertEqual(hostname, "TestMachine", "The hostname does not match the expected value.")

if __name__ == "__main__":
    unittest.main()