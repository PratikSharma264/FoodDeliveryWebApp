from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MerchantSignUpForm, RestaurantForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def merchant_signup_view(request):
    if request.method == 'POST':
        form = MerchantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('merchant-sign-up')
    else:
        form = MerchantSignUpForm()

    return render(request, 'merchant/merchant_signup.html', {'form': form})


def merchant_login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In")

            return redirect("merchant-dashboard")
        else:
            messages.warning(request, "There was an error logging you in")

            return redirect("merchant-login")
    else:
        return render(request, "merchant/merchant_login.html", {})


@login_required
def merchant_dashboard(request):
    form = RestaurantForm()
    return render(request, "merchant/merchant_dashboard.html", {"form": form})


def merchant_logout_view(request):
    logout(request)
    messages.success(request, ("You are successfully logged out"))
    return redirect('merchant-login')
