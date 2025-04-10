import subprocess
import os
import threading
from Library.FrameworkLogging import CustomLogger
from Library.FunctionLibrary import scan_for_video_files
from Library.Capture import capture_window_still  # Import the capture function
import time

def call_image_compare():
    """
    Calls the ImageCompare.py script after all videos have been processed.
    """
    try:
        # Path to the ImageCompare.py script
        image_compare_script = os.path.join(os.getcwd(), "Library", "ImageCompare.py")

        # Run the script using subprocess
        result = subprocess.run(["python", image_compare_script], capture_output=True, text=True)

        # Log the output and errors
        if result.returncode == 0:
            print("ImageCompare.py executed successfully.")
            print(result.stdout)
        else:
            print("Error occurred while executing ImageCompare.py.")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred while calling ImageCompare.py: {e}")

def start_vlc_with_options(file_path, no_video=False, grayscale=False, no_overlay=False, start_time=None, stop_time=None,
                           server_port=None, iface=None, iface_addr=None, mtu=None, ipv6=False, ipv4=False, max_screen=None):
    """
    Launches VLC Media Player with the specified options and plays the given file.
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
        if grayscale is not None:
            command.append("--grayscale")
        if no_overlay:
            command.append("--nooverlay")
        if start_time is not None:
            command.extend(["--start-time", str(start_time)])
        if stop_time is not None:
            command.extend(["--stop-time", str(stop_time)])
        if server_port is not None:
            command.extend(["--server-port", str(server_port)])
        if iface is not None:
            command.extend(["--iface", iface])
        if iface_addr is not None:
            command.extend(["--iface-addr", iface_addr])
        if mtu is not None:
            command.extend(["--mtu", str(mtu)])
        if ipv6:
            command.append("--ipv6")
        if ipv4:
            command.append("--ipv4")
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
        logger.debug(f"Error launching VLC Media Player: {e}")  # Log the error for debugging purposes
        return f"Error launching VLC Media Player: {e}"
    except Exception as e:
        logger.debug(f"An unexpected error occurred: {e}")  # Log any other unexpected errors
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
    LogFileName = "Logging_VLCTester.log"  # Initialize logging (optional, if you have FrameworkLogging set up)

    # Remove the old log file before starting a test run.
    if os.path.exists(LogFileName):
        os.remove(LogFileName)

    # Initialize the logger with a specific log file name
    logger = CustomLogger(LogFileName).get_logger()
    logger.debug("Old log file has been deleted.")
    logger.debug("Starting VLCTester script...")

    current_path = os.getcwd()
    # Path to the Media folder
    media_folder = os.path.join(current_path, "Media")  # Use os.path.join to construct the path
    logger.debug(f"Media folder set to: {media_folder}")

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

        videoNumber = 1
        # Play each video for 6 seconds
        for video_file in video_files:
            print(f"Playing video: {video_file}")
            logger.debug(f"Playing video {videoNumber}: {video_file}")
            videoNumber += 1

            # Construct the VLC window title dynamically
            window_title = f"{os.path.basename(video_file)} - VLC media player"

            # Construct the output image path
            output_image = os.path.join(media_folder, f"{os.path.basename(video_file)}_screenshot.jpg")

            # Capture the VLC window screenshot asynchronously
            capture_screenshot_async(window_title, output_image)

            # Start VLC and play the video
            result = start_vlc_with_options(
                file_path=video_file,
                no_video=False,
                grayscale=True,
                start_time=0,
                stop_time=6,  # Play for 6 seconds
                max_screen=True
               # Set to True if you want to test grayscale
            )

            print(result)

    #     # Call image ImageComare.py not that the screen shots have been captured.
    logger.debug("All videos have been processed, now calling ImageCompare.py...")
    call_image_compare()

