# Braille Reader – Docker Setup Guide

Run the Angelina Braille Reader with a single command using Docker. No Python installation, no dependency conflicts.

---

## Prerequisites

| Requirement | Version | Install Link |
|---|---|---|
| **Docker Desktop** | 4.x+ | [docker.com/get-docker](https://www.docker.com/products/docker-desktop/) |
| **Disk space** | ~4 GB | For image layers + model weights |
| **RAM** | 4 GB+ | Neural-network inference needs memory |

> **Windows users:** Make sure Docker Desktop is running (system-tray icon) before proceeding.

---

## Quick Start – One Command

```bash
cd path/to/BrailleReader
docker compose up --build
```

Then open **http://localhost:5001** in your browser.

The first build takes **5–15 minutes** (downloads ~138 MB model weights + Python packages).
Subsequent starts are instant.

---

## How It Works

The Docker setup:
1. **Downloads the neural-network model** (~138 MB) automatically during build
2. **Installs all Python dependencies** (PyTorch CPU, Flask, OpenCV, etc.)
3. **Runs the web server** on port 5001 in production mode
4. **Persists data** (uploads & results) in a Docker volume across restarts
5. **Health checks** ensure the app is running correctly

---

## Alternative: Use Docker directly (without Compose)

```bash
# Build the image
docker build -t braille-reader .

# Run the container
docker run -d --name braille-reader -p 5001:5001 braille-reader
```

---

## Common Operations

### Stop the application

```bash
# With Compose
docker compose down

# Without Compose
docker stop braille-reader
```

### Restart the application

```bash
# With Compose
docker compose up -d

# Without Compose
docker start braille-reader
```

### Run in debug mode

```bash
docker run -p 5001:5001 braille-reader python run_web_app.py --debug
```

### View logs

```bash
# With Compose
docker compose logs -f

# Without Compose
docker logs -f braille-reader
```

### Check health status

```bash
docker inspect --format='{{.State.Health.Status}}' braille-reader
```

### Rebuild after code changes

```bash
docker compose up --build
```

---

## Configuration

| Environment Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `angilina` | Flask session secret (change in production) |
| `DATA_ROOT` | `static/data` | Path for uploads & results inside the container |

Set variables in `docker-compose.yml` under `environment:` or pass them with `docker run -e`:

```bash
docker run -p 5001:5001 -e SECRET_KEY=my-secret braille-reader
```

---

## Data Persistence

Docker Compose creates a named volume `braille_data` so uploaded images and results survive container restarts.

To **back up** the volume:

```bash
docker run --rm -v braille_data:/data -v "%cd%":/backup alpine tar czf /backup/braille_backup.tar.gz -C /data .
```

To **restore**:

```bash
docker run --rm -v braille_data:/data -v "%cd%":/backup alpine tar xzf /backup/braille_backup.tar.gz -C /data
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| **Port 5001 already in use** | Change the port mapping: `-p 8080:5001`, then open `http://localhost:8080` |
| **Build fails at curl** | Network issue — retry the build |
| **Out of memory** | Increase Docker Desktop memory (Settings → Resources → Memory → 4 GB+) |
| **Container exits immediately** | Run `docker logs braille-reader` to see the error |
| **"docker compose" not found** | Use `docker-compose` (with hyphen) on older Docker versions |
| **Health check unhealthy** | Model takes ~60s to load on first start — wait and check logs |

---

## Uninstall / Cleanup

```bash
# Remove container and volume
docker compose down -v

# Remove the built image
docker rmi braille-reader

# Reclaim disk space
docker system prune
```
