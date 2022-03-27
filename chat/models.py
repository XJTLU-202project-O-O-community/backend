# Create your models here.
from django.db import models
from user.models import UserProfile


class MessageList(models.Model):
    # 消息发出者
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,
                             related_name='sender_id', db_index=True)
    # 消息接收者
    recipient = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE,
                                  related_name='recipient_id', db_index=True)

    def __str__(self):
        return str(self.id)

    # Meta
    class Meta:
        unique_together = ("user_id", "recipient_id")


class MessageModel(models.Model):
    room = models.ForeignKey(to=MessageList, on_delete=models.CASCADE,
                             related_name='room_id', db_index=True)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True, editable=False,
                                     db_index=True)
    hasRead = models.BooleanField(default=True)

    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-createdAt',)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.message)

    def __str__(self):
        return str(self.id)