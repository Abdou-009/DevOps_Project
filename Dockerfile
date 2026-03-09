FROM python:3.11-slim

LABEL maintainer="abdou-009"
LABEL version="1.1.0"
LABEL description="DevOps Monitoring API — production-ready system metrics service"

# Security: create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install dependencies first (leverages Docker layer caching)
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Switch to non-root user
USER appuser

EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Production server via gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
