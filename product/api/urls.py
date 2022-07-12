from django.urls import path

from product.api.views import CategoryListCreate, CategoryRetrieveUpdateDestroy, ProductListCreate, \
    ProductRetrieveUpdateDestroy, search

urlpatterns = [
    path('categories/', CategoryListCreate.as_view()),
    path('categories/<slug>/', CategoryRetrieveUpdateDestroy.as_view()),
    path('products/', ProductListCreate.as_view()),
    path('products/search/', search),
    path('products/<slug>/', ProductRetrieveUpdateDestroy.as_view()),
]
