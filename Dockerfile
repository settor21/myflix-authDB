# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary Ubuntu packages
RUN apt-get update && apt-get install -y \
    libpq-dev

# Make port 6000 available to the world outside this container
EXPOSE 6000

# Run database.py when the container launches
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:6000", "app:app"]
