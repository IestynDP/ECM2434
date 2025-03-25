import base64
import random
import string
from django.db import connection
from django.db.models import Q
from io import BytesIO
import qrcode
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse # Updated path
from apps.accounts.forms import UserProfileForm, AccountForm, RestaurantForm  # Updated path
from django.http import JsonResponse
from apps.accounts.models import account, items, purchases  # Updated path
from apps.accounts.forms import UserProfileForm, AccountForm, RestaurantForm, ItemForm # Updated path
from django.utils.timezone import now
from apps.accounts.models import Restaurant, items, purchases, account,UserCheckIn # Updated path
import os
from django.http import JsonResponse
from apps.accounts.models import Restaurant
from django.utils import timezone
from django.db import transaction
import logging


# we can use this for a wide variety of things that we only want admins to be able to do
def is_admin(user):
    return user.is_staff  # Only allow staff/admin users

def privacy_policy(request):
    return render(request, "accounts/privacy_policy.html", {"user": request.user})

@login_required # Only logged in users can see the home page
# sustainability fact for homepage
def home(request):
    fun_facts = [
        "Recycling one ton of paper saves 17 trees! 🌳",
        "The University of Exeter has reduced carbon emissions by 20% since 2015! 🌎",
        "Switching off unused lights saves up to 10% energy! 💡",
        "A single reusable bottle can replace 167 plastic bottles per year! 🚰",
        "A leaky faucet that drips once per second wastes over 3,000 gallons of water per year! 🚿",
        "Using public transport instead of a car can reduce your carbon footprint by up to 30%! 🚌",
        "Producing one hamburger uses 660 gallons of water – the same as **2 months of showers**! 🍔🚿",
        "Turning off your laptop overnight can save enough electricity to charge your phone for 6 months! 🔋",
        "The UK generates 26 million tons of waste every year – recycling can cut this by half! ♻️",
        "Planting just **one** tree can absorb over 48 pounds of CO₂ per year! 🌲",
        "Leaving appliances on standby mode still uses **5-10%** of their energy consumption. 🔌",
        "If food waste were a country, it would be the **third biggest CO₂ emitter** in the world! 🍏",
        "LED bulbs use **75% less energy** than traditional bulbs and last 25 times longer. 💡",
        "Riding a bike for short trips instead of driving reduces **90% of CO₂ emissions** per trip! 🚲",
        "One cotton T-shirt takes **2,700 liters of water** to produce – equivalent to 3 years of drinking water! 👕",
        "Producing paper from recycled materials uses **70% less energy** than virgin paper. 📄",
        "An estimated **8 million tons of plastic** enter the ocean every year. 🐠",
        "More than **50% of food waste** can be composted instead of sent to landfills. 🍎",
        "Solar panels can reduce a home’s carbon footprint by **80%** per year! ☀️",
        "Plastic straws take over **200 years** to decompose – switch to reusable ones! 🥤",
        "Every kilogram of beef requires **15,400 liters of water** to produce! 🥩💧",
        "Microwaving food is **more energy-efficient** than using a stove or oven. 🍲",
        "It takes **500-1,000 years** for plastic bottles to decompose in landfills. 🚯",
        "Using **eco-friendly search engines** like Ecosia helps plant trees with each search! 🌱🔍",
        "By 2050, there will be more plastic in the ocean than fish if we don’t take action! 🌊",
    ]
    
    fact = random.choice(fun_facts)
    return render(request, "home.html", {"fact": fact})

@login_required
def profile_redirect(request):
    return redirect("profile")

@login_required
#@user_passes_test(is_admin)
def manage_items(request):
    #handling requests
    if request.method == "POST":
        action = request.POST.get("action")
        if isinstance(action,str):
            commands = action.split(" ")
            #deleting the item from items and removing it from purchases
            if commands[0] == "delete":
                item = get_object_or_404(items, itemid = int(commands[1]))
                purchases.objects.filter(item=item).delete()
                item.delete()
        form = ItemForm(request.POST,request.FILES)
        if not form.is_valid():
            print("error submitting form")
        if form.is_valid():
            form.save()
        return redirect("profile_redirect")
    #getting the lists of items/purchases for display
    itemslist = items.objects.order_by('itemid')
    purchaselist = purchases.objects.order_by('id')
    return render(request, "pointsmanagement.html",{"itemlist":itemslist,"purchaselist":purchaselist})


