from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Count, F, Q, DecimalField
from django.db.models.functions import TruncDate, TruncDay, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
import json

from .models import Seller, Product, Order, OrderItem, Payment, Category, SellerSubscription, ProductInteraction
from django.contrib.auth.models import User
from django.http import JsonResponse

# Existing seller dashboard view - already implemented

@login_required
def seller_products(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get filter parameters
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '')
    
    # Start with all products from this seller
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    
    # Apply filters if provided
    if category_id:
        products = products.filter(category_id=category_id)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Paginate the results
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter dropdown
    categories = Category.objects.all()
    
    # Get pending payments count for sidebar
    pending_payments_count = Payment.objects.filter(
        order__items__product__seller=seller,
        status='PENDING',
        seller_reviewed=False
    ).distinct().count()
    
    context = {
        'seller': seller,
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query,
        'pending_payments_count': pending_payments_count,
    }
    
    return render(request, 'myapp/seller_products.html', context)

@login_required
def seller_orders(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get filter parameters
    payment_status = request.GET.get('status', '')
    date_from_str = request.GET.get('date_from', '')
    date_to_str = request.GET.get('date_to', '')
    
    # Get orders that contain products from this seller
    order_items = OrderItem.objects.filter(product__seller=seller)
    order_ids = order_items.values_list('order_id', flat=True).distinct()
    orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
    
    # Apply filters if provided
    if payment_status:
        if payment_status == 'paid':
            orders = orders.filter(is_paid=True)
        elif payment_status == 'pending':
            orders = orders.filter(is_paid=False)
    
    # Parse date strings to datetime objects
    date_from = None
    date_to = None
    
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d')
            orders = orders.filter(created_at__gte=date_from)
        except ValueError:
            pass
    
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d')
            # Add one day to include the end date fully
            date_to = date_to + timedelta(days=1)
            orders = orders.filter(created_at__lt=date_to)
        except ValueError:
            pass
    
    # Paginate the results
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get pending payments count for sidebar
    pending_payments_count = Payment.objects.filter(
        order__items__product__seller=seller,
        status='PENDING',
        seller_reviewed=False
    ).distinct().count()
    
    context = {
        'seller': seller,
        'orders': page_obj,
        'payment_status': payment_status,
        'date_from': date_from,
        'date_to': date_to,
        'pending_payments_count': pending_payments_count,
    }
    
    return render(request, 'myapp/seller_orders.html', context)

@login_required
def seller_order_detail(request, order_id):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get the order
    order = get_object_or_404(Order, id=order_id)
    
    # Check if this seller has products in this order
    seller_products_in_order = OrderItem.objects.filter(
        order=order,
        product__seller=seller
    ).exists()
    
    if not seller_products_in_order:
        messages.error(request, "You don't have permission to view this order.")
        return redirect('seller_orders')
    
    # Get order items for this seller's products
    order_items = OrderItem.objects.filter(
        order=order,
        product__seller=seller
    )
    
    # Get payment information
    payment = Payment.objects.filter(order=order).first()
    
    # Get customer profile if available
    customer_profile = None
    try:
        from .models import UserProfile
        customer_profile = UserProfile.objects.filter(user=order.user).first()
    except:
        pass
    
    # Get pending payments count for sidebar
    pending_payments_count = Payment.objects.filter(
        order__items__product__seller=seller,
        status='PENDING',
        seller_reviewed=False
    ).distinct().count()
    
    context = {
        'seller': seller,
        'order': order,
        'order_items': order_items,
        'payment': payment,
        'customer_profile': customer_profile,
        'pending_payments_count': pending_payments_count,
    }
    
    return render(request, 'myapp/seller_order_detail.html', context)

@login_required
def seller_reports(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get reporting period
    period = request.GET.get('period', '30')  # Default to 30 days
    date_from_str = request.GET.get('date_from', '')
    date_to_str = request.GET.get('date_to', '')
    
    # Set date range based on period
    today = timezone.now().date()
    date_from = None
    date_to = None
    
    if period == 'custom' and date_from_str and date_to_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            date_from = today - timedelta(days=30)
            date_to = today
    else:
        if period == '7':
            date_from = today - timedelta(days=7)
        elif period == '30':
            date_from = today - timedelta(days=30)
        elif period == '90':
            date_from = today - timedelta(days=90)
        elif period == '365':
            date_from = today - timedelta(days=365)
        else:
            date_from = today - timedelta(days=30)
        
        date_to = today
    
    # Get order items for this seller's products within date range
    order_items = OrderItem.objects.filter(
        product__seller=seller,
        order__created_at__date__gte=date_from,
        order__created_at__date__lte=date_to,
        order__is_paid=True  # Only include paid orders for revenue
    )
    
    # Calculate totals
    total_orders = order_items.values('order').distinct().count()
    total_revenue = order_items.aggregate(
        revenue=Sum(F('price') * F('quantity'), output_field=DecimalField())
    )['revenue'] or 0
    products_sold = order_items.aggregate(total=Sum('quantity'))['total'] or 0
    
    # Get total likes
    total_likes = ProductInteraction.objects.filter(
        product__seller=seller,
        interaction_type='LIKE',
        created_at__date__gte=date_from,
        created_at__date__lte=date_to
    ).count()
    
    # Get top selling products
    top_products = Product.objects.filter(seller=seller).annotate(
        units_sold=Sum('orderitem__quantity', filter=Q(
            orderitem__order__created_at__date__gte=date_from,
            orderitem__order__created_at__date__lte=date_to,
            orderitem__order__is_paid=True
        )),
        revenue=Sum(F('orderitem__price') * F('orderitem__quantity'), filter=Q(
            orderitem__order__created_at__date__gte=date_from,
            orderitem__order__created_at__date__lte=date_to,
            orderitem__order__is_paid=True
        ), output_field=DecimalField())
    ).filter(units_sold__gt=0).order_by('-units_sold')[:5]
    
    # Get sales by category
    category_sales = Category.objects.filter(
        product__seller=seller,
        product__orderitem__order__created_at__date__gte=date_from,
        product__orderitem__order__created_at__date__lte=date_to,
        product__orderitem__order__is_paid=True
    ).annotate(
        units_sold=Sum('product__orderitem__quantity'),
        revenue=Sum(F('product__orderitem__price') * F('product__orderitem__quantity'), output_field=DecimalField())
    ).filter(units_sold__gt=0).order_by('-revenue')
    
    # Prepare chart data for sales trend
    # Determine appropriate grouping based on date range
    days_diff = (date_to - date_from).days
    
    if days_diff <= 31:
        # Daily grouping for up to a month
        date_trunc = TruncDay('order__created_at')
        format_str = '%b %d'
    elif days_diff <= 90:
        # Weekly grouping for up to 3 months
        date_trunc = TruncWeek('order__created_at')
        format_str = 'Week %W'
    else:
        # Monthly grouping for longer periods
        date_trunc = TruncMonth('order__created_at')
        format_str = '%b %Y'
    
    sales_data = order_items.annotate(
        date=date_trunc
    ).values('date').annotate(
        revenue=Sum(F('price') * F('quantity'), output_field=DecimalField())
    ).order_by('date')
    
    # Prepare data for charts
    chart_labels = []
    chart_data = []
    
    for item in sales_data:
        if item['date']:
            chart_labels.append(item['date'].strftime(format_str))
            chart_data.append(float(item['revenue']))
    
    # Prepare category chart data
    category_labels = [category.name for category in category_sales]
    category_data = [float(category.revenue) for category in category_sales]
    
    # Get pending payments count for sidebar
    pending_payments_count = Payment.objects.filter(
        order__items__product__seller=seller,
        status='PENDING',
        seller_reviewed=False
    ).distinct().count()
    
    context = {
        'seller': seller,
        'period': period,
        'date_from': date_from,
        'date_to': date_to,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'products_sold': products_sold,
        'total_likes': total_likes,
        'top_products': top_products,
        'category_sales': category_sales,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'category_labels': json.dumps(category_labels),
        'category_data': json.dumps(category_data),
        'pending_payments_count': pending_payments_count,
    }
    
    return render(request, 'myapp/seller_reports.html', context)

@login_required
def seller_settings(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Check if seller has an active subscription
    subscription = SellerSubscription.objects.filter(
        seller=seller,
        is_active=True,
        end_date__gte=timezone.now().date()
    ).first()
    
    # Get Tanzania regions for location dropdown
    regions = Seller.TANZANIA_REGIONS
    
    # Process form submissions
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'shop_info':
            # Update shop information
            seller.shop_name = request.POST.get('shop_name')
            seller.description = request.POST.get('description')
            seller.phone_number = request.POST.get('phone_number')
            seller.whatsapp_number = request.POST.get('whatsapp_number')
            seller.location = request.POST.get('location')
            seller.save()
            
            messages.success(request, "Shop information updated successfully.")
        
        elif form_type == 'payment_info':
            # Update payment information
            seller.bank_name = request.POST.get('bank_name')
            seller.account_number = request.POST.get('account_number')
            seller.mobile_money = request.POST.get('mobile_money')
            seller.save()
            
            messages.success(request, "Payment information updated successfully.")
        
        elif form_type == 'change_password':
            # Change password
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            user = request.user
            
            # Check if current password is correct
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully. Please log in again.")
                return redirect('seller_login')
        
        elif form_type == 'notifications':
            # Update notification preferences
            seller.email_notifications = 'email_notifications' in request.POST
            seller.sms_notifications = 'sms_notifications' in request.POST
            seller.whatsapp_notifications = 'whatsapp_notifications' in request.POST
            seller.save()
            
            messages.success(request, "Notification preferences updated successfully.")
        
        elif form_type == 'toggle_auto_renew':
            # Toggle auto-renew for subscription
            if subscription:
                subscription.auto_renew = not subscription.auto_renew
                subscription.save()
                
                if subscription.auto_renew:
                    messages.success(request, "Auto-renew has been enabled for your subscription.")
                else:
                    messages.success(request, "Auto-renew has been disabled for your subscription.")
    
    # Get pending payments count for sidebar
    pending_payments_count = Payment.objects.filter(
        order__items__product__seller=seller,
        status='PENDING',
        seller_reviewed=False
    ).distinct().count()
    
    context = {
        'seller': seller,
        'subscription': subscription,
        'regions': regions,
        'pending_payments_count': pending_payments_count,
    }
    
    return render(request, 'myapp/seller_settings.html', context)
