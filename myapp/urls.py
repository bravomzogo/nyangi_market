from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<str:category_name>/', views.filter_by_category, name='filter_by_category'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    path('seller/register/', views.seller_register, name='seller_register'),
    path('product/add/', views.add_product, name='add_product'),
    path('login/', views.seller_login, name='seller_login'),
    path('logout/', views.seller_logout, name='logout'),
    path('dashboard/', views.member_dashboard, name='member'),
]
