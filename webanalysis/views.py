import json
import time

import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
from .models import AccessLogFile


def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    return render(request, 'webanalysis/index.html')

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
