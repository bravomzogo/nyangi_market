from django.contrib import admin
from .models import Seller, Product, Order,Category
from django.utils.html import format_html
from django.utils.formats import number_format


class ProductAdmin(admin.ModelAdmin):
    list_display = ('formatted_price',)  # Show formatted price

    def formatted_price(self, obj):
        return format_html(f"{number_format(obj.name, use_l10n=True)}")

    formatted_price.admin_order_field = 'price'
    formatted_price.short_description = 'Price'

admin.site.register(Product, ProductAdmin)


admin.site.register(Category)
admin.site.register(Seller)
admin.site.register(Order)



admin.site.site_title = "CEO portal"
admin.site.site_header = "CEO panel | CEO only"
