from django.urls import include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from django_email_verification import urls as mail_urls


urlpatterns = [
    path('user/', include("UserManagementSystem.urls")),
    path('email/', include(mail_urls)),
    path('',include("PostManagementSystem.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
