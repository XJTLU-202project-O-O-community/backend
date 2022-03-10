from django.urls import path

from . import views

app_name = 'fans'

urlpatterns = [
    path('following/', views.following),
    path('following_delete/', views.following_delete),
    path('fans/', views.fans),
    path('search/', views.search),
]