from __future__ import annotations

import os
from typing import Any, Optional

from flask import Flask, jsonify, render_template_string, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>ENAE VET Simple Chatbot (SCRUM-6)</title>
  </head>
  <body>
    <h1>Simple Chatbot (SCRUM-6)</h1>
    <p>This is a minimal HTML page to exercise the Flask + LangChain chatbot.</p>
    <form id="chat-form">
      <input type="text" id="message" name="message" placeholder="Write your message..." />
      <button type="submit">Send</button>
    </form>
    <pre id="reply"></pre>
    <script>
      const form = document.getElementById("chat-form");
      const input = document.getElementById("message");
      const replyEl = document.getElementById("reply");

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = input.value.trim();
        if (!message) {
          replyEl.textContent = "Please enter a message.";
          return;
        }

        try {
          const response = await fetch("/ask_bot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
          });
          const data = await response.json();
          if (data.reply) {
            replyEl.textContent = data.reply;
          } else if (data.error) {
            replyEl.textContent = "Error: " + data.error;
          } else {
            replyEl.textContent = "Unexpected response.";
          }
        } catch (error) {
          replyEl.textContent = "Network error: " + error;
        }
      });
    </script>
  </body>
</html>
"""


def _build_chain() -> Any:
  """Create the minimal LangChain chain for the chatbot.

  The chain:
  - Uses only the user's current message as input.
  - Has no system prompt.
  - Does not use memory, tools, or RAG.
  """
  if not os.getenv("OPENAI_API_KEY"):
      raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

  prompt = ChatPromptTemplate.from_messages(
      [
          ("human", "{input}"),
      ]
  )
  llm = ChatOpenAI(model="gpt-4o-mini")

  return prompt | llm


def create_app(chain: Optional[Any] = None) -> Flask:
  """Create and configure the Flask application.

  The optional ``chain`` parameter allows tests to inject a fake or mocked
  LangChain runnable so that no real LLM calls are made in CI.
  """
  app = Flask(__name__)

  if chain is None:
      try:
          chain = _build_chain()
      except Exception:
          chain = None

  app.config["BOT_CHAIN"] = chain

  @app.get("/")
  def index() -> str:
      """Serve a minimal HTML chat page."""
      return render_template_string(HTML_TEMPLATE)

  @app.post("/ask_bot")
  def ask_bot() -> Any:
      """Receive the user message, call the chain, and return the reply."""
      data = request.get_json(silent=True) or {}
      message = (data.get("message") or "").strip()

      if not message:
          return jsonify({"error": "message must not be empty"}), 400

      bot_chain: Optional[Any] = app.config.get("BOT_CHAIN")
      if bot_chain is None:
          return (
              jsonify(
                  {"error": "Chatbot is not configured. Check OPENAI_API_KEY."}
              ),
              500,
          )

      try:
          result = bot_chain.invoke({"input": message})
      except Exception as exc:
          return (
              jsonify(
                  {
                      "error": (
                          "Failed to get response from chatbot. "
                          f"Underlying error: {exc}"
                      )
                  }
              ),
              500,
          )

      content = getattr(result, "content", str(result))
      return jsonify({"reply": content})

  return app


app = create_app()


if __name__ == "__main__":
  # Simple development server; in production this would typically be run
  # behind a dedicated WSGI/ASGI server or reverse proxy.
  app.run(host="0.0.0.0", port=5000, debug=True)

