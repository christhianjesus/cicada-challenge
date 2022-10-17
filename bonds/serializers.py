from rest_framework import serializers
from .models import Bond
import requests
import decimal

def GetExchangeRate():
    headers = {'Bmx-Token' : 'a604e7bef5edb4958e6903e10a0fa6596b9e109eb583fb793458707aec01c9ab'}
    response = requests.get('https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno', headers=headers)
    s = SieAPISerializer(data=response.json())
    s.is_valid()

    return s.validated_data["bmx"]["series"][0]["datos"][0]["dato"]

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if "exchange" in self.context['request'].query_params:
            exchange = GetExchangeRate()
            ret['price'] = decimal.Decimal(ret['price']) / exchange

        return ret

class SellActionSerializer(serializers.Serializer):
    type_of_bound = serializers.RegexField(regex=r'^[a-zA-Z0-9]+$', max_length=40, min_length=3)
    quantity = serializers.IntegerField(max_value=10000, min_value=1)
    global_price = serializers.DecimalField(max_digits=13, decimal_places=4, max_value=100000000, min_value=0)

class dataSerializer(serializers.Serializer):
    fecha = serializers.CharField()
    dato = serializers.DecimalField(max_digits=13, decimal_places=4)

class serieSerializer(serializers.Serializer):
    idSerie = serializers.CharField()
    titulo = serializers.CharField()
    datos = dataSerializer(many=True)

class bmxSerializer(serializers.Serializer):
    series = serieSerializer(many=True)

class SieAPISerializer(serializers.Serializer):
    bmx = bmxSerializer()