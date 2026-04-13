from http.server import BaseHTTPRequestHandler
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body)

        user_message = data.get("message", "")

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a veterinary assistant."},
                    {"role": "user", "content": user_message}
                ]
            )

            reply = response.choices[0].message.content

        except Exception as e:
            reply = f"Error: {str(e)}"

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({
            "response": reply
        }).encode("utf-8"))