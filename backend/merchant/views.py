from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import MerchantSignUpForm, RestaurantForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def merchant_home_view(request):
    return render(request, "merchant/m_home.html")


def dummyview(request):
    if request.method == 'POST':
        form = MerchantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = MerchantSignUpForm()

    return render(request, 'dummy.html', {'form': form})


def merchant_login_view(request):
    show_signup = False
    signup_form = MerchantSignUpForm()

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'signup':
            signup_form = MerchantSignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect('home')
            else:
                show_signup = True

        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect('home')
            else:
                messages.warning(request, "Invalid login credentials.")
                show_signup = False

    return render(request, "merchant/m_sign_log.html", {
        'signup_form': signup_form,
        'show_signup': show_signup,
    })


@login_required
def merchant_dashboard(request):
    form = RestaurantForm()
    return render(request, "merchant/merchant_dashboard.html", {"form": form})


def merchant_logout_view(request):
    logout(request)
    messages.success(request, ("You are successfully logged out"))
    return redirect('merchant-login')


def deliveryman_register_view(request):
    return render(request, "merchant/reg_deliveryman.html")


def merchant_form_signup(request):
    pass


def merchant_form_login(request):
    pass


def merchant_form_res_reg(request):
    pass


def merchant_form_del_reg(request):
    pass


def merchant_signuplogin_view(request):
    pass


def merchant_forgetpassword_view(request):
    pass


def merchant_res_reg_view(request):
    return render(request, "merchant/reg_restaurant.html")


def merchant_del_reg_view(request):
    pass
