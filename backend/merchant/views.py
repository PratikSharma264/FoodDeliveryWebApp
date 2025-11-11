from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MerchantSignUpForm, RestaurantRegistrationForm, MerchantForgotPasswordForm, DeliverymanForm, FoodItemForm, RestaurantBioUpdateForm, RestaurantProfilePicUpdateForm, RestaurantLocationUpdateForm, DeliverymanBioUpdateForm, DeliverymanProfilePicUpdateForm
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
from .models import Merchant, Deliveryman, Restaurant, FoodItem, GoToDashClickCheck, Order
from django.contrib.auth.forms import SetPasswordForm
from django.http import Http404, JsonResponse
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Prefetch


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
    if request.user.is_authenticated:
        try:
            obj = GoToDashClickCheck.objects.get(user=request.user)
            if obj.go_to_dash_clicked:
                return redirect('deliveryman-dashboard')
        except GoToDashClickCheck.DoesNotExist:
            pass

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
    obj, created = GoToDashClickCheck.objects.get_or_create(user=request.user)
    if not obj.go_to_dash_clicked:
        obj.go_to_dash_clicked = True
        obj.save()

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
def restaurant_bio_json_response(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, user=request.user)
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


@login_required
def update_restaurant_bio(request):
    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant_id")
        restaurant = get_object_or_404(
            Restaurant, id=restaurant_id, user=request.user)

        form = RestaurantBioUpdateForm(
            request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant updated successfully.")
        else:
            messages.error(
                request, "Failed to update restaurant. Please check the form inputs.")

    return redirect("restaurant-settings")


@login_required
def update_restaurant_profile_picture(request):
    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant_id")
        restaurant = get_object_or_404(
            Restaurant, id=restaurant_id, user=request.user)

        form = RestaurantProfilePicUpdateForm(
            request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile picture updated successfully.")
        else:
            messages.error(
                request, "Failed to update profile picture. Please try again.")

    return redirect("restaurant-settings")


@login_required
def deliveryman_bio_json_response(request, id):
    deliveryman = get_object_or_404(Deliveryman, id=id, user=request.user)
    try:
        contact = deliveryman.user.merchant_profile.phone_number
    except (AttributeError, Merchant.DoesNotExist):
        contact = None
    data = {
        "Firstname": deliveryman.Firstname,
        "Lastname": deliveryman.Lastname,
        "Address": deliveryman.Address,
        "DateofBirth": deliveryman.DateofBirth.isoformat() if deliveryman.DateofBirth else None,
        "PanNumber": deliveryman.PanNumber,
        "Email": deliveryman.user.email if deliveryman.user else None,
        "Contact": contact,
        "Vehicle": deliveryman.Vehicle,
        "VehicleNumber": deliveryman.VehicleNumber,
        "Zone": deliveryman.Zone,
        "DutyTime": deliveryman.DutyTime,
        "UserImage": deliveryman.UserImage.url if getattr(deliveryman, 'UserImage') else None,
    }
    return JsonResponse({"success": True, "data": data})


@login_required
def update_deliveryman_bio(request):
    if request.method == "POST":
        deliveryman_id = request.POST.get(
            "deliveryman_id") or request.POST.get("deliveryman")
        deliveryman = get_object_or_404(
            Deliveryman, id=deliveryman_id, user=request.user)
        form = DeliverymanBioUpdateForm(
            request.POST, request.FILES, instance=deliveryman, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(
                request, "Failed to update profile. Please check the form inputs.")
    return redirect("deliveryman-profile")


@login_required
def update_deliveryman_profile_picture(request):
    if request.method == "POST":
        deliveryman_id = request.POST.get(
            "deliveryman") or request.POST.get("deliveryman_id")
        deliveryman = get_object_or_404(
            Deliveryman, id=deliveryman_id, user=request.user)
        if 'UserImage' in request.FILES:
            form = DeliverymanProfilePicUpdateForm(
                request.POST, request.FILES, instance=deliveryman)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Profile picture updated successfully.")
            else:
                messages.error(
                    request, "Failed to update profile picture. Please try again.")
        elif 'profile_picture' in request.FILES:
            deliveryman.UserImage = request.FILES['profile_picture']
            try:
                deliveryman.save()
                messages.success(
                    request, "Profile picture updated successfully.")
            except Exception:
                messages.error(
                    request, "Failed to save profile picture. Please try again.")
        else:
            messages.error(request, "No image uploaded.")
    return redirect("deliveryman-profile")


@login_required
def update_restaurant_location(request):
    if request.method == "POST":
        restaurant_id = request.POST.get("restaurant_id")
        restaurant = get_object_or_404(
            Restaurant, id=restaurant_id, user=request.user)

        form = RestaurantLocationUpdateForm(request.POST, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Location updated successfully.")
        else:
            messages.error(
                request, "Failed to update location. Please check the values.")

    return redirect("restaurant-settings")


@login_required
def restaurant_orders_json_response(request, id):
    restaurant = get_object_or_404(Restaurant, id=id, user=request.user)
    customer_id = request.GET.get('customer_id')
    orders_qs = Order.objects.filter(restaurant=restaurant).select_related(
        'user', 'restaurant', 'deliveryman').prefetch_related('order_items__food_item')
    if customer_id:
        orders_qs = orders_qs.filter(user_id=customer_id)

    data = []

    for order in orders_qs:
        items = []
        computed_total = Decimal('0.00')
        for oi in order.order_items.all():
            fi = getattr(oi, 'food_item', None)
            price_each = oi.price_at_order or (
                getattr(fi, 'price', Decimal('0.00')) if fi else Decimal('0.00'))
            item_total = price_each * oi.quantity
            computed_total += item_total

            image_url = None
            if fi:
                try:
                    image_url = fi.profile_picture.url if fi.profile_picture else fi.external_image_url
                except Exception:
                    image_url = fi.external_image_url

            items.append({
                "id": oi.pk,
                "food_item": getattr(fi, 'pk', None),
                "food_item_name": getattr(fi, 'name', ''),
                "restaurant_name": getattr(fi.restaurant, 'restaurant_name', getattr(order.restaurant, 'restaurant_name', '')),
                "food_item_image": image_url,
                "quantity": oi.quantity,
                "price_at_order": str(price_each),
                "total_price": float(item_total),
            })

        total_value = order.total_price or computed_total

        user_obj = getattr(order, 'user', None)
        customer_name = user_obj.get_full_name() if user_obj else ''
        phone = None

        if user_obj:

            for attr in ('phone', 'phone_number', 'mobile', 'contact', 'telephone'):
                phone = getattr(user_obj, attr, None)
                if phone:
                    break

            if not phone and hasattr(user_obj, 'user_profile'):
                profile = user_obj.user_profile
                phone = getattr(profile, 'phone', None) or getattr(
                    profile, 'phone_number', None)

            if not phone and hasattr(user_obj, 'merchant_profile'):
                merchant = user_obj.merchant_profile
                phone = getattr(merchant, 'phone_number', None)

        phone = phone or None

        deliveryman_obj = getattr(order, 'deliveryman', None)
        deliveryman_data = None
        if deliveryman_obj:
            deliveryman_data = {
                "id": deliveryman_obj.id,
                "name": f"{getattr(deliveryman_obj, 'Firstname', '')} {getattr(deliveryman_obj, 'Lastname', '')}".strip(),
                "email": getattr(deliveryman_obj, 'email', None),
                # Add phone to Deliveryman model if needed
                "phone": getattr(deliveryman_obj, 'phone', None),
            }

        restaurant_user = getattr(order.restaurant, 'user', None)
        restaurant_user_data = None
        if restaurant_user:
            restaurant_user_data = {
                "id": restaurant_user.id,
                "username": restaurant_user.username,
                "first_name": restaurant_user.first_name,
                "last_name": restaurant_user.last_name,
                "email": restaurant_user.email,
            }

        restaurant_data = {
            "id": order.restaurant.pk,
            "user": restaurant_user_data,
            "restaurant_name": order.restaurant.restaurant_name,
            "owner_name": order.restaurant.owner_name,
            "owner_email": order.restaurant.owner_email,
            "owner_contact": order.restaurant.owner_contact,
            "restaurant_address": order.restaurant.restaurant_address,
            "latitude": order.restaurant.latitude,
            "longitude": order.restaurant.longitude,
            "cuisine": order.restaurant.cuisine,
            "description": order.restaurant.description,
            "restaurant_type": order.restaurant.restaurant_type,
            "profile_picture": getattr(order.restaurant.profile_picture, 'url', None),
            "cover_photo": getattr(order.restaurant.cover_photo, 'url', None),
            "menu": getattr(order.restaurant.menu, 'url', None),
            "created_at": order.restaurant.created_at.isoformat() if order.restaurant.created_at else None,
            "approved": order.restaurant.approved,
        }

        data.append({
            "order_id": order.pk,
            "user": {
                "id": user_obj.id if user_obj else None,
                "username": user_obj.username if user_obj else '',
                "first_name": user_obj.first_name if user_obj else '',
                "last_name": user_obj.last_name if user_obj else '',
                "email": user_obj.email if user_obj else '',
            },
            "deliveryman": deliveryman_data,
            "restaurant_id": order.restaurant.pk,
            "restaurant": restaurant_data,
            "is_transited": order.is_transited,
            "delivery_charge": f"{order.delivery_charge or Decimal('0.00'):.2f}",
            "total_price": f"{total_value:.2f}",
            "order_items": items,
            "order_date": order.order_date.isoformat() if order.order_date else None,
            "status": order.status,
            "payment_method": (order.payment_method or '').lower(),
            "latitude": str(order.latitude) if order.latitude is not None else None,
            "longitude": str(order.longitude) if order.longitude is not None else None,
            "customer_details": {
                "email": user_obj.email if user_obj else '',
                "phone": phone,
            },
        })

    return JsonResponse({"success": True, "data": data}, encoder=DjangoJSONEncoder, safe=True)


@login_required
def application_status_view(request):
    if request.user.is_authenticated:
        try:
            obj = GoToDashClickCheck.objects.get(user=request.user)
            if obj.go_to_dash_clicked:
                return redirect('deliveryman-dashboard')
        except GoToDashClickCheck.DoesNotExist:
            pass

    profile = (
        getattr(request.user, 'deliveryman_profile', None)
        or getattr(request.user, 'restaurant_profile', None)
    )
    if profile is None:
        messages.error(
            request, "Access Denied! You are neither a deliveryman nor a restaurant owner.")
        return redirect('home')

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
    obj, created = GoToDashClickCheck.objects.get_or_create(user=request.user)
    if not obj.go_to_dash_clicked:
        obj.go_to_dash_clicked = True
        obj.save()

    try:
        profile = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        return redirect('deliveryman-dashboard')
    fooditem_count = FoodItem.objects.filter(restaurant=profile).count()
    orders_count = Order.objects.filter(restaurant=profile).count()

    return render(request, "merchant/restaurant_dashboard.html", {
        'restaurant': profile,
        'fooditem_count': fooditem_count,
        'orders_count': orders_count,
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


@login_required
def deliveryman_new_orders(request):
    try:
        profile = Deliveryman.objects.get(user=request.user)
    except Deliveryman.DoesNotExist:
        return redirect('restaurant-dashboard')
    return render(request, "merchant/deliveryman_new_orders.html", {
        'deliveryman': profile,
    })


@login_required
def deliveryman_current_orders(request):
    try:
        profile = Deliveryman.objects.get(user=request.user)
    except Deliveryman.DoesNotExist:
        return redirect('restaurant-dashboard')
    return render(request, "merchant/deliveryman_current_orders.html", {
        'deliveryman': profile,
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
def deliveryman_history(request):
    try:
        profile = Deliveryman.objects.get(user=request.user)
    except Deliveryman.DoesNotExist:
        return redirect('restaurant-dashboard')
    return render(request, "merchant/deliveryman_history.html", {
        'deliveryman': profile,
    })


@login_required
def deliveryman_profile(request):
    try:
        profile = Deliveryman.objects.get(user=request.user)
    except Deliveryman.DoesNotExist:
        return redirect('restaurant-dashboard')
    return render(request, "merchant/deliveryman_profile.html", {
        'deliveryman': profile,
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
