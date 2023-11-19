from django.contrib import admin
from .models import Stock, Option, Portfolio

admin.site.register(Stock)
admin.site.register(Option)
admin.site.register(Portfolio)

