from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),
    path('message/', views.send_message),
    path('message/<str:message_id>/', views.receive_msg)
]