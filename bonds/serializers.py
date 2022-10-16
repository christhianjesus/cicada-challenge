from rest_framework import serializers
from .models import Bond

class BondSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bond
        fields = '__all__'

class SellActionSerializer(serializers.Serializer):
    type_of_bound = serializers.RegexField(regex=r'^[a-zA-Z0-9]+$', max_length=40, min_length=3)
    quantity = serializers.IntegerField(max_value=10000, min_value=1)
    global_price = serializers.DecimalField(max_digits=13, decimal_places=4, max_value=100000000, min_value=0)



class dataSerializer(serializers.Serializer):
    fecha = serializers.CharField()
    dato = serializers.DecimalField()

class serieSerializer(serializers.Serializer):
    idSerie = serializers.CharField()
    titulo = serializers.CharField()
    datos = dataSerializer(many=True)

class bmxSerializer(serializers.Serializer):
    series = serieSerializer(many=True)

class SieAPISerializer(serializers.Serializer):
    bmx = bmxSerializer()