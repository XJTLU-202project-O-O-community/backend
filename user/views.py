import hashlib
import json
import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from fans.models import Following
from user.models import UserProfile


# Create your views here.

def encrypt(code):
    h = hashlib.md5()
    h.update(code.encode("utf-8"))
    return h.hexdigest()


@require_http_methods(["POST"])
def inlog(request):
    print(request.POST)
    email = request.POST.get("email")  # 获取用户名
    password = request.POST.get("password")  # 获取用户的密码
    user = authenticate(username=email, password=password)  # 验证用户名和密码，返回用户对象
    if user:  # 如果用户对象存在
        login(request, user)  # 用户登陆
        person = UserProfile.objects.filter(name=user.name)
        person_info = serializers.serialize("json", person)
        err_code = 200
        result = {
            "error_code": err_code,
            "msg": person[0].name + " login successfully",
            "data": json.loads(person_info)
        }
        request.user.last_login = timezone.now()
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)
    else:
        err_code = 400
        result = {
            "error_code": err_code,
            "msg": "邮箱或密码错误",
            "email": email,
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["POST"])
def email_inlog(request):
    print(request.POST)
    email = request.POST.get("email")
    given_verification = request.POST.get("given_verification")
    try:
        code = request.session.get("code")
        user = UserProfile.objects.get(email=email)
        if given_verification == code and user:
            login(request, user)
            person = UserProfile.objects.filter(name=user.name)
            person_info = serializers.serialize("json", person)
            err_code = 200
            result = {
                "error_code": err_code,
                "msg": person[0].name + " login successfully",
                "data": json.loads(person_info)
            }
            request.user.last_login = timezone.now()
            request.session.delete("email")
            request.session.delete("code")
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)
        else:
            err_code = 400
            result = {
                "error_code": err_code,
                "msg": "邮箱或验证码错误",
                "email": email,
            }
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)

    except Exception as e:
        err_code = 400
        result = {
            "error_code": err_code,
            "msg": str(e),
            "email": email,
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["GET"])
@login_required
def outlog(request):
    if request.method == 'GET':
        user_id = request.user.id
        person = UserProfile.objects.filter(id=user_id)
        person_info = serializers.serialize("json", person)
        err_code = 200
        result = {
            "error_code": err_code,
            "msg": person[0].name + " logout successfully",
            "data": json.loads(person_info)
        }
        logout(request)
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["POST"])
def regist(request):
    try:
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        actual_name = request.POST.get("actual_name")
        birth = request.POST.get("birth")
        given_verification = request.POST.get("given_verification")
        code = request.session.get("code")
        author_email = request.session.get('email')
        print(author_email)
        print(email)
        print(code)
        print(gender)
        print(given_verification)
        if given_verification == code and author_email == email:
            user = UserProfile.objects.create_user(name=username, password=password, email=email)
            err_code = 200
            if gender != "undefined":
                user.gender = gender
            if birth != "undefined":
                user.birth = birth
            if actual_name is not None:
                user.actual_name = actual_name
            user.save()
            result = {
                "error_code": err_code,
                "msg": "创建成功",
            }
            request.session.flush()
        else:
            err_code = 400
            result = {
                "error_code": err_code,
                "msg": "创建失败"
            }


        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)
    except Exception as e:
        err_code = 500
        result = {
            "error_code": err_code,
            "msg": str(e),
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["POST"])
def send_code(request):
    email = request.POST.get("email")
    print(request.POST)
    try:
        code, static = Email_Rand_Code(email)
        if static == 1:
            err_code = 200
            result = {
                "error_code": err_code,
                "msg": "验证码发送成功",
                "author_email": email,
            }
            request.session['code'] = code
            request.session['email'] = email
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)
        else:
            err_code = 400
            result = {
                "error_code": err_code,
                "msg": "验证码发送失败",
            }
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)

    except Exception as e:
        err_code = 500
        result = {
            "error_code": err_code,
            "msg": str(e)
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["GET"])
def personal_page(request):
    if request.method == "GET":
        his_id = request.GET.get("his_id")
        my_id = request.user.id
        try:
            if len(request.session.items()) == 0:
                err_code = 401
                result = {
                    "error_code": err_code,
                    "msg": "session expired",
                }
                return JsonResponse(result, status=200)
            err_code = 200
            if his_id != my_id:
                his_info = UserProfile.objects.filter(id=his_id)
                obj = Following.objects.filter(user_id=my_id)
                is_fan = False
                for each in obj:
                    if str(each.following_id) == his_id:
                        is_fan = True
                        break
                his_json_info = serializers.serialize("json", his_info)
            else:
                his_id = request.user.id
                his_info = UserProfile.objects.filter(id=his_id)
                is_fan = False
                his_json_info = serializers.serialize("json", his_info)

            result = {
                "error_code": err_code,
                "msg": "this is " + his_info[0].name + " personal page",
                "data": {"isFan": is_fan,
                         "personal_data": json.loads(his_json_info)
                         }
            }
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)
        except Exception as e:
            err_code = 500
            result = {
                "error_code": err_code,
                "msg": str(e)
            }
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)


