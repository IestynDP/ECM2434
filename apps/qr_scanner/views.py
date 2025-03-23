from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Restaurant, UserCheckIn, account
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import json
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from apps.accounts.models import Badge, UserBadge
from django.contrib import messages



# QR Scan View (just renders the scanner page)
def qr_scan_view(request):
    return render(request, 'qr_scan/qr_scan.html')

# Scan QR (you can include the logic of scanning here if needed)
def scan_qr(request):
    return render(request, 'qr_scan/qr_scan.html')

# This view handles the QR code check-in logic
@login_required
@csrf_exempt
def checkin_qrcode(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON body
            data = json.loads(request.body)

            # Extract the qr_code_id from the parsed JSON data
            qr_code_id = data.get('qr_code_id')  # Access qr_code_id from the parsed JSON

            if not qr_code_id:
                return JsonResponse({'success': False, 'message': 'QR Code ID is missing'}, status=400)

            # Find the restaurant matching the QR code
            restaurant = Restaurant.objects.filter(qrCodeID=qr_code_id).first()

            if restaurant is None:
                return JsonResponse({'success': False, 'message': 'Invalid QR Code'}, status=400)

            # Use account instead of user
            account = request.user.account  # Get the associated account of the logged-in user

            # Check if the account has already checked in today
            user_check_in = UserCheckIn.objects.filter(
                account=account,  # Changed to account
                restaurant=restaurant,
                check_in_date=date.today()
            ).first()

            if user_check_in:
                return JsonResponse({'success': True, 'already_scanned': True, 'message': 'You already scanned today'})

            # If the account has not checked in, record the check-in and add points to the account
            account.points += restaurant.points  # Add points to the account instead of user
            account.total_points += restaurant.points
            account.save()

            badge_messages = []

            # Award Point Collector badge
            if account.total_points >= 100:
                collector_badge, _ = Badge.objects.get_or_create(
                    name="Point Collector",
                    defaults={"description": "Awarded for collecting 100 total points.",
                              "icon": "badges/point_collector.png"}
                )
                if not UserBadge.objects.filter(user=request.user, badge=collector_badge).exists():
                    UserBadge.objects.create(user=request.user, badge=collector_badge)
                    badge_messages.append("You've earned the 'Point Collector' badge! ")

            # Award Point Hoarder badge
            if account.total_points >= 500:
                hoarder_badge, _ = Badge.objects.get_or_create(
                    name="Point Hoarder",
                    defaults={"description": "Awarded for collecting 500 total points.",
                              "icon": "badges/point_hoarder.png"}
                )
                if not UserBadge.objects.filter(user=request.user, badge=hoarder_badge).exists():
                    UserBadge.objects.create(user=request.user, badge=hoarder_badge)
                    badge_messages.append("You've earned the 'Point Hoarder' badge! ")

            # Record the check-in
            UserCheckIn.objects.create(
                account=account,  # Changed to account
                restaurant=restaurant,
            )

            return JsonResponse({
                'success': True,
                'already_scanned': False,
                'restaurant_name': restaurant.name,
                'points': restaurant.points,
                'total_points': account.points,  # Changed to account
                'badges': badge_messages
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method. Please send a POST request.'}, status=400)


