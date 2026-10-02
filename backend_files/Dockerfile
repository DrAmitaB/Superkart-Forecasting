
# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend requirements file
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY app.py .

# Copy the trained SuperKart model
COPY model.pkl .

# Expose the Flask API port
EXPOSE 7860

# Start the Flask API using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]
