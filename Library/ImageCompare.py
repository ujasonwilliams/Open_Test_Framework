import cv2
import numpy as np
import os

def grade(reference_image_path, comparison_image_path, percentage_threshold):
    """
    Compares a golden image with a specific image and calculates the percentage difference.
    Prints results if the difference exceeds the threshold.
    """
    # Load the reference image
    reference_image = cv2.imread(reference_image_path)
    if reference_image is None:
        print(f"Error: Could not load the reference image: {reference_image_path}")
        return

    # Load the comparison image
    comparison_image = cv2.imread(comparison_image_path)
    if comparison_image is None:
        print(f"Error: Could not load the comparison image: {comparison_image_path}")
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

    # Check if the percentage difference exceeds the threshold
    if percentage_difference >= percentage_threshold:
        print(f"Limit EXCEEDED '{os.path.basename(reference_image_path)}' and '{os.path.basename(comparison_image_path)}': {percentage_difference:.2f}%")
    else:
        print(f"Limit passed for '{os.path.basename(reference_image_path)}' and '{os.path.basename(comparison_image_path)}' with {percentage_difference:.2f}% difference.")

if __name__ == "__main__":
    # Path to the Golden Images folder
    golden_folder = r"C:\Code\Open_Test_Framework\Media\Golden_Images"

    # Path to the Media folder
    media_folder = r"C:\Code\Open_Test_Framework\Media"

    testLimit = 5  # This is the threshold for percentage difference, can be adjusted as needed.
    # Array of golden image files, percentage thresholds, and configurations
    measurements = [
        ("MKV_H.264_29.97FPS_golden.jpg", "MKV_H.264_29.97FPS.mkv_screenshot.jpg", 5, "MKV_H.264_29.97FPS"),
        ("MKV_H.264_60FPS_golden.jpg", "MKV_H.264_60FPS.mkv_screenshot.jpg", 5, "MKV_H.264_60FPS"),
        ("MKV_HEVc_29.97FPs_golden.jpg", "MKV_HEVc_29.97FPs.mkv_screenshot.jpg", 5, "MKV_HEVc_29.97FPs"),
        ("MKV_HEVC_60FPS_golden.jpg", "MKV_HEVC_60FPS.mkv_screenshot.jpg", 5, "MKV_HEVC_60FPS"),
        ("MP4_H.26429.97FPS_golden.jpg", "MP4_H.26429.97FPS.mp4_screenshot.jpg", 5, "MP4_H.26429.97FPS"),
        ("MP4_H.264_120FPS_golden.jpg", "MP4_H.264_120FPS.mp4_screenshot.jpg", 5, "MP4_H.264_120FPS"),
        ("MP4_H.264_240FPS_golden.jpg", "MP4_H.264_240FPS.mp4_screenshot.jpg", 5, "MP4_H.264_240FPS"),
        ("MP4_H.264_60FPS_golden.jpg", "MP4_H.264_60FPS.mp4_screenshot.jpg", 5, "MP4_H.264_60FPS"),
        ("MP4_HEVC29.97FPS_golden.jpg", "MP4_HEVC29.97FPS.mp4_screenshot.jpg", 5, "MP4_HEVC29.97FPS"),
        ("MP4_HEVC_204FPS_golden.jpg", "MP4_HEVC_204FPS.mp4_screenshot.jpg", 5, "MP4_HEVC_204FPS"),
        ("MP4_HEVC_60FPS_golden.jpg", "MP4_HEVC_60FPS.mp4_screenshot.jpg", 5, "MP4_HEVC_60FPS"),
        ("MPEG-2_MPEG-2_60FPS_golden.jpg", "MPEG-2_MPEG-2_60FPS.mpg_screenshot.jpg", 5, "MPEG-2_MPEG-2_60FPS"),
        ("MPEG-2_MPEG_29.97FPS_golden.jpg", "MPEG-2_MPEG_29.97FPS.mpg_screenshot.jpg", 5, "MPEG-2_MPEG_29.97FPS")
    ]

    # Iterate through the array and process each golden image
    for golden_file, comparison_file, percentage_threshold, config in measurements:
        golden_image_path = os.path.join(golden_folder, golden_file)
        comparison_image_path = os.path.join(media_folder, comparison_file)
        #print(f"Grading '{golden_image_path}' against '{comparison_image_path}' with threshold {percentage_threshold}% for config {config}")
        grade(golden_image_path, comparison_image_path, percentage_threshold)