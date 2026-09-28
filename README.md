# Krishi Sahayak (कृषि सहायक)

Smart Multilingual Agricultural Advisory & Farm Management Assistant integrating agronomic handbooks, real-time weather forecasts, automated crop calendars, and AI-powered leaf disease diagnosis.

---

## 1. Local Development Setup

### Prerequisites
* Python 3.10+ (tested on Python 3.11 & 3.13)
* Virtual environment (`venv`)

### Setup Instructions

1. **Activate the Virtual Environment**:
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   *In local development, if `SECRET_KEY` is omitted, the application generates a cryptographically random process key automatically.*

4. **Run the Development Server**:
   ```bash
   python app.py
   ```
   The application will start on `http://127.0.0.1:5000/`.

---

## 2. Production Deployment Guide (Linux / WSGI)

In a live production environment, the Flask built-in development server must **not** be exposed directly. The recommended production architecture pairs **Gunicorn** as the WSGI server with **Nginx** as the front-facing reverse proxy.

```
[ Internet / Clients ]
         │
         ▼
[ Nginx (Port 80/443) ] ──(Direct static file serving)──► /static/ (CSS, JS, Videos)
         │
         ▼ (HTTP reverse proxy to 127.0.0.1:5000)
[ Gunicorn WSGI Pool (2 workers) ]
         │
         ▼
[ Flask Application (app:app) ] ──► SQLite (WAL mode) & PyTorch Model
```

---

### Step A: Configure Production Environment

1. Set `FLASK_ENV=production` and generate a strong 32-byte cryptographic secret:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
   export ENABLE_DEV_MOCK_AUTH=0
   export PORT=5000
   export DATABASE_PATH=/var/lib/krishi-sahayak/database.db
   ```
   *(Or populate these variables in your deployment environment or container orchestrator).*

2. **Database Path Configuration (`DATABASE_PATH`)**:
   * **Development Default**: If `DATABASE_PATH` is unset or empty, the application automatically uses `<project root>/database.db`.
   * **Production Recommendation**: For security and defense-in-depth, store the SQLite database outside the web/application document tree (e.g. `/var/lib/krishi-sahayak/database.db`).
   * **Permissions**: Ensure the target directory exists and is writable by the application service account:
     ```bash
     sudo mkdir -p /var/lib/krishi-sahayak
     sudo chown -R www-data:www-data /var/lib/krishi-sahayak
     sudo chmod 750 /var/lib/krishi-sahayak
     ```
   * **Defense-in-Depth**: Relocating the database ensures the file cannot be accessed via web server misconfigurations. While `nginx.conf` includes rules blocking direct requests for `.db`, `.db-wal`, and `.sqlite` files, Nginx protection alone should not be relied upon without physical directory isolation.
   * **Note on Migration**: Setting `DATABASE_PATH` does not automatically migrate an existing production database; operators should copy their existing database file to the new path when relocating.

> [!IMPORTANT]
> When `FLASK_ENV=production`, `SECRET_KEY` is strictly required. Startup will abort immediately with a `RuntimeError` if it is unset or empty.

---

### Step B: Launching Gunicorn WSGI Server

The repository includes a tuned production configuration file: [`gunicorn.conf.py`](gunicorn.conf.py).

* **Worker Policy**: Exactly **2 workers** are configured. Because Krishi Sahayak incorporates PyTorch / MobileNetV2 image inference, 2 workers prevent excessive memory overhead on typical 8 GB host servers while keeping SQLite write queues safe.
* **Timeout**: Set to **60s** to accommodate CPU model evaluation.
* **Binding**: Binds strictly to `127.0.0.1:5000` to prevent public bypass of the reverse proxy.

Start Gunicorn:
```bash
gunicorn -c gunicorn.conf.py app:app
```

#### Systemd Service Unit Example (Linux):
Create `/etc/systemd/system/krishi-sahayak.service`:
```ini
[Unit]
Description=Krishi Sahayak Gunicorn WSGI Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/krishi-sahayak
EnvironmentFile=/var/www/krishi-sahayak/.env
ExecStart=/var/www/krishi-sahayak/.venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Manage the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start krishi-sahayak
sudo systemctl enable krishi-sahayak
sudo systemctl status krishi-sahayak
```

---

### Step C: Nginx Reverse Proxy Setup

The repository provides a production template in [`nginx.conf`](nginx.conf).

1. Copy and adapt [`nginx.conf`](nginx.conf) to your Nginx sites directory:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/krishi-sahayak.conf
   ```
