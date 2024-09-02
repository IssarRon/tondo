from django.urls import path
from .views import get_details, save_details

#define different endpoints
urlpatterns = [
    path('get_details/', get_details, name='get_details'),
    path('save_details/', save_details, name='save_details'),
]
