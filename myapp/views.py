from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SellerRegistrationForm, ProductForm, CustomUserRegistrationForm
from .models import Product, Category, Seller,Cart
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import WorkerContract, ParentDetails, Referee, EducationRecord, SubscriptionPlan, SellerSubscription
from .forms import WorkerContractForm, ParentDetailsForm, RefereeForm, EducationRecordForm, SubscriptionPlanForm, SellerSubscriptionForm
import pdfkit
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.timezone import timezone
from datetime import timedelta
from django.contrib.auth.models import User

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

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'myapp/add_product.html', {'form': form})


def product_detail(request, id):
    user = request.user
    product = get_object_or_404(Product, id=id)
    return render(request, 'myapp/product_detail.html', {'product': product,
                                                        'user': user})


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
    return render(request, 'myapp/member_dashboard.html')



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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(request.GET.get('next', 'home'))  # Redirect to 'next' if available
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'myapp/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.phone_number = form.cleaned_data['phone_number']
            user.profile.area_of_residence = form.cleaned_data['area_of_residence']
            user.profile.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
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
        referee1_form = RefereeForm(request.POST, request.FILES, prefix='referee1')
        referee2_form = RefereeForm(request.POST, request.FILES, prefix='referee2')
        education_form = EducationRecordForm(request.POST)

        if all([contract_form.is_valid(), father_form.is_valid(), mother_form.is_valid(),
                referee1_form.is_valid(), referee2_form.is_valid(), education_form.is_valid()]):
            father = father_form.save()
            mother = mother_form.save()
            referee1 = referee1_form.save()
            referee2 = referee2_form.save()
            education = education_form.save()

            contract = contract_form.save(commit=False)
            contract.father = father
            contract.mother = mother
            contract.referee1 = referee1
            contract.referee2 = referee2
            contract.education_record = education
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
                'manyerere201@gmail.com',
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
            'phone': '+255 123 456 789',
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