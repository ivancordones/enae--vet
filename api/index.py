from flask import Flask, jsonify, request
import os
from openai import OpenAI

app = Flask(__name__)

@app.route("/api/chat", methods=["GET", "POST"])
def chat():
    try:
        if request.method == "GET":
            return jsonify({"ok": True, "message": "chat route is alive"})

        data = request.get_json(silent=True) or {}
        user_message = (data.get("message") or "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are ENAE VET, a veterinary assistant specialized in sterilization, castration, surgical preparation, and clinic logistics."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return jsonify({"response": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500