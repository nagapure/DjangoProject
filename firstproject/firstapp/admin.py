from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .forms import CustomUserChangeForm, CustomUserCreationsForm

# Register your models here.
from .models import  Cart, CustomUser, Customer, Deal, Product, ProductInCart, Order, Seller

class CustomUserAdmin(UserAdmin):
    add_form: CustomUserCreationsForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','is_staff', 'is_active')
    list_filter = ('email', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_customer', 'is_seller')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    
    )
    
    search_fields = ('email',)
    ordering = ('email',)

# admin.site.unregister(User)
admin.site.register(CustomUser, CustomUserAdmin)




class ProductInCartInline(admin.TabularInline):
    model = ProductInCart

class CartInline(admin.TabularInline):
    model = Cart

class DealInline(admin.TabularInline):
    model = Deal.user.through


# class UserAdmin(UserAdmin):
#     model = User
#     list_display = ('username', 'get_cart','is_staff', 'is_active',)
#     list_filter = ('username', 'is_staff', 'is_active',)
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('permission', {'fields': ('is_staff', ('is_active', 'is_superuser'),)}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Advanced options', {
#             'classes': ('collapse',), 'fields': ('user_permissions', 'groups')
#         }),
#     )

#     add_fieldsets = (
#         (None,{
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'groups')}
#         ),
#     )
#     inlines = [CartInline, DealInline]
#     def get_cart(self, obj):
#         return obj.cart
#     search_fields = ('username',)
#     ordering = ('username',)
    
    
@admin.register(Cart) # through register decorator
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user','staff', 'created_on',)    # here user__is_staff will not work   
    list_filter = ('user', 'created_on',)
    #fields = ('staff',)           # either fields or fieldset
    fieldsets = (
        (None, {'fields': ('user', 'created_on',)}),   # only direct relationship no nested relationship('__') ex. user__is_staff
        #('User', {'fields': ('staff',)}),
    )
    inlines = (
        ProductInCartInline,
    )
    # To display only in list_display
    def staff(self,obj):
        return obj.user.is_staff
    # staff.empty_value_display = '???'
    staff.admin_order_field  = 'user__is_staff'  #Allows column order sorting
    staff.short_description = 'Staff User'  #Renames column head

    #Filtering on side - for some reason, this works
    list_filter = ['user__is_staff', 'created_on',]    # with direct foreign key(user) no error but not shown in filters, with function error
    # ordering = ['user',]
    search_fields = ['user__username']     # with direct foreign key no error but filtering not possible directly




class DealAdmin(admin.ModelAdmin):
    inlines = [DealInline]    
    exclude = ('user',)
    
    

# admin.site.unregister(User)
admin.site.register(User, UserAdmin)




# admin.site.register(Cart)
admin.site.register(Product)
admin.site.register(ProductInCart)
admin.site.register(Order)
admin.site.register(Deal, DealAdmin)
# admin.site.register(UserType)
admin.site.register(Customer)
admin.site.register(Seller)

