# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py ./

# Expose port 5000
EXPOSE 5002

# Run the application
CMD ["python", "app.py"]
