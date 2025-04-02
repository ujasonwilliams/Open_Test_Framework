from Library.FunctionLibrary import get_test_suite_version
import unittest
import os

class TestFunctionLibrary(unittest.TestCase):
    def setUp(self):
        # Use the current working directory for the version file
        self.version_file_path = os.path.join(os.getcwd(), "Version.txt")
        with open(self.version_file_path, "w") as file:
            file.write("9999.0.0")

    def test_get_test_suite_version(self):
        # Example test for get_test_suite_version
        version = get_test_suite_version(self.version_file_path)  # Use the path to the version file created in setUp
        if version == "Version file not found":
            self.fail("Version file was not created as expected")
        elif version == "9999.0.0":
            pass  # Version was read correctly
        else:
            self.fail(f"Unexpected return value from get_test_suite_version: {version}")

        self.assertIsInstance(version, str)
    
    def doCleanups(self):
        # Delete the version file after tests to clean up the environment
        if os.path.exists(self.version_file_path):
            os.remove(self.version_file_path)

if __name__ == "__main__":
    unittest.main()