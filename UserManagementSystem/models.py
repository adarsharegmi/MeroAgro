from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(models.Model):
    user_id= models.CharField(max_length=30)
    user_email = models.EmailField()
    user_address = models.CharField(max_length=50)
    user_password = models.CharField(max_length=200)
    user_type = models.CharField(max_length=20)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email_confirmed  = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender,instance, created,**kwargs):
    if  created:
        Profile.objects.create(user=instance)
        instance.profile.save()