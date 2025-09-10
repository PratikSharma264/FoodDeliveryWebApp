from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MerchantSignUpForm,  RestaurantRegistrationForm, MerchantForgotPasswordForm, DeliverymanForm, FoodItemForm, RestaurantBioUpdateForm, RestaurantProfilePicUpdateForm, RestaurantLocationUpdateForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from .utils import account_activation_token
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from .models import Merchant, Deliveryman, Restaurant, FoodItem
from django.contrib.auth.forms import SetPasswordForm
from django.http import Http404, JsonResponse
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse


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


def merchant_signup_view(request):
    if request.method == "POST":
        signup_form = MerchantSignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.is_staff = False
            user.is_superuser = False
            user.save()
            logout(request)
            login(request, user)

            messages.success(
                request, "Account created. You are now logged in.")
            return redirect("home")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        signup_form = MerchantSignUpForm()

    return render(request, "merchant/merchant_signup.html", {"signup_form": signup_form})


@require_http_methods(["GET", "POST"])
def merchant_login_view(request):
    next_url = request.GET.get('next') or request.session.get('next_url')
    if request.user.is_authenticated:
        return redirect(next_url or "home")

    if request.method == "POST":
        next_url = request.POST.get("next") or next_url
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect(next_url or "home")
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, "merchant/merchant_login.html", {"next": next_url})


@login_required
def deliveryman_dashboard(request):
    try:
        profile = Deliveryman.objects.get(user=request.user)
    except Deliveryman.DoesNotExist:
        return redirect('restaurant-dashboard')
    return render(request, "merchant/deliveryman_dashboard.html", {
        'deliveryman': profile,
    })


@login_required
def merchant_logout_view(request):
    logout(request)
    messages.success(request, ("You are successfully logged out"))
    return redirect('home')


@login_required
@profile_none_required
def merchant_form_register_view(request):
    role = request.POST.get('role') or request.GET.get('role')

    if request.method == "POST":
        if role == "restaurant":
            form = RestaurantRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                restaurant = form.save(commit=False)
                restaurant.user = request.user
                restaurant.save()
                form.save_m2m()
                messages.success(
                    request, 'Your restaurant has been registered. Welcome aboard.')
                return redirect('home')

        elif role == "deliveryman":
            form = DeliverymanForm(request.POST, request.FILES)
            if form.is_valid():
                deliveryman = form.save(commit=False)
                deliveryman.user = request.user
                deliveryman.save()
                form.save_m2m()
                messages.success(
                    request, "Your registration has been successfully completed. Welcome aboard.")
                return redirect('home')
    else:
        if role == "restaurant":
            form = RestaurantRegistrationForm(
                initial={'Email': request.user.email})
        else:
            form = DeliverymanForm(initial={'Email': request.user.email})

    return render(request, "merchant/merchant_form_register.html", {"form": form})


@login_required
@profile_none_required
def merchant_res_reg_view(request):

    if request.method == 'POST':
        form = RestaurantRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            messages.success(
                request, 'Your restaurant has been registered. Welcome aboard.')
            return redirect('application-status')
    else:
        form = RestaurantRegistrationForm()

    return render(request, 'merchant/reg_restaurant.html', {'form': form})

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
def bio_json_response(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, user=request.user)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = {
            "restaurant_name": restaurant.restaurant_name,
            "restaurant_address": restaurant.restaurant_address,
            "description": restaurant.description,
            "owner_name": restaurant.owner_name,
            "owner_contact": restaurant.owner_contact,
            "owner_email": restaurant.owner_email,
            "restaurant_type": restaurant.restaurant_type,
        }
        return JsonResponse({"success": True, "data": data})
    form = RestaurantBioUpdateForm(instance=restaurant)
    return render(request, "merchant/restaurant_update_form.html", {"form": form})

