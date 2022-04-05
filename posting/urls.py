from django.urls import path

from . import views

app_name = 'posting'

urlpatterns = [
    path('momments/', views.get_posts),
    path('moment/', views.single_post),
    path('delete/', views.delete),
    path('edit/', views.edit),

]