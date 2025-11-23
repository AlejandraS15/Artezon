import time
import requests

def random_quote():
    try:
        response = requests.get("http://api.quotable.io/quotes/random?maxLength=50", timeout=4)
        response.raise_for_status()
        return response.json()[0]["content"]
    except:
        return None

def get_random_quote(request):
    last_time = request.session.get("quote_time")
    now = int(time.time())

    if not last_time or now - last_time > 600:
        request.session["quote"] = random_quote()
        request.session["quote_time"] = now

    return {"quote": request.session.get("quote")}
