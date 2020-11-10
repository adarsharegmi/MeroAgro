from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User as SUser
from django.contrib.auth import login, logout, authenticate

from django.shortcuts import render
from .models import *
from django_email_verification import sendConfirm


def create_user(request):
    return render(request, 'signup.html')


def verifyalt(request, user):
    try:
        sendConfirm(user)
    except Exception as e:
        print(e)
    return render(request, "testt.html", {'success': True})


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

        verifyalt(request, user_obj2)
        user_obj.save()
        user_obj2.save()

        print("Account completion")
        return HttpResponse("Check your email and verify your account... Thank you ")
    else:
        return redirect(request, 'signup.html')


def loginPage(request):
    return render(request, "login.html")


def login_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['useremail'], password=request.POST['userpassword'])
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                return render(request, 'base.html')
        else:
            return redirect('/login/')
    else:
        return redirect('/login/')


def logout_user(request):
    logout(request)
    return redirect(loginPage)
