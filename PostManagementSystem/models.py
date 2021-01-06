from PIL.Image import Image
from django.db import models
from UserManagementSystem.models import User


# Create your models here.
class POST(models.Model):
    post_date = models.DateField(auto_now=True)
    post_details = models.CharField(max_length=200)
    post_type = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_picture = models.ImageField(upload_to='user/uploaded')


# overriding the save method for limiting the image size
# to avoid memory problem
def save(self, *args, **kwargs):
    super.save(*args, **kwargs)
    pic = Image.open(self.image.path)
    if pic.height > 500 or pic.width > 400:
        output = (300, 300)
        pic.thumbnail(output)
        pic.save(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(POST, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()


