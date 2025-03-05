from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .forms import TechForm
from .models import Product , Tech
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, TANZANIA_REGIONS




def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    tech = get_object_or_404(Tech, id=id)
    return render(request, 'myapp/product_detail.html', {'product': product,'tech': tech})

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product, TANZANIA_REGIONS

def index(request):
    categories = Product.CATEGORY_CHOICES
    regions = TANZANIA_REGIONS
    
    # Get search parameters from the GET request
    keyword = request.GET.get('keyword', '')  # Default to empty string if no keyword is provided
    category = request.GET.get('category', '')  # Default to empty string if no category is selected
    location = request.GET.get('location', '')  # Default to empty string if no location is selected
    
    # Start with all products
    products = Product.objects.all()

    # Apply filters if parameters are provided
    if keyword:
        products = products.filter(name__icontains=keyword)  # Filter products by name containing keyword

    if category and category != 'All Categories':  # Ignore the default 'All Categories' value
        products = products.filter(category=category)

    if location and location != 'Location':  # Ignore the default 'Location' value
        products = products.filter(location=location)

    # Pagination setup
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page', 1)  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    # If it's an AJAX request, return JSON data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [
            {
                'name': product.name,
                'image': product.image.url,
                'category': product.category,
                'location': product.location,
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

def add_tech(request):
    if request.method == 'POST':
        form = TechForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the product list page after adding
    else:
        form = TechForm()
    return render(request, 'myapp/add_technical_details.html', {'form': form})
