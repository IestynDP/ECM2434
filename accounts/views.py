from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm




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