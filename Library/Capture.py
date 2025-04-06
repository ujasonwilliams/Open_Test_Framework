import pygetwindow as gw
import pyautogui
from PIL import Image

def capture_window_still(window_title, output_file):
    """
    Image needs to be on the primary monitor for pyautogui to capture it properly.

    Captures a still image of a particular window and saves it as a .jpg file.

    Args:
        window_title (str): The title of the window to capture.
        output_file (str): The path to save the captured image (e.g., "output.jpg").

    Returns:
        str: Success message or error message if the window is not found.
    """
    try:
        # Debug: List all available windows
        all_windows = gw.getAllTitles()
        #print(f"Available windows: {all_windows}")

        # Find the window by title
        window = next((w for w in gw.getWindowsWithTitle(window_title) if w.title == window_title), None)
        if not window:
            return f"Error: Window with title '{window_title}' not found."

        # Activate the window to ensure it is in focus
        window.activate()

        # Get the window's bounding box
        bbox = (window.left, window.top, window.right, window.bottom)
       # print(f"Bounding box for window '{window_title}': {bbox}")  # Debugging log

        # Validate the bounding box dimensions
        if bbox[2] - bbox[0] <= 0 or bbox[3] - bbox[1] <= 0:
            return f"Error: Invalid bounding box dimensions for window '{window_title}': {bbox}"

        # Capture the screenshot using pyautogui
        screenshot = pyautogui.screenshot(region=bbox)

        # Save the screenshot as a .jpg file
        screenshot = screenshot.convert("RGB")  # Ensure the image is in RGB mode for JPEG
        screenshot.save(output_file, "JPEG")
        return f"Screenshot saved successfully to {output_file}."
    except Exception as e:
        return f"Error capturing window: {e}"

# if __name__ == "__main__":
#     # Test with Notepad
#     window_title = "*1 - Notepad"  # Example window title, change this to the actual window you want to capture
#     output_file = "screenshot.jpg"
#     result = capture_window_still(window_title, output_file)
#     print(result)