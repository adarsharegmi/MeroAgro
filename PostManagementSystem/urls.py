from django.urls import path, include
from .views import *

urlpatterns = [
    path('', create_post, name='create_post'),
    path('post', save_post, name='save_post'),
    path('delete/<int:id>', delete_post, name='delete_post'),
]
