from django.urls import path
from . import views
from apps.qr_scanner.views import qr_scan  # Updated path

urlpatterns = [
    path("scan-qr/", views.qr_scan, name='qr_scan'),
    path('check-restaurant-link/', views.check_restaurant_link, name='check_restaurant_link'),
    path('check-in/<int:restaurant_id>/', views.check_in, name='check_in'),
]