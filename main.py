import os
import re
import easyocr
import cv2
import numpy as np

def preprocess_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive thresholding to get a binary image
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # Save the preprocessed image temporarily for debugging
    processed_image_path = 'processed_image.png'
    cv2.imwrite(processed_image_path, thresh)

    return processed_image_path

def extract_text_from_images(folder_path):
    parent_directory = os.path.dirname(folder_path)
    output_path = os.path.join(parent_directory, 'extracted_texts.txt')

    def extract_page_number(filename):
        match = re.search(r'page_(\d+)', filename)
        return int(match.group(1)) if match else float('inf')

    image_files = sorted(
        [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))],
        key=extract_page_number
    )

    reader = easyocr.Reader(['en'])

    with open(output_path, 'w', encoding='utf-8') as outfile:
        for filename in image_files:
            file_path = os.path.join(folder_path, filename)
            try:
                # Option 1: Direct OCR on original image
                result_original = reader.readtext(file_path, detail=1)
                text_original = '\n'.join([res[1] for res in result_original])

                # Write the original OCR result to the output file
                outfile.write(f'--- Text from original {filename} ---\n')
                outfile.write(text_original + '\n\n')

                # Option 2: Preprocess the image and then perform OCR
                processed_image_path = preprocess_image(file_path)
                result_processed = reader.readtext(processed_image_path, detail=1)
                text_processed = '\n'.join([res[1] for res in result_processed])

                # Write the preprocessed OCR result to the output file
                outfile.write(f'--- Text from preprocessed {filename} ---\n')
                outfile.write(text_processed + '\n\n')

                print(f'Text extracted from {filename}')
            except Exception as e:
                print(f'Could not process file {filename}: {e}')

    print(f'All texts have been extracted to {output_path}')

# Example usage
folder_path = 'x_images'
extract_text_from_images(folder_path)
