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
            self.wfile.write(b'OK - Container is running')
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
