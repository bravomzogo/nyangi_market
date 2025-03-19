from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.filter_by_category, name='filter_by_category'),
    path('register_1/', views.seller_register, name='seller_register'),
    path('add-product/', views.addo_product, name='add_product'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('login_1/', views.seller_login, name='seller_login'),
    path('logout_1/', views.seller_logout, name='logout'),
    path('dashboard/', views.member_dashboard, name='member'),
    path('buy/', views.buy_page, name='buy_page'),
    path('initiate-mpesa-payment/', views.initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('receipt/', views.receipt_view, name='receipt_view'),
    path('payment-pin-input/<int:product_id>/', views.payment_pin_input, name='payment_pin_input'),
    path('process-payment-pin/', views.process_payment_pin, name='process_payment_pin'),
    path('initiate-payment/', views.initiate_mpesa_payment, name='initiate_payment'),
    
    # Auth URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Password Reset URLs
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
