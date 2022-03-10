from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class UserAccount(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    email = models.EmailField()


class User(models.Model):
    id = models.OneToOneField("user.UserAccount", on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(upload_to="photo/", default='photo/default.jpg')
    username = models.CharField(max_length=32)
    actual_name = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=2, null=True)
    birth = models.DateField(null=True)
    signature = models.CharField(max_length=64, default="这个人很神秘，什么都没写")
