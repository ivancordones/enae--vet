from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request

class handler(BaseHTTPRequestHandler):

    def _send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        self._send_json(200, {"ok": True, "message": "chat route is alive"})

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            user_message = data.get("message", "")

            api_key = os.environ.get("GEMINI_API_KEY")

            if not api_key:
                self._send_json(500, {"error": "Missing GEMINI_API_KEY"})
                return

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": f"You are a veterinary assistant. {user_message}"}
                        ]
                    }
                ]
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode())

            reply = result["candidates"][0]["content"]["parts"][0]["text"]

            self._send_json(200, {"response": reply})

        except Exception as e:
            self._send_json(500, {"error": str(e)})