from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SellerRegistrationForm, ProductForm
from .models import Product, Category, Seller,Cart
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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

    if query:
        products = products.filter(name__icontains=query)

    message = "No products found matching your search query." if not products else ""


    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()

    return render(request, 'myapp/home.html', {
        'products': products,
        'recent_products': recent_products,
        'query': query,
        'message': message,
        'categories': categories,
        'cart_item_count': cart_item_count
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
    product = get_object_or_404(Product, id=id)
    return render(request, 'myapp/product_detail.html', {'product': product})


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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    
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