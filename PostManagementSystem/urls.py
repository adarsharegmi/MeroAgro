from django.urls import path, include
from .views import *
from UserManagementSystem.views import show_user

urlpatterns = [
    path('', create_post, name='create_post'),
    path('post', save_post, name='save_post'),
    path('delete/<int:id>', delete_post, name='delete_post'),
    path('comment_save/<int:id>', post_detailview),
    path('like_post', likePost),
    path('dislike_post', DislikePost),
    path('show_comments',showcomments),
    path('profile',userPosts,name='profile'),
    path(r'show_profile/<int:user_id>',show_user)
]
