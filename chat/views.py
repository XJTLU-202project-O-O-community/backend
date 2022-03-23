import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.http import require_http_methods

from chat.models import MessageModel
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
        msg = MessageModel(user_id=user_id, recipient_id=recipent_id, message=message)
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
        msg_obj = MessageModel.objects.get(id=int(message_id))
        avatar = User.objects.get(id=msg_obj.user_id).photo

        result = {
            "error_code": 200,
            "msg": "success",
            "data": {
                "_id": message_id,
                "type": 'text',
                "content": {"text": msg_obj.message},
                "createdAt": msg_obj.timestamp,
                "position": "right" if int(user_id) == msg_obj.user_id else "left",
                "user": {"avatar": "/server/user/" + str(avatar)},
            }
        }
        return JsonResponse(result, status=200)
    except ArithmeticError as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": "Something wrong happens, please try again later.",
        }
        return JsonResponse(result, status=500)
