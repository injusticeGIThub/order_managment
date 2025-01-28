from django.views.generic import ListView, CreateView

from .constants import ORDER_STATUS
from .models import Orders, Dishes


class OrderListView(ListView):
    model = Orders
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_status'] = [status[0] for status in ORDER_STATUS]
        return context


class OrderCreateView(CreateView):
    model = Orders
    template_name = 'orders/new_order.html'
    fields = ['table_number', 'items']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = Dishes.objects.all()
        return context
