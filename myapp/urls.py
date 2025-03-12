from django.urls import path
from .views import register, login_view, index, add_product, add_tech, product_detail, logout_view, profile_view, settings_view
# cart_view
from .views import register, login_view, index, add_product, add_tech, product_detail, logout_view, profile_view, settings_view
# cart_view
from . import views


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('', index, name='index'),
    path('add/', add_product, name='add_product'),
     path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('tech/',views.add_tech, name='tech_details'),
    path('logout/', logout_view, name='logout_view'),
    path('profile/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    # path('cart/', cart_view, name='cart'),
    # path('cart/', cart_view, name='cart'),
]
