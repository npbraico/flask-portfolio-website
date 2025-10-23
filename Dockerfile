# Use a slim Python image
FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system deps (if needed). sqlite3 CLI is optional; Python has sqlite built-in.
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY website.py DAL.py ./
COPY templates ./templates
COPY static ./static

# Expose Flask port
EXPOSE 5000

# Ensure DB exists at container start via a tiny bootstrap
# We import DAL and call ensure_db before launching gunicorn
CMD python -c "import DAL; DAL.ensure_db()" && \
    gunicorn -b 0.0.0.0:5000 website:app