@login_required
def leaderboard(request):
    # top 10 users sorted by points in descending order
    top_players = account.objects.order_by('-total_points')[:10]
    return render(request, "leaderboard.html", {"top_players": top_players})


# Articles with info for the info page
def info(request):
    articles = [
        {
            "title": "Devon Food Partnership",
            "summary": "Ensuring affordable, nutritious, and locally sourced food for all in Devon.",
            "url": "https://devonclimateemergency.org.uk/taking-action-old/devon-sustainable-food-partnership/"
        },
        {
            "title": "Sustainable Seafood Initiatives in Plymouth",
            "summary": "A project to introduce fish fingers made from locally caught fish into schools, reducing food waste and supporting local fisheries.",
            "url": "https://www.theguardian.com/environment/article/2024/aug/18/fish-finger-sandwich-plymouth-project-rebrand-rejected-catch-for-schools"
        },
        {
            "title": "National Trust Tree Planting Initiatives",
            "summary": "An Initiative where nearly half a million trees are being planted across the UK, including 30,000 at Buckland Abbey in Devon.",
            "url": "https://www.theguardian.com/uk-news/2025/jan/17/national-trust-plant-almost-half-a-million-trees-winter"
        },
        {
            "title": "Environmental Land Management Scheme (ELMS)",
            "summary": "UK farmers, including those in Devon, are adopting eco-friendly farming through ELMS, boosting biodiversity.",
            "url": "https://www.theguardian.com/environment/article/2024/aug/23/baby-owls-farming-policy-wildlife-environmental-land-management-england"
        }
    ]

    return render(request, "info.html", {"articles": articles})

# Register View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect("home")  # Redirects to homepage
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect("login")





from django.db import transaction

@login_required
def profile_view(request, username=None):
    if username is None:
        return redirect('profile_with_username', username=request.user.username)

    user = get_object_or_404(User, username=username)
    user_account, created = account.objects.get_or_create(user=user)

    try:
        purchased_items = items.objects.filter(purchases__user__user=user).distinct()
        not_purchased_items = items.objects.exclude(purchases__user__user=user)
        equipped_items = purchases.objects.filter(user__user=user, equipState=True)

        header = None
        border = None

        for item in equipped_items:
            if item.item.itemslot == "header":
                header = item.item
            if item.item.itemslot == "border":
                border = item.item

    except account.DoesNotExist:
        user_account = None

    success = False  # Flag to track if an item was equipped successfully

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "addpoints":
            user_account.points += 5
            user_account.save()

        else:
            action_request = action.split(" ")

            if len(action_request) < 2:
                return redirect("profile_redirect")

            if action_request[0] == "purchase":
                try:
                    purchaseitem = items.objects.get(itemName=action_request[1])
                    if purchaseitem.itemCost > user_account.points:
                        pass  # Not enough points
                    elif purchaseitem.itemCost <= user_account.points:
                        if not purchases.objects.filter(item=purchaseitem, user__user=user).exists():
                            purchases.objects.create(user=user_account, item=purchaseitem, equipState=False)
                            user_account.points -= purchaseitem.itemCost
                            user_account.save()
                except items.DoesNotExist:
                    pass

            if action_request[0] == "equip":
                try:
                    equipitem = items.objects.get(itemName=action_request[1])

                    # Ensure the user has purchased the item
                    purchase_record = purchases.objects.filter(item=equipitem, user=user_account).first()

                    if purchase_record:  # Item found in user's purchased items
                        with transaction.atomic():  # Ensures all changes are made as a single transaction
                            if not purchase_record.equipState:
                                purchases.objects.filter(
                                    user=user_account,
                                    item__itemslot=equipitem.itemslot,
                                    equipState=True
                                ).update(equipState=False)  # Disable other items in the same slot


                                purchase_record.equipState = True
                                purchase_record.save()
                                

                                success = True
                except items.DoesNotExist:
                    pass

    return render(request, "accounts/profile.html", {
        "user": user,
        "user_account": user_account,
        "header": header,
        "border": border,
        "owned": purchased_items,
        "purchaseable": not_purchased_items,
        "equipped_items": equipped_items,
        "success": success
    })













    
