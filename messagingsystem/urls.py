from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'message/<int:user_id>', views.room, name='room'),
]