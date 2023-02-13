from django.contrib import admin
from .models import MyCart, MyCartItem, Coupons, MyFav
# Register your models here.


admin.site.register(MyCartItem)
admin.site.register(MyCart)
admin.site.register(Coupons)
admin.site.register(MyFav)