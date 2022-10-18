import pytest

from collections import OrderedDict
from decimal import Decimal
from model_bakery import baker
from django.contrib.auth.models import User

from bonds.serializers import BondSerializer, SellActionSerializer

class TestBondSerializer:

    def test_serialize_model(self):
        bond = baker.prepare('bonds.Bond', owner=None)
        serializer = BondSerializer(bond)
        
        expected_serialized_data = {
            'id': None,
            'owner': None,
            'buyer': bond.buyer,
            'type': bond.type,
            'price': str(bond.price),
            'created': bond.created,
            'updated': bond.updated,
        }

        assert serializer.data == expected_serialized_data

    def test_serialize_model_usd(self):
        bond = baker.prepare('bonds.Bond', owner=None)
        exchange_rate = Decimal('19.11')
        serializer = BondSerializer(bond, context={'exchange_rate': str(exchange_rate)})
        
        expected_serialized_data = {
            'id': None,
            'owner': None,
            'buyer': bond.buyer,
            'type': bond.type,
            'price': str(bond.price / exchange_rate),
            'created': bond.created,
            'updated': bond.updated,
        }

        assert serializer.data == expected_serialized_data

    @pytest.mark.django_db
    def test_serialized_data(self, mocker):
        user = baker.make(User)
        bond = baker.prepare('bonds.Bond', owner=user)

        valid_serialized_data  = {
            'id': bond.id,
            'owner': bond.owner.id,
            'buyer': bond.buyer,
            'type': bond.type,
            'price': str(bond.price),
            'created': bond.created,
            'updated': bond.updated,
        }

        serializer = BondSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}


class TestSellActionSerializer:

    def test_serialize_repr(self):
        internal_repr = OrderedDict([('type_of_bound', 'sometype'), ('quantity', 1), ('global_price', Decimal('1.0000'))])
        serializer = SellActionSerializer(internal_repr)

        expected_serialized_data = {
            'type_of_bound': internal_repr['type_of_bound'],
            'quantity': internal_repr['quantity'],
            'global_price': str(internal_repr['global_price']),
        }

        assert serializer.data == expected_serialized_data

    def test_serialized_data(self):
        internal_repr = OrderedDict([('type_of_bound', 'sometype'), ('quantity', 1), ('global_price', Decimal('1.0000'))])

        valid_serialized_data = {
            'type_of_bound': internal_repr['type_of_bound'],
            'quantity': internal_repr['quantity'],
            'global_price': str(internal_repr['global_price'])
        }
        serializer = SellActionSerializer(data=valid_serialized_data)

        assert serializer.is_valid(raise_exception=True)
        assert serializer.errors == {}
