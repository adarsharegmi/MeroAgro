from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', create_user, name='register'),
    path('signup', register_user),
    path('login', loginPage, name='login_user'),
    path('login_user',login_user),
    path('signout',logout_user, name='signout'),
]
