import xml.etree.ElementTree as ET
import subprocess
import time
import socket
import os

def set_sleep_time(timeBeforeSleep):
    # Keep a Windows system awake for testing. 
    # Disable timeouts for AC (plugged-in) mode
    subprocess.run(["powercfg", "-change", "-monitor-timeout-ac", str(timeBeforeSleep)]) # Set monitor timeout for AC mode
    subprocess.run(["powercfg", "-change", "-standby-timeout-ac",  str(timeBeforeSleep)])
    subprocess.run(["powercfg", "-change", "-hibernate-timeout-ac",  str(timeBeforeSleep)])
    
    # Disable timeouts for DC (battery) mode
    subprocess.run(["powercfg", "-change", "-monitor-timeout-dc",  str(timeBeforeSleep)])
    subprocess.run(["powercfg", "-change", "-standby-timeout-dc",  str(timeBeforeSleep)])
    subprocess.run(["powercfg", "-change", "-hibernate-timeout-dc",  str(timeBeforeSleep)])

def get_test_suite_version(file_path="Version.txt"):
    # Open a version file from the specified path and return the version number.
    try:
        with open(file_path, "r") as file:
            version = file.readline().strip()
        return version
    except FileNotFoundError:
        return "Version file not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_bios_serial_number():
    """
    Retrieves the BIOS serial number of the device.
    Returns:
        str: The BIOS serial number.
    """
    bios_serial_number = ""

    while not bios_serial_number:
        try:
            # Use WMIC (Windows Management Instrumentation Command-line) to query the BIOS serial number
            result = subprocess.run(
                ["wmic", "bios", "get", "serialnumber"],
                capture_output=True,
                text=True,
                check=True
            )
            # Extract the serial number from the output
            output_lines = result.stdout.strip().split("\n")
            if len(output_lines) > 1:
                bios_serial_number = output_lines[1].strip()
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving BIOS serial number: {e}")
        
        # Wait for 500 milliseconds before retrying
        time.sleep(0.5)

    return bios_serial_number

def get_hostname():
    """
    Retrieves the hostname of the current machine.
    Returns:
        str: The hostname of the machine.
    """
    hostname = socket.gethostname()
    return hostname

def get_event_log_data(xml_file):
    """
    Gathers event log data from an XML file.
    Args:
        xml_file (str): The path to the XML file.
    Returns:
        dict: A dictionary containing the parsed XML data if successful.
        str: An error message if the file does not exist or cannot be read.
    """
    def write_log(message):
        """Logs a message to the console."""
        print(message)

    write_log(f"Gathering EventLogData. Using pattern file: {xml_file}")

    # Check if the XML file exists
    if not os.path.exists(xml_file):
        write_log(f"{xml_file} not found, exiting.")
        return f"Error: {xml_file} not found."

    try:
        # Read and parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        write_log(f"Successfully read contents of {xml_file}")
        return {"root": root, "tree": tree}
    except ET.ParseError:
        write_log(f"Failed to read contents of {xml_file}")
        return f"Error: Failed to parse {xml_file}."
    except Exception as e:
        write_log(f"An unexpected error occurred: {e}")
        return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    xml_file_path = "example.xml"
    result = get_event_log_data(xml_file_path)
    if isinstance(result, dict):
        print("XML data successfully parsed.")
    else:
        print(result)

def generate_system_report(file_path):
    """
    Generates a system information report using the msinfo32 command.
    Args:
        file_path (str): The path where the report will be saved.
    Returns:
        str: Success message if the report is generated successfully, or an error message if it fails.
    """
    try:
        # Ensure the directory for the file exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # Run the msinfo32 command to generate the report
        subprocess.run(["msinfo32", "/report", file_path], check=True)
        return f"System information report successfully generated at: {file_path}"
    except subprocess.CalledProcessError as e:
        return f"Error generating system information report: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

