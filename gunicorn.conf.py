# gunicorn.conf.py
# Production WSGI Configuration for Krishi Sahayak
# ------------------------------------------------------------------------------
# Hardware & Architecture Rationale:
# This project incorporates PyTorch/MobileNetV2 image classification for leaf
# disease diagnosis alongside SQLite WAL-mode persistence.
# On resource-constrained host machines (e.g., 8 GB RAM), spawning the standard
# formula (2 * cores + 1) would lead to multiple redundant deep-learning model
# instances in memory, risking excessive memory pressure and swap thrashing.
#
# A conservative baseline of 2 workers is intentionally configured to provide
# reliable concurrency without starving system memory during ML inference.
# ------------------------------------------------------------------------------

# Network Binding
# Bind strictly to localhost loopback so requests must transit through the
# front-facing reverse proxy (e.g., Nginx) and cannot bypass perimeter security.
bind = "127.0.0.1:5000"

# Worker Concurrency
# Exactly 2 synchronous workers: safe baseline for PyTorch model footprint and SQLite.
workers = 2
worker_class = "sync"

# Timeouts
# 60s timeout accommodates PyTorch MobileNetV2 image evaluation and cold-start model weights loading.
timeout = 60
graceful_timeout = 30
keepalive = 5

# Logging
# Stream access and error logs to stdout/stderr for container/systemd journal capture.
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)ss'

# Process Management & Lifecycle
# Do NOT preload the application:
# Ensuring preload_app = False guarantees that SQLite database handles, in-memory caches,
# and PyTorch model states are safely and independently initialized per worker process,
# avoiding inherited file descriptors and cross-fork concurrency hazards.
preload_app = False
