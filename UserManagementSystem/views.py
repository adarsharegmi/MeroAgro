from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse


def create_user(request):
    return render(request, 'signup.html')
