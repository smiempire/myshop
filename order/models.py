from django.contrib.auth.models import User
from django.db import models

from core.helpers import BaseEnumerate
from shop.models import Product


class OrderStatus(BaseEnumerate):
    AWAITING_PAYMENT = 1
    AWAITING_DISPATCH = 2
    SENT = 3
    AMENDED = 4
    PUBLISHED = 5
    values = {
        AWAITING_PAYMENT: u'Ожидает оплаты',
        AWAITING_DISPATCH: u'Ожидает отправки',
        SENT: u'Отправлен',
    }


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.IntegerField(u'Status', choices=OrderStatus.get_choices(), default=OrderStatus.AWAITING_PAYMENT)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
