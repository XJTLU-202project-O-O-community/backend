from django.urls import path
from mysite import settings
from . import views
from django.views.static import serve

app_name = 'user'

urlpatterns = [

    # 注册页面
    path('register/', views.regist),
    # 密码登陆页面
    path('login/', views.inlog),
    #邮箱登陆界面
    path('email_login/', views.email_inlog),
    # 登出页面
    path('logout/', views.outlog),
    # 他人信息页面
    path('currentUser/', views.personal_page),
    #本人个人界面
    path('my/', views.my_page),
    #发送验证码
    path('send_email/', views.send_code),
    # 修改密码页面
    path('change_pwd/', views.change_pwd),
    # 修改个人信息页面
    path('personal_info_edit/', views.edit),
    #图片上传
    path('images/', views.img_uploader),
    # 搜索用户
    path('search/', views.search),
]
