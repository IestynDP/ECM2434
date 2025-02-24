import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now
from .models import account, Restaurant, CheckIn
from .forms import UserProfileForm, AccountForm, RestaurantForm


@login_required # Only logged in users can see the home page
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

# Points View
@login_required
def points_view(request):
    try:
        user_account = account.objects.get(user=request.user)  # Get the logged-in user's account
    except account.DoesNotExist:
        user_account = None  # If no account exists, handle gracefully
# Check if the button was clicked
    if request.method == "POST":
        user_account.points += 1  # Increase points by 1
        user_account.save()
        return redirect("points")  # Reload the page to show updated points

    return render(request, "points.html", {"user_account": user_account})  # Pass the object to the template

@login_required
def leaderboard(request):
    # top 10 users sorted by points in descending order
    top_players = account.objects.order_by('-points')[:10]

    return render(request, "leaderboard.html", {"top_players": top_players})

# Register View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect("home")  # Redirect to homepage (update as needed)
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

# Profile View
@login_required
def profile_view(request, username=None):
    if username is None:
        # Redirect to the logged-in user's profile page
        return redirect('profile_with_username', username=request.user.username)
    
    user = get_object_or_404(User, username=username)  # Fetch user by username
    user_account, created = account.objects.get_or_create(user=user)  # Ensure account exists

    return render(request, "accounts/profile.html", {
        "user": user,
        "user_account": user_account,
    })
    
# Profile Searching
@login_required
def search_users(request):
    query = request.GET.get("q")  # Get search input
    users = User.objects.filter(username__icontains=query) if query else None  # Case-insensitive search

    return render(request, "accounts/search_results.html", {"users": users, "query": query})

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


# ALL RESTAURANT CODE GOES BETWEEN HERE

@login_required
def add_restaurant(request):
    if request.method == "POST":
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user  # Set the restaurant owner
            restaurant.save()
            return redirect("restaurant_list")  # Redirect to the restaurant list page
    else:
        form = RestaurantForm()

    return render(request, "restaurants/add_restaurant.html", {"form": form})

def restaurant_list(request):
    restaurants = Restaurant.objects.filter(verified=True)  # Only show verified restaurants
    return render(request, "restaurants/restaurant_list.html", {"restaurants": restaurants})

@login_required
def check_in(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    user = request.user

    # Check if the user has already checked in today
    today_checkin = CheckIn.objects.filter(user=user, restaurant=restaurant, timestamp__date=now().date()).exists()

    if today_checkin:
        # Prevent multiple check-ins in a single day
        return render(request, "restaurants/check_in_failed.html", {"restaurant": restaurant})

    # Record the check-in
    CheckIn.objects.create(user=user, restaurant=restaurant)

    # Award points to the user
    user_account, created = account.objects.get_or_create(user=user)
    user_account.points += 10  # Award 10 points per check-in (can adjust later)
    user_account.save()

    return render(request, "restaurants/check_in_success.html", {"restaurant": restaurant})


# AND HERE (just for organisation purposes ty ty, i'll tidy the rest up at some point)