# ============================================================
#  Dockerfile — Marketing Intelligence AI Platform
# ============================================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Create runtime directories
RUN mkdir -p logs uploads data/raw data/processed data/features data/outputs

# Expose port
EXPOSE 5000

# Default environment
ENV FLASK_ENV=production
ENV PORT=5000

# Run with Gunicorn (4 workers)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
