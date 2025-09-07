from django import template

register = template.Library()

@register.filter
def get_shop_name(order):
    """
    Return a reliable shop name for an order:
    - If a single seller supplies all items, return that seller.shop_name
    - If multiple sellers, return a comma-separated list of unique shop names
    - On any error or missing data, return a safe default.
    """
    try:
        if hasattr(order, 'items'):
            items = order.items.select_related('product__seller').all()
            names = []
            for item in items:
                product = getattr(item, 'product', None)
                if not product:
                    continue
                seller = getattr(product, 'seller', None)
                if not seller:
                    continue
                shop_name = getattr(seller, 'shop_name', None)
                if not shop_name:
                    # fallback: use associated user username if present
                    user = getattr(seller, 'user', None)
                    shop_name = getattr(user, 'username', None) if user else None
                if shop_name and shop_name not in names:
                    names.append(shop_name)
            
            if not names:
                return "Nyangi Shop"
            if len(names) == 1:
                return names[0]
            return ", ".join(names)
        else:
            # Legacy single product order (if it exists)
            product = getattr(order, 'product', None)
            if product and hasattr(product, 'seller'):
                return getattr(product.seller, 'shop_name', 'Nyangi Shop')
            return "Nyangi Shop"
    except Exception:
        return "Nyangi Shop"
