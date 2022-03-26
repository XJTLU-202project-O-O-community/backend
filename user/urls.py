from django.urls import path
from mysite import settings
from . import views
from django.views.static import serve

app_name = 'user'

urlpatterns = [

    # 注册页面
    path('register/', views.regist),
    # 登陆页面
    path('login/', views.inlog),
    # 登出页面
    path('logout/', views.outlog),
    # 个人信息页面
    path('currentUser/', views.personal_page),
    # 这个是用来测试的，别管
    path('get_photo/', views.photo_upload),
    # 修改密码页面
    path('change_pwd/', views.change_pwd),
    # 修改个人信息页面
    path('personal_info_edit/', views.edit),
]
