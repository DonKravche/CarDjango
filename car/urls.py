from django.urls import path
from . import views

app_name = 'car'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),

    # path('add-product/', views.add_product, name='add_product'),
    # path('login/', views.login_view, name='login'),
    # Add any other necessary URLs here
]