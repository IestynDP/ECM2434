from django.urls import path
from . import views

urlpatterns = [
    path('qr_scanner/qr_scan/', views.qr_scan_view, name='qr_scan'),
    path('scan_qr/', views.scan_qr, name='scan_qr'),
]
