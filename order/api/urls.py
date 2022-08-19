from django.urls import path
from .views import checkout, OrderListView

urlpatterns = [
    path('checkout/', checkout),
    path('orders/', OrderListView.as_view()),
]
