
from collections import OrderedDict
from decimal import Decimal
import json
import pytest

from django.urls import reverse
from django_mock_queries.mocks import MockSet
from rest_framework.relations import RelatedField, SlugRelatedField

from bonds.models import Bond
from bonds.serializers import BondSerializer, SellActionSerializer
from bonds.views import BondViewSet

from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

from model_bakery import baker

class TestBondViewset:

    def test_list(self, mocker, rf):
        url = reverse('bond-list')
        request = rf.get(url)
        user = baker.prepare(User)
        force_authenticate(request, user=user)
        qs = MockSet(
            baker.prepare('bonds.Bond', owner=None),
            baker.prepare('bonds.Bond', owner=None),
            baker.prepare('bonds.Bond', owner=None)
        )
        mocker.patch.object(
            BondViewSet, 'get_queryset', return_value=qs
        )
        view = BondViewSet.as_view(
            {'get': 'list'}
        )

        response = view(request).render()

        assert response.status_code == 200
        assert len(json.loads(response.content)) == 3

    def test_retrieve(self, mocker, rf):
        user = baker.prepare(User)
        bond = baker.prepare('bonds.Bond', owner=user)
        expected_json = {
            'id': bond.id,
            'type': bond.type,
            'price': str(bond.price),
            'created': bond.created,
            'updated': bond.updated,
            'owner': bond.owner.id,
            'buyer': None
        }
        url = reverse('bond-detail', kwargs={'pk': bond.id})
        request = rf.get(url)
        force_authenticate(request, user=user)
        mocker.patch.object(
            BondViewSet, 'get_queryset', return_value=MockSet(bond)
        )
        view = BondViewSet.as_view(
            {'get': 'retrieve'}
        )

        response = view(request, pk=bond.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json

    @pytest.mark.django_db
    def test_sell(self, mocker, rf):
        user = baker.make(User)
        url = reverse('bond-sell')
        quantity = 2
        valid_data_dict = {
            'type_of_bound': 'sometype',
            'quantity': quantity,
            'global_price': '1.0000',
        }
        expected_json = {
            'status': 'ok'
        }
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(valid_data_dict)
        )
        force_authenticate(request, user=user)
        mocker.patch.object(
            Bond, 'save'
        )
        view = BondViewSet.as_view(
            {'post': 'sell'}
        )
        spy = mocker.spy(Bond, 'save')

        response = view(request).render()


        assert response.status_code == 200
        assert spy.call_count == quantity
        assert json.loads(response.content) == expected_json

    @pytest.mark.django_db
    def test_sell_fail(self, mocker, rf):
        user = baker.make(User)
        url = reverse('bond-sell')
        quantity = -1
        valid_data_dict = {
            'type_of_bound': 'sometype//..--',
            'quantity': quantity,
            'global_price': '-1.0000',
        }
        expected_json = {
            'global_price': ['Ensure this value is greater than or equal to 0.'],
            'quantity': ['Ensure this value is greater than or equal to 1.'],
            'type_of_bound': ['This value does not match the required pattern.']
        }
        request = rf.post(
            url,
            content_type='application/json',
            data=json.dumps(valid_data_dict)
        )
        force_authenticate(request, user=user)
        view = BondViewSet.as_view(
            {'post': 'sell'}
        )

        response = view(request).render()


        assert response.status_code == 400
        assert json.loads(response.content) == expected_json

    @pytest.mark.django_db
    def test_buy(self, mocker, rf):
        user = baker.make(User)
        bond = baker.prepare('bonds.Bond', owner=user, buyer=None)
        expected_json = {
            'status': 'ok'
        }
        url = reverse('bond-buy', kwargs={'pk': bond.id})
        request = rf.post(url)
        force_authenticate(request, user=user)
        mocker.patch.object(
            BondViewSet, 'get_queryset', return_value=MockSet(bond)
        )
        view = BondViewSet.as_view(
            {'post': 'buy'}
        )

        response = view(request, pk=bond.id).render()

        assert response.status_code == 200
        assert json.loads(response.content) == expected_json
        assert bond.buyer

    @pytest.mark.django_db
    def test_buy_fail(self, mocker, rf):
        user = baker.make(User)
        bond = baker.prepare('bonds.Bond', owner=user, buyer=user)
        expected_json = {
            'status': 'error',
            'msg': 'invalid operation'
        }
        url = reverse('bond-buy', kwargs={'pk': bond.id})
        request = rf.post(url)
        force_authenticate(request, user=user)
        mocker.patch.object(
            BondViewSet, 'get_queryset', return_value=MockSet(bond)
        )
        view = BondViewSet.as_view(
            {'post': 'buy'}
        )

        response = view(request, pk=bond.id).render()

        assert response.status_code == 400
        assert json.loads(response.content) == expected_json
        assert bond.buyer