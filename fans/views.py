from django.db.models import Q, F, Max
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user.models import UserProfile
from .models import Following


# Create your views here.

# 【GET】返回 用户关注的人 的列表
# 【POST】关注用户
@require_http_methods(["GET", "POST"])
def following(request):
    if request.method == 'GET':
        user_id = request.GET.get("user_id")
        following_ids = Following.objects.filter(user_id=user_id).order_by("created_time").values("following_id")
        followings_info = []
        for x in following_ids:
            info = UserProfile.objects.filter(id=x['following_id']) \
                .annotate(username=F('name'), moment=F("moments_info__content")).order_by('-moments_info__ctime') \
                .values("username", "email", "photo", "actual_name", "gender", "birth",
                        "signature", "id", "moment")[0]
            followings_info.append(info)
        result = {
            "error_code": 200,
            "msg": "success",
            "data": {
                "user_id": user_id,
                "following_list": followings_info
            }
        }
        return JsonResponse(result, status=200)
    elif request.method == 'POST':
        user_id = request.POST.get("user_id")
        following_id = request.POST.get("following_id")
        try:
            obj, isCreated = Following.objects.get_or_create(user_id_id=user_id, following_id_id=following_id)
            if isCreated:
                result = {
                    "error_code": 200,
                    "msg": "user_" + str(user_id) + ' follows user_' + str(following_id) + " successfully.",
                }
            else:
                result = {
                    "error_code": 200,
                    "msg": "user_" + str(user_id) + ' has already followed user_' + str(
                        following_id) + " successfully.",
                }
            return JsonResponse(result, status=200)
        except Exception as e:
            print(e)
            result = {
                "error_code": 500,
                "msg": 'Something wrong happens. Try again later.',
            }
            return JsonResponse(result, status=500)
    else:
        result = {
            "error_code": 400,
            'msg': 'INVALID REQUEST'
        }
        return JsonResponse(result, status=400)


# 【POST】取消关注
@require_http_methods(["POST"])
def following_delete(request):
    user_id = request.POST.get("user_id")
    following_id = request.POST.get("following_id")
    try:
        following_obj = Following.objects.get(user_id=user_id, following_id=following_id)
        following_obj.delete()
        result = {
            "error_code": 200,
            "msg": "user_" + str(user_id) + ' cancels following user_' + str(following_id) + " successfully.",
        }
        return JsonResponse(result, status=200)
    except Following.DoesNotExist:
        result = {
            "error_code": 430,
            'msg': 'The following relationship does not exist.'
        }
        return JsonResponse(result, status=430)
    except Following.MultipleObjectsReturned:
        followings = Following.objects.filter(user_id=user_id, following_id=following_id)
        followings.delete()
        result = {
            "error_code": 200,
            "msg": "user_" + str(user_id) + ' cancels following user_' + str(following_id) + " successfully.",
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": 'Something wrong happens. Try again later.',
        }
        return JsonResponse(result, status=500)


# 【GET】返回粉丝列表
@require_http_methods(["GET"])
def fans(request):
    user_id = request.GET.get("user_id")
    try:
        fan_ids = Following.objects.filter(following_id=user_id).order_by('created_time').values('user_id')
        fans_info = []
        for x in fan_ids:
            info = UserProfile.objects.filter(id=x['user_id']) \
                .annotate(username=F('name'), moment=F('moments_info__content')).order_by('-moments_info__ctime') \
                .values("username", "email", "photo", "actual_name", "gender", "birth", "signature", "id", "moment")[0]
            fans_info.append(info)
        result = {
            "error_code": 200,
            "msg": "success",
            "data": {
                "user_id": user_id,
                "fans_list": fans_info
            }
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": 'Something wrong happens. Try again later.',
        }
        return JsonResponse(result, status=500)


# 【GET】关键词搜索关注的人
@require_http_methods(["GET"])
def search(request):
    user_id = request.GET.get("user_id")
    keyword = request.GET.get('keyword')

    if keyword == "":
        result = {
            "error_code": 403,
            "msg": 'empty keyword',
        }
        return JsonResponse(result, status=403)
    else:
        try:
            following_ids = Following.objects.filter(
                Q(user_id=user_id) & Q(following_id__name__contains=keyword)).order_by('created_time')\
                .values("following_id")
            followings_info = []
            for x in following_ids:
                info = UserProfile.objects.filter(id=x['following_id']) \
                    .annotate(username=F('name'), moment=F("moments_info__content")).order_by('-moments_info__ctime') \
                    .values("username", "email", "photo", "actual_name", "gender", "birth",
                            "signature", "id", "moment")[0]
                followings_info.append(info)
            result = {
                "error_code": 200,
                "msg": "success",
                "data": {
                    "user_id": user_id,
                    "following_list": followings_info
                }
            }
            return JsonResponse(result, status=200)
        except Exception as e:
            print(e)
            result = {
                "error_code": 500,
                "msg": 'Something wrong happens. Try again later.',
            }
            return JsonResponse(result, status=500)