# Profile Searching
def search_users(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query)

    # Create a dictionary to store the avatar URL for each user
    user_avatars = {}

    for user in users:
        # Check if user has an avatar
        avatar_url = user.account.avatar.url if user.account.avatar else None
        user_avatars[user] = avatar_url

    context = {
        'users': users,
        'user_avatars': user_avatars,  # Passing the user avatars to the template
        'query': query,
    }

    return render(request, "accounts/search_results.html", context)



# Editing Profiles
@login_required
def edit_profile(request, username=None):
    if username is None:
        username = request.user.username  # Set the username to the logged-in user's username

    if username != request.user.username:
        return redirect('profile_with_username', username=request.user.username)

    user = get_object_or_404(User, username=username)  # Fetch user by username
    user_account, created = account.objects.get_or_create(user=user)  # Ensure account exists

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        account_form = AccountForm(request.POST, request.FILES, instance=user_account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect('profile_with_username', username=user.username)

    else:
        user_form = UserProfileForm(instance=user)
        account_form = AccountForm(instance=user_account)

    return render(request, "accounts/edit_profile.html", {
        "user_form": user_form,
        "account_form": account_form,
        "user": user,
    })
    

@login_required
def delete_account(request):
    user = request.user
    user.delete()  # Completely removes user data
    logout(request)
    return redirect("home")  # Redirect to home page

def privacy_policy(request):
    return render(request, "privacy_policy.html")

@login_required
def download_data(request):
    """Allows users to download their personal data in JSON format."""
    user = request.user
    user_account = account.objects.get(user=user)

    data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "bio": user_account.bio if user_account else "",
        "points": user_account.points if user_account else 0,
    }

    return JsonResponse(data, json_dumps_params={"indent": 2})


def generate_unique_qr_code():
    # Generate a unique 16-character alphanumeric QR Code, only querying the DB after migration
    qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

    # Check if the table exists before querying the database
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts_restaurant';")
        table_exists = cursor.fetchone() is not None  # True if the table exists

    if table_exists:
        while Restaurant.objects.filter(qrCodeID=qr_code).exists():
            qr_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))  # Generate a new one if duplicate

    return qr_code


@login_required
@user_passes_test(is_admin)
def add_restaurant(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user  # Assign the logged-in admin as the owner
            
            restaurant.save()  # ✅ Force Django to generate an ID

            # Refresh to ensure the ID is generated
            restaurant.refresh_from_db()

            # Now assign the QR Code ID
            restaurant.qrCodeID = generate_unique_qr_code()
            restaurant.save()  # ✅ Save again with the QR Code

            return redirect("restaurant_list")
    else:
        form = RestaurantForm()

    return render(request, "restaurants/add_restaurant.html", {"form": form})


def restaurant_list(request):
    query = request.GET.get("q")  # Get search query from URL
    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(Q(name__icontains=query) | Q(location__icontains=query))

    return render(request, "restaurants/restaurant_list.html", {"restaurants": restaurants})





def restaurant_details(request, restaurant_id):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
        data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'description': restaurant.description,
            'location': restaurant.location,
            'sustainability_features': restaurant.sustainability_features,
        }
        if request.user.is_staff:
            data['qr_base64'] = restaurant.qr_code_base64()
        return JsonResponse(data)
    except Restaurant.DoesNotExist:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)



def check_in(request, restaurant_id):
    # Get the restaurant object
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    
    # Check if the user has already checked in today at the same restaurant
    if UserCheckIn.objects.filter(user=request.user, restaurant=restaurant, scan_date=timezone.now().date()).exists():
        return HttpResponse("You have already checked in today at this restaurant.", status=400)

    # If not, create a new check-in entry
    UserCheckIn.objects.create(user=request.user, restaurant=restaurant, scan_date=timezone.now().date())

    return HttpResponse(f"Checked in successfully at {restaurant.name}!", status=200)

