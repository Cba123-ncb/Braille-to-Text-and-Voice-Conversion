# ============================================================
# Dockerfile for Angelina Braille Reader
# ============================================================
# Builds a self-contained image with all dependencies and
# model weights baked in. Clients run with a single command.
# ============================================================

FROM python:3.10-slim

LABEL maintainer="BrailleReader"
LABEL description="Braille Reader – optical Braille recognition web app"

# Install OS-level dependencies required by OpenCV / PyMuPDF
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libfontconfig1 \
        libmupdf-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ---------- Python dependencies (cached layer) ---------------
# Install PyTorch CPU first (uses a separate index URL)
RUN pip install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cpu

# Install remaining Python packages (pinned to match working local setup)
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    flask==2.3.3 \
    flask-wtf==1.2.1 \
    flask-mobility==1.1.0 \
    werkzeug==2.3.7 \
    wtforms==3.1.2 \
    opencv-python-headless \
    pillow \
    albumentations==0.4.5 \
    imgaug \
    PyMuPDF==1.23.26 \
    matplotlib \
    scipy

# ---------- Copy application source code ---------------------
# NOTE: weights/ is excluded via .dockerignore to keep this
#       layer small and avoid caching stale model files.
COPY . /app

# ---------- Install ovotools from local source ---------------
RUN pip install --no-cache-dir -e /app/src/ovotools

# ---------- Create required data directories ------------------
RUN mkdir -p /app/web_app/static/data/raw \
             /app/web_app/static/data/results \
             /app/web_app/static/data/tasks

# ---------- Copy model weights LAST (avoids stale cache) ------
# weights/model.t7 (~138 MB) must exist in the build context.
# This is a separate layer so it is always fresh and verifiable.
COPY weights/model.t7 /app/weights/model.t7
COPY weights/param.txt /app/weights/param.txt

# Verify the model file is real (not a 404 HTML page)
RUN MODEL_SIZE=$(stat -c%s /app/weights/model.t7) && \
    echo "model.t7 size: ${MODEL_SIZE} bytes" && \
    if [ "$MODEL_SIZE" -lt 1000000 ]; then \
        echo "ERROR: weights/model.t7 is too small (${MODEL_SIZE} bytes)." && \
        echo "It may be a corrupt download. Expected ~144 MB." && \
        head -n 3 /app/weights/model.t7 && \
        exit 1; \
    fi

# ---------- Health check --------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5001/ || exit 1

# ---------- Expose port & set default command -----------------
EXPOSE 5001

# Run the web application in production mode on port 5001
CMD ["python", "run_web_app.py"]
