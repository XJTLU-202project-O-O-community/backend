import json

from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from user.models import UserAccount, User


# Create your views here.
@require_http_methods(["POST"])
def register(request):
    if request.method == 'POST':
        #获取前端传过来的信息
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        actual_name = request.POST.get("actual_name")
        gender = request.POST.get("gender")
        birth = request.POST.get("birth")

        try:
            #如果username，email不存在于数据库中，成功创建账户
            if UserAccount.objects.filter(username=username).count() == 0 and UserAccount.objects.filter(
                    email=email).count() == 0:
                err_code = 200
                UserAccount.objects.create(username=username, password=password, email=email)
                User.objects.create(id_id=UserAccount.objects.get(username=username).id, actual_name=actual_name,
                                    gender=gender, birth=birth, username=username)
                result = {
                    "err_code": err_code,
                    "msg": "创建成功",
                    "username": username
                }
            #用户名重复
            elif UserAccount.objects.filter(username=username).count() != 0:
                err_code = 400
                result = {
                    "err_code": err_code,
                    "msg": "duplicated username",
                    "username": username
                }
            #email重复
            elif UserAccount.objects.filter(email=email).count() != 0:
                err_code = 400
                result = {
                    "err_code": err_code,
                    "msg": "duplicated email address",
                    "username": username
                }
            return JsonResponse(result, status=err_code)
        except Exception as e:
            err_code = 500
            result = {
                "err_code": err_code,
                "msg": str(e)
            }
            return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
def login(request):
    if request.method == "POST":
        #接受用户名，密码
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            #从数据库中获取用户名,密码
            account = UserAccount.objects.get(username=username)
            db_username = account.username
            db_password = account.password
            #匹配
            if db_username == username and password == db_password:
                err_code = 200
                result = {
                    "error_code": err_code,
                    "msg": 'Login Successfully',
                    "username": username
                }
            #不匹配
            elif password != db_password:
                err_code = 400
                result = {
                    "err_code": err_code,
                    "msg": "wrong password",
                    "username": username
                }
            return JsonResponse(result, status=err_code)
        #账号不存在
        except Exception as e:
            print(e)
            err_code = 400
            result = {
                "err_code": err_code,
                "msg": "the username does not exist",
                "username": username
            }
            return JsonResponse(result, status=err_code)


@require_http_methods(["GET"])
def personal_page(request):
    if request.method == "GET":
        #获取用户名
        username = request.GET.get('username')
        try:
            err_code = 200
            #从数据库中获取数据
            person = User.objects.filter(username=username)
            person_info = serializers.serialize("json", person)
            result = {
                "err_code": err_code,
                "msg": "this is " + username + " personal page",
                "data": json.loads(person_info)
            }
            return JsonResponse(result, status=err_code)
        except Exception as e:
            err_code = 500
            result = {
                "err_code": err_code,
                "msg": e
            }
            return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
def edit(request):
    #利用old_username获取数据库中信息
    old_username = request.POST.get("old_username")
    old_info = User.objects.get(username=old_username)
    new_username = request.POST.get("new_username")
    #修改用户名
    if new_username is not None:
        old_info.username = new_username
    #修改头像
    if len(request.FILES) != 0:
        photo = request.FILES['photo']
        old_info.photo = photo
    actual_name = request.POST.get('actual_name')
    #修改真实姓名
    if actual_name is not None:
        old_info.actual_name = actual_name
    gender = request.POST.get('gender')
    #修改性别
    if gender is not None:
        old_info.gender = gender
    birth = request.POST.get('birth')
    #修改生日
    if birth is not None:
        birth = request.POST.get('birth')
        old_info.birth = birth
    #修改个签
    signature = request.POST.get('signature')
    old_info.signature = signature
    old_info.save()
    #发回修改后信息
    personal_info = serializers.serialize('json', User.objects.filter(username=new_username))
    err_code = 200
    result = {
        'err_code': err_code,
        "data": json.loads(personal_info),
    }

    return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
def change_pwd(request):
    username = request.POST.get("username")
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    #核对旧密码
    db_password = UserAccount.objects.get(username=username).password
    if db_password == old_password:
        err_code = 200
        UserAccount.objects.filter(username=username).update(password=new_password)
        res = {
            "err_code": err_code,
            "msg": "修改密码成功",
        }
        return JsonResponse(res, status=err_code)
    else:
        err_code = 400
        res = {
            "err_code": err_code,
            "msg": "修改失败，原密码不匹配",
        }
        return JsonResponse(res, status=err_code)


@require_http_methods(["POST"])
def photo_upload(request):
    if len(request.FILES) != 0:
        file = request.FILES['photo']
        file_data = file.read()
        result = {
            "data": file.name
        }
        return JsonResponse(result, status=200)
    else:
        result = {
            "data": "a",
        }
        return JsonResponse(result, status=200)
