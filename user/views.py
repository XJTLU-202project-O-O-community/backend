import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from user.models import UserAccount, User, UserProfile


# Create your views here.
@require_http_methods(["POST"])
def inlog(request):
    email = request.POST.get("email")  # 获取用户名
    password = request.POST.get("password")  # 获取用户的密码

    user = authenticate(username=email, password=password)  # 验证用户名和密码，返回用户对象
    if user:  # 如果用户对象存在
        login(request, user)  # 用户登陆

        return HttpResponse("成功")

    else:

        return HttpResponse("邮箱或密码错误")


@require_http_methods(["GET"])
@login_required
def outlog(request):
    if request.method == 'GET':
        username = request.user.name
        person = UserProfile.objects.filter(name=username)
        person_info = serializers.serialize("json", person)
        err_code = 200
        result = {
            "err_code": err_code,
            "msg": username + " logout successfully",
            "data": json.loads(person_info)
        }
        logout(request)
        return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
def regist(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get("email")
        UserProfile.objects.create_user(name=username, password=password, email=email)
        person = UserProfile.objects.get(name=username)
        err_code = 200
        result = {
            "err_code": err_code,
            "msg": "创建成功",
            "username": person.name
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        err_code = 400
        print(e)
        result = {
            "err_code" : err_code,
            "msg": "e",
        }
        return JsonResponse(result, status=err_code)


@require_http_methods(["GET"])
@login_required
def personal_page(request):
    if request.method == "GET":
        username = request.GET.get("username")
        try:
            err_code = 200
            # 从数据库中获取数据
            #username = request.user.name
            person = UserProfile.objects.filter(name=username)
            person_info = serializers.serialize("json", person)
            result = {
                "err_code": err_code,
                "msg": "this is " + username + " personal page",
                "data": json.loads(person_info)
            }
            return JsonResponse(result, status=err_code)
        except Exception as e:
            print(e)
            err_code = 500
            result = {
                "err_code": err_code,
                "msg": e
            }
            return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
@login_required
def edit(request):
    # 利用old_username获取数据库中信息
    try:

        old_username = request.POST.get("old_username")
        old_info = UserProfile.objects.get(name=old_username)
        new_username = request.POST.get("new_username")
        # 修改用户名
        if new_username is not None:
            old_info.name = new_username
            username = new_username
        else:
            username = old_username
        # 修改头像
        if len(request.FILES) != 0:
            photo = request.FILES['photo']
            old_info.photo = photo
        actual_name = request.POST.get('actual_name')
        # 修改真实姓名
        if actual_name is not None:
            old_info.actual_name = actual_name
        gender = request.POST.get('gender')
        # 修改性别
        if gender is not None:
            old_info.gender = gender
        birth = request.POST.get('birth')
        # 修改生日
        if birth is not None:
            birth = request.POST.get('birth')
            old_info.birth = birth
        # 修改个签
        signature = request.POST.get('signature')
        old_info.signature = signature
        old_info.save()
        # 发回修改后信息
        personal_info = serializers.serialize('json', UserProfile.objects.filter(name=username))
        err_code = 200
        result = {
            'err_code': err_code,
            "msg": "modify success",
            "data": json.loads(personal_info),
        }

        return JsonResponse(result, status=err_code)
    except Exception as e:
        err_code = 500
        result = {
            'err_code': err_code,
            "msg": str(e)
        }
        return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
@login_required
def change_pwd(request):
    username = request.user.name
    old_password = request.POST.get("old_password")
    new_password = request.POST.get("new_password")
    # 核对旧密码
    if request.user.check_password(old_password):
        request.user.set_password(new_password)
        personal_info = serializers.serialize('json', UserProfile.objects.filter(name=username))
        err_code = 200
        result = {
            'err_code': err_code,
            "msg": "修改密码成功",
            "data": json.loads(personal_info),
        }

        return JsonResponse(result, status=err_code)
    else:
        err_code = 400
        res = {
            "err_code": err_code,
            "msg": "修改失败，原密码不匹配",
        }
        return JsonResponse(res, status=err_code)


'''@require_http_methods(["POST"])
def photo_upload(request):
    username = request.POST.get("username")
    url = User.objects.get(username=username).photo.url
    file = open("./" + url, 'rb')
    with open("try.jpg", 'wb') as f:
        f.write(file.read())
    response = HttpResponse("a")
    return HttpResponse("a")'''
