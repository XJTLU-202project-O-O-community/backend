import json
from django.db.models import Q, F, Model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from user.models import UserProfile
from .models import Following, Group


# Create your views here.

# 【GET】返回 用户关注的人 的列表（以分组的形式）
# 【POST】关注用户 并 保存分组
@require_http_methods(["GET", "POST"])
def following(request):
    if request.method == 'GET':
        user_id = request.GET.get("user_id")

        group_info = Following.objects.filter(user_id=user_id).values("group").order_by("created_time")
        groups = set()
        for x in group_info:
            groups.add(x['group'])
        if len(groups) <= 0:
            result = {
                "error_code": 204,
                "msg": "No followings",
            }
            return JsonResponse(result, status=200)

        followings = []
        for group in group_info:
            group_members = []
            followings_info = Following.objects.filter(user_id=user_id, group=group).values("following").order_by(
                "created_time")
            for following in followings_info:
                info = UserProfile.objects.filter(id=following['following']) \
                    .annotate(username=F('name'), moment=F("moments_info__content")).order_by('-moments_info__ctime') \
                    .values("username", "email", "photo", "actual_name", "gender", "birth",
                            "signature", "id", "moment")[0]
                group_members.append(info)
            followings.append({
                "group_id": group.id,
                "group_name": group.group_name,
                "group_members": group_members,
            })
        result = {
            "error_code": 200,
            "msg": "success",
            "data": {
                "user_id": user_id,
                "following_list": followings
            }
        }
        return JsonResponse(result, status=200)

    elif request.method == 'POST':
        request_body = json.loads(request.body)
        user_id = request_body.get("user_id")
        following_id = request_body.get("following_id")
        group_id = request_body.get("group_id")
        try:
            obj, isCreated = Following.objects.get_or_create(user_id=user_id, following_id=following_id,)
            if isCreated:
                result = {
                    "error_code": 200,
                    "msg": "user_" + str(user_id) + ' follows user_' + str(following_id) + " successfully.",
                }
            else:
                obj.group_id = group_id
                obj.save()
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
            return JsonResponse(result, status=200)
    else:
        result = {
            "error_code": 400,
            'msg': 'INVALID REQUEST'
        }
        return JsonResponse(result, status=200)


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
    print(user_id)
    try:
        fan_ids = Following.objects.filter(following_id=user_id).order_by('created_time').values('user')
        fans_info = []
        for x in fan_ids:
            info = UserProfile.objects.filter(id=x['user']) \
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
        following_ids = Following.objects.filter(user_id=user_id).order_by("created_time").values("following")
        followings_info = []
        for x in following_ids:
            info = UserProfile.objects.filter(id=x['following']) \
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
    else:
        try:
            following_ids = Following.objects.filter(
                Q(user_id=user_id) & Q(following__name__contains=keyword)).order_by('created_time') \
                .values("following")
            followings_info = []
            for x in following_ids:
                info = UserProfile.objects.filter(id=x['following']) \
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


# 【POST】增加分组
@require_http_methods(["POST"])
def group(request):
    request_body = json.loads(request.body)
    user_id = request_body.get("user_id")
    group_name = request_body.get("group_name")
    try:
        obj, isCreated = Group.objects.get_or_create(user_id=user_id, group_name=group_name)
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": 'Something wrong happens. Try again later.',
        }
        return JsonResponse(result, status=200)
    if isCreated:
        result = {
            "error_code": 200,
            "msg": "group name %s has existed" % group_name,
        }
    else:
        result = {
            "error_code": 200,
            "msg": "user_%s created group %s successfully." % (user_id, group_name),
        }
    return JsonResponse(result, status=200)


# 【POST】修改分组名称
@require_http_methods(["POST"])
def group_edit(request):
    request_body = json.loads(request.body)
    user_id = request_body.get("user_id")
    group_id = request_body.get("group_id")
    group_name = request_body.get("group_name")
    try:
        group = Group.objects.get(id=group_id)
        if user_id == group.following__user_id:
            group.group_name = group_name
            group.save()
        else:
            result = {
                "error_code": 204,
                "msg": 'do not have sufficient permission'
            }
            return JsonResponse(result, status=200)
    except Model.DoesNotExist as e:
        print(e)
        result = {
            "error_code": 400,
            "msg": 'group id %s does not exist'
        }
        return JsonResponse(result, status=200)
    result = {
        "error_code": 200,
        "msg": "user has edited group %s into name %s successfully." % (group_id, group_name),
    }
    return JsonResponse(result, status=200)


# 【POST】删除分组
@require_http_methods(["POST"])
def following_group_delete(request):
    request_body = json.loads(request.body)
    group_id = request_body.get("group_id")
    user_id = request_body.get("user_id")
    following_id = request_body.get("following_id")
    try:
        following_obj = Following.objects.filter(user_id=user_id, following_id=following_id)
        following_obj.group_id = group_id
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": 'Something wrong happens. Please try again later'
        }
        return JsonResponse(result, status=200)
    result = {
        "error_code": 200,
        "msg": "user id %s has edited user id %s into group id %s successfully." % (user_id, following_id, group_id),
    }
    return JsonResponse(result, status=200)


# 【POST】删除分组
@require_http_methods(["POST"])
def group_delete(request):
    request_body = json.loads(request.body)
    group_id = request_body.get("group_id")
    try:
        Following.objects.filter(group_id=group_id).update(group=None)
        Group.objects.get(id=group_id).delete()
    except Model.DoesNotExist as e:
        print(e)
        result = {
            "error_code": 400,
            "msg": 'Group id %s does not exist' % group_id
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        print(e)
        result = {
            "error_code": 500,
            "msg": 'Something wrong happens. Please try again later'
        }
        return JsonResponse(result, status=200)
    result = {
        "error_code": 200,
        "msg": "user has deleted group id %s successfully." % group_id,
    }
    return JsonResponse(result, status=200)