from django.db import models
from django.contrib.auth.models import User


class DM(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(
        User, default=7, on_delete=models.SET_DEFAULT, related_name='sender')
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reciever')
    message_subject = models.CharField(max_length=150)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    new = models.BooleanField(default=True)
    deleted_sender = models.BooleanField(default=False)
    deleted_reciever = models.BooleanField(default=False)


class friend_list(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend")
