from FunctionLibrary import set_sleep_time
import subprocess
import os

def start_video(file_path):
    """
    Opens VLC Media Player and plays the specified file.
    Args:
        file_path (str): The path to the media file to be played.
    Returns:
        str: Success message if VLC is launched successfully, or an error message if it fails.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            return f"Error: The file '{file_path}' does not exist."

        # Path to VLC executable (update this path if VLC is installed elsewhere)
        vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

        # Check if VLC is installed
        if not os.path.exists(vlc_path):
            return "Error: VLC Media Player is not installed or the path is incorrect."

        # Launch VLC with the specified file
        subprocess.run([vlc_path, file_path], check=True)
        return f"VLC Media Player launched successfully with file: {file_path}"
    except subprocess.CalledProcessError as e:
        return f"Error launching VLC Media Player: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage
if __name__ == "__main__":
    # media_file = r"C:\Users\jason\Videos\Margin Call.mp4"  # Replace with the path to your media file
    # result = start_video(media_file)
    # print(result)
    set_sleep_time(1)  # Set the system to never sleep before launching VLC