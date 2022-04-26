from django.urls import path

from . import views

app_name = 'posting'

urlpatterns = [
    path('momments/', views.get_posts),
    path('moment/', views.single_post),
    path('delete/', views.delete),
    path('edit/', views.edit),
    path('imgs/', views.img_uploader),
    path('view_comment/',views.get_moments),
    path('newcomment/',views.post_moment),

]