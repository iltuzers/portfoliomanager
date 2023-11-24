from django.contrib import admin
from .models import Stock, Option, Portfolio, StockQuantity, OptionQuantity

admin.site.register(Stock)
admin.site.register(Option)
admin.site.register(Portfolio)
admin.site.register(StockQuantity)
admin.site.register(OptionQuantity)

