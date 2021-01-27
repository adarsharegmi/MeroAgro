from random import randint

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as SUser
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render
from .models import *
from django_email_verification import sendConfirm
from MeroAgro.settings import EMAIL_ADDRESS
import json
from PostManagementSystem.views import create_post

cross = 0


def create_user(request):
    return render(request, 'signup.html')


def verifyalt(request, user):
    try:
        sendConfirm(user)
    except Exception as e:
        print(e)
    return render(request, "emailverify/testt.html", {'success': True})


def register_user(request):
    if request.method == 'POST':
        get_username = request.POST['username']
        get_address = request.POST['useraddress']
        get_email = request.POST['useremail']
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

        verifyalt(request, user_obj2)
        user_obj.save()
        user_obj2.save()
        image.save()
        print("Account completion")
        return HttpResponse("Check your email and verify your account... Thank you ")
    else:
        return redirect(request, 'signup.html')


def loginPage(request):
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
            print("password error")
            return HttpResponse("error password")
    else:
        return render(request, 'login.html')


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

    context = {"cross":cross}

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


def show_user(request):
    user = request.session['id']
    u = User.objects.get(id=user)
    address = u.user_address
    password = u.user_password
    useremail = u.user_email
    username = request.session['username']
    context = {}
    try:
        image = Images.objects.get(id=user)
        data = {"address": address, "email": useremail, "password": password, "username": username,
                "profileimage": image.profile_picture.url}
    except:
        data = {"address": address, "email": useremail, "password": password, "username": username,
                "profileimage": "/default/pp.png"}

    context["user_data"] = json.dumps(data)

    return render(request, 'userdetails.html',
                  context)


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
        img_obj.name = request.POST['username']

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
