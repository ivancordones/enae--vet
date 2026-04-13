import time

for attempt in range(3):
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            break
    except urllib.error.HTTPError as e:
        if e.code == 503 and attempt < 2:
            time.sleep(2)
        else:
            raise