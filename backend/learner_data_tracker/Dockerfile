
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install flask

# Expose port and run
EXPOSE 8001
CMD ["python", "app.py"]
