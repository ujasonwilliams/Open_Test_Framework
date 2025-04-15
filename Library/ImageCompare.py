import logging
import cv2
import numpy as np
import os
from FrameworkLogging import CustomLogger

# Remove the old log file before starting a test run.
LogFile = "Logging_ImageCompare.log"
if os.path.exists(LogFile):
    os.remove(LogFile)

# Initialize the logger
log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), LogFile)  # Move log file one folder up
logger = CustomLogger(log_file).get_logger()

# Add a StreamHandler to output logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the desired log level for the console
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Ensure print statements are not overridden by the logger
logger.propagate = True

def grade(reference_image_path, comparison_image_path, percentage_threshold, results_file):
    """
    Compares a golden image with a specific image and calculates the percentage difference.
    Logs results if the difference exceeds the threshold and writes them to a results file.
    """
    logger.info(f"Grading started for '{reference_image_path}' and '{comparison_image_path}' with threshold {percentage_threshold}%.")

    # Load the reference image
    reference_image = cv2.imread(reference_image_path)
    if reference_image is None:
        logger.error(f"Error: Could not load the reference image: {reference_image_path}")
        return

    # Load the comparison image
    comparison_image = cv2.imread(comparison_image_path)
    if comparison_image is None:
        logger.error(f"Error: Could not load the comparison image: {comparison_image_path}")
        return

    # Resize both images to a fixed size (e.g., 800x600)
    desired_width = 800
    desired_height = 600
    reference_image_resized = cv2.resize(reference_image, (desired_width, desired_height))
    comparison_image_resized = cv2.resize(comparison_image, (desired_width, desired_height))

    # Convert both images to grayscale
    reference_gray = cv2.cvtColor(reference_image_resized, cv2.COLOR_BGR2GRAY)
    comparison_gray = cv2.cvtColor(comparison_image_resized, cv2.COLOR_BGR2GRAY)

    # Compute the absolute difference
    difference = cv2.absdiff(reference_gray, comparison_gray)

    # Calculate the percentage difference
    total_pixels = reference_gray.size  # Total number of pixels
    difference_sum = np.sum(difference)  # Sum of absolute differences
    max_difference = total_pixels * 255  # Maximum possible difference (255 per pixel)
    percentage_difference = (difference_sum / max_difference) * 100

    # Determine pass or fail
    result = "Pass" if percentage_difference < percentage_threshold else "Fail"

    # Write the result to the results file in CSV format
    with open(results_file, "a") as f:
        f.write(f"{os.path.basename(comparison_image_path)},{percentage_difference:.2f},{result}\n")

    # Check if the percentage difference exceeds the threshold
    if percentage_difference >= percentage_threshold:
        logger.warning(f"Limit EXCEEDED '{os.path.basename(reference_image_path)}' and '{os.path.basename(comparison_image_path)}': {percentage_difference:.2f}%")
        print(f"Limit EXCEEDED '{os.path.basename(reference_image_path)}' and '{os.path.basename(comparison_image_path)}': {percentage_difference:.2f}%")
    else:
        logger.info(f"Limit passed for '{os.path.basename(reference_image_path)}' and '{os.path.basename(comparison_image_path)}' with {percentage_difference:.2f}% difference.")
        print(f"Limit passed for '{os.path.basename(reference_image_path)}' and '{os.path.basename(comparison_image_path)}' with {percentage_difference:.2f}% difference.")


def compare_and_grade(golden_folder, media_folder, percentage_threshold=5):
    """
    Compares files in the Golden_Images folder with corresponding files in the Media folder.
    Grades them using the grade function and writes results to a file.
    """
    logger.info(f"Starting comparison between golden images in '{golden_folder}' and screenshots in '{media_folder}'.")

    # Path to the results file
    results_file = os.path.join(os.getcwd(), "Measurements.txt")
    
    # Write the header to the results file in CSV format
    with open(results_file, "a") as f:
        f.write("Screenshot Filename,Percentage Difference,Result\n")

    # Iterate through all files in the Media folder
    for file_name in os.listdir(media_folder):
        if file_name.endswith(".jpg"):  # Only process .jpg files
            logger.debug(f"Processing file: {file_name}")

            # Construct full paths for the golden and comparison images
            golden_image_path = os.path.join(golden_folder, file_name)
            comparison_image_path = os.path.join(media_folder, file_name)

            logger.debug(f"Golden image path: {golden_image_path}")
            logger.debug(f"Comparison image path: {comparison_image_path}")

            # Check if the golden image exists
            if not os.path.exists(golden_image_path):
                logger.warning(f"Golden image not found: {golden_image_path}. Skipping.")
                continue

            # Check if the comparison image exists
            if not os.path.exists(comparison_image_path):
                logger.warning(f"Comparison image not found: {comparison_image_path}. Skipping.")
                continue

            # Grade the images and write results to the file
            logger.info(f"Comparing '{golden_image_path}' with '{comparison_image_path}'.")
            grade(golden_image_path, comparison_image_path, percentage_threshold, results_file)

    logger.info("Comparison and grading completed.")
    logger.info(f"Results written to {results_file}")


if __name__ == "__main__":
    # Get the invocation directory
    invocation_directory = os.getcwd()
    logger.info(f"Script invoked from: {invocation_directory}")

    # Path to the Golden Images folder
    golden_folder = os.path.join(invocation_directory, "Media", "Golden_Images")

    # Path to the Media folder
    media_folder = os.path.join(invocation_directory, "Media")

    # Call the compare_and_grade function
    compare_and_grade(golden_folder, media_folder, percentage_threshold=12)