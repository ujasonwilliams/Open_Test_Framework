import subprocess
import os
import threading
from Library.FrameworkLogging import CustomLogger
from Library.FunctionLibrary import scan_for_video_files
from Library.Capture import capture_window_still  # Import the capture function
import time

def start_vlc_with_options(file_path, no_video=False, grayscale=False, no_overlay=False, start_time=None, stop_time=None,
                           server_port=None, iface=None, iface_addr=None, mtu=None, ipv6=False, ipv4=False, max_screen=None):
    """
    Launches VLC Media Player with the specified options and plays the given file.

    Note: The script requires you to not interact with the system otherqwise it may interfere with identifying the VLC window for screenshot capture.
    """
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            logger.debug(f"File '{file_path}' does not exist.")
            return f"Error: The file '{file_path}' does not exist."

        # Path to VLC executable (update this path if VLC is installed elsewhere)
        vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

        # Check if VLC is installed
        if not os.path.exists(vlc_path):
            logger.debug(f"VLC Media Player not found at '{vlc_path}'.")
            return "Error: VLC Media Player is not installed or the path is incorrect."

        # Build the VLC command
        command = [vlc_path, file_path]

        # Add optional parameters
        if no_video:
            command.append("--no-video")
        if grayscale:
            command.append("--grayscale")
        if no_overlay:
            command.append("--nooverlay")
        if start_time is not None:
            command.extend(["--start-time", str(start_time)])
        if stop_time is not None:
            command.extend(["--stop-time", str(stop_time)])
        if max_screen is not None:
            command.append("--fullscreen")

        # Launch VLC with the specified options
        logger.debug(f"Launching VLC with command: {' '.join(command)}")
        process = subprocess.Popen(command)

        # Wait for the video to finish playing
        if stop_time is not None:
            time_to_play = stop_time - (start_time or 0)
            print(f"Playing video '{file_path}' for {time_to_play} seconds...")
            logger.debug(f"Playing video '{file_path}' for {time_to_play} seconds...")
            time.sleep(time_to_play)  # Wait for the specified duration
        else:
            logger.debug(f"No stop time specified, waiting for the video to finish playing...")
            process.wait()

        # Terminate the VLC process
        process.terminate()
        process.wait()  # Ensure the process is fully terminated
        logger.debug(f"VLC Media Player finished playing file: {file_path}")
        return f"VLC Media Player finished playing file: {file_path}"
    except subprocess.CalledProcessError as e:
        logger.debug(f"Error launching VLC Media Player: {e}")
        return f"Error launching VLC Media Player: {e}"
    except Exception as e:
        logger.debug(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

def capture_screenshot_async(window_title, output_image):
    """
    Captures a screenshot asynchronously after 3 seconds.
    """
    def capture():
        time.sleep(5)  # Wait for 5 seconds
        capture_result = capture_window_still(window_title, output_image)
        logger.debug(capture_result)
        print(capture_result)

    # Start the capture in a separate thread
    threading.Thread(target=capture).start()

if __name__ == "__main__":
    LogFileName = "Logging_Training.log"  # Initialize logging (optional, if you have FrameworkLogging set up)

    # Remove the old log file before starting a test run.
    if os.path.exists(LogFileName):
        os.remove(LogFileName)

    # Initialize the logger with a specific log file name
    logger = CustomLogger(LogFileName).get_logger()
    logger.debug("Old log file has been deleted.")
    logger.debug("Starting Training script...")

    current_path = os.getcwd()
    # Path to the Media folder
    media_folder = os.path.join(current_path, "Media")  # Use os.path.join to construct the path
    logger.debug(f"Media folder set to: {media_folder}")

    # Path to the Golden Images folder under the Media folder
    golden_folder = os.path.join(media_folder, "Golden_Images")
    os.makedirs(golden_folder, exist_ok=True)
    logger.debug(f"Golden Images folder set to: {golden_folder}")

    # Get the list of video files
    video_files = scan_for_video_files(media_folder)

    # Print the log file names to the debug log for verification
    if video_files:
        logger.debug(f"Video files found: {video_files}")
    else:
        logger.debug("No video files found in the specified media folder.")

    # Check if any video files were found
    if not video_files:
        print(f"No video files found in the folder: {media_folder}")
        logger.warning(f"No video files found in the folder: {media_folder}")
    else:
        print(f"Found {len(video_files)} video files in the folder: {media_folder}")
        logger.debug(f"Found {len(video_files)} video files in the folder: {media_folder}")

        # Process each video file
        for video_file in video_files:
            print(f"Processing video: {video_file}")
            logger.debug(f"Processing video: {video_file}")

            # Extract the video name from the file path
            video_name = os.path.splitext(os.path.basename(video_file))[0]

            # Run the video once and capture a golden screenshot
            print(f"Playing video {video_name} to capture golden image")
            logger.debug(f"Playing video {video_name} to capture golden image")

            # Construct the VLC window title dynamically
            window_title = f"{os.path.basename(video_file)} - VLC media player"
            logger.debug(f"Looking for VLC title: {window_title}")  

            # Construct the golden image path
            golden_image_path = os.path.join(golden_folder, f"{video_name}_golden.jpg")
            logger.debug(f"Golden image path: {golden_image_path}")
         
            # Capture the VLC window screenshot asynchronously
            capture_screenshot_async(window_title, golden_image_path)

            # Start VLC and play the video
            result = start_vlc_with_options(
                file_path=video_file,
                no_video=False,
                grayscale=True,
                start_time=0,
                stop_time=6,  # Play for 6 seconds
                max_screen=True
            )

            print(result)