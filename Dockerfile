# Use Python 3.10
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Flask
EXPOSE 10000

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
