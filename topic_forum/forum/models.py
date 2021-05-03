from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from books.models import book


class discussion(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(book, on_delete=models.CASCADE)
    discussion = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.book.book + ' / ' + self.discussion


class comment(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(null=True)
    post_title = models.CharField(max_length=150)
    text = models.TextField()
    user = models.ForeignKey(User, default=7,
                             on_delete=models.SET_DEFAULT)
    location = models.ForeignKey(discussion, on_delete=models.CASCADE)

    def __str__(self):
        return self.location.book.book + ' => ' + self.user.username
