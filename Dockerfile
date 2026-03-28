# Use official minimal Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy application source code
COPY src/ ./src/
COPY run_tests.py .

# Run the Python application as the entrypoint
ENTRYPOINT ["python", "src/main.py"]
