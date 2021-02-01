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
def room(request,user_id):
    u1 = User.objects.get(id=request.session['id'])
    u2 = User.objects.get(id=user_id)

    room = Room.objects.filter(user=u1).filter(user=u2)

    #
    try:
        ms = all_messages(room[0].id)
        print("all the messages",ms)
        return render(request, 'chat/room.html', {
            'room_name': room[0].room_name,
            'user_id': u1.id,
            'messages':ms
        })
    except :
        return render(request,'chat/room.html',{
            'room_name':"room"+str(Room.objects.all().count()+1),
            'user_id':u1.id
        })


def all_messages(room_id):
    print("the messages---",room_id)
    ms = Message.objects.filter(user_room=room_id)

    return ms
    # print(user_room.id)