@login_required
def update_restaurant_bio(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, user=request.user)

    if request.method == "POST":
        form = RestaurantBioUpdateForm(
            request.POST, request.FILES, instance=restaurant
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant updated successfully.")
        else:
            messages.error(request, "Failed to update restaurant. Please check the form inputs.")

    return redirect("restaurant-settings")

@login_required
def update_restaurant_profile_picture(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, user=request.user)

    if request.method == "POST":
        form = RestaurantProfilePicUpdateForm(
            request.POST, request.FILES, instance=restaurant
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(request, "Failed to update profile picture. Please try again.")

    return redirect("restaurant-settings")

@login_required
def update_restaurant_location(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, user=request.user)

    if request.method == "POST":
        form = RestaurantLocationUpdateForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Location updated successfully.")
        else:
            messages.error(request, "Failed to update location. Please check the values.")

    return redirect("restaurant-settings")

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

    model_name = profile._meta.model_name

    return render(request, "merchant/application_status.html", {
        'profile': profile,
    })


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
                return redirect('merchant-signin')
        else:
            form = SetPasswordForm(user)

        return render(request, 'merchant/reset_password.html', {'form': form, 'merchant': merchant})
    else:
        messages.error(
            request, 'Password reset link is invalid or has expired.')
        return redirect('mechant-signin')


def email_sent_view(request):
    return render(request, "merchant/email_sent.html")


@login_required
def restaurant_dashboard(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    return render(request, "merchant/restaurant_dashboard.html", {
        'restaurant': profile,
    })


@login_required
def restaurant_orders(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    return render(request, "merchant/restaurant_orders.html", {
        'restaurant': profile,
    })


def serialize_item(request, item):
    return {
        "id": item.id,
        "name": item.name,
        "price": float(item.price) if item.price is not None else None,
        "discount": float(item.discount) if item.discount is not None else 0.0,
        "description": item.description or "",
        "veg_nonveg": item.veg_nonveg,
        "availability_status": item.availability_status,
        "profile_picture": request.build_absolute_uri(item.profile_picture.url) if item.profile_picture else None,
        "restaurant_id": item.restaurant_id,
    }


@login_required
def menu_update_view(request, pk):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    item = get_object_or_404(FoodItem, pk=pk, restaurant=profile)

    data = {
        "id": item.id,
        "name": item.name,
        "price": str(item.price) if item.price is not None else "",
        "discount": str(item.discount) if item.discount is not None else "0",
        "veg_nonveg": item.veg_nonveg,
        "availability_status": item.availability_status,
        "profile_picture": item.profile_picture.url if item.profile_picture else None,
        "description": item.description or "",
    }

    return JsonResponse(data)


@login_required
def restaurant_menu_dishes(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        if item_id:
            item = get_object_or_404(FoodItem, pk=item_id, restaurant=profile)
            form = FoodItemForm(request.POST, request.FILES, instance=item)
        else:
            form = FoodItemForm(request.POST, request.FILES)

        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = profile
            food_item.save()
            form.save_m2m()
            messages.success(
                request, "Item updated." if item_id else "Item created.")
            return redirect("restaurant-menu-dishes")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = FoodItemForm()

    qs = FoodItem.objects.filter(restaurant=profile).order_by("-id")
    foods = []
    for itm in qs:
        foods.append({
            "id": itm.id,
            "name": itm.name,
            "price": float(itm.price) if itm.price is not None else None,
            "discount": float(itm.discount) if itm.discount is not None else 0.0,
            "veg_nonveg": itm.veg_nonveg,
            "availability_status": itm.availability_status,
            "profile_picture": itm.profile_picture.url if itm.profile_picture else None,
            "description": itm.description or "",
        })

    return render(request, "merchant/restaurant_menu_dishes.html", {
        "restaurant": profile,
        "form": form,
        "foods": foods,
    })


@login_required
def delete_food_item(request):
    if request.method == "POST":
        try:
            profile = Restaurant.objects.get(user=request.user)
        except Restaurant.DoesNotExist:
            return redirect('deliveryman-dashboard')

        item_id = request.POST.get("item_id")
        item = get_object_or_404(FoodItem, pk=item_id, restaurant=profile)
        item.delete()
        messages.success(request, "Item deleted successfully.")
        return redirect("restaurant-menu-dishes")

    return redirect("restaurant-menu-dishes")


@login_required
def restaurant_customers(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    return render(request, "merchant/restaurant_customers.html", {
        'restaurant': profile,
    })


@login_required
def restaurant_settings(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    return render(request, "merchant/restaurant_settings.html", {
        'restaurant': profile,
    })


def lobby_view(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    return render(request, 'merchant/dummy_lobby.html')


def order_receive_view(request):
    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    return render(request, 'merchant/order_receive.html')


def check_deliveryman_status(request):
    # Get all active sessions
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []

    for session in sessions:
        data = session.get_decoded()
        uid = data.get("_auth_user_id")
        if uid:
            user_ids.append(int(uid))

    # Get online and offline deliverymen
    online_deliverymen = Deliveryman.objects.filter(user__id__in=user_ids)
    offline_deliverymen = Deliveryman.objects.exclude(user__id__in=user_ids)

    # For testing - print them out
    print("ONLINE DELIVERYMEN:")
    for d in online_deliverymen:
        print(f"- {d.Firstname} {d.Lastname}")

    print("\nOFFLINE DELIVERYMEN:")
    for d in offline_deliverymen:
        print(f"- {d.Firstname} {d.Lastname}")

    return JsonResponse({
        "online": [f"{d.Firstname} {d.Lastname}" for d in online_deliverymen],
        "offline": [f"{d.Firstname} {d.Lastname}" for d in offline_deliverymen],
    })
