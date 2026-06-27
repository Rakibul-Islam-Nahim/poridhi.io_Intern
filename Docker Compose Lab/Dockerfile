# syntax=docker/dockerfile:1

# Small, Debian-based Python image
FROM python:3.11-slim

# Everything happens in /app inside the image
WORKDIR /app

# Copy deps first so layer caching skips pip install on code-only changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then the application source
COPY app.py .

# Drop privileges: run as an unprivileged user
RUN useradd -m appuser
USER appuser

# Documents that the container listens on 80 (does NOT publish it —
# publishing happens in compose.yaml under `ports:`)
EXPOSE 80

# Default start command
CMD ["python", "app.py"]