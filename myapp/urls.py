from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin  # Ensure this is imported only once
from . import views
from . import views_password_reset
from . import views_username_validation

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.filter_by_category, name='filter_by_category'),
    path('register_1/', views.seller_register, name='seller_register'),
    path('add-product/', views.addo_product, name='add_product'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
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

    # Password Reset URLs - WhatsApp and Email
    path('password-reset/', views_password_reset.password_reset_choice, name='password_reset_choice'),
    path('password-reset/whatsapp/', views_password_reset.password_reset_whatsapp, name='password_reset_whatsapp'),
    path('password-reset/whatsapp/verify/', views_password_reset.password_reset_whatsapp_verify, name='password_reset_whatsapp_verify'),
    path('password-reset/whatsapp/confirm/', views_password_reset.password_reset_whatsapp_confirm, name='password_reset_whatsapp_confirm'),
    path('password-reset/email/', views_password_reset.password_reset_email_form, name='password_reset_email'),
    path('password-reset/email/verify/', views_password_reset.password_reset_email_verify, name='password_reset_email_verify'),
    path('password-reset/email/confirm/', views_password_reset.password_reset_email_confirm, name='password_reset_email_confirm'),
    path('password-reset/complete/', views_password_reset.password_reset_complete_view, name='password_reset_complete'),
    path('password-reset/resend-code/', views_password_reset.resend_whatsapp_code, name='resend_whatsapp_code'),
    
    # Legacy password reset URLs (keeping for backwards compatibility)
    path('password-reset-old/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),

    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Worker Contract URLs
    path('ceo/contract/create/', views.worker_contract_create, name='worker_contract_create'),
    path('ceo/contract/<int:pk>/', views.worker_contract_detail, name='worker_contract_detail'),
    path('ceo/contract/<int:pk>/pdf/', views.worker_contract_pdf, name='worker_contract_pdf'),
    
    # Subscription URLs
    path('subscription/plans/', views.subscription_plan_list, name='subscription_plan_list'),
    path('subscription/plan/create/', views.subscription_plan_create, name='subscription_plan_create'),
    path('seller/subscription/create/', views.seller_subscription_create, name='seller_subscription_create'),
    
    # About Us URL
    path('about-us/', views.about_us, name='about_us'),
    path('get-category-attributes/', views.get_category_attributes, name='get_category_attributes'),
    path('receipt/<int:receipt_id>/', views.download_receipt, name='download_receipt'),


    path('process-fictional-payment/', views.process_fictional_payment, name='process_fictional_payment'),

    # Username validation URL
    path('check-username-availability/', views_username_validation.check_username_availability, name='check_username_availability'),

    # New Payment URLs
    path('payment/checkout/', views.payment_checkout, name='payment_checkout'),
    path('payment/submit-proof/', views.submit_payment_proof, name='submit_payment_proof'),
    path('payment/confirmation/', views.payment_confirmation, name='payment_confirmation'),
    path('orders/', views.user_orders, name='user_orders'),
    
    # Seller Payment Management URLs
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/payments/', views.seller_payment_list, name='seller_payment_list'),
    path('seller/payments/<int:payment_id>/', views.seller_payment_detail, name='seller_payment_detail'),
    
    # New Seller URLs
    path('seller/products/', views.seller_products, name='seller_products'),
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    path('seller/orders/<int:order_id>/', views.seller_order_detail, name='seller_order_detail'),
    path('seller/reports/', views.seller_reports, name='seller_reports'),
    path('seller/settings/', views.seller_settings, name='seller_settings'),
    
    # Product Interaction URLs
    path('product/<int:product_id>/interaction/', views.product_interaction, name='product_interaction'),
    path('product/<int:product_id>/interaction-status/', views.get_product_interaction_status, name='product_interaction_status'),
]
