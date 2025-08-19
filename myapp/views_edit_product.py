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
