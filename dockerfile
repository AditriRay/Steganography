# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 && rm -rf /var/lib/apt/lists/*

# Install NumPy first to ensure compatibility with OpenCV
RUN pip install --no-cache-dir "numpy<2"

# Install all other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside the container
EXPOSE 8080

# Define environment variable for Cloud Run's expected port
ENV PORT=8080

# Run the app when the container launches
CMD ["python", "app.py"]
