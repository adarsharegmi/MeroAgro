from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from UserManagementSystem.models import Images
from .models import *
import json


# Create your views here.
def create_post(request):
    data = {}
    try:
        image = Images.objects.get(name_id=request.session['id'])

        posts = list(POST.objects.all())
        if not posts:
            return render(request, "homepage.html")
        data = {"posts": posts, "pp": image.profile_picture}
        return render(request, "homepage.html", data)
    except:
        return render(request,"startpage.html")

def save_post(request):
    fs = FileSystemStorage()
    if request.method == 'POST' and request.FILES:
        get_text = request.POST['text']
        get_type = request.POST['type']
        get_picture = request.FILES['profilepicture']
        get_profile = fs.save("uu", get_picture)
        user = request.session['id']
        u = User.objects.get(id=user)
        post = POST(post_details=get_text, post_type=get_type, user=u)
        post.uploaded_picture = fs.url(get_profile)
        post.save()

    data = {}
    posts = list(POST.objects.all())
    if not posts:
        raise Http404("No MyModel matches the given query.")
    data = {"posts": posts}
    return render(request, "homepage.html", data)


def delete_post(request, id):
    # fetch the object related to passed id
    obj = POST.objects.get(id=id)
    print(id)
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/")

    return redirect(request, create_post(request))
