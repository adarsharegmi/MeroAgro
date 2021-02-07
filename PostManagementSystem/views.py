from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from UserManagementSystem.models import Images
from .models import *
import json


# Create your views here.
def create_post(request):
    if not request.user.is_authenticated:
        return render(request,'startpage.html')

    try:
        u = get_User(request)
        image = Images.objects.get(name_id=u.id)
        posts = get_list(request, POST.objects.all())
        dict_image = get_images()
        if not posts:
            return render(request, "homepage.html")
        comment_dict = post_to_dict(request, posts)
        data = {"user": request.session['id'], "posts": posts, "pp": image.profile_picture.url,
                "comments": comment_dict,
                "images": dict_image,
                "size": 3, 'temp': 0}

        return render(request, "homepage.html", data)
    except Exception as e:
        return render(request, "startpage.html")


def save_post(request):
    # fs = FileSystemStorage()
    if request.method == 'POST' and request.FILES:
        get_text = request.POST['text']
        get_type = request.POST['type']
        get_pictures = request.FILES.getlist('post_pictures')


        # get_profile = fs.save("uu", get_picture)
        user = request.session['id']
        u = User.objects.get(id=user)
        post = POST(post_details=get_text, post_type=get_type, user=u)
        post.save()
        for p in get_pictures:
            PostImages(uploaded_picture=p,post=post).save()

    data = {}
    posts = list(POST.objects.all())
    if not posts:
        raise Http404("No MyModel matches the given query.")
    return HttpResponseRedirect('/')
    return redirect(request, create_post(request))


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


def likePost(request):
    if request.method == 'GET':
        u = get_User(request)
        liked_post = get_Post(request)
        try:
            Like_obj = like.objects.get(post_id=liked_post.id)
            Like_obj.dislikes = 0
            Like_obj.like = 1
            Like_obj.save()
        except Exception as e:
            m = like(post=liked_post, like=1, dislikes=0, user=u)
            m.save()
        return HttpResponse("Liked")
    else:
        return HttpResponse("Request method is not a GET")


def DislikePost(request):
    if request.method == 'GET':
        u = get_User(request)
        liked_post = get_Post(request)
        try:
            Like_obj = like.objects.get(post_id=liked_post.id)
            Like_obj.like = 0
            Like_obj.dislikes = 1
            Like_obj.save()
        except Exception as e:
            m = like(post=liked_post, like=0, dislikes=1, user=u)
            m.save()
        return HttpResponse("Disliked")
    else:
        return HttpResponse("Request method is not a GET")


def userPosts(request):
    u = get_User(request)
    image = Images.objects.get(name_id=u.id)
    posts = POST.objects.filter(user=u)
    dict_image = get_images()
    if not posts:
        return render(request, "profilepage.html")
    comment_dict = post_to_dict(request, posts)
    data = {"user": request.session['id'], "posts": posts, "pp": image.profile_picture.url,
            "comments": comment_dict,
            "images": dict_image,
            "size": 3, 'temp': 0}

    return render(request, "profilepage.html", data)



from django.core import serializers
from django.http import JsonResponse


def showcomments(request):
    offset = int(request.GET['size'])
    post_id = int(request.GET['post_id'])
    page = int(request.GET['page'])
    comments = get_list(request, Comment.objects.filter(post_id=post_id).order_by('-id'))
    hasMore = comments.has_next()

    totalComments = Comment.objects.count()
    u = User.objects.all()
    for a_comment in comments:
        a_comment.user_id = Images.objects.get(name_id=a_comment.user_id).profile_picture

    comments_json = serializers.serialize('json', comments)
    return JsonResponse(data={
        'comments': comments_json,
        'totalResult': totalComments,
        'hasMore': hasMore,
    })


def get_User(request):
    user = request.session['id']
    return User.objects.get(id=user)


def get_Post(request):
    post_id = request.GET['post_id']
    return POST.objects.get(id=post_id)


def get_list(request, L):
    page = request.GET.get('page', 1)
    paginator = Paginator(L, 2)
    try:
        p = paginator.page(page)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        p = paginator.page(paginator.num_pages)
    return p


def get_images():
    dict = {}
    images = Images.objects.all()
    for image in images:
        dict[image.name_id] = image.profile_picture
    return dict


def post_to_dict(request, posts):
    dic = {}
    for post in posts:
        temp = Comment.objects.filter(post_id=post.id).order_by('-id')
        dic[post.id] = get_list(request, temp)
    return dic
