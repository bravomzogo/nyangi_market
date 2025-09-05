from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SellerRegistrationForm, ProductForm, CustomUserRegistrationForm, EmailOrUsernameAuthenticationForm
import logging

logger = logging.getLogger(__name__)
from .models import Product, Category, Seller, Cart, WorkerContract, ParentDetails, Referee, EducationRecord, SubscriptionPlan, SellerSubscription, Receipt, ProductAttribute, Order, Payment, OrderItem, ProductInteraction, AdminMessage
from django.http import HttpResponse, FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .forms import WorkerContractForm, ParentDetailsForm, RefereeForm, EducationRecordForm, SubscriptionPlanForm, SellerSubscriptionForm
import pdfkit
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from weasyprint import HTML
import os

def buy_page(request):
    return render(request, 'myapp/buy.html')

def receipt_view(request):
    receipt = request.session.get('mpesa_receipt', None)
    return render(request, 'myapp/receipt.html', {'receipt': receipt})


def home(request):
    products = Product.objects.all().order_by('-created_at')
    recent_products = list(products[:4])  # Get the latest four products
    categories = Category.objects.all()
    query = request.GET.get('query', '')
    selected_category = request.GET.get('category', '')

    if query:
        products = products.filter(name__icontains=query)

    if selected_category:
        products = products.filter(category__name=selected_category)

    message = "No products found matching your search query." if not products else ""

    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()

    contracts = WorkerContract.objects.all() if request.user.is_staff else None

    return render(request, 'myapp/home.html', {
        'products': products,
        'recent_products': recent_products,
        'query': query,
        'message': message,
        'categories': categories,
        'cart_item_count': cart_item_count,
        'selected_category': selected_category,
        'contracts': contracts,
    })

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')    


def filter_by_category(request, category_name):
    products = Product.objects.filter(category__name=category_name)
    categories = Category.objects.all()
    return render(request, 'myapp/home.html', {
        'products': products,
        'categories': categories,
        'category_name': category_name
    })


def seller_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            seller = form.save()
            login(request, seller.user)
            return redirect('home')
    else:
        form = SellerRegistrationForm()

    return render(request, 'myapp/seller_register.html', {'form': form})


def addo_product(request):
    if not request.user.is_authenticated or not hasattr(request.user, 'seller'):
        return redirect('seller_register')

    # Check if seller has payment details
    seller = request.user.seller
    if not seller.has_payment_details():
        messages.error(request, "You must enter your payment details before posting products. Please complete your payment information in seller settings.")
        return redirect('seller_settings')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            # Handle optional fields
            if not form.cleaned_data.get('release_year'):
                product.release_year = None
            if not form.cleaned_data.get('video'):  # Handle optional video field
                product.video = None
            product.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'myapp/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    # Get the product
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the logged-in user is the seller of this product
    if not hasattr(request.user, 'seller') or product.seller != request.user.seller:
        messages.error(request, "You don't have permission to edit this product.")
        return redirect('seller_products')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            # Handle optional fields
            if not form.cleaned_data.get('release_year'):
                updated_product.release_year = None
            if not form.cleaned_data.get('video') and 'video-clear' in request.POST:
                updated_product.video = None
            updated_product.save()
            messages.success(request, "Product updated successfully!")
            return redirect('seller_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'myapp/edit_product.html', {
        'form': form,
        'product': product,
        'seller': request.user.seller
    })


@login_required
def delete_product(request, product_id):
    # Get the product
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the logged-in user is the seller of this product
    if not hasattr(request.user, 'seller') or product.seller != request.user.seller:
        messages.error(request, "You don't have permission to delete this product.")
        return redirect('seller_products')
    
    # Delete the product
    product_name = product.name
    product.delete()
    
    messages.success(request, f"Product '{product_name}' has been deleted.")
    return redirect('seller_products')


