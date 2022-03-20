
from django.urls import path
from mysite import settings
from . import views
from django.views.static import serve
from django.conf.urls.static import static
app_name = 'user'

urlpatterns = [
    #注册页面
    path('register/', views.register),
    #登陆页面
    path('login/', views.login),
    #个人信息页面
    path('personal_info/', views.personal_page),
    #这个是用来测试的，别管
    path('get_photo/', views.photo_upload),
    #修改密码页面
    path('change_pwd/', views.change_pwd),
    #修改个人信息页面
    path('personal_info_edit/', views.edit),
    path(r'^client_header/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
