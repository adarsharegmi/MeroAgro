from django.db import models
from UserManagementSystem.models import User
# Create your models here.
class POST(models.Model):
    post_date = models.DateField(auto_now=True)
    post_details = models.CharField(max_length=200)
    post_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_picture = models.ImageField(upload_to='user/uploaded')
