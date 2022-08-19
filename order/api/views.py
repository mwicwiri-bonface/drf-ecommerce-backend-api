import stripe
from django.conf import settings
from django.db.models import Sum
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view, authentication_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.api.serializers import OrderSerializer
from order.models import Order


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def checkout(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(
            item.get('quantity') * item.get('product').price for item in serializer.validated_data['items']
        )
        print("THis is paid amount >>>>", paid_amount)
        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='usd',
                description='Charge from jackets',
                source=serializer.validated_data['stripe_token'],
            )
            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except stripe.error.CardError as e:
            return Response(e.json_body, status=e.http_status)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
