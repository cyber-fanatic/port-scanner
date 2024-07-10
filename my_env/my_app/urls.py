from django.urls import path
from .views import port_scan

urlpatterns = [
    path('scan/', port_scan, name='port_scan'),
]
