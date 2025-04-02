import psutil

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


