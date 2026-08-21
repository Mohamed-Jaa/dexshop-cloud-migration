# ==========================================
# Stage 1: Build & Dependencies
# ==========================================
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build-time system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install system-wide
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==========================================
# Stage 2: Minimal & Secure Runtime
# ==========================================
FROM python:3.12-slim AS final

# Security & Optimization environment flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOME=/home/appuser \
    PORT=5000

WORKDIR /app

# Install minimal runtime shared libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root group and user with an explicit home directory
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --home /home/appuser --shell /bin/bash appuser

# Copy installed Python packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application source code and adjust ownership
COPY --chown=appuser:appgroup . .

# Ensure upload directory exists and has proper permissions
RUN mkdir -p static/uploads && chown -R appuser:appgroup /app /home/appuser

# Switch to the unprivileged user
USER appuser

# Expose internal container port
EXPOSE 5000

# Start production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--access-logfile", "-", "--error-logfile", "-", "app:app"]