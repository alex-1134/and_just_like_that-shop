import uuid
import decimal

from django.db import models
from django.conf import settings
from django.db.models import Sum

from decimal import Decimal
from items.models import Item
from profiles.models import UserProfile


# from Code Institute
class Order(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders')
    order_number = models.CharField(max_length=32, null=False, editable=False)
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = models.CharField(max_length=40, null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)


    def generate_order_number(self):
        return uuid.uuid4().hex.upper()


    def delete_total(self):
        self.delivery_cost = Decimal(self.order_total) * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / 100
        self.grand_total = Decimal(self.order_total) + Decimal(self.delivery_cost)
        self.save()

    def new_total(self):
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
        self.delivery_cost = Decimal(self.order_total) * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / 100
        self.grand_total = Decimal(self.order_total) + Decimal(self.delivery_cost)
        self.save()


    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    item = models.ForeignKey(Item, null=False, blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        self.lineitem_total = Decimal(self.item.price) * Decimal(self.quantity)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'SKU {self.item.sku} on order {self.order.order_number}'
