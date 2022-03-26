from django.db import models
from user.models import UserProfile

# Create your models here.

# 存储每个user关注的人的id
class Following(models.Model):
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='user_id')
    created_time = models.DateTimeField(auto_now_add=True)
    following_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='following_id')
    # 该用户关注的人的id

    class Meta:
        unique_together = ("user_id", "following_id")
