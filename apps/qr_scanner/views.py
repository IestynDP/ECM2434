from django.shortcuts import render
from django.http import JsonResponse
from apps.accounts.models import Restaurant, QRCodeScan
from django.utils import timezone

from django.shortcuts import render, get_object_or_404
from apps.accounts.models import Restaurant, QRCodeScan
from django.http import HttpResponse



def qr_scan_view(request):
    return render(request, 'qr_scan/qr_scan.html')

def scan_qr(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        qr_code_id = data.get('qrCodeID')

        try:
            # Find the restaurant with the given QR Code ID
            restaurant = Restaurant.objects.get(qrCodeID=qr_code_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid QR code.'}, status=400)

        user = request.user  # Assuming the user is authenticated

        # Check if the user has already scanned the restaurant's QR code today
        today = timezone.now().date()
        existing_scan = QRCodeScan.objects.filter(user=user, restaurant=restaurant, scan_date=today).first()

        if existing_scan:
            # If scan exists, return a message indicating the user already scanned
            return JsonResponse({'success': False, 'message': 'You have already scanned this QR code today.'})

        # If no previous scan exists, create a new scan record
        QRCodeScan.objects.create(user=user, restaurant=restaurant, scan_date=today)

        # Return success message with check-in details
        return JsonResponse({
            'success': True,
            'message': f"Successfully checked into {restaurant.name}. You gained {restaurant.points} points!",
            'restaurant_name': restaurant.name,
            'restaurant_points': restaurant.points
        })
    return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)