@require_http_methods(["GET"])
def my_page(request):
    my_id = request.user.id
    try:
        if len(request.session.items()) == 0:
            err_code = 401
            result = {
                "error_code": err_code,
                "msg": "session expired",
            }
            return JsonResponse(result, status=200)
        my_info = UserProfile.objects.filter(id=my_id)
        my_json_info = serializers.serialize("json", my_info)
        err_code = 200
        result = {
            "error_code": err_code,
            "msg": "this is " + my_info[0].name + " personal page",
            "data": json.loads(my_json_info),
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)
    except Exception as e:
        err_code = 500
        result = {
            "error_code": err_code,
            "msg": str(e)
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["POST"])
def edit(request):
    print(request.POST)
    # 利用old_username获取数据库中信息
    try:
        if len(request.session.items()) == 0:
            err_code = 401
            result = {
                "error_code": err_code,
                "msg": "session expired",
            }
            return JsonResponse(result, status=200)
        old_username = request.user.name
        old_info = UserProfile.objects.get(name=old_username)

        # 修改用户名
        new_username = request.POST.get("new_username")
        if new_username is not None:
            old_info.name = new_username
            username = new_username
        else:
            username = old_username
        # 修改头像
        photo_name = request.POST.get('photo')
        if photo_name is not None:
            if old_info.photo != "photo/default.jpg":
                os.remove('./media/'+str(old_info.photo))
            old_info.photo = "photo/" + photo_name


        # 修改背景
        background_name = request.POST.get('background')
        if background_name is not None:
            old_info.background = background_name

        # 修改真实姓名
        actual_name = request.POST.get('actual_name')
        if actual_name is not None:
            old_info.actual_name = actual_name

        # 修改性别
        gender = request.POST.get('gender')
        if gender != "undefined":
            old_info.gender = gender

        # 修改城市
        city = request.POST.get('city')
        if city is not None:
            old_info.city = city

        # 修改生日
        birth = request.POST.get('birth')
        if birth != "undefined":
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
            'error_code': err_code,
            "msg": "modify success",
            "data": json.loads(personal_info),
        }

        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)

    except Exception as e:
        err_code = 500
        result = {
            'error_code': err_code,
            "msg": str(e)
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["POST"])
def change_pwd(request):
    username = request.user.name
    new_password = request.POST.get("new_password")
    try:
        if len(request.session.items()) == 0:
            err_code = 401
            result = {
                "error_code": err_code,
                "msg": "session expired",
            }
            return JsonResponse(result, status=200)
        request.user.set_password(new_password)
        personal_info = serializers.serialize('json', UserProfile.objects.filter(name=username))
        err_code = 200
        result = {
            'error_code': err_code,
            "msg": "修改密码成功",
            "data": json.loads(personal_info),
        }
        #request.session.flush()
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)
    except Exception as e:
        return HttpResponse(str(e), status=200)


def Email_Rand_Code(email):
    import random
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    for i in range(65, 91):  # 对应从“A”到“Z”的ASCII码
        code_list.append(chr(i))
    for i in range(97, 123):  # 对应从“a”到“z”的ASCII码
        code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)
    # try:
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    res = send_mail('oo_community的验证码', verification_code, '1076627773@qq.com',
                    [email], fail_silently=False)
    if res != 1:
        static = 0
        print('验证码发送失败')
    else:
        static = 1
        print('验证码发送成功')
    return verification_code, static


@require_http_methods(["GET"])
def search(request):
    username = request.GET.get("username")
    try:
        if len(request.session.items()) == 0:
            err_code = 401
            result = {
                "error_code": err_code,
                "msg": "session expired",
            }
            return JsonResponse(result, status=200)
        obj = UserProfile.objects.filter(name=username)
        if obj:
            his_info = serializers.serialize('json', obj)
            err_code = 200
            result = {
                'error_code': err_code,
                "msg": "这是" + username + "的信息",
                "data": json.loads(his_info),
            }
            # return JsonResponse(result, status=err_code)
            return JsonResponse(result, status=200)
        else:

            err_code = 400
            result = {
                'error_code': err_code,
                "msg": "查无此人",
            }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)
    except Exception as e:
        err_code = 500
        result = {
            "error_code": err_code,
            "msg": str(e)
        }
        # return JsonResponse(result, status=err_code)
        return JsonResponse(result, status=200)


@require_http_methods(["POST"])
def img_uploader(request):
    try:
        if len(request.session.items()) == 0:
            err_code = 401
            result = {
                "error_code": err_code,
                "msg": "session expired",
            }
            return JsonResponse(result, status=200)
        img = request.FILES['file']
        f = open('./media/photo/' + img.name, 'wb+')
        f.write(img.read())
        f.close()
        result = {
            'error_code': 200,
            'message': 'upload success'
        }
        # return JsonResponse(result, status=200)
        return JsonResponse(result, status=200)
    except Exception as e:
        result = {
            'error_code': 500,
            'message': 'Count problems'
        }
        # return JsonResponse(result, status=500)
        return JsonResponse(result, status=200)

