# Climate AI Docker Deployment
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs

# Generate sample data and train models
RUN python src/generate_sample_data.py
RUN python src/modeling.py

# Expose port
EXPOSE 8503

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8503/_stcore/health || exit 1

# Start the application
CMD ["streamlit", "run", "src/dashboard_futuristic.py", "--server.port=8503", "--server.address=0.0.0.0"]