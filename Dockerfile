# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Copy dependency definition
COPY requirements.txt .

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Expose port 5000
EXPOSE 5000

# Create a non-root user for security compliance
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Health check configuration
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Start server using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]