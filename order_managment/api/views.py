from django.utils import timezone
from django.urls import reverse
from rest_framework import status, filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.constants import ORDER_STATUS
from orders.models import Orders
from .serializers import OrderSerializer


class OrderViewSet(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['table_number', 'status']

    @action(detail=False, methods=['get'])
    def revenue(self, request):
        today_orders = self.queryset.filter(status='paid', created_at__date=timezone.now().date())
        revenue = sum(order.total_price for order in today_orders)
        return Response({'revenue': revenue})

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in [status[0] for status in ORDER_STATUS]:
            order.status = new_status
            order.save()
            return Response({'message': 'Статус обновлен', 'status': new_status}, status=status.HTTP_200_OK)
        return Response(
            {'error': 'Недопустимый статус'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            redirect_url = reverse('orders:order_list')
            return Response(
                {'redirect': redirect_url},
                status=status.HTTP_201_CREATED
            )
        return response
