from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ['username','is_customer','is_resturent','is_rider','is_superuser','is_active','is_staff']


admin.site.unregister(Group)
admin.site.register(Customer)
admin.site.register(Division)
admin.site.register(Place)
admin.site.register(ResturantUser)
admin.site.register(Rider)
admin.site.register(FoodCategory)
admin.site.register(FoodName)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(allowResturant)
