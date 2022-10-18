from rest_framework import serializers
from bonds.models import Bond
from bonds.utils import GetExchangeRate
from decimal import Decimal

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        if self.context and self.context.get('exchange_rate'):
            new_price = Decimal(ret['price']) / Decimal(self.context['exchange_rate'])
            ret['price'] = str(new_price)

        return ret

class SellActionSerializer(serializers.Serializer):
    type_of_bound = serializers.RegexField(regex=r'^[a-zA-Z0-9]+$', max_length=40, min_length=3)
    quantity = serializers.IntegerField(max_value=10000, min_value=1)
    global_price = serializers.DecimalField(max_digits=13, decimal_places=4, max_value=100000000, min_value=0)
