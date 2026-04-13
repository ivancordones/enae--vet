from http.server import BaseHTTPRequestHandler
import json
import os
import urllib.request
import urllib.error

class handler(BaseHTTPRequestHandler):

    def _send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_GET(self):
        self._send_json(200, {
            "ok": True,
            "message": "chat route is alive"
        })

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(body.decode("utf-8"))

            user_message = (data.get("message") or "").strip()
            if not user_message:
                self._send_json(400, {"error": "No message provided"})
                return

            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self._send_json(500, {"error": "Missing GEMINI_API_KEY"})
                return

            model = "gemini-2.5-flash"
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": (
                                    "You are ENAE VET, a veterinary assistant specialized in "
                                    "sterilization, castration, preparation and clinic logistics. "
                                    f"User question: {user_message}"
                                )
                            }
                        ]
                    }
                ]
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))

            reply = result["candidates"][0]["content"]["parts"][0]["text"]
            self._send_json(200, {"response": reply})

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            self._send_json(e.code, {"error": f"Gemini HTTP {e.code}: {error_body}"})

        except Exception as e:
            self._send_json(500, {"error": str(e)})