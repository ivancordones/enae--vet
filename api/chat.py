import json
import os
from typing import Dict, List

from openai import OpenAI

SYSTEM_PROMPT = """
You are ENAE VET, a veterinary clinic assistant specialized in helping users
with sterilization and castration appointment questions.

Rules:
- Be helpful, clear, and calm.
- Do not diagnose.
- Focus on sterilization, castration, preparation, and scheduling guidance.
- If the situation sounds urgent, recommend contacting the clinic or an emergency vet.
- Keep responses short and practical.
""".strip()

SESSION_HISTORY: Dict[str, List[dict]] = {}

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

RAW_DOCS = [
    "The clinic is specialized in sterilization and castration for dogs and cats.",
    "Before surgery, pets should fast for 8 to 12 hours. Water is allowed until 1 to 2 hours before surgery.",
    "Dogs cannot be sterilized while in heat. They should usually wait around two months after the end of heat.",
    "For animals older than 6 years, preoperative bloodwork is required before surgery.",
    "Approximate pick-up time is 12:00 for dogs and 15:00 for cats.",
    "If the pet has active bleeding, pale gums, breathing difficulty, or does not respond well after surgery, the clinic or an emergency veterinary service should be contacted immediately.",
]


def retrieve_context(message: str) -> str:
    message_lower = message.lower()
    matches = []

    for doc in RAW_DOCS:
        doc_lower = doc.lower()
        if any(word in doc_lower for word in message_lower.split()):
            matches.append(doc)

    if not matches:
        matches = RAW_DOCS[:2]

    return "\n\n".join(matches[:3])


def handler(request):
    if request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps({"ok": True}),
        }

    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Method not allowed"}),
        }

    if not os.environ.get("OPENAI_API_KEY"):
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "OPENAI_API_KEY is not configured"}),
        }

    try:
        body = json.loads(request.body or "{}")
    except Exception:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Invalid JSON body"}),
        }

    message = (body.get("message") or "").strip()
    session_id = (body.get("session_id") or "default").strip()

    if not message:
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "message must not be empty"}),
        }

    history = SESSION_HISTORY.get(session_id, [])
    context = retrieve_context(message)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history[-10:])
    messages.append(
        {
            "role": "user",
            "content": f"Clinic context:\n{context}\n\nUser question: {message}",
        }
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
        )
        reply = completion.choices[0].message.content or "I could not generate a response."
    except Exception as exc:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": f"OpenAI request failed: {str(exc)}"}),
        }

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": reply})
    SESSION_HISTORY[session_id] = history

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(
            {
                "response": reply,
                "session_id": session_id,
                "context_used": context,
            }
        ),
    }  