"""Simple health endpoint for Vercel deployment checks."""

from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    """Vercel-compatible health handler."""

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "service": "enae-vet-chatbot"}).encode("utf-8"))
