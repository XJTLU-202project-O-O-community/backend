from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('personal/', views.personal_page),
    path('upload_photo/', views.photo_upload),
]
