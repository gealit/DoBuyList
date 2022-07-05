from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('todolist.urls')),
    path('', include('room.urls')),
    path('', include('chat.urls')),
]
