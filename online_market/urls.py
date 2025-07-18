from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
