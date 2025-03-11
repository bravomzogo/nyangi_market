from django.contrib import admin
from .models import Product, Tech, CustomUser

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'stock', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'location')

class TechAdmin(admin.ModelAdmin):
    list_display = ('condition', 'brand', 'model', 'release_year', 'power_consumption')
    search_fields = ('brand', 'model')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_type', 'email')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)

# Register the models with their custom admin classes
admin.site.register(Product, ProductAdmin)
admin.site.register(Tech, TechAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
