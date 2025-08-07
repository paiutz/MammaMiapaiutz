import os
import shutil
import uvicorn
from dotenv import load_dotenv
from datetime import datetime

# --- Constants ---
base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, ".env")
log_path = os.path.join(base_dir, "log.txt")
log_max_size = 1 * 1024 * 1024  # 1MB

# --- Logging ---
def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")

# --- Rotate Log ---
if os.path.exists(log_path) and os.path.getsize(log_path) > log_max_size:
    backup = log_path.replace(".txt", f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")
    shutil.move(log_path, backup)
    log(f"Log rotated to {backup}")

log("MammaMiapaiutz.exe started")

# --- Load .env ---
if os.path.exists(env_path):
    load_dotenv(env_path)
    log(".env loaded successfully")
else:
    log("WARNING: .env file not found")

# --- Log important vars ---
for var in ["TMDB_KEY", "PORT", "HOST", "DEBUG", "ENV"]:
    val = os.environ.get(var)
    if val:
        log(f"{var} = {val}")
    else:
        log(f"WARNING: {var} not set in environment")

# --- Uvicorn Config ---
host = os.environ.get("HOST", "0.0.0.0")
port = int(os.environ.get("PORT", "7000"))
certfile = os.path.join(base_dir, "cert.pem")
keyfile = os.path.join(base_dir, "key.pem")
use_ssl = os.path.exists(certfile) and os.path.exists(keyfile)

if use_ssl:
    log("SSL certificates found: using HTTPS")
else:
    log("SSL certificates not found: using HTTP")

# --- Run App ---
try:
    import run  # dynamically import your FastAPI app
    uvicorn.run(
        run.app,
        host=host,
        port=port,
        ssl_certfile=certfile if use_ssl else None,
        ssl_keyfile=keyfile if use_ssl else None,
    )
except Exception as e:
    log(f"ERROR: Failed to run app: {e}")
    raise
