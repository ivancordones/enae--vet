from http.server import BaseHTTPRequestHandler
import json
import os

try:
    from openai import OpenAI
except Exception as e:
    OpenAI = None
    IMPORT_ERROR = str(e)
else:
    IMPORT_ERROR = None


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
            if OpenAI is None:
                self._send_json(500, {"error": f"OpenAI import failed: {IMPORT_ERROR}"})
                return

            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                self._send_json(500, {"error": "OPENAI_API_KEY is missing in Vercel"})
                return

            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(raw_body.decode("utf-8"))
            user_message = (data.get("message") or "").strip()

            if not user_message:
                self._send_json(400, {"error": "No message provided"})
                return

            client = OpenAI(api_key=api_key)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are ENAE VET, a veterinary assistant. Answer clearly and briefly."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            reply = response.choices[0].message.content
            self._send_json(200, {"response": reply})

        except Exception as e:
            self._send_json(500, {"error": str(e)})