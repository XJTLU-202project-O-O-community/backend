from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('messagelist/', views.messagelist),
    path('history/', views.history)
]