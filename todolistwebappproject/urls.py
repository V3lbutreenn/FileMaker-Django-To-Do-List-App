# todolistwebappproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Bu satırı ekle
from django.conf.urls.static import static # Bu satırı ekle

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todolist.urls')),
]

