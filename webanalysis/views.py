import json
import time

import os

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from functools import wraps

from .models import AccessLogFile, AccessLog

def login_required(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.session.get('user') is None:
            #判断是是不是ajax请求
            if request.is_ajax():
                return JsonResponse({'code':403,'result':[]})
            return redirect('user:login')
        return func(request,*args,**kwargs)
    return wrapper

@login_required
def index(request):
    files = AccessLogFile.objects.filter(status=0).order_by('-created_time')[:10]
    return render(request, 'webanalysis/index.html',{"files":files})

@login_required
#上传文件
def  upload(request):
    #input定义了name为log
    log = request.FILES.get('log',None)
    if log:
        path = os.path.join(settings.BASE_DIR,'media','uploads',str(time.time()))
        fhander = open(path,'wb')
        #将文件内容chunks读取到指定的文件中
        for chunk in log.chunks():
            fhander.write(chunk)
        fhander.close()
        obj = AccessLogFile(name=log.name,path=path)
        obj.save()
        path=os.path.join(settings.BASE_DIR,'media','notices',str(time.time()))
        with open(path,'w') as fhander:
            fhander.write(json.dumps({'id':obj.id,'path':obj.path}))
    return HttpResponse('upload Success')

@login_required
#状态码饼状图
def dist_status_code(request):
    legend,series = AccessLog.dist_status_code(request.GET.get('id',0))
    return JsonResponse({'code':200,'result':{'legend':legend,'series':series}})

@login_required
def trend_visit(request):
    xAxis,series = AccessLog.trend_visit(request.GET.get('id',0))
    return JsonResponse({'code':200,'result':{'xAxis':xAxis,'series':series}})

@login_required
def request_user_ip(request):
    xAxis,series = AccessLog.request_user_ip(request.GET.get('id',0))
    return JsonResponse({'code':200,'result':{'xAxis':xAxis,'series':series}})

@login_required
def http_request_user_host(request):
    yAxis,series = AccessLog.http_request_user_host(request.GET.get('id',0))
    return JsonResponse({'code':200,'result':{'yAxis':yAxis,'series':series}})