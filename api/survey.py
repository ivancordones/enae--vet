import json


def handler(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body or "{}")
        except Exception:
            body = {}

        answer = body.get("answer", "")
        print("SURVEY RESPONSE:", answer)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Survey received successfully"})
        }

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": "Survey API is running"})
    }