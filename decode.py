import cv2
import numpy as np
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

def decode_message(image_path):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError(f"Error: Could not open image. Check file path and format: {image_path}")

    # Check for color channels
    if len(img.shape) < 3:
        raise ValueError("Error: Image must have at least 3 color channels (RGB).")

    height, width, channels = img.shape

    n, m, z = 0, 0, 0
    decrypted_bytes = []

    while True:
        pixel_value = img[n % height, m % width, z]
        
        # Break if null terminator is found
        if pixel_value == 0:
            break

        decrypted_bytes.append(pixel_value)
        n += 1
        m += 1
        z = (z + 1) % 3  # Cycle through RGB channels

        # Prevent infinite loop
        if len(decrypted_bytes) > height * width:
            raise ValueError("Error: No valid encoded message found in the image.")

    # Decode byte message
    decrypted_message = bytes(decrypted_bytes).decode("utf-8", errors="ignore")
    return decrypted_message

if __name__ == "__main__":
    image_path = input("Enter the path of the encoded image: ")

    try:
        message = decode_message(image_path)
        print(f"Decrypted Message: {message}")
    except ValueError as e:
        print(e)
