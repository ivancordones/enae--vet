from http.server import BaseHTTPRequestHandler
import json


def get_mock_response(message: str) -> str:
    text = message.lower().strip()

    if any(word in text for word in ["hola", "hello", "hi"]):
        return (
            "Hello! I am ENAE VET, your veterinary assistant. "
            "I can help you with sterilization, castration, preparation, and clinic logistics."
        )

    if any(word in text for word in ["sterilization", "spay", "neuter", "castration"]):
        return (
            "Before a sterilization procedure, the patient should usually have a clinical evaluation, "
            "preoperative fasting according to the veterinarian's guidance, and confirmation of general health status. "
            "The surgical area, sterile instruments, anesthesia plan, and monitoring equipment should also be prepared."
        )

    if any(word in text for word in ["fasting", "ayuno", "preparation", "preparación"]):
        return (
            "Preoperative preparation typically includes fasting instructions, hydration assessment, "
            "physical examination, anesthetic planning, and confirmation that the surgical instruments "
            "and recovery area are ready."
        )

    if any(word in text for word in ["clinic", "logistics", "quirófano", "surgical room"]):
        return (
            "Clinic logistics for surgery usually include confirming patient records, sterile material availability, "
            "anesthesia supplies, surgical instruments, staff coordination, postoperative recovery space, "
            "and monitoring equipment readiness."
        )

    if any(word in text for word in ["dog", "perra", "perro", "cat", "gato", "gatta"]):
        return (
            "For dogs and cats, surgical preparation generally includes evaluation by the veterinarian, "
            "fasting instructions, sterile field preparation, anesthesia planning, and postoperative monitoring."
        )

    return (
        "I can help with topics related to sterilization, castration, preoperative preparation, "
        "and veterinary clinic logistics. Please ask a more specific question."
    )


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
            raw_body = self.rfile.read(content_length) if content_length > 0 else b"{}"
            data = json.loads(raw_body.decode("utf-8"))

            user_message = (data.get("message") or "").strip()
            if not user_message:
                self._send_json(400, {"response": "No message provided."})
                return

            reply = get_mock_response(user_message)
            self._send_json(200, {"response": reply})

        except Exception as e:
            self._send_json(200, {
                "response": "The assistant is temporarily unavailable, but the chat route is working correctly."
            })