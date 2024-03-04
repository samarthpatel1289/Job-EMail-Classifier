# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run orchestra.py when the container launches
CMD ["python", "./orchestra.py"]
# This Dockerfile does not require additional commands to "run".
# To build and run the Docker image created by this Dockerfile,
# use the following commands in your terminal:

# Build the Docker image
# docker build -t job-email-classifier .

# Run the Docker container from the image
# docker run -it --rm job-email-classifier
