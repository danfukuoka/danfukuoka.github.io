# Use the official Python image as a base
FROM --platform=linux/amd64 python:latest as build

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app

# Install dependencies
RUN pip install pymongo[srv]==4.11

# Command to run the Python script
CMD ["python", "-u", "app.py"]