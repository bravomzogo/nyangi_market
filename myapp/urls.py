from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_product, name='add_product'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('tech/',views.add_tech, name='tech_details')

]
