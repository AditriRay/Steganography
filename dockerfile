# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside the container
EXPOSE 8080

# Define environment variable for the port that Cloud Run will use
ENV PORT 8080

# Run the app when the container launches
CMD ["python", "app.py"]
