from typing import Set
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .tools import get_user_with_email_or_username, send_email, send_html_mail
from .forms import SignupForm, ProfilesForm, AddWalletAddressForm, UserLogin, KycForm
from .token import account_activation_token

from django.contrib.auth import get_user_model
User = get_user_model()

def handle_not_found(request, exception):
    return render(request, "profiles/error-404.html")

def index(request):
    return render(request,"index.html")

def account_inactive_all_auth_problem(request):
    return redirect("profile-page")

def login_view(request):

    message = ""
    username = ""
    user_object = None
    if request.POST:
        form = UserLogin(request.POST)
        if request.POST.get('submit'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            try: 
                if '@' in username:
                    
                        user_object = User.objects.get(email=username)
                        username = user_object.username
                    
                else:
                    user_object = User.objects.get(username=username)
            except:
                    pass
            request.session['last-username-entered'] = username
            user =  authenticate(request, username=username, password = password)
            if user != None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                message = f"Successfully logged in as {request.user.username}"

                return redirect('profile-page')
            else:
                if user_object:
                    if not user_object.is_active:
                        message = "Please activate your account"
                    else:
                        message = "No account was found with the given credentials"

                else:
                    message = "No account was found with the given credentials"
        
        if request.POST.get('activate-submit'):
            domain = get_current_site(request)
            mail_subject = 'Activate your account.'
            user_object = get_user_with_email_or_username(request)
            send_html_mail(mail_subject=mail_subject, user=user_object, domain=domain)
            messages.info(request, "An email has been sent to you")
    else:
        form = UserLogin()
    # context = {'form': form, 'message': message}

    return render(request, 'profiles/login.html', {'form': form, 'message': message})


def logout_user(request):
    logout(request)
    return redirect('login')



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            domain = get_current_site(request)
            mail_subject = 'Activate your account.'
            # send_email(mail_subject=mail_subject, user=user, domain=domain)
            send_html_mail(mail_subject=mail_subject, user=user, domain=domain)
            return redirect('login')
            # return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'profiles/signup.html', {'form': form})





def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def update_profile(request):
    current_user=request.user.username
    # profile_object = CustomUser.objects.get(username=current_user)

    form = ProfilesForm(instance=request.user)
    wallet_form=AddWalletAddressForm()
    password_form = PasswordChangeForm(request.user)
    try:
        obj = request.user.kyc_set.last()
        kyc_form = KycForm(instance=obj)
    except:
        kyc_form = KycForm()
    if request.user.is_kyc_verified:
        for field in kyc_form.fields:
            kyc_form.fields[field].disabled = True

    if request.POST:
        print("=============== image =====================")
        if "profile_picture" in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']

            request.user.save()
        if request.POST.get('update-submit'):
            form = ProfilesForm(request.POST, request.FILES, instance=request.user)

            if form.is_valid():
                # if 'remove_photo' in request.POST:
                #     profile_object.profile_picture = None
                                
                # if 'profile_picture' in request.FILES:
                #     profile_object.profile_picture = request.FILES['profile_picture']
        
                messages.success(request, "Your profile has been updated")
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                

        if request.POST.get("wallet-submit"):
            wallet_form = AddWalletAddressForm(request.POST)
            if wallet_form.is_valid():
                wallet_form = wallet_form.save(commit=False)
                wallet_form.user = request.user
                wallet_form.save()
                return redirect('profile-page')

        if request.POST.get("password-submit"):
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                password_form = password_form.save(commit=False)
                password_form.user = request.user
                password_form.save()

                return redirect('login')

        if request.POST.get("kyc-submit"):
            kyc_form = KycForm(request.POST, request.FILES)
            if kyc_form.is_valid():
                kyc_form = kyc_form.save(commit=False)
                kyc_form.user = request.user
                kyc_form.save()
                return redirect('profile-page')

    # return render(request, 'user 2/profile.html', {'form': form, 'wallet_form': wallet_form, 'password_form': password_form, 'kyc_form': kyc_form})
    return render(request, 'profiles/profile.html', {'form': form, 'wallet_form': wallet_form, 'password_form': password_form, 'kyc_form': kyc_form})

@login_required
def user_dashboard(request):
    return render(request, "profiles/user-dashboard.html")



# get device info in request, create a model that stores this info having a one to one relationship with the request.user
#https://medium.com/@arrosid/how-to-get-visitor-detail-information-in-django-687fbe565f7e