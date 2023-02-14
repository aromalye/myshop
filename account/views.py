from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from orders.models import Order

from typing import Protocol
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'Username Already Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(email=email, username=username, password=password)
                user.is_active = False
                user.save()

                # user activation
                current_site = get_current_site(request).domain
                mail_subject = 'Please activate your account'
                message_on = render_to_string('account_verification_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, 
                    message_on, 
                    settings.EMAIL_HOST_USER,
                    to=[to_email],
                    )
                email.fail_silently=False
                email.send()

                return redirect('account/signin/?command=verification&email='+to_email)
        else:
            messages.error(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('signin')
                  
    else:
        return render(request, 'signin.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        user_model = User.objects.get(id=user.id)
        new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
        new_profile.save()

        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('signin')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('signup')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        print("dd")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # password reset mail
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            print(message)
            to_email = email
            email = EmailMessage(
                mail_subject, 
                message, 
                settings.EMAIL_HOST_USER,
                to=[to_email],
                )
            email.fail_silently=False
            email.send()

            messages.info(request, 'Password reset email has been sent to your email address.')
            return redirect('signin')
        
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('signin')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('signin')
        else:
            messages.error(request, 'Password do not match')
            return redirect('resetpassword')
    else:
        return render(request, 'resetpassword.html')


@login_required(login_url='signin')
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
        orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
        order_count = orders.count()

        context = {
            'order_count': order_count,
            'profile': profile,
        }
        return render(request, 'dashboard/dashboard.html', context)
    except Profile.DoesNotExist:
        return render(request, 'dashboard/dashboard.html')
    # profile = Profile.objects.get(user=request.user)
    # orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    # order_count = orders.count()

    # context = {
    #     'order_count': order_count,
    #     'profile': profile,
    # }
    # return render(request, 'dashboard/dashboard.html', context)


def edit_profile(request):
    print(request.user)
    profile = Profile.objects.get(user=request.user)
    # print(profile)
    if request.method == 'POST': 
        
        if request.FILES.get('profile_pic') == None:
            image = profile.profileimg

            profile.profileimg = image
            profile.save()

        if request.FILES.get('profile_pic') != None:
            image = request.FILES.get('profile_pic')

            profile.profileimg = image
            profile.save()

    context = {
        'profile': profile
    }
    return render(request, 'dashboard/edit_profile.html', context)


@login_required(login_url='signin')
def my_orders(request):
    orders = Order.objects.order_by('-created_at').filter(user=request.user, is_ordered=True)

    context = {
        'orders': orders
    }
    return render(request, 'dashboard/orders.html', context)