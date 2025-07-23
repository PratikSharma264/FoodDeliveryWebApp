from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MerchantSignUpForm,  RestaurantRegistrationForm, MerchantForgotPasswordForm, DeliverymanForm, BusinessPlanForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from .models import Merchant, Deliveryman, Restaurant
from django.contrib.auth.forms import SetPasswordForm
from django.http import Http404
from functools import wraps
from django.shortcuts import redirect


def profile_none_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        profile = (
            getattr(request.user, 'deliveryman_profile', None)
            or getattr(request.user, 'restaurant_profile', None)
        )
        if profile is None:
            return view_func(request, *args, **kwargs)
        return redirect('application-status')
    return _wrapped_view


def merchant_home_view(request):
    return render(request, "merchant/m_home.html")


def merchant_login_view(request):
    show_signup = False
    signup_form = MerchantSignUpForm()

    next_url = request.GET.get('next', None)
    print(next_url)
    if next_url:
        request.session['next_url'] = next_url

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == 'signup':
            signup_form = MerchantSignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                return redirect(request.session.get('next_url', 'home'))
            else:
                show_signup = True

        elif form_type == 'login':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect(request.session.get('next_url', 'home'))
            else:
                messages.warning(request, "Invalid login credentials.")
                show_signup = False

    return render(request, "merchant/m_sign_log.html", {
        'signup_form': signup_form,
        'show_signup': show_signup,
    })


@login_required
def merchant_dashboard(request):
    profile = get_object_or_404(Deliveryman, user=request.user)
    return render(request, "merchant/merchant_dashboard.html", {
        'deliveryman': profile,
    })


@login_required
def merchant_logout_view(request):
    logout(request)
    messages.success(request, ("You are successfully logged out"))
    return redirect('signup_login')


@login_required
@profile_none_required
def deliveryman_register_view(request):
    if request.method == "POST":
        form = DeliverymanForm(request.POST, request.FILES)
        if form.is_valid():
            deliveryman = form.save(commit=False)
            deliveryman.user = request.user
            form.save()
            messages.success(
                request, "Your registration has been successfully completed. Welcome aboard.")
            return redirect('merchant-dashboard')
    else:
        form = DeliverymanForm(initial={
            'Email': request.user.email
        })

    return render(request, "merchant/reg_deliveryman.html", {"form": form})


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


@login_required
@profile_none_required
def merchant_res_reg_view(request):
    restaurant_id = request.session.get('restaurant_id')

    # If business plan step
    if restaurant_id:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        if request.method == 'POST':
            plan_form = BusinessPlanForm(request.POST, instance=restaurant)
            if plan_form.is_valid():
                plan_form.save()
                messages.success(
                    request, 'Your business plan has been saved. Welcome aboard.')
                # cleanup session
                request.session.pop('restaurant_id', None)
                return redirect('merchant-dashboard')
        else:
            plan_form = BusinessPlanForm(instance=restaurant)
        return render(request, 'merchant/reg_restaurant.html', {'form': plan_form})

    # Otherwise, general registration step
    if request.method == 'POST':
        form = RestaurantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.user = request.user
            restaurant.save()
            request.session['restaurant_id'] = restaurant.id
            return redirect(request.path)
    else:
        form = RestaurantRegistrationForm()
    return render(request, 'merchant/reg_restaurant.html', {'form': form})


@login_required
def application_status_view(request):
    profile = (
        getattr(request.user, 'deliveryman_profile', None)
        or getattr(request.user, 'restaurant_profile', None)
    )
    if profile is None:
        messages.error(
            request, "Access Denied! You are neither a deliveryman nor a restaurant owner.")
        return redirect('home')

    model_name = profile._meta.model_name  # 'deliveryman' or 'restaurant'

    return render(request, "merchant/application_status.html", {
        'profile': profile,
    })


def merchant_del_reg_view(request):
    pass


def merchant_forgetpassword_view(request):
    if request.method == 'POST':
        form = MerchantForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            try:
                user = User.objects.get(email=email)

                try:
                    merchant = Merchant.objects.get(user=user)

                    current_site = get_current_site(request)
                    mail_subject = 'Reset your merchant password'
                    message = render_to_string('merchant/password_reset_email.html', {
                        'user': user,
                        'merchant': merchant,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        'protocol': 'https' if request.is_secure() else 'http',
                    })

                    email_message = EmailMessage(
                        mail_subject, message, to=[email])
                    email_message.content_subtype = "html"

                    try:
                        email_message.send()
                        messages.success(
                            request, 'Password reset email has been sent. Please check your inbox.')
                        return redirect('email-sent')
                    except Exception as e:
                        messages.error(
                            request, 'Failed to send email. Please try again later.')

                except Merchant.DoesNotExist:
                    messages.error(
                        request, 'This email is not associated with any merchant account.')
            except User.DoesNotExist:
                messages.error(
                    request, 'No account found with that email address.')
    else:
        form = MerchantForgotPasswordForm()

    return render(request, 'merchant/forget_password.html', {'form': form})


def merchant_reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
        merchant = Merchant.objects.get(user=user)
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist, Merchant.DoesNotExist):
        user = None
        merchant = None

    if user is not None and merchant is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(
                    request, 'Your merchant password has been reset successfully.')
                return redirect('signup_login')
        else:
            form = SetPasswordForm(user)

        return render(request, 'merchant/reset_password.html', {'form': form, 'merchant': merchant})
    else:
        messages.error(
            request, 'Password reset link is invalid or has expired.')
        return redirect('signup_login')


def email_sent_view(request):
    return render(request, "merchant/email_sent.html")


def lobby_view(request):
    return render(request, 'merchant/dummy_lobby.html')
