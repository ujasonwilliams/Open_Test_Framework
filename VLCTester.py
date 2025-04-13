import os
import subprocess
import threading
import time
from Library.FrameworkLogging import CustomLogger
from Library.FunctionLibrary import scan_for_video_files
from Library.Capture import capture_window_still  # Import the capture function

def call_image_compare():
    """
    Calls the ImageCompare.py script after all videos have been processed.
    """
    try:
        # Path to the ImageCompare.py script
        image_compare_script = os.path.join(os.getcwd(), "Library", "ImageCompare.py")
        logger.debug(f"ImageCompare script path: {image_compare_script}")

        # Run the script using subprocess
        result = subprocess.run(["python", image_compare_script], capture_output=True, text=True)

        # Log the output and errors
        if result.returncode == 0:
            logger.debug("ImageCompare.py executed successfully.")
            logger.debug(f"ImageCompare.py output: {result.stdout}")
        else:
            logger.error("Error occurred while executing ImageCompare.py.")
            logger.error(f"ImageCompare.py error: {result.stderr}")
    except Exception as e:
        logger.error(f"An error occurred while calling ImageCompare.py: {e}")

def start_vlc_with_options(file_path, no_video=False, grayscale=False, no_overlay=False, start_time=None, stop_time=None,
                           server_port=None, iface=None, iface_addr=None, mtu=None, ipv6=False, ipv4=False, max_screen=None):
    """
    Launches VLC Media Player with the specified options and plays the given file.
    """
    try:
        logger.debug(f"Starting VLC with file: {file_path}")
        logger.debug(f"Options - no_video: {no_video}, grayscale: {grayscale}, no_overlay: {no_overlay}, "
                     f"start_time: {start_time}, stop_time: {stop_time}, server_port: {server_port}, "
                     f"iface: {iface}, iface_addr: {iface_addr}, mtu: {mtu}, ipv6: {ipv6}, ipv4: {ipv4}, max_screen: {max_screen}")

        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File '{file_path}' does not exist.")
            return f"Error: The file '{file_path}' does not exist."

        # Path to VLC executable (update this path if VLC is installed elsewhere)
        vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
        logger.debug(f"VLC executable path: {vlc_path}")

        # Check if VLC is installed
        if not os.path.exists(vlc_path):
            logger.error(f"VLC Media Player not found at '{vlc_path}'.")
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
        if max_screen:
            command.append("--fullscreen")

        logger.debug(f"VLC command: {' '.join(command)}")

        # Launch VLC with the specified options
        process = subprocess.Popen(command)

        # Wait for the video to finish playing
        if stop_time is not None:
            time_to_play = stop_time - (start_time or 0)
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
        logger.error(f"Error launching VLC Media Player: {e}")
        return f"Error launching VLC Media Player: {e}"
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred: {e}"

def capture_screenshot_async(window_title, output_image):
    """
    Captures a screenshot asynchronously after 3 seconds.
    """
    logger.debug(f"Preparing to capture screenshot for window: {window_title}, output image: {output_image}")

    def capture():
        time.sleep(5)  # Wait for 5 seconds
        capture_result = capture_window_still(window_title, output_image)
        logger.debug(f"Screenshot capture result: {capture_result}")
        print(capture_result)

    # Start the capture in a separate thread
    threading.Thread(target=capture).start()
if __name__ == "__main__":
    LogFileName = "Logging_VLCTester.log"

    # Remove the old log file before starting a test run.
    if os.path.exists(LogFileName):
        os.remove(LogFileName)

    # Initialize the logger with a specific log file name
    logger = CustomLogger(LogFileName).get_logger()
    logger.debug("Old log file has been deleted.")
    logger.debug("Starting VLCTester script...")

    current_path = os.getcwd()
    logger.debug(f"Current working directory: {current_path}")

    # Path to the Media folder
    media_folder = os.path.join(current_path, "Media")
    logger.debug(f"Media folder set to: {media_folder}")

    # Get the list of video files
    video_files = scan_for_video_files(media_folder)
    logger.debug(f"Video files found: {video_files}")

    if not video_files:
        logger.warning(f"No video files found in the folder: {media_folder}")
    else:
        logger.debug(f"Found {len(video_files)} video files in the folder: {media_folder}")

        # Specify the number of test loops
        test_loops = 3  # Change this value to specify the number of loops
        logger.debug(f"Running tests for {test_loops} loops.")

        for loop in range(1, test_loops + 1):
            logger.debug(f"Starting test loop {loop} of {test_loops}.")

            videoNumber = 1
            for video_file in video_files:
                logger.debug(f"Processing video {videoNumber} in loop {loop}: {video_file}")
                videoNumber += 1

                # Use the consistent naming convention for screenshots
                output_image = os.path.join(media_folder, f"{os.path.splitext(os.path.basename(video_file))[0]}.jpg")
                logger.debug(f"Output image path: {output_image}")

                # Capture screenshot for the current loop
                capture_screenshot_async(f"{os.path.basename(video_file)} - VLC media player", output_image)

                # Start VLC and play the video
                result = start_vlc_with_options(
                    file_path=video_file,
                    no_video=False,
                    grayscale=True,
                    start_time=0,
                    stop_time=6,
                    max_screen=True
                )
                logger.debug(f"VLC result: {result}")

            logger.debug(f"Test loop {loop} completed.")

            # Evaluate results after each loop
            logger.debug("Calling ImageCompare.py to evaluate results...")
            call_image_compare()

    logger.debug("All test loops have been processed.")