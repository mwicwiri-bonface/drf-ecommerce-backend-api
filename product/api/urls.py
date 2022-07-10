from django.urls import path

from product.api.views import CategoryListCreate, CategoryRetrieveUpdateDestroy, ProductListCreate, \
    ProductRetrieveUpdateDestroy

urlpatterns = [
    path('categories/', CategoryListCreate.as_view()),
    path('categories/<slug>/', CategoryRetrieveUpdateDestroy.as_view()),
    path('products/', ProductListCreate.as_view()),
    path('products/<slug>/', ProductRetrieveUpdateDestroy.as_view()),
]
