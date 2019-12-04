#encoding: utf-8
from django.urls import path
from . import views

app_name = 'webanalysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload',views.upload,name='upload'),
    path('dist_status_code/',views.dist_status_code,name='dist_status_code'),
    path('trend_visit/',views.trend_visit,name='trend_visit'),
    path('request_user_ip/',views.request_user_ip,name='request_user_ip'),
    path('http_request_user_host/',views.http_request_user_host,name='http_request_user_host'),
]