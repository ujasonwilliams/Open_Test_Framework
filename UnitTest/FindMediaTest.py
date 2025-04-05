import unittest
import os
import tempfile
from Library.FunctionLibrary import scan_for_video_files

class TestScanForVideoFiles(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary directory with test files for each test case.
        """
        # Create a temporary directory
        self.test_dir = tempfile.TemporaryDirectory()

        # Create test files and subdirectories
        self.files = [
            "movie1.mkv",
            "movie2.mp4",
            "document.txt",
            "clip1.mpg",
            "clip2.doc"
        ]
        self.subfolder = os.path.join(self.test_dir.name, "subfolder")
        os.makedirs(self.subfolder)

        # Create files in the main directory
        for file in self.files[:3]:  # First three files in the main directory
            with open(os.path.join(self.test_dir.name, file), "w") as f:
                f.write("Test content")

        # Create files in the subdirectory
        for file in self.files[3:]:  # Last two files in the subdirectory
            with open(os.path.join(self.subfolder, file), "w") as f:
                f.write("Test content")

    def tearDown(self):
        """
        Clean up the temporary directory after each test case.
        """
        self.test_dir.cleanup()

    def test_scan_for_video_files(self):
        """
        Test that scan_for_video_files retrieves all .mkv, .mp4, and .mpg files from the specified directory.
        """
        # Call the function with the temporary directory path
        result = scan_for_video_files(self.test_dir.name)

        # Expected video files
        expected_files = [
            os.path.join(self.test_dir.name, "movie1.mkv"),
            os.path.join(self.test_dir.name, "movie2.mp4"),
            os.path.join(self.subfolder, "clip1.mpg"),
        ]

        # Assert that the result matches the expected files
        self.assertEqual(sorted(result), sorted(expected_files))

    def test_scan_for_video_files_empty_directory(self):
        """
        Test that scan_for_video_files returns an empty list when the directory contains no video files.
        """
        # Create an empty temporary directory
        empty_dir = tempfile.TemporaryDirectory()

        # Call the function with the empty directory path
        result = scan_for_video_files(empty_dir.name)

        # Assert that the result is an empty list
        self.assertEqual(result, [])

        # Clean up the empty directory
        empty_dir.cleanup()

    def test_scan_for_video_files_invalid_path(self):
        """
        Test that scan_for_video_files handles an invalid directory path gracefully.
        """
        # Call the function with an invalid directory path
        invalid_path = r"C:\Invalid\Path"
        result = scan_for_video_files(invalid_path)

        # Assert that the result is an empty list
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()