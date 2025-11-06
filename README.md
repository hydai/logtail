# logtail

A lightweight, password-protected HTTP server for tailing and viewing application logs with real-time auto-refresh capabilities.

## Features

- HTTP Basic Auth password protection
- View recent log lines (default 500 lines)
- Auto-refresh page (default 10 seconds)
- Download complete log files
- Support multiple log sources (dev/main)
- Customizable configuration

## Installation

### 1. Activate Virtual Environment

```bash
# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

Edit the `config.py` file to modify settings:

```python
# Authentication settings
USERNAME = "admin"
PASSWORD = "admin123"  # Change to your password

# Server settings
PORT = 8080

# Display settings
DEFAULT_LINES = 500  # Default number of lines to display
REFRESH_INTERVAL = 10  # Auto-refresh interval in seconds

# Log file paths
LOG_PATHS = {
    "dev": "x402-mvp-dev/data/app.log",
    "main": "x402-mvp-main/data/app.log"
}
```

## Usage

### Start Server

```bash
python3 server.py
```

The server will start at `http://0.0.0.0:8080`.

### Access Logs

Access the following URLs in your browser:

- Home: `http://localhost:8080/`
- Development logs: `http://localhost:8080/logs-dev`
- Main logs: `http://localhost:8080/logs-main`

On first access, the browser will prompt for username and password.

### Query Parameters

You can use the following query parameters to customize the display:

- `?lines=N` - Display last N lines (e.g., `/logs-dev?lines=1000`)
- `?download=true` - Download complete log file

### Examples

```
# View last 100 lines
http://localhost:8080/logs-dev?lines=100

# View last 1000 lines
http://localhost:8080/logs-main?lines=1000

# Download complete log file
http://localhost:8080/logs-dev?download=true
```

## Stop Server

Press `Ctrl+C` in the terminal to stop the server.

## File Structure

```
.
├── config.py           # Configuration file
├── server.py           # Main server code
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── venv/              # Python virtual environment
└── x402-mvp-dev/      # Development log directory (needs to be created)
    └── data/
        └── app.log
└── x402-mvp-main/     # Main log directory (needs to be created)
    └── data/
        └── app.log
```

## Notes

1. Ensure log file paths are correctly configured in `config.py`
2. If log files don't exist, the page will display a friendly error message
3. Use a stronger password in production environments
4. Server binds to `0.0.0.0`, accessible from other devices on the local network

## Troubleshooting

### Log File Not Found

If you see a "Log File Not Found" error, check:
1. Log file path is correct
2. Log file exists
3. Server process has permission to read the file

### Cannot Access Server

If unable to connect to the server, check:
1. Server is running
2. Port is not occupied by another program
3. Firewall settings are not blocking the connection
