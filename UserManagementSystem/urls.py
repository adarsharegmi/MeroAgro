from django.contrib import admin
from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', create_user, name='register'),
    path('signup', register_user),
    path('login', loginPage, name='login_user'),
    path('login_user', login_user),
    path('signout', logout_user, name='signout'),
    #     for email reset
    path('reset_password', reset_password, name='reset'),
    path('reset',send_reset),
    path('profile',show_user, name='refshowme'),
    path('save',update_user_details),
    path('saveprofile',update_user_profile),
]

