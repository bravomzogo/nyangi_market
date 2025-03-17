from django.urls import path
from .views import buy_page, initiate_mpesa_payment ,receipt_view
from .views import (
    home,
    filter_by_category,
    seller_register,
    add_product,
    product_detail,
    seller_login,
    seller_logout,
    member_dashboard,
    view_cart,
    add_to_cart,
    remove_from_cart,
)
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('category/<str:category_name>/', filter_by_category, name='filter_by_category'),
    path('register_1/', seller_register, name='seller_register'),
    path('add-product/', add_product, name='add_product'),
    path('product/<int:id>/', product_detail, name='product_detail'),
    path('login_1/', seller_login, name='seller_login'),
    path('logout_1/', seller_logout, name='logout'),
    path('dashboard/', member_dashboard, name='member'),
    path('buy/', buy_page, name='buy_page'),
    path('initiate-mpesa-payment/', initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('receipt/', receipt_view, name='receipt_view'),
    path('payment-pin-input/<int:product_id>/', views.payment_pin_input, name='payment_pin_input'),
    path('process-payment-pin/', views.process_payment_pin, name='process_payment_pin'),
    path('initiate-payment/', views.initiate_mpesa_payment, name='initiate_payment'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),




]
