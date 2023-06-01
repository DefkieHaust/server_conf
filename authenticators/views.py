from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, AddressForm, UpdateForm, CustomPasswordResetForm, PasswordRecoveryForm
from .models import Address
from django_otp.plugins.otp_totp.models import TOTPDevice
from io import BytesIO
import qrcode
import base64
from accounts.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


# Create your views here.


def register(resp):
    if resp.user.is_authenticated:
        return redirect("/")
    else:
        if resp.method == "POST":
            form = RegisterForm(resp.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(resp, user)
                return redirect("/")
        else:
            form = RegisterForm()
        relay = {"form": form}
        return render(resp, "pages/register.html", relay)


@login_required(login_url='/login/')
def logout_view(resp):
    logout(resp)
    return redirect("/login/")


@login_required(login_url='/login/')
def address(resp):
    if resp.method == "POST":
        if resp.POST.get("address"):
            addr_obj = Address(user=resp.user)
            address_form = AddressForm(resp.POST, instance=addr_obj)
            if address_form.is_valid():
                address_form.save()
        else:
            for i in resp.POST:
                if i.isdigit():
                    resp.user.addresses.filter(pk=int(i))[0].delete()
    addresses = resp.user.addresses.all()
    form_relay = {
        "user": resp.user,
    }
    relay = {
        "addressform": AddressForm(initial=form_relay),
        "addresses": addresses,
    }
    return render(resp, "pages/address.html", relay)


@login_required(login_url='/login/')
def edit_profile(resp):
    if resp.method == "POST":
        update_form = UpdateForm(resp.POST, instance=resp.user)
        if update_form.is_valid():
            update_form.save()
    relay = {
        "updateform": UpdateForm(instance=resp.user),
    }
    return render(resp, "pages/edit_profile.html", relay)


@login_required(login_url='/login/')
def change_password(resp):
    if resp.method == 'POST':
        form = PasswordChangeForm(resp.user, resp.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(resp, user)
            return redirect("/")
    else:
        form = PasswordChangeForm(resp.user)
    relay = {
        'passwordform': form,
    }
    return render(resp, 'pages/change_password.html', relay)


@login_required(login_url='/login/')
def totp_setup(request):
    # Retrieve the current user
    user = request.user

    try:
        # Try to retrieve the TOTP device for the user
        totp_device = TOTPDevice.objects.get(user=user)

    except TOTPDevice.DoesNotExist:
        # If the TOTP device doesn't exist, create a new one for the user
        totp_device = TOTPDevice.objects.create(user=user)

    # Get the provisioning URI for the TOTP device
    provisioning_uri = totp_device.config_url

    # Generate the QR code image
    qr_code = qrcode.make(provisioning_uri)

    # Create a BytesIO object to store the image data
    qr_code_bytes = BytesIO()
    qr_code.save(qr_code_bytes, format='PNG')

    # Set the BytesIO object's file pointer to the beginning
    qr_code_bytes.seek(0)

    # Encode the image data as Base64 and convert it to a string
    qr_code_base64 = base64.b64encode(qr_code_bytes.getvalue()).decode('utf-8')

    # Construct the full data URI with the Base64 image data
    qr_code_data_uri = f'data:image/png;base64,{qr_code_base64}'

    # Convert the binary secret key to a string
    secret_key_str = base64.b32encode(totp_device.bin_key).decode('utf-8')

    # Pass the QR code image data to the template
    context = {
        'provisioning_uri': qr_code_data_uri,
        'secret_key': secret_key_str,
    }

    return render(request, 'pages/totp_setup.html', context)


@login_required(login_url='/login/')
def totp_verify(request):
    if request.method == 'POST':
        totp_code = request.POST.get('totp_code')

        # Retrieve the current user
        user = request.user

        try:
            # Retrieve the TOTP device for the user
            totp_device = TOTPDevice.objects.get(user=user)

            # Verify the TOTP code entered by the user
            is_verified = totp_device.verify_token(totp_code)

            if is_verified:
                # Proceed with successful authentication
                return render(request, 'pages/totp_success.html')
            else:
                # Handle invalid TOTP code
                return render(request, 'pages/totp_verification_failed.html')

        except TOTPDevice.DoesNotExist:
            # Handle the case where the user does not have a TOTP device
            return render(request, 'pages/totp_verification_failed.html')


def password_recovery(request):
    if request.method == 'POST':
        form = PasswordRecoveryForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            totp_code = form.cleaned_data['totp_code']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                error_message = 'Invalid username'
                return render(request, 'pages/password_recovery.html', {'form': form, 'error_message': error_message})

            # Verify TOTP code
            totp_device, created = TOTPDevice.objects.get_or_create(user=user)
            if totp_code and totp_device.verify_token(totp_code):
                # Authentication successful, log in the user
                # user = authenticate(request, username=username, password=None)
                # if user is not None:
                #     login(request, user)
                token_generator = default_token_generator
                token = token_generator.make_token(user)

                # Encode the username in uidb64 format
                uidb64 = urlsafe_base64_encode(user.username.encode())

                # Build the password reset URL
                reset_url = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})

                # Redirect to the password reset page
                return redirect(reset_url)

            else:
                error_message = 'Invalid TOTP code'
                return render(request, 'pages/password_recovery.html', {'form': form, 'error_message': error_message})
    else:
        form = PasswordRecoveryForm()

    return render(request, 'pages/password_recovery.html', {'form': form})


def custom_password_reset(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(username=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['password1']
                user.set_password(new_password)
                user.save()
                return redirect('/login/')
        else:
            form = CustomPasswordResetForm()
        return render(request, 'pages/password_reset_confirm.html', {'form': form})
    else:
        return render(request, 'pages/invalid_reset_link.html')
