from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

    url: api/categories/
    """
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name']


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id='Get Category', operation_description='Endpoint to get the category object using slug'))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_id='Update Category', operation_description='Endpoint to Update category'))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_id='Category Partial Update', operation_description='Endpoint to Update category partially'))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_id='Delete Category', operation_description='Endpoint to Delete category'))
class CategoryRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Endpoint to get category by slug, update category and delete category.

    url: api/categories/<slug>/
    """
    queryset = Category.objects.prefetch_related('products').all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id='Products List', operation_description='Endpoint to get the list of products ordered by latest'))
@method_decorator(name='post', decorator=swagger_auto_schema(
    operation_id='Create Product', operation_description='Endpoint to create a product'))
class ProductListCreate(ListCreateAPIView):
    """
    Endpoint to get the list of products ordered by -timestamp and create product.

    url: api/products/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']
    pagination_class = StandardResultsPagination


@method_decorator(name='get', decorator=swagger_auto_schema(
    operation_id='Get Product', operation_description='Endpoint to get the product object using slug'))
@method_decorator(name='put', decorator=swagger_auto_schema(
    operation_id='Update Product', operation_description='Endpoint to Update product'))
@method_decorator(name='patch', decorator=swagger_auto_schema(
    operation_id='Partial Product Update', operation_description='Endpoint to Update product partially'))
@method_decorator(name='delete', decorator=swagger_auto_schema(
    operation_id='Delete Product', operation_description='Endpoint to Delete product'))
class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Endpoint to get product by slug, update product and delete product.

    url: api/products/<slug>/
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    vector = SearchVector('name', weight='A') + SearchVector('description', weight='B')
    query = SearchQuery(query)
    if query:
        products = Product.objects.annotate(rank=SearchRank(
            vector, query, cover_density=True)).filter(rank__gte=0.2).order_by('-rank')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    return Response({"product": []})
