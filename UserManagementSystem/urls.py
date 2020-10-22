from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', create_user, name='create_user'),
    path('signup', register_user),
    path('login', login_user),

]
