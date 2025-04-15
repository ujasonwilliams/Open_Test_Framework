import os
import requests

def download_vlc_installer(download_url, save_path):
    """
    Downloads the VLC installer from the specified URL and saves it to the given path.

    :param download_url: The URL to download the VLC installer.
    :param save_path: The local path to save the downloaded installer.
    """
    try:
        print(f"Downloading VLC installer from {download_url}...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise an error for HTTP issues

        # Save the installer to the specified path
        with open(save_path, "wb") as installer_file:
            for chunk in response.iter_content(chunk_size=8192):
                installer_file.write(chunk)

        print(f"VLC installer downloaded successfully to {save_path}.")
    except requests.RequestException as e:
        print(f"Failed to download VLC installer: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # URL to download the VLC installer
    vlc_download_url = "https://get.videolan.org/vlc/3.0.21/win32/vlc-3.0.21-win32.exe"

    # Path to save the downloaded installer
    vlc_installer_path = os.path.join(os.getcwd(), "vlc-3.0.21-win32.exe")

    # Download the VLC installer
    download_vlc_installer(vlc_download_url, vlc_installer_path)