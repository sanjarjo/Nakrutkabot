import requests
from config import SMM_API_URL, SMM_API_KEY

def create_order(service_id, link, quantity):
    """
    SMM panelga buyurtma yuboradi
    service_id : paneldagi xizmat ID
    link : foydalanuvchi yuborgan link
    quantity : buyurtma miqdori
    """
    payload = {
        'action': 'add',
        'service': service_id,
        'link': link,
        'quantity': quantity,
        'key': SMM_API_KEY
    }
    try:
        response = requests.post(SMM_API_URL, data=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('error'):
            return {'success': False, 'error': data['error']}
        return {'success': True, 'order_id': data.get('order')}
    except requests.RequestException as e:
        return {'success': False, 'error': str(e)}

def check_order_status(panel_order_id):
    """
    Paneldan buyurtma statusini oladi
    panel_order_id : SMM paneldagi order ID
    """
    payload = {
        'action': 'status',
        'order': panel_order_id,
        'key': SMM_API_KEY
    }
    try:
        response = requests.get(SMM_API_URL, params=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('error'):
            return {'success': False, 'error': data['error']}
        return {
            'success': True,
            'status': data.get('status'),
            'start_count': data.get('start_count'),
            'remains': data.get('remains')
        }
    except requests.RequestException as e:
        return {'success': False, 'error': str(e)}

def get_services():
    """
    Paneldagi xizmatlarni olish
    E'tibor: biz faqat kerakli xizmat ID larini olamiz
    """
    payload = {
        'action': 'services',
        'key': SMM_API_KEY
    }
    try:
        response = requests.get(SMM_API_URL, params=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('error'):
            return {'success': False, 'error': data['error']}
        return {'success': True, 'services': data}
    except requests.RequestException as e:
        return {'success': False, 'error': str(e)}
