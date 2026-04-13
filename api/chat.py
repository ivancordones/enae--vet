from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/chat", methods=["GET"])
def health():
    return jsonify({"ok": True, "message": "chat route is alive"})