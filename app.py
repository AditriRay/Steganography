from flask import Flask, render_template, request, send_file
import os
import cv2
import encode
import decode

app = Flask(__name__, template_folder="templates", static_folder="static")  

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure the uploads folder exists

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/encode", methods=["POST"])
def encode_route():
    file = request.files["image"]
    message = request.form["message"]
    password = request.form["password"]

    if not file or not message or not password:
        return "Error: All fields are required!", 400

    image_path = os.path.join(UPLOAD_FOLDER, "uploaded.png")
    file.save(image_path)

    # Combine password and message
    full_message = password + "|" + message

    encoded_image_path = encode.encode_message(image_path, full_message, "encrypted.png")

    return send_file(encoded_image_path, as_attachment=True)

@app.route("/decode", methods=["POST"])
def decode_route():
    file = request.files["image"]
    password = request.form["password"]

    if not file or not password:
        return "Error: All fields are required!", 400

    image_path = os.path.join(UPLOAD_FOLDER, "decode.png")
    file.save(image_path)

    decrypted_message = decode.decode_message(image_path)

    # Extract password and message
    if "|" in decrypted_message:
        stored_password, original_message = decrypted_message.split("|", 1)
        if stored_password == password:
            return f"Decrypted Message: {original_message}"
        else:
            return "Error: Incorrect password!", 403
    else:
        return "Error: No valid message found!", 400

if __name__ == "__main__":
    # Make sure the app listens on 0.0.0.0:8080
    app.run(host='0.0.0.0', port=8080)
