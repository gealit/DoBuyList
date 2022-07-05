from django.db import models

from account.models import Account


class Room(models.Model):
    participants = models.ManyToManyField(Account)
    name = models.CharField(max_length=50)
    info = models.TextField(max_length=200, null=True, blank=True)
    password = models.CharField(max_length=10)

    def __str__(self):
        return f'Room: {self.name}'


class RoomTask(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    info = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField(default=False)

    class Meta:
        ordering = ('done', '-created',)

    def __str__(self):
        return f'Task: {self.title}'

