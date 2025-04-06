import unittest
from unittest.mock import patch, MagicMock
from Library.Capture import capture_window_still

class TestCaptureWindowStill(unittest.TestCase):
    @patch("Library.Capture.gw.getWindowsWithTitle")
    @patch("Library.Capture.pyautogui.screenshot")  # Mock pyautogui.screenshot instead of ImageGrab.grab
    def test_capture_window_still_success(self, mock_screenshot, mock_get_windows):
        """
        Test that capture_window_still successfully captures a Notepad window and saves a screenshot.
        """
        # Mock the Notepad window object
        mock_window = MagicMock()
        mock_window.title = "Untitled - Notepad"
        mock_window.left = 0
        mock_window.top = 0
        mock_window.right = 800
        mock_window.bottom = 600
        mock_get_windows.return_value = [mock_window]

        # Mock the screenshot
        mock_image = MagicMock()
        mock_image.convert.return_value = mock_image  # Ensure convert() returns the same mock object
        mock_screenshot.return_value = mock_image

        # Call the function
        result = capture_window_still("Untitled - Notepad", "output.jpg")

        # Assertions
        self.assertEqual(result, "Screenshot saved successfully to output.jpg.")
        mock_get_windows.assert_called_once_with("Untitled - Notepad")
        mock_screenshot.assert_called_once_with(region=(0, 0, 800, 600))
        mock_image.convert.assert_called_once_with("RGB")
        mock_image.save.assert_called_once_with("output.jpg", "JPEG")

if __name__ == "__main__":
    unittest.main()