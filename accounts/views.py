from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


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
