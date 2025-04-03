import subprocess
import os

def start_vlc_with_options(file_path, no_video=False, grayscale=False, no_overlay=False, start_time=None, stop_time=None,
                           server_port=None, iface=None, iface_addr=None, mtu=None, ipv6=False, ipv4=False):
    """
    Launches VLC Media Player with the specified options and plays the given file.
    
    Args:
        file_path (str): The path to the media file to be played.
        no_video (bool): Disable video output.
        grayscale (bool): Enable grayscale video output.
        no_overlay (bool): Disable overlay.
        start_time (int): Start time in seconds.
        stop_time (int): Stop time in seconds.
        server_port (int): Server port for streaming.
        iface (str): Network interface to use.
        iface_addr (str): Network interface address.
        mtu (int): Maximum Transmission Unit for streaming.
        ipv6 (bool): Enable IPv6.
        ipv4 (bool): Enable IPv4.
    
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

        # Launch VLC with the specified options
        subprocess.run(command, check=True)
        return f"VLC Media Player launched successfully with file: {file_path} and options: {command[1:]}"
    except subprocess.CalledProcessError as e:
        return f"Error launching VLC Media Player: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Example usage
if __name__ == "__main__":
    media_file = r"C:\Users\jason\Videos\example.mp4"  # Replace with the path to your media file
    result = start_vlc_with_options(
        file_path=media_file,
        no_video=True,
        grayscale=True,
        start_time=10,
        stop_time=60,
        server_port=8080,
        iface="eth0",
        iface_addr="192.168.1.1",
        mtu=1500,
        ipv4=True
    )
    print(result)



#     To enable streaming with VLC Media Player, follow these steps:

# Open VLC Media Player: Launch VLC on your computer.
# Select Media: Click on the "Media" menu and choose "Stream".
# Open Media: In the Open Media dialog, select the media you want to stream. This can be a file, disc, or even a capture device like your desktop or webcam.
# Stream Output: Click the "Stream" button. The Stream Output window will appear.
# Destination Setup: Choose a destination for your stream. You can select HTTP, UDP, or other options. Click "Add" after selecting your destination.
# Configure Settings: Customize the settings for your chosen destination. You can tweak transcoding settings to manage bandwidth.
# Start Streaming: Click "Stream" to start broadcasting. If you selected "Display locally", the media will play on your local computer as well.
# To connect to the stream from another device:

# Open VLC: On the other device, open VLC Media Player.
# Open Network Stream: Click on the "Media" menu and select "Open Network Stream".
# Enter Stream URL: Enter the URL of the stream (e.g., http://IP.Address:8080).
# For more detailed instructions, you can check out this guide1.

