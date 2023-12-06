from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('input/upload-tweet/', views.upload_tweet, name='upload_tweet'),
    path('input/list-tweet/', views.list_tweet, name='list_tweet'),
    path('delete/list-tweet/<int:idt>/', views.delete_tweet, name='delete_tweet'),
    path('task/input/prepro/', views.prepro, name='prepro'),
]