from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductsListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class ProductsInCartAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        products = Product.objects.filter(id__in=request.data['products_ids'])
        serializer = ProductSerializer(products, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class CategoriesListAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class ProductsOfCategoryAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_id):
        products = Product.objects.filter(categories=category_id)
        serializer = ProductSerializer(products, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class ProductDetailApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SearchProductsAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        search_query = request.GET.get('search')
        print(search_query)
        list_of_products = Product.objects.filter(name__icontains=search_query)
        if len(list_of_products) > 10:
            list_of_products = list_of_products[:10]

        serializer = ProductSerializer(list_of_products, many=True)

        if list_of_products:
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Ничего не найдено'}, status=status.HTTP_404_NOT_FOUND)
