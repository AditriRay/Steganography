import cv2
import numpy as np
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

def encode_message(image_path, message, output_filename="encoded.png"):
    # Read image
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError(f"Error: Could not open image. Check file path and format: {image_path}")

    # Ensure the image has at least 3 channels (RGB)
    if len(img.shape) < 3:
        raise ValueError("Error: Image must have at least 3 color channels (RGB).")

    height, width, channels = img.shape

    # Convert message to bytes and add a null terminator
    message_bytes = message.encode("utf-8") + b"\0"

    if len(message_bytes) > height * width:
        raise ValueError("Error: Message too long for image capacity.")

    n, m, z = 0, 0, 0
    for byte in message_bytes:
        img[n % height, m % width, z] = byte
        n += 1
        m += 1
        z = (z + 1) % 3  # Cycle through RGB channels

    # Save the encoded image
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)
    cv2.imwrite(output_path, img)
    
    return output_path

if __name__ == "__main__":
    image_path = input("Enter the image path: ")
    message = input("Enter your secret message: ")

    try:
        encoded_image = encode_message(image_path, message)
        print(f"Encoded image saved at: {encoded_image}")
    except ValueError as e:
        print(e)
