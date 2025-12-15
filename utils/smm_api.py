import requests
from config import SMM_API_URL, SMM_API_KEY

def create_order(service_id: int, link: str, quantity: int):
    payload = {
        "key": SMM_API_KEY,
        "action": "add",
        "service": service_id,
        "link": link,
        "quantity": quantity
    }

    r = requests.post(SMM_API_URL, data=payload, timeout=30)
    return r.json()


def order_status(order_id: int):
    payload = {
        "key": SMM_API_KEY,
        "action": "status",
        "order": order_id
    }

    r = requests.post(SMM_API_URL, data=payload, timeout=30)
    return r.json()


def balance():
    payload = {
        "key": SMM_API_KEY,
        "action": "balance"
    }

    r = requests.post(SMM_API_URL, data=payload, timeout=30)
    return r.json()
