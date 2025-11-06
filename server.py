"""
Password-protected Log Viewer Server
"""

import os
from functools import wraps
from flask import Flask, request, Response, send_file, make_response
import config

app = Flask(__name__)


def check_auth(username, password):
    """Verify username and password"""
    return username == config.USERNAME and password == config.PASSWORD


def authenticate():
    """Send 401 response requiring browser authentication"""
    return Response(
        'Authentication required.\n'
        'Please provide valid credentials.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def requires_auth(f):
    """Decorator to require HTTP Basic Auth authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def read_last_n_lines(file_path, n):
    """Read the last N lines of a file"""
    try:
        with open(file_path, 'rb') as f:
            # Move to end of file
            f.seek(0, os.SEEK_END)
            file_size = f.tell()

            # If file is empty
            if file_size == 0:
                return ""

            # Read from end to beginning
            lines = []
            buffer = bytearray()
            pointer = file_size - 1

            while pointer >= 0 and len(lines) < n:
                f.seek(pointer)
                byte = f.read(1)

                if byte == b'\n' and buffer:
                    lines.append(buffer[::-1].decode('utf-8', errors='replace'))
                    buffer = bytearray()
                else:
                    buffer.extend(byte)

                pointer -= 1

            # Add the last line if exists
            if buffer:
                lines.append(buffer[::-1].decode('utf-8', errors='replace'))

            # Reverse to get correct order
            return '\n'.join(reversed(lines))
    except FileNotFoundError:
        return f"Error: Log file not found at {file_path}"
    except Exception as e:
        return f"Error reading log file: {str(e)}"


def generate_html_page(content, log_type, lines, refresh_interval):
    """Generate HTML page with auto-refresh"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="{refresh_interval}">
    <title>Logs - {log_type}</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}
        .header {{
            position: sticky;
            top: 0;
            background-color: #2d2d2d;
            padding: 10px 15px;
            margin: -20px -20px 20px -20px;
            border-bottom: 2px solid #007acc;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 18px;
            color: #007acc;
        }}
        .controls {{
            display: flex;
            gap: 10px;
        }}
        .controls a {{
            color: #007acc;
            text-decoration: none;
            padding: 5px 10px;
            border: 1px solid #007acc;
            border-radius: 3px;
            font-size: 12px;
        }}
        .controls a:hover {{
            background-color: #007acc;
            color: #ffffff;
        }}
        .info {{
            color: #858585;
            margin-bottom: 10px;
            font-size: 11px;
        }}
        pre {{
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Log Viewer - {log_type.upper()}</h1>
        <div class="controls">
            <a href="?lines=100">100 lines</a>
            <a href="?lines=500">500 lines</a>
            <a href="?lines=1000">1000 lines</a>
            <a href="?download=true">Download Full Log</a>
        </div>
    </div>
    <div class="info">
        Showing last {lines} lines | Auto-refresh every {refresh_interval} seconds
    </div>
    <pre>{content}</pre>
</body>
</html>"""
    return html


@app.route('/')
@requires_auth
def index():
    """Home page - Display available log links"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Log Viewer</title>
    <style>
        body {
            margin: 0;
            padding: 40px;
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        h1 {
            color: #007acc;
        }
        .links {
            margin-top: 30px;
        }
        .links a {
            display: block;
            color: #007acc;
            text-decoration: none;
            padding: 15px 20px;
            margin: 10px 0;
            border: 1px solid #007acc;
            border-radius: 5px;
            font-size: 16px;
            transition: all 0.3s;
        }
        .links a:hover {
            background-color: #007acc;
            color: #ffffff;
        }
    </style>
</head>
<body>
    <h1>Log Viewer</h1>
    <div class="links">
        <a href="/logs-dev">View Development Logs</a>
        <a href="/logs-main">View Main Logs</a>
    </div>
</body>
</html>"""
    return html


@app.route('/logs-dev')
@requires_auth
def logs_dev():
    """View development environment logs"""
    return serve_log('dev')


@app.route('/logs-main')
@requires_auth
def logs_main():
    """View main environment logs"""
    return serve_log('main')


def serve_log(log_type):
    """
    Serve log file content
    Supported parameters:
    - lines: Number of lines to display (default from config)
    - download: Whether to download full file (true/false)
    """
    log_path = config.LOG_PATHS.get(log_type)

    if not log_path:
        return f"Error: Unknown log type '{log_type}'", 404

    # Check if file exists
    if not os.path.exists(log_path):
        error_msg = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Log Not Found</title>
    <style>
        body {{
            margin: 0;
            padding: 40px;
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        .error {{
            color: #f48771;
            border: 1px solid #f48771;
            padding: 20px;
            border-radius: 5px;
        }}
        a {{
            color: #007acc;
        }}
    </style>
</head>
<body>
    <div class="error">
        <h2>Log File Not Found</h2>
        <p>The log file at <code>{log_path}</code> does not exist yet.</p>
        <p>Please ensure the application is running and generating logs.</p>
        <p><a href="/">Back to Home</a></p>
    </div>
</body>
</html>"""
        return error_msg, 404

    # Check if this is a download request
    download = request.args.get('download', 'false').lower() == 'true'

    if download:
        # Return full file as download
        return send_file(
            log_path,
            mimetype='text/plain',
            as_attachment=True,
            download_name=f'{log_type}-app.log'
        )

    # Get number of lines to display
    lines = request.args.get('lines', config.DEFAULT_LINES, type=int)

    # Read last N lines
    content = read_last_n_lines(log_path, lines)

    # Generate HTML page
    html = generate_html_page(content, log_type, lines, config.REFRESH_INTERVAL)

    response = make_response(html)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response


if __name__ == '__main__':
    print(f"Starting log viewer server on http://0.0.0.0:{config.PORT}")
    print(f"Username: {config.USERNAME}")
    print(f"Password: {config.PASSWORD}")
    print(f"\nAvailable endpoints:")
    print(f"  - http://localhost:{config.PORT}/logs-dev")
    print(f"  - http://localhost:{config.PORT}/logs-main")

    app.run(host='0.0.0.0', port=config.PORT, debug=False)