def product_detail(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    
    # Get the user's interaction with this product if they're logged in
    user_interaction = None
    if user.is_authenticated:
        try:
            user_interaction = ProductInteraction.objects.get(user=user, product=product)
        except ProductInteraction.DoesNotExist:
            pass
    
    # Ensure like/dislike counts are available even if they're zero
    if product.likes_count is None:
        product.likes_count = 0
    if product.dislikes_count is None:
        product.dislikes_count = 0
    
    return render(request, 'myapp/product_detail.html', {
        'product': product,
        'user': user,
        'user_interaction': user_interaction,
        'seller': product.seller,  # Include seller information for contact
    })


def seller_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login1.html', {'form': form})


def seller_logout(request):
    logout(request)
    return redirect('home')


def member_dashboard(request):
    # Check if the user is a seller
    try:
        seller = Seller.objects.get(user=request.user)
        return redirect('seller_dashboard')
    except Seller.DoesNotExist:
        # Regular member dashboard
        return render(request, 'myapp/member_dashboard.html')

@login_required
def seller_dashboard(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get products by this seller
    products = Product.objects.filter(seller=seller).order_by('-created_at')
    
    # Get orders that contain products from this seller
    order_items = OrderItem.objects.filter(product__seller=seller)
    order_ids = order_items.values_list('order_id', flat=True).distinct()
    orders = Order.objects.filter(id__in=order_ids).order_by('-created_at')
    
    # Get pending payments for this seller's products
    pending_payments = Payment.objects.filter(
        order__id__in=order_ids,
        status='PENDING',
        seller_reviewed=False
    )
    
    # Get recent payments for this seller's products
    recent_payments = Payment.objects.filter(
        order__id__in=order_ids
    ).order_by('-created_at')[:5]  # Show latest 5 payments
    
    context = {
        'seller': seller,
        'products_count': products.count(),
        'orders_count': orders.count(),
        'pending_payments_count': pending_payments.count(),
        'recent_payments': recent_payments,
        'products': products[:5],  # Show latest 5 products
        'orders': orders[:5]  # Show latest 5 orders
    }
    return render(request, 'myapp/seller_dashboard.html', context)

@login_required
def seller_payment_detail(request, payment_id):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get the payment
    try:
        # Find order items with products from this seller
        payment = Payment.objects.get(id=payment_id)
        order_items = payment.order.items.filter(product__seller=seller)
        
        if not order_items.exists():
            messages.error(request, "This payment doesn't include any of your products.")
            return redirect('seller_payment_list')
        
        # Process review form
        if request.method == 'POST':
            action = request.POST.get('action')
            notes = request.POST.get('notes', '')
            
            if action in ['approve', 'reject']:
                payment.seller_reviewed = True
                payment.seller_notes = notes
                payment.seller_reviewed_at = timezone.now()
                
                if action == 'approve':
                    payment.seller_approval = True
                    
                    # Use the helper function to approve payment without sending emails first
                    from myapp.tasks import approve_payment_without_emails, send_payment_approved_emails_with_pdf
                    approve_payment_without_emails(payment, request.user)
                    
                    # Send emails with PDF receipts
                    try:
                        send_payment_approved_emails_with_pdf(payment.id)
                        messages.success(request, "Payment has been approved successfully. Emails with receipts have been sent to both buyer and seller.")
                    except Exception as e:
                        logger.error(f"Error sending emails for payment {payment.id}: {str(e)}")
                        messages.success(request, "Payment has been approved successfully, but there was an issue sending emails.")
                else:
                    payment.seller_approval = False
                    
                    # Use helper function to reject payment without sending emails
                    from myapp.tasks import reject_payment_without_emails
                    reject_payment_without_emails(payment, request.user)
                    
                    messages.info(request, "Payment has been rejected.")
                
                payment.save()
                return redirect('seller_payment_list')
        
        # Get the seller's products in this order
        seller_items = order_items.select_related('product')
        
        context = {
            'payment': payment,
            'seller': seller,
            'order_items': seller_items,
            'seller_total': sum(item.price * item.quantity for item in seller_items)
        }
        return render(request, 'myapp/seller_payment_detail.html', context)
    
    except Payment.DoesNotExist:
        messages.error(request, "Payment not found.")
        return redirect('seller_payment_list')



# payments/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import base64
from datetime import datetime
from django.conf import settings
import json

@csrf_exempt
def initiate_mpesa_payment(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            amount = data.get('amount')  # Amount to be paid
            phone = data.get('phone')  # User's phone number in format 2547XXXXXXXX

            # Validate phone number
            if not phone or len(phone) != 12 or not phone.startswith('254'):
                return JsonResponse({"error": "Invalid phone number. Use format 2547XXXXXXXX."}, status=400)

            # Generate access token
            auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
            response = requests.get(auth_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
            access_token = response.json().get('access_token')

            # Prepare STK Push request payload
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = base64.b64encode((settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()

            payload = {
                'BusinessShortCode': settings.MPESA_SHORTCODE,
                'Password': password,
                'Timestamp': timestamp,
                'TransactionType': 'CustomerPayBillOnline',
                'Amount': amount,
                'PartyA': phone,
                'PartyB': settings.MPESA_SHORTCODE,
                'PhoneNumber': phone,
                'CallBackURL': settings.MPESA_CALLBACK_URL,
                'AccountReference': 'TestPayment',
                'TransactionDesc': 'Payment for testing'
            }

            # Send STK Push request
            headers = {'Authorization': f'Bearer {access_token}'}
            stk_push_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
            response = requests.post(stk_push_url, json=payload, headers=headers)

            # Return the Mpesa API response
            return JsonResponse(response.json())

        except Exception as e:
            # Handle any exceptions
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

@csrf_exempt


def mpesa_callback(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from M-Pesa
            data = json.loads(request.body)
            print("Callback Data:", data)  # Debugging

            # Check if payment was successful
            result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
            if result_code == 0:
                # Extract payment details
                callback_metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
                payment_data = {item['Name']: item.get('Value') for item in callback_metadata}

                # Store transaction in session (for receipt)
                request.session['mpesa_receipt'] = payment_data

                return JsonResponse({"success": "Payment successful!", "receipt": payment_data})

            else:
                return JsonResponse({"error": "Payment failed: " + data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"}, status=400)




from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product
import random

# Simulate the PIN entry page (GET request)
def payment_pin_input(request, product_id):
    # Fetch the product or some amount related to the product
    product = Product.objects.get(id=product_id)
    phone_number = "254777777777"  # This should be passed or fetched dynamically
    amount = product.price  # Assuming the product has a price field

    return render(request, 'myapp/payment_pin_input.html', {
        'phone_number': phone_number,
        'amount': amount
    })

# Process payment PIN entry (POST request)
@csrf_exempt
def process_payment_pin(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        pin = request.POST.get('pin')

        # Simulating checking the PIN (you can validate the pin further)
        if pin == '1234':  # Simulate a successful PIN check
            # Simulate processing the payment here and trigger a success response
            payment_status = 'success'
            receipt_number = f"MPESA{random.randint(100000, 999999)}"  # Simulate receipt number
            return JsonResponse({
                'status': payment_status,
                'receipt_number': receipt_number,
                'amount': amount,
                'phone_number': phone_number,
            })

        else:
            # Simulate failed PIN attempt
            return JsonResponse({
                'status': 'failure',
                'error': 'Invalid PIN. Please try again.'
            }, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def login_view(request):
    if request.method == 'POST':
        form = EmailOrUsernameAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect(request.GET.get('next', 'home'))  # Redirect to 'next' if available
        else:
            messages.error(request, "Invalid email/username or password.")
    else:
        form = EmailOrUsernameAuthenticationForm()
    
    return render(request, 'myapp/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            # Validate WhatsApp number format
            phone_number = form.cleaned_data['phone_number']
            if not phone_number.startswith('+'):
                form.add_error('phone_number', 'WhatsApp number must include country code (e.g., +255XXXXXXXXX)')
                messages.error(request, "Registration failed. Please correct the highlighted errors below.")
                return render(request, 'myapp/register.html', {'form': form})
                
            user = form.save()
            user.profile.phone_number = phone_number
            user.profile.area_of_residence = form.cleaned_data['area_of_residence']
            user.profile.use_whatsapp_for_recovery = False  # Email-only recovery
            user.profile.save()
            
            messages.success(request, "Your account has been created successfully! You can now log in with your email or username.")
            # Re-authenticate to obtain the backend path safely
            auth_user = authenticate(request, username=user.username, password=form.cleaned_data.get('password1'))
            if auth_user is not None:
                login(request, auth_user)
            else:
                # Fallback: explicitly set backend (should rarely happen)
                user.backend = 'myapp.backends.EmailOrUsernameBackend'
                login(request, user)
            return redirect('home')
        else:
            # Provide a clearer generic message while detailed errors render inline
            messages.error(request, "Registration failed. Please correct the highlighted errors below.")
    else:
        form = CustomUserRegistrationForm()
    
    return render(request, 'myapp/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    # Calculate total price per item
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    
    # Calculate overall total price
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'myapp/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('view_cart')  # Redirect to cart instead of home

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def worker_contract_create(request):
    if request.method == 'POST':
        contract_form = WorkerContractForm(request.POST, request.FILES)
        father_form = ParentDetailsForm(request.POST, prefix='father')
        mother_form = ParentDetailsForm(request.POST, prefix='mother')
        referee1_form = RefereeForm(request.POST, prefix='referee1')
        referee2_form = RefereeForm(request.POST, prefix='referee2')
        education_form = EducationRecordForm(request.POST)

        if all([contract_form.is_valid(), father_form.is_valid(), mother_form.is_valid(),
                referee1_form.is_valid(), referee2_form.is_valid(), education_form.is_valid()]):
            father = father_form.save()
            mother = mother_form.save()
            referee1 = referee1_form.save(commit=False)
            referee2 = referee2_form.save(commit=False)
            
            # Skip signature upload for referees
            referee1.signature = None
            referee2.signature = None
            referee1.save()
            referee2.save()
            
            education = education_form.save()

            contract = contract_form.save(commit=False)
            contract.father = father
            contract.mother = mother
            contract.referee1 = referee1
            contract.referee2 = referee2
            contract.education_record = education
            
            # Skip signature and stamp uploads
            contract.chairperson_signature = None
            contract.chairperson_stamp = None
            contract.worker_signature = None
            contract.lawyer_signature = None
            contract.lawyer_stamp = None
            contract.ceo_signature = None
            contract.ceo_stamp = None
            
            contract.save()

            messages.success(request, 'Contract created successfully!')
            return redirect('worker_contract_detail', pk=contract.pk)
    else:
        contract_form = WorkerContractForm()
        father_form = ParentDetailsForm(prefix='father')
        mother_form = ParentDetailsForm(prefix='mother')
        referee1_form = RefereeForm(prefix='referee1')
        referee2_form = RefereeForm(prefix='referee2')
        education_form = EducationRecordForm()

    return render(request, 'myapp/worker_contract_form.html', {
        'contract_form': contract_form,
        'father_form': father_form,
        'mother_form': mother_form,
        'referee1_form': referee1_form,
        'referee2_form': referee2_form,
        'education_form': education_form,
    })

@login_required
@user_passes_test(is_admin)
def worker_contract_detail(request, pk):
    contract = get_object_or_404(WorkerContract, pk=pk)
    return render(request, 'myapp/worker_contract_detail.html', {'contract': contract})

@login_required
@user_passes_test(is_admin)
def worker_contract_pdf(request, pk):
    contract = get_object_or_404(WorkerContract, pk=pk)
    template = get_template('myapp/worker_contract_pdf.html')
    html = template.render({'contract': contract})
    
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }
    
    pdf = pdfkit.from_string(html, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contract_{contract.pk}.pdf"'
    return response

@login_required
@user_passes_test(is_admin)
def subscription_plan_create(request):
    if request.method == 'POST':
        form = SubscriptionPlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subscription plan created successfully!')
            return redirect('subscription_plan_list')
    else:
        form = SubscriptionPlanForm()
    return render(request, 'myapp/subscription_plan_form.html', {'form': form})

@login_required
def subscription_plan_list(request):
    plans = SubscriptionPlan.objects.filter(is_active=True)
    return render(request, 'myapp/subscription_plan_list.html', {'plans': plans})

@login_required
def seller_subscription_create(request):
    if request.method == 'POST':
        form = SellerSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.seller = request.user.seller
            subscription.start_date = timezone.now()
            subscription.end_date = timezone.now() + timedelta(days=subscription.plan.duration_days)
            subscription.save()
            messages.success(request, 'Subscription created successfully!')
            return redirect('seller_dashboard')
    else:
        form = SellerSubscriptionForm()
    return render(request, 'myapp/seller_subscription_form.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            
            subject = 'Password Reset Request'
            message = render_to_string('myapp/password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            email.send()
            
            messages.success(request, 'Password reset email has been sent.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email address.')
    return render(request, 'myapp/password_reset_request.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been reset successfully.')
            return redirect('login')
        return render(request, 'myapp/password_reset_confirm.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('password_reset_request')

def about_us(request):
    technical_team = [
        {
            'name': 'John Doe',
            'position': 'Lead Developer',
            'email': 'john.doe@example.com',
            'phone': '+255 761 434 077',
            'image': 'team/john.jpg'
        },
        {
            'name': 'Jane Smith',
            'position': 'UI/UX Designer',
            'email': 'jane.smith@example.com',
            'phone': '+255 987 654 321',
            'image': 'team/jane.jpg'
        },
        {
            'name': 'Mike Johnson',
            'position': 'System Administrator',
            'email': 'mike.johnson@example.com',
            'phone': '+255 456 789 123',
            'image': 'team/mike.jpg'
        }
    ]
    return render(request, 'myapp/about_us.html', {'technical_team': technical_team})

def generate_receipt(order):
    receipt = Receipt.objects.create(order=order)
    
    # Generate PDF
    context = {
        'receipt': receipt,
        'order': order,
        'logo_url': os.path.join(settings.STATIC_URL, 'images/logo.png'),
        'company_phone': settings.COMPANY_PHONE
    }
    
    html_string = render_to_string('myapp/receipt.html', context)
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()
    
    # Save PDF
    receipt_path = f'receipts/{receipt.transaction_id}.pdf'
    with open(os.path.join(settings.MEDIA_ROOT, receipt_path), 'wb') as f:
        f.write(pdf_file)
    
    receipt.pdf_file = receipt_path
    receipt.save()
    
    return receipt

def get_category_attributes(request):
    category_id = request.GET.get('category_id')
    product_id = request.GET.get('product_id')
    
    product_values = {}
    if product_id:
        try:
            product = Product.objects.get(id=product_id)
            # Get existing attribute values for this product
            if hasattr(product, 'attributes'):
                for attr_value in product.attributes.all():
                    product_values[attr_value.attribute.id] = attr_value.value
        except Product.DoesNotExist:
            pass
    
    if category_id:
        attributes = ProductAttribute.objects.filter(category_id=category_id)
        grouped_attributes = {}
        for attr in attributes:
            group = attr.group or "General"
            if group not in grouped_attributes:
                grouped_attributes[group] = []
            grouped_attributes[group].append({
                'id': attr.id,
                'name': attr.name,
                'attribute_type': attr.attribute_type,
                'required': attr.required,
                'options': attr.options,
            })
        return JsonResponse({'attributes': grouped_attributes, 'product_values': product_values})
    return JsonResponse({'attributes': {}, 'product_values': product_values})

from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Receipt
import os

def download_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    # If no PDF associated yet or file missing, regenerate it on the fly
    regenerate = False
    if not receipt.pdf_file or not getattr(receipt.pdf_file, 'name', None):
        regenerate = True
    else:
        try:
            receipt_path = receipt.pdf_file.path
            if not os.path.exists(receipt_path):
                regenerate = True
        except (ValueError, FileNotFoundError):
            regenerate = True

    if regenerate:
        # Build minimal data for regeneration (fallback values if some data missing)
        order = receipt.order
        items = []
        if hasattr(order, 'items'):
            for item in order.items.all():
                items.append({
                    'name': getattr(item.product, 'name', 'Item'),
                    'quantity': item.quantity,
                    'price': item.price,
                    'total': item.price * item.quantity,
                })
        elif getattr(order, 'product', None):
            # Legacy single-product order structure
            items.append({
                'name': getattr(order.product, 'name', 'Item'),
                'quantity': getattr(order, 'quantity', 1),
                'price': getattr(order.product, 'price', 0),
                'total': getattr(order.product, 'price', 0) * getattr(order, 'quantity', 1),
            })

        total_price = sum(i['total'] for i in items) if items else getattr(order, 'total_price', 0)
        from datetime import datetime
        receipt_data = {
            'company_name': 'Nyangi Marketplace',
            'company_email': getattr(settings, 'DEFAULT_FROM_EMAIL', 'support@nyangiassetsmarketplace.co.tz'),
            'company_address': 'P.o.box 1282 TABORA',
            'company_phone': '+255 761 434 077',
            'transaction_id': receipt.transaction_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'username': getattr(order.user, 'username', ''),
            'user_email': getattr(order.user, 'email', ''),
            'payment_method': 'Manual / Approved',
            'shop_name': items[0]['name'] if items else 'Nyangi Shop',
            'items': items,
            'subtotal': total_price,
            'total': total_price,
            'logo_url': os.path.join(settings.STATIC_URL, 'images/logo.png')
        }
        html_string = render_to_string('myapp/receipt_template.html', {'receipt': receipt_data})
        html = HTML(string=html_string)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'receipts'), exist_ok=True)
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'receipts', f'{receipt.transaction_id}.pdf')
        html.write_pdf(pdf_path)
        receipt.pdf_file = f'receipts/{receipt.transaction_id}.pdf'
        receipt.save(update_fields=['pdf_file'])
        receipt_path = pdf_path
    else:
        receipt_path = receipt.pdf_file.path

    return FileResponse(open(receipt_path, 'rb'), content_type='application/pdf')



from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
import os
import random
import string
from datetime import datetime
from .models import Cart, Receipt, Order
from django.contrib.auth.decorators import login_required

@login_required
def process_fictional_payment(request):
    if request.method == 'POST':
        # Get cart items
        cart_items = Cart.objects.filter(user=request.user)
        
        if not cart_items.exists():
            return redirect('view_cart')
        
        # Calculate total price
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create an order (for receipt purposes)
        order = Order.objects.create(
            user=request.user,
            product=cart_items.first().product,  # Just use the first product for simplicity
            quantity=sum(item.quantity for item in cart_items),
            total_price=total_price
        )
        
        # Generate receipt
        receipt = Receipt.objects.create(order=order)
        
        # Prepare receipt data
        receipt_data = {
            'company_name': 'Nyangi Marketplace',
            'company_email': settings.DEFAULT_FROM_EMAIL,
            'company_address': 'P.o.box 1282 TABORA',
            'company_phone': '+255 761 434 077',
            'transaction_id': receipt.transaction_id,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'time': datetime.now().strftime('%H:%M:%S'),
            'username': request.user.username,
            'user_email': request.user.email,
            'payment_method': 'LIPA NO(123456)',
            'shop_name': cart_items.first().product.seller.shop_name if cart_items.first().product.seller else 'Unknown Shop',
            'items': [
                {
                    'name': item.product.name,
                    'quantity': item.quantity,
                    'price': item.product.price,
                    'total': item.product.price * item.quantity
                } for item in cart_items
            ],
            'subtotal': total_price,
            'total': total_price,
            'logo_url': os.path.join(settings.STATIC_URL, 'images/logo.png')  # Make sure you have a logo.png in static/images
        }
        
        # Generate PDF receipt
        html_string = render_to_string('myapp/receipt_template.html', {'receipt': receipt_data})
        html = HTML(string=html_string)
        
        # Ensure receipts directory exists
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'receipts'), exist_ok=True)
        
        # Save PDF
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'receipts', f'{receipt.transaction_id}.pdf')
        html.write_pdf(pdf_path)
        
        # Update receipt with PDF path
        receipt.pdf_file = f'receipts/{receipt.transaction_id}.pdf'
        receipt.save()
        
        # Clear the cart
        cart_items.delete()
        
        # Redirect to receipt download page
        return redirect('download_receipt', receipt_id=receipt.id)
    
    return redirect('view_cart')

def payment_checkout(request):
    # Check if we're coming from an existing order
    order_id = request.GET.get('order_id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            cart_items = order.items.all()
            total_amount = order.total_price
            
            # If this order already has a payment, redirect to orders page
            if Payment.objects.filter(order=order).exists():
                messages.info(request, 'Payment for this order has already been submitted')
                return redirect('user_orders')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
            return redirect('view_cart')
    else:
        # Create a new order from the cart
        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty')
            return redirect('view_cart')
        
        # Calculate total amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create a new order
        order = Order.objects.create(
            user=request.user,
            total_price=total_amount
        )
        
        # Add cart items to order
        for cart_item in cart_items:
            order.items.create(
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
    
    # Get unique sellers from the order items for payment information
    sellers_payment_info = []
    if order_id:
        # For existing orders, get sellers from order items
        for item in cart_items:
            seller = item.product.seller
            if seller not in [info['seller'] for info in sellers_payment_info]:
                sellers_payment_info.append({
                    'seller': seller,
                    'shop_name': seller.shop_name,
                    'mobile_money': seller.mobile_money,
                    'bank_name': seller.bank_name,
                    'account_number': seller.account_number,
                })
    else:
        # For cart items, get sellers
        for item in cart_items:
            seller = item.product.seller
            if seller not in [info['seller'] for info in sellers_payment_info]:
                sellers_payment_info.append({
                    'seller': seller,
                    'shop_name': seller.shop_name,
                    'mobile_money': seller.mobile_money,
                    'bank_name': seller.bank_name,
                    'account_number': seller.account_number,
                })
    
    context = {
        'order': order,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'sellers_payment_info': sellers_payment_info,
        'lipa_number': 'NYANGI-123456'  # Fallback if no seller payment info
    }
    return render(request, 'myapp/payment_checkout.html', context)

def submit_payment_proof(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        reference_number = request.POST.get('reference_number')
        payment_proof = request.FILES.get('payment_proof')
        
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            
            # Get LIPA number (optional)
            lipa_number = request.POST.get('lipa_number', '').strip()
            if not lipa_number:
                lipa_number = None
            
            # Create payment record
            payment = Payment.objects.create(
                order=order,
                user=request.user,
                amount=order.total_price,
                payment_proof=payment_proof,
                lipa_number=lipa_number,
                reference_number=reference_number
            )
            
            # Clear the user's cart
            Cart.objects.filter(user=request.user).delete()
            
            messages.success(
                request, 
                'Payment proof submitted successfully. You will receive your receipt via email once the payment is approved.'
            )
            return redirect('payment_confirmation')
            
        except Order.DoesNotExist:
            messages.error(request, 'Invalid order')
            return redirect('view_cart')
    
    return redirect('view_cart')


@login_required
def seller_payment_list(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        messages.error(request, "You don't have seller privileges.")
        return redirect('home')
    
    # Get all order items containing products from this seller
    order_items = OrderItem.objects.filter(product__seller=seller)
    order_ids = order_items.values_list('order_id', flat=True).distinct()
    
    # Get payments for these orders
    payments = Payment.objects.filter(
        order__id__in=order_ids
    ).order_by('-created_at')
    
    # Filter payments based on request parameters
    status = request.GET.get('status')
    if status:
        payments = payments.filter(status=status)
    
    reviewed = request.GET.get('reviewed')
    if reviewed:
        seller_reviewed = (reviewed == 'yes')
        payments = payments.filter(seller_reviewed=seller_reviewed)
    
    context = {
        'payments': payments,
        'seller': seller,
        'current_status': status,
        'current_reviewed': reviewed
    }
    return render(request, 'myapp/seller_payment_list.html', context)


@login_required

def payment_confirmation(request):
    return render(request, 'myapp/payment_confirmation.html')

@login_required
def user_orders(request):
    """Display all orders for the current user with their approval status"""
    # Get all orders for the current user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # For each order, get payment information if it exists
    orders_data = []
    for order in orders:
        order_info = {
            'order': order,
            'items': order.items.all(),
            'payment': None,
            'status': 'Not Submitted'
        }
        
        # Check if payment exists for this order
        try:
            payment = Payment.objects.get(order=order)
            order_info['payment'] = payment
            order_info['status'] = dict(Payment.PAYMENT_STATUS).get(payment.status, payment.status)
        except Payment.DoesNotExist:
            pass
        
        orders_data.append(order_info)
    
    context = {
        'orders_data': orders_data,
        'title': 'My Orders'
    }
    
    return render(request, 'myapp/user_orders.html', context)


@login_required
@require_POST
def product_interaction(request, product_id):
    """Handle like and dislike functionality for products"""
    product = get_object_or_404(Product, id=product_id)
    interaction_type = request.POST.get('interaction_type')
    
    # Validate interaction type
    if interaction_type not in [ProductInteraction.LIKE, ProductInteraction.DISLIKE]:
        return JsonResponse({'status': 'error', 'message': 'Invalid interaction type'}, status=400)
    
    with transaction.atomic():
        # Check if user already has an interaction with this product
        interaction, created = ProductInteraction.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'interaction_type': interaction_type}
        )
        
        if not created:
            # User is changing their interaction or removing it
            if interaction.interaction_type == interaction_type:
                # User clicked the same button again, remove the interaction
                if interaction.interaction_type == ProductInteraction.LIKE:
                    product.likes_count = max(0, product.likes_count - 1)
                else:
                    product.dislikes_count = max(0, product.dislikes_count - 1)
                interaction.delete()
                interaction_status = 'removed'
            else:
                # User is changing from like to dislike or vice versa
                if interaction.interaction_type == ProductInteraction.LIKE:
                    product.likes_count = max(0, product.likes_count - 1)
                    product.dislikes_count += 1
                else:
                    product.dislikes_count = max(0, product.dislikes_count - 1)
                    product.likes_count += 1
                
                interaction.interaction_type = interaction_type
                interaction.save()
                interaction_status = 'changed'
        else:
            # New interaction
            if interaction_type == ProductInteraction.LIKE:
                product.likes_count += 1
            else:
                product.dislikes_count += 1
            interaction_status = 'added'
        
        product.save()
    
    # Check if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Get the current interaction type after all changes
        current_interaction = None
        try:
            interaction = ProductInteraction.objects.get(user=request.user, product=product)
            current_interaction = interaction.interaction_type
        except ProductInteraction.DoesNotExist:
            pass
            
        return JsonResponse({
            'status': 'success',
            'interaction_status': interaction_status,
            'interaction_type': current_interaction,
            'likes_count': product.likes_count,
            'dislikes_count': product.dislikes_count
        })
    else:
        # Regular form submission - redirect back to product detail
        return redirect('product_detail', id=product_id)


@login_required
def get_product_interaction_status(request, product_id):
    """Get the current user's interaction status with a product"""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        interaction = ProductInteraction.objects.get(user=request.user, product=product)
        interaction_type = interaction.interaction_type
    except ProductInteraction.DoesNotExist:
        interaction_type = None
    
    return JsonResponse({
        'status': 'success',
        'interaction_type': interaction_type,
        'likes_count': product.likes_count,
        'dislikes_count': product.dislikes_count
    })

# Import seller views
from .views_seller import seller_products, seller_orders, seller_order_detail, seller_reports, seller_settings