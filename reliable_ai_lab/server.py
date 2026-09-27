"""A loopback-only demo server, not a production deployment server."""
from __future__ import annotations
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from importlib.resources import files
from urllib.parse import urlsplit, parse_qs
from .common import integer
from .registry import PROJECTS, get_project
from .__main__ import reject_nonfinite

MAX_BODY = 5_000_000


class Handler(BaseHTTPRequestHandler):
    server_version = "ReliableAILab/0.1"

    def allowed_request(self):
        port = self.server.server_port
        hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
        origin = self.headers.get("Origin")
        return (self.headers.get("Host") in hosts and
                (origin is None or origin in {f"http://{host}" for host in hosts}) and
                self.headers.get("Sec-Fetch-Site") != "cross-site")

    def send(self, status, value, html=False):
        body = value.encode("utf-8") if html else json.dumps(value, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8" if html else "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if not self.allowed_request():
            self.send(403, {"error": "Only same-origin loopback requests are accepted"})
            return
        parts = urlsplit(self.path)
        if parts.path == "/":
            self.send(200, files("reliable_ai_lab").joinpath("web/index.html").read_text(encoding="utf-8"), html=True)
        elif parts.path == "/api/projects":
            self.send(200, PROJECTS)
        elif parts.path.startswith("/api/sample/"):
            try:
                name = parts.path.removeprefix("/api/sample/")
                seed = int(parse_qs(parts.query).get("seed", ["7"])[0])
                seed = integer(seed, "seed", 0, 1000000)
                self.send(200, get_project(name).sample(seed))
            except (ValueError, KeyError, TypeError) as exc:
                self.send(400, {"error": str(exc)})
        else:
            self.send(404, {"error": "Not found"})

    def do_POST(self):
        if not self.allowed_request() or self.headers.get("X-Lab-Request") != "1":
            self.send(403, {"error": "Same-origin requests with X-Lab-Request: 1 are required"})
            return
        if self.headers.get("Content-Type", "").split(";")[0].strip() != "application/json":
            self.send(415, {"error": "Content-Type must be application/json"})
            return
        parts = urlsplit(self.path)
        if not parts.path.startswith("/api/run/"):
            self.send(404, {"error": "Not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= MAX_BODY:
                raise ValueError("Body must be nonempty and at most 5 MB")
            raw = self.rfile.read(length)
            payload = json.loads(raw, parse_constant=reject_nonfinite)
            if not isinstance(payload, dict):
                raise ValueError("Input JSON must be an object")
            result = get_project(parts.path.removeprefix("/api/run/")).run(payload)
            self.send(200, result)
        except (ValueError, TypeError, KeyError, OverflowError) as exc:
            self.send(400, {"error": str(exc)})
        except Exception:
            self.send(500, {"error": "The experiment failed; use the CLI and inspect the input locally"})

    def log_message(self, format, *args):
        # Do not print request bodies or source documents.
        return


class LocalServer(HTTPServer):
    def get_request(self):
        sock, address = super().get_request()
        sock.settimeout(20)
        return sock, address


def serve(port=8765):
    port = integer(port, "port", 1024, 65535)
    with LocalServer(("127.0.0.1", port), Handler) as server:
        print(f"Reliable AI Lab: http://127.0.0.1:{port} (local only; Ctrl+C to stop)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
