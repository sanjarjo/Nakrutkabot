import requests
from config import API_URL, API_KEY

def create_order_panel(service_id, link, quantity):
    payload = {
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": quantity,
        "key": API_KEY
    }
    try:
        r = requests.post(API_URL, data=payload, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}

def check_status_panel(panel_order_id):
    params = {
        "action": "status",
        "order": panel_order_id,
        "key": API_KEY
    }
    try:
        r = requests.get(API_URL, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}
