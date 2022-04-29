from django.urls import path

from . import views

app_name = 'fans'

urlpatterns = [
    path('following/', views.following),
    path('following_delete/', views.following_delete),
    path('fans/', views.fans),
    path('search/', views.search),
    path('group/', views.group),
    path('group_edit/', views.group_edit),
    path('following_group_change/', views.following_group_change),
    path('group_delete/', views.group_delete)
]
