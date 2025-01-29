# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create a working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .
# Copy the python code
COPY app.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files


# Set the default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "4000"]
