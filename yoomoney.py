from yookassa import Configuration
from yookassa import Payout
from yookassa.domain.models.currency import Currency
import requests
import uuid
import json

account_id='505279'
secret_key='test_*gtBL0HwCla35kCv5n_o7JlpgWwt7zUAPt53x1rnXKTT4'

Configuration.account_id = account_id
Configuration.secret_key = secret_key

#В тестовом режиме выплаты только на yoo_money, при переходе на официал, заменить 
# 'payout_destination_data': {
#        'type': 'bank_card',
#        'card': {
#            'number': str(cardnumber),
#        },
def CreatePayout(value, cardnumber:str, description:str, Login:str):
    idempotence_key = str(uuid.uuid4())
    try:
        res = Payout.create({
            'amount': {
                'value': str(value),
                'currency': Currency.RUB,
            },
            'payout_destination_data': {
                'type': 'yoo_money',
                'account_number': str(cardnumber),
            },
            'description': description,
            'metadata': {
                'userLogin': Login,
            },
        })
    except Exception as ex:
        return ex
    return dict(json.loads(res.json()))

def GetPayout(uuid):
    try:
        res = Payout.find_one(uuid)
    except Exception as ex:
        return ex
    return dict(json.loads(res.json()))

#print(CreatePayout(100, '4100116075156746', 'Тестовая выплата', 'Login'))
#print(GetPayout('po-2d4c7dd7-0003-5000-a000-05382ac28a77'))