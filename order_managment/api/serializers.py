from rest_framework import serializers

from orders.models import Orders, Dishes


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = DishSerializer(many=True)

    class Meta:
        model = Orders
        fields = '__all__'
