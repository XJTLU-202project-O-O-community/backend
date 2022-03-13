from django.urls import path

from . import views

app_name = 'posting'

urlpatterns = [
    path('momments/', views.get_posts),
    path('momment/', views.single_post),

]