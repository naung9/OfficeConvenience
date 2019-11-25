'''
Created on Apr 23, 2019

@author: naung9
'''
from django.db.models.signals import pre_save
from django.dispatch import receiver
from . import models


@receiver(pre_save,sender=models.order_history,dispatch_uid="update_credit_item_info")
def update_credit_item_info(sender, instance, **kwargs):
    print("Order History Pre Save")
    item = instance.item
    print(instance.confirmed_order.order_time)
    if instance.order_status == 'delivered' and instance.quantity < item.stock_quantity:
        item.stock_quantity -= instance.quantity
        item.save()
