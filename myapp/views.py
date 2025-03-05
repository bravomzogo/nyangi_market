from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .forms import TechForm
from .models import Product , Tech
from django.core.paginator import Paginator
from django.http import JsonResponse

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    tech = get_object_or_404(Tech, id=id)
    return render(request, 'myapp/product_detail.html', {'product': product,'tech': tech})

def index(request):
    products = Product.objects.all()
    paginator = Paginator(products, 9)  # Show 5 products per page
    page_number = request.GET.get('page', 1)  # Get the page number from the request
    page_obj = paginator.get_page(page_number)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # If it's an AJAX request, return JSON data
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
    return render(request, 'myapp/index.html', {'products': page_obj})



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
