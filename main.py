import os
from PIL import Image
import pytesseract
import re

# Update this line with the correct path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_images(folder_path):
    # Get the parent directory of the image folder
    parent_directory = os.path.dirname(folder_path)
    # Specify the path to the output text file in the parent directory
    output_path = os.path.join(parent_directory, 'extracted_texts.txt')

    # Helper function to extract the page number from the filename
    def extract_page_number(filename):
        match = re.search(r'page_(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    # Get a sorted list of image filenames based on page number
    image_files = sorted(
        [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))],
        key=extract_page_number
    )

    # Open the output file in write mode
    with open(output_path, 'w') as outfile:
        # Iterate through all sorted files in the folder
        for filename in image_files:
            # Construct full file path
            file_path = os.path.join(folder_path, filename)
            try:
                # Open the image file
                with Image.open(file_path) as img:
                    # Use pytesseract to extract text from the image
                    text = pytesseract.image_to_string(img,lang='ara')
                    # Write the filename and the extracted text to the output file
                    outfile.write(f'--- Text from {filename} ---\n')
                    outfile.write(text + '\n\n')
                    print(f'Text extracted from {filename}')
            except Exception as e:
                print(f'Could not process file {filename}: {e}')

    print(f'All texts have been extracted to {output_path}')


# Example usage
folder_path = 'x_images'
extract_text_from_images(folder_path)
