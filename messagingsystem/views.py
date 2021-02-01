from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *


def index(request):
    return render(request, 'chat/index.html')


@csrf_exempt
def room(request):
    print("loading room view")
    room_name = request.POST['room']
    user = request.POST.get('user')
    print(room_name)
    # breakpoint()

    try:
        ms = all_messages(room_name)
        print("all the messages",ms)
        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'user_id': user,
            'messages':ms
        })
    except :
        return render(request,'chat/room.html',{
            'room_name':room_name,
            'user_id':user
        })


def all_messages(room_name):
    room_id = Room.objects.get(room_name=room_name)
    print("the messages---",room_id.id)
    ms = Message.objects.filter(user_room=room_id)

    return ms
    # print(user_room.id)