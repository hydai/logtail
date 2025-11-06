"""
Configuration file - Modify these settings to customize server behavior
Settings can be overridden using environment variables (useful for Docker deployments)
"""
import os

# HTTP Basic Auth settings
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "admin123")  # Change to your desired password

# Server settings
PORT = 8080  # Server listening port (use docker-compose port mapping to change external port)

# Log display settings
DEFAULT_LINES = int(os.getenv("DEFAULT_LINES", "500"))  # Default number of log lines to display
REFRESH_INTERVAL = int(os.getenv("REFRESH_INTERVAL", "10"))  # Auto-refresh interval in seconds

# Log file path configuration
LOG_PATHS = {
    "dev": os.getenv("LOG_PATH_DEV", "x402-mvp-dev/data/app.log"),
    "main": os.getenv("LOG_PATH_MAIN", "x402-mvp-main/data/app.log")
}
