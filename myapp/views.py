from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .forms import TechForm
from .models import Product , Tech
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    return render(request, 'myapp/profile.html')

@login_required
def settings_view(request):
    return render(request, 'myapp/settings.html')

# @login_required(login_url='login')
# def cart_view(request):
#     cart = get_cart_for_user(request.user)  # Example function to get the cart
#     return render(request, 'myapp/cart.html', {'cart': cart})












def product_detail(request, id):  # Ensure 'id' is the parameter name
    # Fetch the product
    product = get_object_or_404(Product, id=id)
    
    # Try to fetch the Tech object, but don't raise a 404 if it doesn't exist
    try:
        tech = Tech.objects.get(id=id)
    except Tech.DoesNotExist:
        tech = None
    
    return render(request, 'myapp/product_detail.html', {'product': product, 'tech': tech})


from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, TANZANIA_REGIONS

def index(request):
    categories = Product.CATEGORY_CHOICES
    regions = TANZANIA_REGIONS
    
    # Get search parameters from the GET request
    keyword = request.GET.get('keyword', '')
    category = request.GET.get('category', '')
    location = request.GET.get('location', '')
    
    # Start with all products
    products = Product.objects.all()

    # Apply filters if parameters are provided
    if keyword:
        products = products.filter(name__icontains=keyword)

    if category and category != 'All Categories':
        products = products.filter(category=category)

    if location and location != 'Location':
        products = products.filter(location=location)

    # Pagination setup
    paginator = Paginator(products, 3)  # Show 9 products per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # If it's an AJAX request, return JSON data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [
            {
                'id': product.id,
                'name': product.name,
                'image': product.image.url,
                'category': product.get_category_display(),
                'location': product.get_location_display(),
                'price': product.price,
                'description': product.description,
                'stock': product.stock,
                'created_at': product.created_at.strftime("%b %d, %Y"),
            }
            for product in page_obj
        ]
        return JsonResponse({'products': products_data, 'has_next': page_obj.has_next()})

    # For the initial page load, render the template
    return render(request, 'myapp/index.html', {
        'products': page_obj,
        'categories': categories,
        'regions': regions,
        'keyword': keyword,
        'category': category,
        'location': location,
    })





def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('tech_details')  # Redirect to the product list page after adding
    else:
        form = ProductForm()
    return render(request, 'myapp/add_product.html', {'form': form})

def add_tech(request, product_id=None):
    if request.method == 'POST':
        form = TechForm(request.POST)
        if form.is_valid():
            tech = form.save()
            if product_id:
                product = get_object_or_404(Product, id=product_id)
                product.tech = tech
                product.save()
            return redirect('index')  # Or redirect to product_detail
    else:
        form = TechForm()
    return render(request, 'myapp/add_technical_details.html', {'form': form})