from django.contrib import admin
from .models import Product, ProductColor, ProductSize, RateProduct, ReviewProduct
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
admin.site.register(ReviewProduct)
admin.site.register(RateProduct)