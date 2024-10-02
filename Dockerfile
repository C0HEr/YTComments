# Use an official Python image as the base, specifying the platform
FROM --platform=linux/amd64 python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code to the container
COPY . .

# Expose the port (Railway will override this with their own PORT)
EXPOSE 8501

# Start the Python app using Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]