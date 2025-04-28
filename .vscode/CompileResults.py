import os
import glob
import csv

def create_combined_table(folder_path, output_file):
    """
    Combines data from Measurement*.txt files into a single table.

    Args:
        folder_path (str): Path to the folder containing Measurement*.txt files.
        output_file (str): Path to save the combined table as a CSV file.
    """
    # Find all Measurement*.txt files in the folder
    measurement_files = glob.glob(os.path.join(folder_path, "Measurement*.txt"))

    # Dictionary to store data with Screenshot Filename as the key
    combined_data = {}

    # List to store the column headers (file names)
    column_headers = []

    # Process each Measurement*.txt file
    for file_path in measurement_files:
        file_name = os.path.basename(file_path)  # Get the file name
        column_headers.append(file_name)  # Add the file name as a column header

        # Read the file and extract data
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                screenshot_filename = row[0]
                percentage_difference = row[1]

                # Add data to the combined_data dictionary
                if screenshot_filename not in combined_data:
                    combined_data[screenshot_filename] = {}
                combined_data[screenshot_filename][file_name] = percentage_difference

    # Write the combined data to the output CSV file
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Screenshot Filename"] + column_headers)

        # Write the data rows
        for screenshot_filename, file_data in sorted(combined_data.items()):
            row = [screenshot_filename]
            for file_name in column_headers:
                row.append(file_data.get(file_name, ""))  # Add data or empty cell if missing
            writer.writerow(row)

# Folder containing Measurement*.txt files
folder_path = r"C:\Code\Open_Test_Framework"

# Output file for the combined table
output_file = os.path.join(folder_path, "Combined_Table.csv")

# Create the combined table
create_combined_table(folder_path, output_file)

print(f"Combined table created successfully: {output_file}")