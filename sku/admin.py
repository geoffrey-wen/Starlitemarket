from django.contrib import admin
from .models import SKU, Warehouse, Product, Inbound, Outbound, TestProduct, Marketplace

# Register your models here.
admin.site.register(SKU)
admin.site.register(Warehouse)
admin.site.register(Product)
admin.site.register(Inbound)
admin.site.register(Outbound)
admin.site.register(Marketplace)
admin.site.register(TestProduct)
