from django.contrib import admin

# Register your models here.
from django.contrib import admin
from products.models import ItemCategory, Item, PayCheck, SoldItem, Supplier, Supply, Price, PriceHistory, SoldItemProxy, SoldWeightItemProxy
admin.site.register(ItemCategory)
admin.site.register(Item)
admin.site.register(PayCheck)
admin.site.register(SoldItem)
admin.site.register(Supplier)
admin.site.register(Supply)
admin.site.register(Price)
admin.site.register(PriceHistory)
admin.site.register(SoldItemProxy)
admin.site.register(SoldWeightItemProxy)