from django.db import models
from django.contrib.auth.admin import User
from django.core.validators import MaxValueValidator, MinValueValidator
from . import apps

# Create your models here.


class customer(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=100)
    discount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_discount_ratio(self):
        return self.discount/100


class category(models.Model):
    def __str__(self):
        return self.category_name
    category_name = models.CharField(max_length=100)
    discount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    description = models.CharField(max_length=200)


class item(models.Model):
    def __str__(self):
        return self.item_name
    item_image = models.ImageField(default=None,upload_to=(apps.IsgmstoreConfig.name+"/images/center/"))
    item_image_side = models.ImageField(default=None, upload_to=(apps.IsgmstoreConfig.name + "/images/side/"))
    item_image_back = models.ImageField(default=None, upload_to=(apps.IsgmstoreConfig.name + "/images/back/"))
    item_name = models.CharField(max_length=100)
    discount = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(80)])
    price = models.FloatField()
    stock_quantity = models.IntegerField()
    description = models.CharField(max_length=200)
    category = models.ForeignKey(category,on_delete=models.CASCADE)

    def get_discount_amount(self):
        return ((self.discount/100)+(self.category.discount/100))*self.price

    def get_discount_ratio(self):
        return (self.discount/100)+(self.category.discount/100)


class confirmed_order(models.Model):
    def __str__(self):
        return "Order by "+self.user.customer.name+" at "+str(self.order_time)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)


class order_history(models.Model):
    item = models.ForeignKey(item,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    original_price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    confirmed_order = models.ForeignKey(confirmed_order,on_delete=models.CASCADE)
    order_status = models.CharField(max_length=20,choices=[('confirmed','Confirmed'),('cancelled','Cancelled'),('delivered','Delivered')],default="confirmed")

    def total_price(self):
        return (self.original_price - self.discount)*self.quantity
