import psutil
import subprocess

def set_power_settings_never_sleep():
    """
    Configures the system's power settings to prevent it from sleeping.
    Sets both the display and system sleep timeout to 'Never'.
    """
    try:
        # Set the system sleep timeout to 'Never' (0 minutes)
        subprocess.run(["powercfg", "/change", "standby-timeout-ac", "0"], check=True)
        subprocess.run(["powercfg", "/change", "standby-timeout-dc", "0"], check=True)

        # Set the display sleep timeout to 'Never' (0 minutes)
        subprocess.run(["powercfg", "/change", "monitor-timeout-ac", "0"], check=True)
        subprocess.run(["powercfg", "/change", "monitor-timeout-dc", "0"], check=True)

        print("Power settings have been updated to never sleep.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update power settings: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
def get_battery_level():
    """
    Retrieves the current battery level as a percentage.
    Returns:
        int: Battery level (0-100) if available.
        None: If no battery is detected.
    """
    battery = psutil.sensors_battery()
    if battery is None:
        print("No battery detected on this device.")
        return None

    battery_level = battery.percent
    print(f"Battery Level: {battery_level}%")
    return battery_level


def get_charger_state():
    """
    Checks if the system is connected to AC power (charger connected).
    Returns:
        True: If the charger is connected (AC power).
        False: If running on battery.
        None: If no battery is detected.
    """
    battery = psutil.sensors_battery()
    if battery is None:
        print("No battery detected on this device.")
        return None

    if battery.power_plugged:
        print("Charger is connected.")
        return True
    else:
        print("Charger is not connected.")
        return False


