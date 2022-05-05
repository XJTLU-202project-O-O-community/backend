from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from chat.models import MessageList, MessageModel


@require_http_methods(["GET"])
def history(request):
    result = {}
    user_id = request.GET.get("user_id")
    target_id = request.GET.get("target_id")
    try:
        MessageModel.objects.filter(room__user_id=target_id, room__recipient_id=user_id, hasRead=False).update(
            hasRead=True)
        history_msgs = MessageModel.objects \
            .filter(Q(room__user_id__in=[user_id, target_id]) & Q(room__recipient_id__in=[user_id, target_id])) \
            .order_by("createdAt") \
            .annotate(recipient_id=F('room__recipient_id'), user_id=F('room__user_id')) \
            .values("recipient_id", "user_id", "message", "createdAt", "id")
        if len(history_msgs)>0:
            result = {
                "error_code": 200,
                "msg": "success",
                "data": list(history_msgs),
            }

            channel_layer = get_channel_layer()
            notification = {
                'type': 'change_target',
                'target_user_id': target_id,
            }
            async_to_sync(channel_layer.group_send)("{}".format(user_id), notification)
        else:
            result = {
                "error_code": 430,
                "msg": "no chat history",
            }
    except Exception as e:
        print(e)
        result = {
            "error_code": 200,
            "msg": "Something wrong happens. Please try again later",
        }
    finally:
        return JsonResponse(result)


@require_http_methods(["GET"])
def messagelist(request):
    result = {}
    user_id = request.GET.get("user_id")
    try:
        id_1 = MessageList.objects.filter(recipient_id=user_id) \
            .annotate(message_user_id=F('user_id'), username=F('user__name'), avatar=F('user__photo')) \
            .values('message_user_id', 'username', 'avatar')
        print(id_1)
        id_2 = MessageList.objects.filter(user_id=user_id)\
            .exclude(recipient_id__in=[x['message_user_id'] for x in list(id_1)]) \
            .annotate(message_user_id=F('recipient_id'), username=F('recipient__name'), avatar=F('recipient__photo')) \
            .values('message_user_id', 'username', 'avatar')
        print(id_2)
        message_list = [*id_1, *id_2]
        print(message_list)
        if message_list:
            for x in message_list:
                try:
                    x['msg'] = MessageModel.objects \
                                   .filter((Q(room__user_id=x['message_user_id']) & Q(room__recipient_id=user_id)) |
                                           (Q(room__user_id=user_id) & Q(room__recipient_id=x['message_user_id'])))[:1][0].message
                except Exception as e:
                    print(e)
                x['num'] = MessageList.objects \
                    .filter(recipient_id=user_id, user_id=x['message_user_id'], room_id__hasRead=False).count()
            result = {
                "error_code": 200,
                "msg": "success",
                "data": list(message_list),
            }
        else:
            result = {
                "error_code": 430,
                "msg": "no message list",
            }
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": "Something wrong happens. Please try again later",
        }
    finally:
        return JsonResponse(result)
