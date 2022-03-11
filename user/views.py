from django.shortcuts import render
from django.http import JsonResponse
from user.models import UserAccount
import hashlib


# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        md5 = hashlib.md5()
        password = password.encode(encoding='utf-8')
        md5.update(password)
        password = md5.hexdigest()
        if UserAccount.objects.filter(username=username).count() == 0:
            err_code = 200
            UserAccount.objects.create(username=username, password=password, email=email)
            result = {
                "err_code": err_code,
                "msg": "创建成功",
                "username": username
            }

        else:
            err_code = 400
            result = {
                "err_code": err_code,
                "msg": "duplicated username",
                "username": username
            }
        return JsonResponse(result, status=err_code)


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            account = UserAccount.objects.get(username=username)
            db_username = account.username
            db_password = account.password
            md5 = hashlib.md5()
            password = password.encode(encoding='utf-8')
            md5.update(password)
            password = md5.hexdigest()
            if db_username == username and password == db_password:
                err_code = 200
                result = {
                    "error_code": err_code,
                    "msg": 'Login Successfully',
                    "username": username
                }
            else:
                err_code = 400
                result = {
                    "err_code": err_code,
                    "msg": "wrong password",
                    "username": username
                }
            return JsonResponse(result, status=err_code)
        except Exception as e:
            print(e)
            err_code = 400
            result = {
                "err_code": err_code,
                "msg": "the username does not exist",
                "username": username
            }
            return JsonResponse(result, status=err_code)
