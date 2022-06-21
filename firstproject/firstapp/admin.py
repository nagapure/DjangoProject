from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
from .models import  Cart, Deal, Product, ProductInCart, Order

class ProductInInline(admin.TabularInline):
    model = ProductInCart

class CartInline(admin.TabularInline):
    model = Cart

class DealInline(admin.TabularInline):
    model = Deal.user.through


class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'get_cart','is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('permission', {'fields': ('is_staff', ('is_active', 'is_superuser'),)}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Advanced options', {
            'classes': ('collapse',), 'fields': ('user_permissions', 'groups')
        }),
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}
        ),
    )
    inlines = [CartInline, DealInline]
    def get_cart(self, obj):
        return obj.cart
    search_fields = ('username',)
    ordering = ('username',)
    
    
    
class DealAdmin(admin.ModelAdmin):
    inlines = [DealInline]    
    exclude = ('user',)
    
    

admin.site.unregister(User)
admin.site.register(User, UserAdmin)




admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)
admin.site.register(Deal, DealAdmin)
