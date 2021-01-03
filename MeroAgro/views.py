from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from UserManagementSystem.models import Images

def base(request):
    try:
        user_id = request.session['id']
        img = Images.objects.get(name_id=user_id)
        context={"img_url":img.profile_picture}
        return render(request, 'homepage.html',context)
    except :
        return render(request,'homepage.html')