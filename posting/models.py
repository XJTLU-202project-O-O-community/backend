from user.models import *


class moments_info(models.Model):
    user_id = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    content = models.TextField(max_length=100, default="")
    ctime = models.DateTimeField(auto_now_add=True)
    thumbs = models.SmallIntegerField(null=True, default=0)
    likes = models.SmallIntegerField(null=True, default=0)


    class Meta:
        ordering = ('-ctime',)


class comments(models.Model):
    poster = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, to_field="id")
    match_moment = models.ForeignKey(to="moments_info", on_delete=models.CASCADE)
    content = models.TextField(max_length=100, default="")
    ctime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-ctime',)


class imgs(models.Model):
    url = models.CharField(max_length=64, default="/media/logo")
    moments = models.ForeignKey(to='moments_info', on_delete=models.CASCADE)


