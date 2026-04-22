from django.contrib.auth import login, authenticate
from django.core.signing import loads, BadSignature
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from customers.models import Feedback
from orders.models import Order, Fabric, Measurements
from .models import User, UserProfile
from .forms import CustomSignupForm, CustomLoginForm, UserProfileForm, UserForm
from django.contrib import messages, auth
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .utils import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied

def role_required(allowed_roles=[]):

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.get_role() in allowed_roles:
                    return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator


def redirect_to_login(request):
    return redirect('accounts:account_login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset your password'
            email_template = 'accounts/email/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has sent to your email address')
            return redirect('accounts:account_login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('accounts:forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the user and pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect('accounts:home_page')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('accounts:account_login')
        else:
            messages.error(request, 'Password not match!')
            return redirect('accounts:reset_password')
    return render(request, 'accounts/reset_password.html')


class CustomRegistrationView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home_page')
        form = CustomSignupForm()

        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            # user.role = form.cleaned_data.get('role', 1)
            user.save()
            send_email_confirmation(request, user)  # Email verification with allauth
            messages.success(request, "Registration successful. Please verify your email.")
            return redirect('accounts:account_login')
        return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('accounts:home_page')
        form = CustomLoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            # Check if the user's email is verified
            if user is not None:
                email_address = EmailAddress.objects.filter(user=user, email=user.email).first()
                if email_address and email_address.verified:
                    login(request, user)


                    if user.get_role() == "Admin":
                        return redirect("accounts:admin_dashboard")
                    elif user.get_role() == "Staff":
                        return redirect("accounts:staff_dashboard")
                    elif user.get_role() == "Customer":
                        return redirect("accounts:customer_dashboard")
                    else:
                        return redirect('accounts:home_page')  # Redirect to a success page or home page

                else:
                    messages.error(request, "Please verify your email before logging in.")
            else:
                messages.error(request, "Invalid credentials. Please try again.")
        return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successfully')
    return redirect('accounts:account_login')


def home_page(request):
    return render(request, 'index.html', )


@login_required
# @role_required(["Admin"])
def admin_dashboard(request):
    return render(request, "accounts/dashboard/admin_dashboard.html")


@login_required
def staff_dashboard(request):
    orders = (
        Order.objects.filter(items__measurement__staff=request.user)
        .exclude(status="pending")
        .select_related("customer")
        .prefetch_related("items__measurement__dress_type")
        .order_by('-created_at')
        .distinct()
    )
    return render(request, "accounts/dashboard/staff_dashboard.html", {'orders': orders})


@login_required
@role_required(["Customer"])
def customer_dashboard(request):
    return render(request, "accounts/dashboard/customer_dashboard.html")


@login_required
def staff_update_order(request, order_id):
    """Staff can update fabric used, status, progress, and inventory notes."""
    order = get_object_or_404(Order, id=order_id)
    fabrics = Fabric.objects.all()

    if request.method == "POST":
        fabric_id = request.POST.get("fabric")
        status = request.POST.get("status")
        progress = request.POST.get("progress")
        notes = request.POST.get("inventory_notes")

        # Update fields
        if fabric_id:
            order.customer_fabric_id = fabric_id
        if status:
            order.status = status
        if progress:
            order.progress = int(progress)
        order.inventory_notes = notes
        order.save()

        return redirect("accounts:staff_dashboard")

    return render(request, "staff/update_order.html", {
        "order": order,
        "fabrics": fabrics
    })


@login_required
def customer_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        # Update User fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()

        # Update Profile fields
        profile.address_line_1 = request.POST.get('address_line_1')
        profile.address_line_2 = request.POST.get('address_line_2')
        profile.address_line_3 = request.POST.get('address_line_3')
        profile.district = request.POST.get('district')
        profile.state = request.POST.get('state')
        profile.country = request.POST.get('country')
        profile.zip_code = request.POST.get('zip_code')
        profile.is_organization = request.POST.get('is_organization') == 'True'
        profile.organization_name = request.POST.get('organization_name')

        # Handle file uploads
        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']
        if 'cover_image' in request.FILES:
            profile.cover_image = request.FILES['cover_image']

        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('accounts:customer_profile')

    # Always get the latest data from DB
    profile.refresh_from_db()


    return render(request, 'accounts/profile/profile_detail.html', {
        'user': user,
        'profile': profile,

    })

@login_required
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('accounts:customer_profile')  # redirect to profile page
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile/profile_edit.html', context)


@login_required
def measurement_detail_for_staff(request, pk):
    measurement = get_object_or_404(
        Measurements,
        id=pk,
        staff=request.user,
        is_deleted=False
    )

    order_item = measurement.order_items.first()
    order = order_item.order
    customer = order.customer
    customer_profile = UserProfile.objects.filter(user=customer).first()

    return render(request, 'staff/view_details.html', {
        'measurement': measurement,
        'customer' : customer,
        'customer_profile' : customer_profile,
    })
