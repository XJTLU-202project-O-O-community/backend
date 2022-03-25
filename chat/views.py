import json
from django.core import serializers
from django.db.models import Q, Sum, Count, F, Max
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from chat.models import MessageList, MessageModel
from user.models import User


def index(request):
    return render(request, 'chat/index.html')


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })


@require_http_methods(["POST"])
def send_message(request):
    print(request)
    request_body = json.loads(request.body)
    user_id = request_body.get("user_id")
    recipent_id = request_body.get("recipient_id")
    message = request_body.get("message")
    print(user_id, "===>", message, "===>", recipent_id)
    try:
        msg = MessageList(user_id=user_id, recipient_id=recipent_id, message=message)
        msg.save()

        result = {
            "error_code": 200,
            "msg": "success",
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": "Something wrong happens, please try again later.",
        }
        return JsonResponse(result, status=500)


@require_http_methods(["GET"])
def receive_msg(request, message_id):
    user_id = request.GET.get("user_id")
    try:
        msg_obj = MessageList.objects.get(id=int(message_id))
        avatar = User.objects.get(id=msg_obj.user_id).photo

        result = {
            "error_code": 200,
            "msg": "success",
            "data": {
                "_id": message_id,
                "type": 'text',
                "content": {"text": msg_obj.message},
                "createdAt": msg_obj.createdAt,
                "position": "right" if int(user_id) == msg_obj.user_id else "left",
                "user": {"avatar": "/server/media/" + str(avatar)},
            }
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": "Something wrong happens, please try again later.",
        }
        return JsonResponse(result, status=500)


@require_http_methods(["GET"])
def history(request):
    user_id = request.GET.get("user_id")
    print(user_id)
    target_id = request.GET.get("target_id")
    print(target_id)
    history_msgs = MessageModel.objects\
        .filter(Q(room__user_id__in=[user_id, target_id]) & Q(room__recipient_id__in=[user_id, target_id]))\
        .order_by("createdAt")\
        .annotate(recipient_id=F('room__recipient_id'), user_id=F('room__user_id'))\
        .values("recipient_id", "user_id", "message", "createdAt", "id")
    # history_msgs = json.loads(serializers.serialize("json", history_msgs))
    result = {
        "error_code": 200,
        "msg": "success",
        "data": list(history_msgs),
    }
    return JsonResponse(result)


@require_http_methods(["GET"])
def messagelist(request):
    user_id = request.GET.get("user_id")
    id_1 = MessageList.objects.filter(user_id=user_id) \
        .annotate(message_user_id=F('recipient_id'), username=F('recipient__username'), avatar=F('recipient__photo')) \
        .values('message_user_id', 'username', 'avatar')
    id_2 = MessageList.objects.filter(recipient_id=user_id).exclude(
        user_id__in=[x['message_user_id'] for x in list(id_1)]) \
        .annotate(message_user_id=F('user_id'), username=F('user__username'), avatar=F('user__photo')) \
        .values('message_user_id', 'username', 'avatar')
    message_list = id_1 | id_2 if (id_1 and id_2) else id_1 if id_1 else id_2
    for x in message_list:
        x['msg'] = MessageModel.objects.filter((Q(room__user_id=x['message_user_id']) & Q(room__recipient_id=user_id)) |
                                    (Q(room__user_id=user_id) & Q(room__recipient_id=x['message_user_id'])))[:1][0].message
    result = {
        "error_code": 200,
        "msg": "success",
        "data": list(message_list),
    }
    return JsonResponse(result)
