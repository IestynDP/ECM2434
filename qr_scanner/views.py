from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required  
def qr_scan(request):
    return render(request, "qr_scanner/qr_scan.html")