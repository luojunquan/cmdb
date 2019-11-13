#encoding: utf-8
from django.urls import path

from . import views

app_name = 'asset'
urlpatterns = [
    path('', views.index, name='index'),
    path('list/ajax/', views.list_ajax, name='list_ajax'),
    path('delete/ajax/', views.delete_ajax, name='delete_ajax'),
    path('get/ajax/', views.get_ajax, name='get_ajax'),
    path('resource/ajax/', views.resource_ajax, name='resource_ajax'),
]