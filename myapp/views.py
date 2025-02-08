from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SellerRegistrationForm, ProductForm
from .models import Product, Category


def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = request.GET.get('query', '')
    if query:
        products = products.filter(name__icontains=query)

    # Check if no products are found
    if not products:
        message = "No products found matching your search query."
    else:
        message = ""

    return render(request, 'myapp/home.html', {'products': products, 'query': query, 'message': message, 'categories':categories})

def filter_by_category(request, category_name):
    products = Product.objects.filter(category__name=category_name)
    categories = Category.objects.all()
    return render(request, 'myapp/home.html', {'products': products, 'categories': categories, 'category_name': category_name})



def seller_register(request):
    # If the user is already logged in, redirect them to the home page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            seller = form.save()  # Save the seller
            login(request, seller.user)  # Log in the user after registration
            return redirect('home')  # Redirect to home page after registration
    else:
        form = SellerRegistrationForm()

    return render(request, 'myapp/seller_register.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SellerRegistrationForm, ProductForm
from .models import Product, Seller

def add_product(request):
    # Check if the user is logged in and has a seller profile
    if not request.user.is_authenticated or not hasattr(request.user, 'seller'):
        return redirect('seller_register')  # Redirect to seller registration if not registered

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller  # Assign the logged-in seller to the product
            product.save()
            return redirect('home')  # Redirect to home after saving the product
    else:
        form = ProductForm()  # If not POST, show the form

    return render(request, 'myapp/add_product.html', {'form': form})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'myapp/product_detail.html', {'product': product})



from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def seller_login(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect authenticated users to home page
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home page after login
            else:
                form.add_error(None, "Invalid credentials.")
    else:
        form = AuthenticationForm()

    return render(request, 'myapp/login.html', {'form': form})
from django.contrib.auth import logout
from django.shortcuts import redirect

def seller_logout(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

from django.shortcuts import render

def member_dashboard(request):
    return render(request, 'myapp/member_dashboard.html')

