from rest_framework import status,viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Bond
from .serializers import BondSerializer, SellActionSerializer

class BondViewSet(mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def sell(self, request):
        user = self.request.user
        serializer = SellActionSerializer(data=request.data)
        if serializer.is_valid():
            type_of_bound = serializer.validated_data['type_of_bound']
            quantity = serializer.validated_data['quantity']
            price = serializer.validated_data['global_price'] / quantity

            for _ in range(quantity):
                bond = Bond(owner=user, type=type_of_bound, price=price)
                bond.save()

            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def buy(self, request, pk=None):
        bond = self.get_object()
        if bond.buyer is None:
            bond.buyer = self.request.user
            bond.save()

            return Response({'status': 'ok'})
        else:
            return Response({'status': 'error', 'msg': 'invalid operation'},
                            status=status.HTTP_400_BAD_REQUEST)
