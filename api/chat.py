import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def handler(request):
    try:
        body = json.loads(request.get("body", "{}"))
        user_message = body.get("message", "")

        if not user_message:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No message provided"})
            }

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a veterinary assistant specialized in sterilization and clinic procedures."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"response": reply})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }