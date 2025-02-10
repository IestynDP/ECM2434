import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


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

#Points view
@login_required
def points(request):
    return render(request,"points.html")

# Register View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # Create form instance with submitted data
        if form.is_valid():
            user = form.save() 
            login(request, user)  
            return redirect("home")
    else:
        form = UserCreationForm()  # Display an empty form for GET requests
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