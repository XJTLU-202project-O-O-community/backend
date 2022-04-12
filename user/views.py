import json
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, HttpResponse, request
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from user.models import UserProfile
from fans.models import Following


# Create your views here.
@require_http_methods(["POST"])
def inlog(request):
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
        return JsonResponse(result, status=err_code)

    else:
        err_code = 400
        result = {
            "error_code": err_code,
            "msg": "邮箱或密码错误",
            "email": email,
        }
        return JsonResponse(result, status=err_code)


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
        return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
def regist(request):
    try:
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get("email")
        UserProfile.objects.create_user(name=username, password=password, email=email)
        err_code = 200
        result = {
            "error_code": err_code,
            "msg": "创建成功",
        }
        return JsonResponse(result, status=200)
    except Exception as e:
        err_code = 400
        print(e)
        result = {
            "error_code": err_code,
            "msg": str(e),
        }
        return JsonResponse(result, status=err_code)


@require_http_methods(["GET"])
@login_required
def personal_page(request):
    if request.method == "GET":
        his_id = request.GET.get("his_id")
        my_id = request.user.id
        print("abcde")
        print(his_id)
        try:
            err_code = 200
            if his_id != my_id:
                his_info = UserProfile.objects.filter(id=his_id)
                print(his_info)
                obj = Following.objects.filter(user_id=my_id)
                is_friend = False
                for each in obj:
                    if str(each.following_id) == his_id:
                        print("T")
                        is_friend = True
                        break
                his_json_info = serializers.serialize("json", his_info)
            else:
                his_id = request.user.id
                his_info = UserProfile.objects.filter(id=his_id)
                is_friend = True
                his_json_info = serializers.serialize("json", his_info)

            result = {
                "error_code": err_code,
                "msg": "this is " + his_info[0].name + " personal page",
                "isFriend": is_friend,
                "data": json.loads(his_json_info),
            }
            return JsonResponse(result, status=err_code)
        except Exception as e:
            err_code = 500
            result = {
                "error_code": err_code,
                "msg": str(e)
            }
            return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
@login_required
def edit(request):
    # 利用old_username获取数据库中信息
    # try:
    print("修改")
    print(request.POST)
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
    if photo_name != '':
        print(photo_name)
        old_info.photo = "photo/"+ photo_name


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
        'err_code': err_code,
        "msg": "modify success",
        "data": json.loads(personal_info),
    }

    return JsonResponse(result, status=err_code)


'''    except Exception as e:
        err_code = 500
        result = {
            'err_code': err_code,
            "msg": str(e)
        }
        return JsonResponse(result, status=err_code)'''


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
            "error_code": err_code,
            "msg": "修改失败，原密码不匹配",
        }
        return JsonResponse(res, status=err_code)


def Email_Rand_Code(request):
    email = request.POST.get('email')
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
    # 将随机的验证存在session表中，方便进行验证
    request.session['rand_code'] = verification_code
    # try:
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    res = send_mail('oo_community的验证码', verification_code, '1076627773@qq.com',
                    [email], fail_silently=False)
    print(res)
    if res != 1:
        static = '验证码发送失败'
        print('验证码发送失败')
    else:
        static = '验证码发送成功'
        print('验证码发送成功')
    return HttpResponse(static)


@require_http_methods(["GET"])
@login_required
def search(request):
    username = request.GET.get("username")
    try:
        his_info = serializers.serialize('json', UserProfile.objects.filter(name=username))
        err_code = 200
        result = {
            'err_code': err_code,
            "msg": "这是" + username + "的信息",
            "data": json.loads(his_info),
        }
        return JsonResponse(result, status=err_code)
    except Exception as e:
        err_code = 400
        result = {
            "error_code": err_code,
            "msg": str(e)
        }
        return JsonResponse(result, status=err_code)


@require_http_methods(["POST"])
@login_required
def img_uploader(request):

    try:
        img = request.FILES['file']
        print(img)
        print("gauiawhil")
        f = open('./media/photo/' + img.name, 'wb+')
        f.write(img.read())
        print("写入数据")
        f.close()
        res = {
            'code': 200,
            'message': 'upload success'
        }
        return JsonResponse(res, status=200)
    except Exception as e:
        print(e)
        res = {
            'code': 500,
            'message': 'Count problems'
        }
        return JsonResponse(res, status=500)


'''@login_required
@require_http_methods(["GET"])
def my_page(request):
    my_id'''
