from django.urls import path
from .views import (ProductsListAPIView,
                    CategoriesListAPIView,
                    ProductsInCartAPIView,
                    ProductsOfCategoryAPIView,
                    ProductDetailApiView
                    )

app_name = 'catalog'

urlpatterns = [
    path('product/', ProductsListAPIView.as_view(), name='products_list'),
    path('product/<int:product_id>', ProductDetailApiView.as_view(), name='product_detail'),
    path('product/cart/', ProductsInCartAPIView.as_view(), name='products_in_cart'),
    path('category/', CategoriesListAPIView.as_view(), name='categories_list'),
    path('category/<int:category_id>', ProductsOfCategoryAPIView.as_view(), name='category_detail')
]
