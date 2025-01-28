from django.contrib import admin

from .models import Orders, Dishes


class OrdersAdmin(admin.ModelAdmin):
    exclude = ('total_price',)
    list_display = ('table_number', 'total_price', 'get_items', 'status')

    def get_items(self, obj):
        return ", ".join([dish.name for dish in obj.items.all()])
    get_items.short_description = 'Блюда'


class DishesAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')


admin.site.register(Orders, OrdersAdmin)
admin.site.register(Dishes, DishesAdmin)
