from django.db import models
from user.models import UserProfile


# Create your models here.

class Group(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    group_name = models.TextField(max_length=20)


# 存储每个user关注的人的id
class Following(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='user_id')
    created_time = models.DateTimeField(auto_now_add=True)
    following = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='following_id')
    group = models.ForeignKey(to=Group, on_delete=models.CASCADE, null=True)

    # 该用户关注的人的id

    class Meta:
        unique_together = ("user_id", "following_id")
