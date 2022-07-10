from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

from product.api.pagination import StandardResultsPagination
from product.api.serializers import CategorySerializer, ProductSerializer
from product.models import Category, Product


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id='Categories List', operation_description='Endpoint to get the list of categories ordered by name'))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id='Category Create', operation_description='Endpoint to create a category'))
class CategoryListCreate(ListCreateAPIView):
    """
    Endpoint to get the list of categories ordered by name and create category.

    url: api/super-admin-portal/clients/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductListCreate(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = StandardResultsPagination


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
