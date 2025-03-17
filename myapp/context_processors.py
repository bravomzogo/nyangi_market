# context_processors.py
from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        return {'cart_item_count': Cart.objects.filter(user=request.user).count()}
    return {'cart_item_count': 0}