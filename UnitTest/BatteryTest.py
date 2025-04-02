import unittest
from Library.Battery import get_battery_level, get_charger_state

class TestBatteryFunctions(unittest.TestCase):
    def test_get_battery_level(self):
        """
        Test that the battery level is between 5% and 100%.
        """
        battery_level = get_battery_level()
        if battery_level is not None:
            # Assert that the battery level is within the valid range
            self.assertGreaterEqual(battery_level, 5, "Battery level is below 5%.")
            self.assertLessEqual(battery_level, 100, "Battery level is above 100%.")
        else:
            self.skipTest("No battery detected on this device.")

    def test_get_charger_state(self):
        """
        Test that the charger is connected.
        """
        charger_state = get_charger_state()
        if charger_state is not None:
            # Assert that the charger is connected
            self.assertTrue(charger_state, "Charger is not connected. Connect a charger and try again.")
        else:
            self.skipTest("No battery detected on this device.")

if __name__ == "__main__":
    unittest.main()