2. Update the `/static/` alias directive in the configuration to point to your server's project directory:
   ```nginx
   location /static/ {
       alias /var/www/krishi-sahayak/static/;
       expires 30d;
       add_header Cache-Control "public, no-transform";
   }
   ```
3. Enable the site and reload Nginx:
   ```bash
   sudo ln -s /etc/nginx/sites-available/krishi-sahayak.conf /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

---

### Step D: HTTPS / TLS Termination

* TLS certificates should be managed at the reverse proxy or load balancer layer.
* In Linux environments, automated free certificates can be provisioned using **Certbot**:
  ```bash
  sudo apt install certbot python3-certbot-nginx
  sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
  ```
* Certbot will automatically configure the SSL listener on port 443 and redirect port 80 traffic.
* Flask's built-in `ProxyFix` middleware accurately detects `X-Forwarded-Proto` and enforces secure cookies and HSTS headers.

---

## 3. Maintenance & Process Lifecycle

* **Graceful Reload**:
  ```bash
  sudo systemctl reload krishi-sahayak
  # Or via Gunicorn master PID:
  kill -HUP <gunicorn_master_pid>
  ```
* **View Application Logs**:
  ```bash
  journalctl -u krishi-sahayak -f
  ```

---

### 3.2 Automated Database Backups & Recovery (SQLite VACUUM INTO)

Krishi Sahayak implements point-in-time, WAL-safe SQLite backups using SQLite's native `VACUUM INTO` statement. This creates defragmented, atomic snapshots without acquiring exclusive locks that block concurrent web traffic.

#### 1. Manual Backup Command
Create an on-demand database snapshot via the Flask CLI:
```bash
flask backup-db
```
*(Or in virtualenv: `python -m flask backup-db`)*

#### 2. Default Backup Location & Naming
* Backups are written to the `backups/` directory in the project root:
  `backups/krishi_sahayak_backup_YYYYMMDD_HHMMSS.db`
* Output files are fully defragmented and self-contained (no separate `-wal` or `-shm` required).

#### 3. Retention Policy
* Backups are automatically pruned: the **newest 7 backups** are retained by default (`keep_count=7`).
* Files not matching the timestamped naming convention or files outside `backups/` are never deleted.

#### 4. Recommended Production Scheduling (Systemd Timer / Cron)
Because backups are managed via the CLI command, regular scheduling in production should be handled by an OS-level scheduler:

**Option A: Crontab (Daily at 2:00 AM)**
```bash
0 2 * * * cd /var/www/krishi-sahayak && /var/www/krishi-sahayak/.venv/bin/flask backup-db >> /var/log/krishi_backup.log 2>&1
```

**Option B: Systemd Timer**
Create `/etc/systemd/system/krishi-sahayak-backup.service`:
```ini
[Unit]
Description=Krishi Sahayak SQLite Backup Service
After=network.target

[Service]
Type=oneshot
User=www-data
WorkingDirectory=/var/www/krishi-sahayak
EnvironmentFile=/var/www/krishi-sahayak/.env
ExecStart=/var/www/krishi-sahayak/.venv/bin/flask backup-db
```

Create `/etc/systemd/system/krishi-sahayak-backup.timer`:
```ini
[Unit]
Description=Daily Krishi Sahayak SQLite Backup Timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:
```bash
sudo systemctl daemon-reload
sudo systemctl enable --now krishi-sahayak-backup.timer
```

> [!WARNING]
> **Do not run a backup scheduler inside Gunicorn worker processes.** Because production Gunicorn runs multiple worker processes (`gunicorn.conf.py`), each worker would execute independent, duplicate backup jobs. External scheduling via cron or systemd ensures single-process, reliable execution.

#### 5. Database Restore Guidance
In disaster recovery or rollback scenarios:
1. **Stop the application service**:
   ```bash
   sudo systemctl stop krishi-sahayak
   ```
2. **Safely archive the current database and active WAL files**:
   ```bash
   mv database.db database.db.bak
   rm -f database.db-wal database.db-shm
   ```
3. **Copy the desired backup snapshot to `database.db`**:
   ```bash
   cp backups/krishi_sahayak_backup_YYYYMMDD_HHMMSS.db database.db
   chmod 640 database.db
   chown www-data:www-data database.db
   ```
4. **Restart the application service**:
   ```bash
   sudo systemctl start krishi-sahayak
   sudo systemctl status krishi-sahayak
   ```
