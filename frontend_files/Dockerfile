
# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the frontend dependency file into the container
COPY requirements.txt .

# Install all required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit application into the container
COPY app.py .

# Expose the port used by the Streamlit application
EXPOSE 8501

# Start the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
