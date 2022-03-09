from django.db import models


class moments_info(models.Model):
    id = models.AutoField(primarykey=True)
    user_id = models.ForeignKey(to="user_personal_info", to_field="id")
    content = models.TextField(max_length=100, default="")
    ctime = models.DateTimeField(auto_now_add=True)
    thumbs = models.SmallIntegerField(null=False, default=0)
    img_list = models.TextField(null=True)  # json 格式


class comments(models.Model):
    id = models.AutoField(primarykey=True)
    poster = models.ForeignKey(to="user_personal_info", to_field="id")
    match_moment = models.ForeignKey(to="moments_info", to_field="id")
    content = models.TextField(max_length=100, default="")
    ctime = models.DateTimeField(auto_now_add=True)


class imgs(models.Model):
    id = models.AutoField(primarykey=True)
    url = models.CharField(max_length=64, default="")

# Create your models here.
