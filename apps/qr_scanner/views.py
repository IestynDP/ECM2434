from typing import Dict, Any
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from datetime import date
import json
from apps.accounts.models import (
    Restaurant,
    UserCheckIn,
    account,
    Badge,
    UserBadge,
)

def qr_scan_view(request: HttpRequest) -> HttpResponse:
    """Render the QR code scanner page."""
    return render(request, 'qr_scan/qr_scan.html')

def scan_qr(request: HttpRequest) -> HttpResponse:
    """Render the QR scanner interface."""
    return render(request, 'qr_scan/qr_scan.html')

@login_required
@csrf_exempt
def checkin_qrcode(request: HttpRequest) -> JsonResponse:
    """
    Handle QR code check-in logic.

    Process a QR code scan, verify the restaurant, and award points and badges
    if appropriate. Prevents multiple check-ins on the same day.

    Args:
        request: The HTTP request object containing the QR code data

    Returns:
        JsonResponse: Response containing success status, points awarded, and any earned badges
    
    Raises:
        JsonResponse: With error message if request is invalid or processing fails
    """
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


            account = request.user.account  # Get the associated account of the logged-in user

            # Check if the account has already checked in today
            user_check_in = UserCheckIn.objects.filter(
                account=account,
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
                account=account,
                restaurant=restaurant,
            )

            return JsonResponse({
                'success': True,
                'already_scanned': False,
                'restaurant_name': restaurant.name,
                'points': restaurant.points,
                'total_points': account.points,
                'badges': badge_messages
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method. Please send a POST request.'}, status=400)