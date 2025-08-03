# context_processors.py
from .models import Cart, Order, Payment, AdminMessage
from django.utils import timezone

def cart_item_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
        return {'cart_item_count': count}
    return {'cart_item_count': 0}

def pending_orders_count(request):
    """Count orders that need attention (no payment or pending approval)"""
    if request.user.is_authenticated:
        # Count orders without payments
        orders_without_payment = Order.objects.filter(
            user=request.user
        ).exclude(
            id__in=Payment.objects.values_list('order_id', flat=True)
        ).count()
        
        # Count orders with pending payments
        pending_payments = Payment.objects.filter(
            order__user=request.user,
            status='PENDING'
        ).count()
        
        total_pending = orders_without_payment + pending_payments
        return {'pending_orders_count': total_pending}
    
    return {'pending_orders_count': 0}

def active_admin_messages(request):
    """Provide active admin messages to all templates"""
    now = timezone.now()
    messages = AdminMessage.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).order_by('-priority')
    
    # Split messages by position
    left_messages = messages.filter(position='left')
    right_messages = messages.filter(position='right')
    
    return {
        'admin_messages_left': left_messages,
        'admin_messages_right': right_messages,
        'has_admin_messages': messages.exists()
    }