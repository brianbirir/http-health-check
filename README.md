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
- RQ worker monitoring
- Simple service availability checks
- Development environment health endpoints
