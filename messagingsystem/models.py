from django.db import models

# Create your models here.
from django.db import models
from UserManagementSystem.models import User


class Room(models.Model):
    room_name = models.CharField(max_length=100, unique=True)
    user = models.ManyToManyField(User)


class Message(models.Model):
    messageId = models.CharField(max_length=50)
    messageDate = models.DateTimeField()
    messageText = models.TextField()
    user_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
