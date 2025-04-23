from django.contrib import admin
from .models import (
    Seller, Product, Category, Cart, Order, Profile,
    WorkerContract, ParentDetails, Referee, EducationRecord,
    SubscriptionPlan, SellerSubscription, SubscriptionFeature,
    ProductAttribute, Receipt
)
from django.utils.html import format_html
from django.utils.formats import number_format


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_filter = ['category']
    search_fields = ('name', 'description', 'seller__user__username')
    readonly_fields = []
    filter_horizontal = []
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Media', {
            'fields': ('video',)
        }),
        ('Seller Information', {
            'fields': ('seller',)
        }),
        ('Additional Details', {
            'fields': ('attributes',)
        }),
        ('Timestamps', {
            'fields': (),
            'classes': ('collapse',)
        })
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

@admin.register(WorkerContract)
class WorkerContractAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'third_name', 'nationality', 'is_approved')
    list_filter = ('is_approved', 'nationality')
    search_fields = ('first_name', 'second_name', 'third_name', 'passport_nida')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ParentDetails)
class ParentDetailsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'second_name', 'residence', 'is_mother')
    list_filter = ('is_mother',)
    search_fields = ('first_name', 'second_name', 'residence')

@admin.register(Referee)
class RefereeAdmin(admin.ModelAdmin):
    list_display = ('name', 'occupation')
    search_fields = ('name', 'occupation')

@admin.register(EducationRecord)
class EducationRecordAdmin(admin.ModelAdmin):
    list_display = ('university', 'high_school')
    search_fields = ('university', 'high_school', 'secondary', 'primary')

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(SellerSubscription)
class SellerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('seller', 'plan', 'level', 'start_date', 'end_date', 'is_active', 'payment_status')
    list_filter = ('is_active', 'payment_status', 'level')
    search_fields = ('seller__shop_name', 'plan__name')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(SubscriptionFeature)
class SubscriptionFeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'is_active')
    list_filter = ('is_active', 'plan')
    search_fields = ('name', 'description')

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'attribute_type', 'required')
    list_filter = ('category', 'attribute_type', 'required')
    search_fields = ('name', 'category__name')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'date_created')
    list_filter = ('date_created',)
    search_fields = ('transaction_id', 'order__id')
    readonly_fields = ('transaction_id', 'date_created')

# Register other existing models
admin.site.register(Seller)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Profile)

admin.site.site_title = "CEO portal"
admin.site.site_header = "CEO panel | CEO only"
