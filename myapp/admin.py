from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')