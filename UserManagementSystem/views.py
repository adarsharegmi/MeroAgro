from random import randint

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as SUser
from django.contrib.auth import login, logout, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

from verify_email.email_handler import send_verification_email


from django.shortcuts import render
from .models import *
from MeroAgro.settings import EMAIL_ADDRESS
import json
import re

from PostManagementSystem.views import create_post

cross = 0


def create_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'signup.html')


def check_username(email):
    return SUser.objects.filter(username__iexact=email).exists()



def register_user(request):

    if request.method == 'POST':
        get_username = request.POST['username']
        get_address = request.POST['useraddress']
        get_email = request.POST['useremail']

        if check_username(get_email):
            return render(request,'signup.html',{'message':'user email already used'})

        get_password = request.POST['userpassword']
        # get_password = hash(get_password)
        get_type = request.POST['usertype']

        user_obj = User(user_id=get_username,
                        user_email=get_email,
                        user_address=get_address,
                        user_password=get_password,
                        user_type=get_type)

        user_obj2 = SUser.objects.create_user(get_email, get_email, get_password)

        image = Images(name=user_obj)
        user_obj2.is_active = False
        user_obj2.save()
        current_site = get_current_site(request)
        token = account_activation_token.make_token(user_obj2)
        message = render_to_string('emailverify/testt.html', {
            'user': user_obj2,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user_obj2.pk)),
            'token':token,
        })
        mail_subject = 'Active your MeroAgro Account.'
        to_email = get_email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        print("before",str(token))

        user_obj.save()
        user_obj2.save()
        image.save()
        print("Account completion")
        return HttpResponse("Check your email and verify your account... Thank you ")
    else:
        return redirect(request, 'signup.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = SUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print(token)
    # breakpoint()
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')

        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, "login.html")


def login_user(request):
    if request.method == 'POST':
        useremail = request.POST['useremail']
        user = authenticate(username=useremail, password=request.POST['userpassword'])

        if user is not None:
            login(request, user)
            request.session['id'] = User.objects.get(user_email=useremail).id
            request.session['username'] = User.objects.get(user_email=useremail).user_id

            if request.user.is_authenticated:
                return redirect('/')

        else:
            return render(request,'login.html',{'message':'credentials mismatched'})
    else:
        return render(request, 'login.html')


def google_sign_in(request):
    if request.method == 'POST':
        useremail = request.POST['gusername']

        user = User.objects.get(user_email=useremail)
        print(user)

        if user is None:
            get_username = request.POST['gusername']
            image_url = request.POST['gprofile']
            fullname = request.POST['gname']
            import random
            mask = str(random.randint(100000))
            user_obj = User(user_id=fullname, user_password=mask)
            user_obj2 = SUser.objects.create_user(get_username, get_username, mask)
            image = Images(name=user_obj, profile_picture=image_url)

            user_obj.save()
            image.save()

        user_object = User.objects.get(user_email=useremail)
        user = authenticate(username=user_object.user_email, password=user_object.user_password)
        login(request, user)

        request.session['id'] = user_object.id
        request.session['username'] = User.objects.get(user_email=useremail).user_id

        return redirect('/')
    return HttpResponse("Haha tried something out of  the setting ..  check documentation")


def logout_user(request):
    logout(request)
    return redirect(loginPage)


def reset_password(request):
    return render(request, 'reset/password_reset_form.html')


from django.core.mail import send_mail


# method to reset the password of user
def send_reset(request):
    global cross
    cross = randint(000000, 999999)
    toemail = request.POST['uemail']
    request.session['email'] = toemail

    context = {"cross": cross}

    try:
        user = User.objects.get(user_email=toemail)
        send_mail('Reset Password', 'Please enter this number ' + str(cross), EMAIL_ADDRESS, [toemail],
                  fail_silently=False)
        return render(request, 'reset/password_reset_confirm.html')
    except Exception as e:
        print("error sending mail")
        print(e)

    return render(request, 'reset/password_reset_form.html')


def check(request):
    print(cross)

    if int(request.POST['reset']) == cross:
        return render(request, "reset/password_reset_done.html")
    else:
        return render(request, "reset/password_reset_confirm.html")


def update_password(request):
    if request.method == 'POST':
        password = request.POST['upassword']
        email = request.session['email']
        user = User.objects.get(user_email=email)
        user.user_password = password
        su = SUser.objects.get(username=email)
        su.set_password(password)
        su.save()
        return render(request, "login.html")


def show_user(request, user_id=0):
    context = {}

    if user_id == 0:
        data = get_user(request, request.session['id'])
        data['current'] = 1
        context["user_data"] = json.dumps(data)
    else:
        data = get_user(request, user_id)
        data['current'] = 0
        context['user_data'] = json.dumps(data)
    return render(request, 'userdetails.html',
                  context)


def get_user(request, user):
    u = User.objects.get(id=user)
    address = u.user_address
    password = u.user_password
    useremail = u.user_email
    username = request.session['username']
    try:
        image = Images.objects.get(id=user)
        data = {"id": user, "address": address, "email": useremail, "password": password, "username": username,
                "profileimage": image.profile_picture.url}
    except:
        data = {"id": user, "address": address, "email": useremail, "password": password, "username": username,
                "profileimage": "/default/pp.png"}

    return data


def update_user_details(request):
    if request.method == 'POST':
        user_id = request.session['id']
        update(request, 1, user_id)
        return show_user(request)
    else:
        return show_user(request)


def update_user_profile(request):
    if request.method == 'POST' and request.FILES['profilepicture']:
        user_id = request.session['id']
        update(request, 2, user_id)
        return show_user(request)
    else:
        return HttpResponse("userdetails.html")


def update(request, n, user_id):
    print(user_id)
    fs = FileSystemStorage()
    img_obj = Images.objects.get(name=user_id)

    if n == 1:
        user_obj = User.objects.get(id=user_id)
        # update user details
        get_username = request.POST['username']
        get_address = request.POST['useraddress']
        get_email = request.POST['useremail']

        user_obj.user_email = get_email
        user_obj.user_id = get_username
        user_obj.user_address = get_address
        user_obj.save()
        img_obj.save()
        request.session['username'] = get_username

    elif n == 2:

        get_profile = request.FILES['profilepicture']
        get_profilename = fs.save("pp.png", get_profile)
        img_obj.profile_picture = fs.url(get_profilename)
        img_obj.save()


def load_user(request):
    request.session['username']
