from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import Restaurant
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from accounts.models import CheckIn,account

@login_required  
def qr_scan(request):
    return render(request, "qr_scanner/qr_scan.html")

@csrf_exempt
def check_restaurant_link(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        try:
            restaurant = Restaurant.objects.get(link=link)
            return JsonResponse({'exists': True, 'restaurant_id': restaurant_id})
        except Restaurant.DoesNotExist:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
@csrf_exempt
@login_required
def check_in(request, restaurant_id):
    if request.method == 'POST':
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        user = request.user

        if CheckIn.objects.filter(user=user, restaurant=restaurant, timestamp__date=now().date()).exists():
            return JsonResponse({'status': 'failed', 'message': 'you already checked in today!'})

        CheckIn.objects.create(user=user, restaurant=restaurant)

        user_account, created = account.objects.get_or_create(user=user)
        user_account.points += 5
        user_account.save()

        return JsonResponse({'status': 'success', 'message': 'you gained 5 points'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)