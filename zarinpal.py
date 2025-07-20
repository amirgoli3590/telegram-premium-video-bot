import requests
import os

MERCHANT_ID = os.environ.get('ZARINPAL_MERCHANT_ID')
CALLBACK_URL = 'https://api.telegram.org'

def create_payment_link(user_id):
    data = {
        "MerchantID": MERCHANT_ID,
        "Amount": 10000,
        "CallbackURL": CALLBACK_URL,
        "Description": f"خرید اشتراک توسط {user_id}"
    }
    response = requests.post('https://api.zarinpal.com/pg/v4/payment/request.json', json=data)
    res = response.json()
    if res['data']['code'] == 100:
        link = f"https://www.zarinpal.com/pg/StartPay/{res['data']['authority']}"
        return link, res['data']['authority']
    return None, None

def verify_payment(authority):
    response = requests.post('https://api.zarinpal.com/pg/v4/payment/verify.json', json={
        "MerchantID": MERCHANT_ID,
        "Amount": 10000,
        "Authority": authority
    })
    res = response.json()
    return res['data']['code'] == 100
