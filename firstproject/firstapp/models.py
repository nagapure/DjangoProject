from time import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin



# class UserType(models.Model):
#     CUSTOMER = 1
#     SELLER =2
#     TYPE_CHOICES = (
#         (SELLER, 'Seller'),
#         (CUSTOMER, 'Customer'),
#     )

#     id = models.PositiveIntegerField(primary_key=True, choices=TYPE_CHOICES)
#     def __str__(self):
#         return self.get_id_display()
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # username = None
    email = models.EmailField(_('email address'),unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # This is the first option
    # is_customer = models.BooleanField(default=True)
    # is_seller = models.BooleanField(default=False)
    
    # This is an second option 
    # type = (
    #     (1, 'seller'),
    #     (2, 'customer'),
    # )
    # user_type = models.IntegerField(choices=type, default=2)
    
    # usertype = models.ManyToManyField(UserType)
    
    class Types(models.TextChoices):
        SELLER = "Seller", "SELLER"
        CUSTOMER = "Customer", "CUSTOMER"
    
    default_type = Types.CUSTOMER
    
    type = models.CharField(_('Type'), max_length=255, choices=Types.choices, default=default_type)
    
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    # if not the code below then taking default value in User model not in proxy models
    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args, **kwargs)


class CustomerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)


class SellerAdditional(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gst = models.CharField(max_length=15)
    warehouse_location = models.CharField(max_length=1000)



# Model Managers for proxy models
class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type= CustomUser.Types.SELLER)
    
class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type= CustomUser.Types.CUSTOMER)
    

# Proxy models they do not create separate table
class Seller(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = SellerManager()
    class Meta:
        proxy = True
    
    def sell(self):
        print("I can sell")
        
        
class Customer(CustomUser):
    default_type = CustomUser.Types.SELLER
    objects = CustomerManager()
    class Meta:
        proxy = True
        
    def buy(self):
        print("I can buy")
        
        



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


class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        return cart
    
    
# class cart_manager(object):
#     def __init__(self, user):
#         self.user = user
#         self.cart = Cart.objects.filter(user=user)
#         if self.cart.count() == 0:
#             self.cart = Cart.create(user)
#         else:
#             self.cart = self.cart.first()
    
#     def add_to_cart(self, product_id):
#         product = Product.objects.get(product_id=product_id)
#         self.cart.products.add(product)
#         self.cart.save()
#         return self.cart
    
#     def remove_from_cart(self, product_id):
#         product = Product.objects.get(product_id=product_id)
#         self.cart.products.remove(product)
#         self.cart.save()
#         return self.cart
    
#     def get_cart(self):
#         return self.cart
    
#     def get_total(self):
#         total = 0
#         for product in self.cart.products.all():
#             total += product.price
#         return total
    
#     def __str__(self):
#         return self.user.username 
class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=status_choices, default=1)
    
class Deal(models.Model):
    user = models.ManyToManyField(CustomUser)
    deal_name = models.CharField(max_length=250)