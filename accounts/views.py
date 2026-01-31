from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
import os
from django.http import HttpResponse
from django.contrib.auth.models import User

def register(request):
    """
    Handles user registration.
    Creates a new user account after validating the form.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Display empty registration form
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    """
    Authenticates and logs in an existing user.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "accounts/login.html")


def user_logout(request):
    """
    Logs out the current user and clears session messages.
    """
    # Clear any pending messages before logout
    list(messages.get_messages(request))

    logout(request)
    return redirect("login")

def create_superuser_once(request):
    """
    Creates a superuser ONE TIME using env variables.
    Disable/remove after it works.
    """
    token = request.GET.get("token")
    if token != os.environ.get("ADMIN_CREATE_TOKEN"):
        return HttpResponse("Forbidden", status=403)

    username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Admin@12345")

    if User.objects.filter(username=username).exists():
        return HttpResponse("Superuser already exists ✅")

    User.objects.create_superuser(username=username, email=email, password=password)
    return HttpResponse("Superuser created ✅ You can now login to /admin")
