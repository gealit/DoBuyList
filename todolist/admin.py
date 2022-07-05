from django.contrib import admin

from todolist.models import Task, Room, RoomTask

admin.site.register(Task)
admin.site.register(Room)
admin.site.register(RoomTask)
