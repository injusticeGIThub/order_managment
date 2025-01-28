from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .constants import ORDER_STATUS, WAITING_STATUS


class Dishes(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название блюда')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'

    def __str__(self):
        return self.name


class Orders(models.Model):
    table_number = models.PositiveSmallIntegerField(verbose_name='Номер стола')
    items = models.ManyToManyField(Dishes, verbose_name='Блюда')
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Итоговая цена'
    )
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUS,
        default=WAITING_STATUS,
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'

    def calculate_total_price(self):
        self.total_price = sum(dish.price for dish in self.items.all())
        self.save()


@receiver(m2m_changed, sender=Orders.items.through)
def update_total_price(sender, instance, action, **kwargs):
    if action in ['post_add', 'post_remove']:
        instance.calculate_total_price()
