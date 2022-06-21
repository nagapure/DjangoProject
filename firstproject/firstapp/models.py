from time import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
# from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # objects = CustomUserManager()
    
    # def__str__(self):
    #     return self.email





class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length= 250)
    price = models.FloatField()
    
    @classmethod
    def updateprice(cls, product_id, price):
        product = cls.objects.get(product_id=product_id)
        product = product.first()
        product.price = price
        product.save()
        return product
    
    @classmethod
    def create(cls, product_name, price):
        product = cls(product_name=product_name, price=price)
        product.save()
        return product
    
    def __str__(self):
        return self.product_name
 
class cart_manager(object):
    def __init__(self, user):
        self.user = user
        self.cart = Cart.objects.filter(user=user)
        if self.cart.count() == 0:
            self.cart = Cart.create(user)
        else:
            self.cart = self.cart.first()
    
    def add_to_cart(self, product_id):
        product = Product.objects.get(product_id=product_id)
        self.cart.products.add(product)
        self.cart.save()
        return self.cart
    
    def remove_from_cart(self, product_id):
        product = Product.objects.get(product_id=product_id)
        self.cart.products.remove(product)
        self.cart.save()
        return self.cart
    
    def get_cart(self):
        return self.cart
    
    def get_total(self):
        total = 0
        for product in self.cart.products.all():
            total += product.price
        return total
    
    def __str__(self):
        return self.user.username 
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField()
    
class ProductInCart(models.Model):
    class Meta:
        unique_together = ('cart', 'product')
    product_in_cart_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
        
class Order(models.Model):
    status_choices = (
        (1, 'Pending'),
        (2, 'Ready for shipment'),
        (3, 'Shipped'),
        (4, 'Delivered'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices, default=1)
    
class Deal(models.Model):
    user = models.ManyToManyField(User)
    deal_name = models.CharField(max_length=250)