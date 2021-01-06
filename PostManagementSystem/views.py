from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from UserManagementSystem.models import Images
from .models import *
import json


# Create your views here.
def create_post(request):
    data = {}
    dict_image = {}
    try:
        image = Images.objects.get(name_id=request.session['id'])
        posts = list(POST.objects.all())
        comments = list(Comment.objects.all())
        images = Images.objects.all()
        # creating a dictionary of images modal..

        for image in images:
            dict_image[image.name_id] = image.profile_picture

        if not posts:
            return render(request, "homepage.html")
        data = {"posts": posts, "pp": image.profile_picture.url, "comments": comments, "images": dict_image,"temp":0}
        return render(request, "homepage.html", data)
    except Exception as e:
        print(e)
        return render(request, "startpage.html")


def save_post(request):
    # fs = FileSystemStorage()
    if request.method == 'POST' and request.FILES:
        get_text = request.POST['text']
        get_type = request.POST['type']
        get_picture = request.FILES['profilepicture']
        # get_profile = fs.save("uu", get_picture)
        user = request.session['id']
        u = User.objects.get(id=user)
        post = POST(post_details=get_text, post_type=get_type, user=u)
        post.uploaded_picture = get_picture
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
    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/")

    return redirect(request, create_post(request))


# view for commenting the section
def post_detailview(request, id):
    if request.method == 'POST':
        content = request.POST.get('comment')

        user = request.session['id']
        p = POST.objects.get(id=id)
        u = User.objects.get(id=user)

        comment = Comment.objects.create(post=p, text=content, user=u)
        comment.save()
        return HttpResponseRedirect('/')
    return redirect(request, create_post(request))
