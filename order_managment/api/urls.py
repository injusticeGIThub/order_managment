from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrderViewSet

app_name = 'api'

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
