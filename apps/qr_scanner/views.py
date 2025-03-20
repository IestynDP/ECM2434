from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import date
from apps.accounts.models import Restaurant, UserCheckIn
from django.shortcuts import render

def qr_scan(request):
    # Your logic for handling QR scanning
    return render(request, 'qr_scanner/scan.html')

@login_required
def qr_scanner(request):
    return render(request, 'qr_scanner.html')

@login_required
def validate_qr(request, qr_codeid):
    # Check if the QR code matches a valid restaurant
    try:
        restaurant = Restaurant.objects.get(qr_codeid=qr_codeid)
        # Check if the user has already checked in today
        today = date.today()
        if UserCheckIn.objects.filter(user=request.user, restaurant=restaurant, check_in_date=today).exists():
            return JsonResponse({'status': 'checked_in', 'restaurant_name': restaurant.name})
        return JsonResponse({'status': 'valid', 'restaurant_name': restaurant.name, 'points': restaurant.points})
    except Restaurant.DoesNotExist:
        return JsonResponse({'status': 'invalid'})
