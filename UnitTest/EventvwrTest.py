import unittest
from unittest.mock import patch, mock_open
from Library.FunctionLibrary import get_event_log_data
import xml.etree.ElementTree as ET

class TestFunctionLibrary(unittest.TestCase):
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="<root><event>Test Event</event></root>")
    def test_get_event_log_data_valid_file(self, mock_file, mock_exists):
        """
        Test that get_event_log_data successfully parses a valid XML file.
        """
        mock_exists.return_value = True  # Simulate that the file exists

        # Call the function
        result = get_event_log_data("valid_file.xml")

        # Assert that the result is a dictionary containing the parsed XML data
        self.assertIsInstance(result, dict, "The result should be a dictionary.")
        self.assertIn("root", result, "The result dictionary should contain the 'root' key.")
        self.assertIsInstance(result["root"], ET.Element, "The 'root' key should contain an XML Element.")

    @patch("os.path.exists")
    def test_get_event_log_data_file_not_found(self, mock_exists):
        """
        Test that get_event_log_data returns an error message when the file does not exist.
        """
        mock_exists.return_value = False  # Simulate that the file does not exist

        # Call the function
        result = get_event_log_data("nonexistent_file.xml")

        # Assert that the result is an error message
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertEqual(result, "Error: nonexistent_file.xml not found.", "The error message is incorrect.")

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open, read_data="<root><event>Test Event</event>")
    def test_get_event_log_data_invalid_xml(self, mock_file, mock_exists):
        """
        Test that get_event_log_data returns an error message when the XML file is invalid.
        """
        mock_exists.return_value = True  # Simulate that the file exists

        # Call the function
        result = get_event_log_data("invalid_file.xml")

        # Assert that the result is an error message
        self.assertIsInstance(result, str, "The result should be a string.")
        self.assertEqual(result, "Error: Failed to parse invalid_file.xml.", "The error message is incorrect.")

if __name__ == "__main__":
    unittest.main()