from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class register_info(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=32, null=False)
    email = models.EmailField(default="default@365.com")


class user_personal_info(models.Model):
    id = models.OneToOneField("register_info", on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(height_field=300, width_field=300, upload_to="photo", default='default.jpg')
    username = models.CharField(max_length=32, null=False)
    actual_name = models.CharField(max_length=32, default="")
    gender = models.CharField(max_length=2, default="没写")
    birth = models.DateField(default=2022-3-9)
    signature = models.CharField(max_length=64, default="这个人很神秘，什么都没写")

