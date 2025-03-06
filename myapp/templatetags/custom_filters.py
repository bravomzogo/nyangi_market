# filepath: /home/mdami/Tempo/Nyangi-Market/nyangi_market/myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def in_group(user, group_names):
    return user.is_authenticated and user.user_type in group_names.split(',')