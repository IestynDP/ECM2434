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
from apps.accounts.models import Restaurant, CheckIn, items, purchases, account # Updated path
from apps.accounts.models import Restaurant, CheckIn  # Updated path

# we can use this for a wide variety of things that we only want admins to be able to do
def is_admin(user):
    return user.is_staff  # Only allow staff/admin users

def privacy_policy(request):
    return render(request, "accounts/privacy_policy.html", {"user": request.user})

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
    #setting up the querysets of dbs relating to the user
    try:
        user_account = account.objects.get(user=request.user)  # Get the logged-in user's account
        user_items = items.objects.all() #get item list
        user_purchases = purchases.objects.filter(user=user_account)
        hatslot = "nohat.PNG"
    except account.DoesNotExist:
        user_account = None  # If no account exists, handle gracefully
    # Updating the avatar to reflect equipped cosmetics
    try:
        equipped = user_purchases.filter(equipState=True)
        for x in equipped:
            if x.item.itemslot == "hat": #currently only one hat exists. more hats and other types will be implemented later
                hatslot = x.item.itemimage
    except items.DoesNotExist: #handles unexpected errors such as and item not existing
        pass
# Check if the button was clicked
    if request.method == "POST":
        action = request.POST.get("action")
        #for handling points for demonstrative purposes - will be removed once actual point gains are added
        if action == "addpoints":
            user_account.points += 5  # Increase points by 5
            user_account.total_points += 5
            user_account.save()
        else:
            action_request = action.split(" ")
            if action_request[0] == "purchase": #purchasing an item
                try:
                    purchaseitem = items.objects.get(itemName=action_request[1]) #item reference
                    #checking if the user has enough points to buy the item
                    if purchaseitem.itemCost > user_account.points:
                        print("not enough points")
                        pass
                    #if they do, proceed
                    if purchaseitem.itemCost <= user_account.points:
                        if not user_purchases.filter(item=purchaseitem).exists(): #checking they have not already bought the item
                            try:
                                user = user_account
                                item = purchaseitem
                                print(user, item)
                                purchases.objects.create(user=user, item=item,equipState=0)
                                user_account.points -= purchaseitem.itemCost
                                user_account.save()
                            except: #handles unexpected failures
                                print("All items in DB:", items.objects.values_list("itemName", flat=True))
                                print("could not create purchase value")
                                pass
                    else:
                        print("item already owned")
                except items.DoesNotExist: #if for whatever reason there isn't a corresponding item
                    print("no item found")
                    pass
            if action_request[0] == "equip":#equipping items
                try:
                    equipitem = items.objects.get(itemName=action_request[1])
                    if user_purchases.filter(item = equipitem).exists():
                        toequip = user_purchases.get(item=equipitem)
                        current_equipState = toequip.equipState
                        equipped = user_purchases.filter(item__itemslot = equipitem.itemslot,equipState=True)
                        #unequipping all ites in that slot
                        for x in equipped:
                            x.equipState = False
                        #flipping the equipped boolean
                        toequip.equipState= not current_equipState
                        toequip.save()
                        print(toequip.equipState,equipitem.itemName)
                except items.DoesNotExist:  # if for whatever reason there isn't a corresponding item
                    print("no cosmetic owned")
                    pass
            return redirect("points")  # Reload the page to show updated points
    return render(request, "points.html", {"user_account": user_account,"items":user_items,"purchases":user_purchases,"hat":hatslot})  # Pass the object to the template

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
    #getting the lists of items/purchases for display
    itemslist = items.objects.order_by('itemid')
    purchaselist = purchases.objects.order_by('id')
    return render(request, "pointsmanagement.html",{"itemlist":itemslist,"purchaselist":purchaselist})


@login_required
def leaderboard(request):
    # top 10 users sorted by points in descending order
    top_players = account.objects.order_by('-points')[:10]
    return render(request, "leaderboard.html", {"top_players": top_players})


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
            return redirect("home")  # Redirect to homepage (update as needed)
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

# Login Vie
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
    # setting up the querysets of dbs relating to the user
    try:
        purchased_items = items.objects.filter(purchases__user__user=user).distinct()#getting the purchased items as a list
        not_purchased_items = items.objects.exclude(purchases__user__user=user)#getting not purchased items
        try:
            equipped = purchases.objects.filter(equipState=True, user__user=user)
            for x in equipped:
                if x.item.itemslot == "header":
                    headerslot = x.item
                if x.item.itemslot == "border":
                    borderslot = x.item
                print(x.item.itemName)
        except items.DoesNotExist:  # handles unexpected errors such as an item not existing
            pass
        #if no items are equipped
        try:
            borderslot
        except:
            borderslot = ""
        try:
            headerslot
        except:
            headerslot=""
    except account.DoesNotExist:
        user_account = None  # If no account exists, handle gracefully
    # Check if the button was clicked
    if request.method == "POST":
        action = request.POST.get("action")
        # for handling points for demonstrative purposes - will be removed once actual point gains are added
        if action == "addpoints":
            user_account.points += 5  # Increase points by 5
            user_account.save()
        else:
            action_request = action.split(" ")
            if action_request[0] == "purchase":  # purchasing an item
                try:
                    purchaseitem = items.objects.get(itemName=action_request[1])  # item reference
                    # checking if the user has enough points to buy the item
                    if purchaseitem.itemCost > user_account.points:
                        print("not enough points")
                        pass
                    # if they do, proceed
                    if purchaseitem.itemCost <= user_account.points:
                        if not purchases.objects.filter(item=purchaseitem,user__user=user).exists():  # checking they have not already bought the item
                            try:
                                user = user_account
                                item = purchaseitem
                                purchases.objects.create(user=user, item=item, equipState=0)
                                user_account.points -= purchaseitem.itemCost
                                user_account.save()
                            except:  # handles unexpected failures
                                print("All items in DB:", items.objects.values_list("itemName", flat=True))
                                print("could not create purchase value")
                                pass
                    else:
                        print("item already owned")
                except items.DoesNotExist:  # if for whatever reason there isn't a corresponding item
                    print("no item found")
                    pass
        if action_request[0] == "equip":  # Equipping items
            try:
                equipitem = items.objects.get(itemName=action_request[1])
                if purchases.objects.filter(item=equipitem,user=user_account).exists():
                    purchases.objects.filter(user=user_account,item__itemslot=equipitem.itemslot).exclude(item=equipitem).update(equipState=False)
                    toequip = purchases.objects.filter(item=equipitem).first()  # Get the first instance safely
                    current_equipState = toequip.equipState
                    toequip.equipState = not current_equipState
                    toequip.save()
            except items.DoesNotExist:  # if for whatever reason there isn't a corresponding item
                print("no cosmetic owned")
            print("b",borderslot,"h",headerslot)
            return render(request, "accounts/profile.html", {
                    "user": user,
                    "user_account": user_account,
                    "border": borderslot,
                    "header": headerslot,
                    "owned": purchased_items,
                    "purchaseable": not_purchased_items
                    })
    print("b", borderslot, "h", headerslot)
    return render(request, "accounts/profile.html", {
        "user": user,
        "user_account": user_account,
        "border":borderslot,
        "header":headerslot,
        "owned":purchased_items,
        "purchaseable":not_purchased_items
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
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Generate QR code only if user is admin
    qr_base64 = None
    if request.user.is_staff:
        qr = qrcode.make(restaurant.qrCodeID)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "restaurants/restaurant_details.html", {
        "restaurant": restaurant,
        "qr_base64": qr_base64,  # Pass QR code data to template
    })

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
