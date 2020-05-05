from decimal import Decimal

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Order, OrderItem
from user.models import User
from promo_code.models import PromoCode
from localization.models import City
from catalog.models import Product
from .serializers import OrderSerializer


# Create your views here.
class CreateOrderAPIView(APIView):

    @staticmethod
    def __get_or_create_user(email, phone, full_name):

        try:
            user = User.objects.get(email=email)
            return user

        except User.DoesNotExist:
            new_user = User.create_user_with_default_password(
                email=email,
                phone=phone,
                full_name=full_name
            )
            return new_user

    @staticmethod
    def __get_or_none_promo_code(request_promo_code):

        try:
            promo_code = PromoCode.objects.get(code=request_promo_code)
            return promo_code

        except PromoCode.DoesNotExist:
            return

    def post(self, request):

        email = request.data['email']
        phone = request.data['phone']
        full_name = request.data['fullName']
        user = self.__get_or_create_user(email, phone, full_name)
        city = City.objects.get(query_id=request.data['city'])
        promo_code = self.__get_or_none_promo_code(request.data['promoCode'])

        new_order = Order.objects.create(
            user=user,
            city=city,
            promo_code=promo_code,
            discount=request.data['discount'],
            total_price=request.data['totalPrice'],
            full_name=request.data['fullName'],
            phone=phone,
            email=email,
            delivery=request.data['delivery'],
            address=request.data.get('address', ''),
            entrance=request.data.get('entrance', ''),
            floor=request.data.get('floor', ''),
            apartment=request.data.get('apartment', ''),
            comments_from_client=request.data['comments'],
        )
        new_order.save()

        for item in request.data['itemsList']:
            item_product = Product.objects.get(id=item['id'])

            new_item = OrderItem.objects.create(
                order=new_order,
                product=item_product,
                price=Decimal(item['price']),
                quantity=int(item['quantity'])
            )

        # print(new_order.items)
        order = Order.objects.get(id=new_order.id)
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_200_OK)


def get(self, request):
    order = Order.objects.first()
    serializer = OrderSerializer(order)

    return Response(serializer.data, status=status.HTTP_200_OK)
