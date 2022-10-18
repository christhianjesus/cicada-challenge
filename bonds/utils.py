import os
import requests
from decimal import Decimal

def GetExchangeRate():
    headers = {'Bmx-Token' : os.environ.get('SIE_TOKEN')}
    response = requests.get(os.environ.get('SIE_URL'), headers=headers)
    data=response.json()

    return data["bmx"]["series"][0]["datos"][0]["dato"]