from django.contrib import admin
from .models import (
    Seller, Product, Category, Cart, Order, Profile,
    WorkerContract, ParentDetails, Referee, EducationRecord,
    SubscriptionPlan, SellerSubscription, SubscriptionFeature,
    ProductAttribute, Receipt, Payment, OrderItem, AdminMessage
)
from django.utils.html import format_html
from django.utils.formats import number_format
from django.utils import timezone


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

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'status', 'seller_review_status', 'created_at', 'approved_at']
    list_filter = ['status', 'seller_reviewed', 'seller_approval', 'created_at', 'approved_at']
    search_fields = ['user__username', 'reference_number', 'lipa_number']
    readonly_fields = ['created_at', 'seller_reviewed', 'seller_approval', 'seller_notes', 'seller_reviewed_at']
    
    def seller_review_status(self, obj):
        if not obj.seller_reviewed:
            return format_html('<span style="color: orange;">Pending Seller Review</span>')
        elif obj.seller_approval:
            return format_html('<span style="color: green;">Seller Approved</span>')
        else:
            return format_html('<span style="color: red;">Seller Rejected</span>')
    
    seller_review_status.short_description = "Seller Review"
    
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status == 'APPROVED':
            return self.readonly_fields + ['status', 'approved_at', 'approved_by']
        return self.readonly_fields
    
    def save_model(self, request, obj, form, change):
        try:
            if 'status' in form.changed_data and obj.status == 'APPROVED':
                obj.approve_payment(request.user)
                self.message_user(request, "Payment approved successfully. Email notifications have been sent.")
            elif 'status' in form.changed_data and obj.status == 'REJECTED':
                obj.reject_payment(request.user, obj.notes)
                self.message_user(request, "Payment rejected successfully.")
            else:
                super().save_model(request, obj, form, change)
        except Exception as e:
            self.message_user(request, f"Error processing payment: {str(e)}", level='ERROR')
            # Log the error for debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error in payment processing: {str(e)}", exc_info=True)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'created_at']
    inlines = [OrderItemInline]
    readonly_fields = ['total_price', 'created_at']

# Register other existing models
admin.site.register(Seller)
admin.site.register(Cart)
admin.site.register(Profile)

@admin.register(AdminMessage)
class AdminMessageAdmin(admin.ModelAdmin):
    list_display = ['title', 'message_preview', 'start_date', 'end_date', 'is_active', 'position', 'status']
    list_filter = ['is_active', 'position', 'start_date', 'end_date']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at', 'updated_at']
    
    def message_preview(self, obj):
        if len(obj.message) > 50:
            return obj.message[:50] + "..."
        return obj.message
    
    def status(self, obj):
        now = timezone.now()
        if obj.is_active:
            if obj.start_date <= now <= obj.end_date:
                return format_html('<span style="color: green;">Active</span>')
            elif now < obj.start_date:
                return format_html('<span style="color: orange;">Scheduled</span>')
            else:
                return format_html('<span style="color: red;">Expired</span>')
        else:
            return format_html('<span style="color: gray;">Disabled</span>')
    
    message_preview.short_description = 'Message'
    status.short_description = 'Status'

admin.site.site_title = "CEO portal"
admin.site.site_header = "CEO panel | CEO only"
