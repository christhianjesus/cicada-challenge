import requests
import io
from rest_framework.parsers import JSONParser
from bonds.serializers import SieAPISerializer

def getExchangeRatet():
    headers = {'Bmx-Token' : 'a604e7bef5edb4958e6903e10a0fa6596b9e109eb583fb793458707aec01c9ab'}
    response = requests.get('https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno', headers=headers)
    s = SieAPISerializer(data=response.json())
    s.is_valid()

    return s.validated_data.bmx.series[0].datos[0].dato