# Health Check HTTP Server

A lightweight Python HTTP server designed to provide health check endpoints for monitoring applications, particularly useful for containerized RQ (Redis Queue) workers.

## Features

- Simple HTTP server with health check endpoints
- Configurable port via environment variable
- Reduced logging noise (logs every 10th request)
- Returns 200 OK status for health checks
- Minimal dependencies (uses Python standard library)

## Endpoints

- `GET /health` - Returns `200 OK` with message "OK - RQ Worker is running"
- `GET /` - Returns `200 OK` with message "OK - RQ Worker is running"
- All other paths return `404 Not Found`

## Usage

### Basic Usage

```bash
python health_check.py
```

By default, the server listens on port 8080.

### Custom Port

Set the `PORT` environment variable to use a different port:

```bash
PORT=8000 python health_check.py
```

### Docker/Container Usage

```dockerfile
# Example Dockerfile snippet
ENV PORT=8080
CMD ["python", "health_check.py"]
```

The script can be easily integrated into Docker containers to provide health check endpoints for orchestration tools like Kubernetes. It can be added to the entrypoint or command section of your Dockerfile.

Example in entrypoint script for starting both the RQ (Redis Queue) worker and the health check server:

```bash
echo ""
echo "=========================================="
echo "Starting Health Check Server"
echo "=========================================="
# Start a simple HTTP server in the background for Cloud Run health checks
# This runs in the background so the RQ worker can run in the foreground
cat > /tmp/health_server.py << 'HEALTH_SERVER_SCRIPT'
import http.server
import socketserver
import os
import sys

PORT = int(os.environ.get('PORT', 8080))

class HealthCheckHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK - RQ Worker is running')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Only log health check requests every 10th time to reduce noise
        if not hasattr(self.server, 'request_count'):
            self.server.request_count = 0
        self.server.request_count += 1
        if self.server.request_count % 10 == 0:
            sys.stdout.write('[Health Check #%d] %s - - [%s] %s\n' %
                           (self.server.request_count,
                            self.address_string(),
                            self.log_date_time_string(),
                            format % args))
            sys.stdout.flush()

with socketserver.TCPServer(('', PORT), HealthCheckHandler) as httpd:
    print(f'Health check server listening on port {PORT}', flush=True)
    httpd.serve_forever()
HEALTH_SERVER_SCRIPT

# Start the health check server in the background
python /tmp/health_server.py &
HEALTH_PID=$!

# Give the health server a moment to start
sleep 2

echo "✓ Health check server started on port ${PORT:-8080} (PID: $HEALTH_PID)"
```

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `PORT` | 8080 | The port on which the server listens |

## Logging

The server implements smart logging to reduce noise:

- Only every 10th health check request is logged
- Each logged entry includes a request counter
- Format: `[Health Check #N] IP - - [timestamp] request_info`

This is particularly useful in containerized environments where health checks may occur very frequently.

## Requirements

- Python 3.x (uses standard library only)

## Use Cases

- Kubernetes/Docker container health checks
- Celery or RQ worker monitoring
- Simple service availability checks
- Development environment health endpoints
