from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'car'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('car/detail/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/add/', views.AddCarView.as_view(), name='car_add'),
    path('car/about-us/', views.AboutUsView.as_view(), name='about_us'),
    path('car/contact-us/', views.ContactView.as_view(), name='contact_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)