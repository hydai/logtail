"""
Configuration file - Modify these settings to customize server behavior
"""

# HTTP Basic Auth settings
USERNAME = "admin"
PASSWORD = "admin123"  # Change to your desired password

# Server settings
PORT = 8080  # Server listening port

# Log display settings
DEFAULT_LINES = 500  # Default number of log lines to display
REFRESH_INTERVAL = 10  # Auto-refresh interval in seconds

# Log file path configuration
LOG_PATHS = {
    "dev": "x402-mvp-dev/data/app.log",
    "main": "x402-mvp-main/data/app.log"
}
