from django.db import models
from django.contrib.auth.models import User


class book(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.CharField(max_length=150)
    published = models.DateField(auto_now_add=True)
    abstract = models.TextField()
    pdf = models.FileField(upload_to='books')
    cover = models.ImageField()
    line = models.TextField(default='')

    def __str__(self):
        return self.book


class contact(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(User, default=7, on_delete=models.SET_DEFAULT)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.email
