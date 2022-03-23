# Create your models here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models

from user.models import User


class MessageModel(models.Model):
    # 消息发出者
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='sender_id', db_index=True)
    # 消息接收者
    recipient = models.ForeignKey(to=User, on_delete=models.CASCADE,
                                  related_name='recipient_id', db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False,
                                     db_index=True)
    message = models.TextField()

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.message)

    def notify_ws_clients(self):
        print("======================================")
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'chat_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user_id))
        print("user.id {}".format(self.recipient_id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user_id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient_id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.message = self.message.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'chat'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)
