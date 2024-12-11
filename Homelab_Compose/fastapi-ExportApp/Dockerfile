FROM python:3.9-slim

# Update package lists and install necessary system packages including build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libc6-dev \
    libssl-dev \
    libffi-dev \
    libmariadb3 \
    libmariadb-dev \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file to leverage Docker cache
COPY ./requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Copy the templates directory into the container
COPY ./templates /app/templates

# Expose the port that FastAPI will run on
EXPOSE 80

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
