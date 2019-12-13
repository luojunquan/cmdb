# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 9:55
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : v1.py
# @Software: PyCharm
import json
from asset.models import Host,Resource
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

class APIView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(APIView,self).dispatch(request,*args,**kwargs)

    def get_json(self):
        try:
            return json.loads(self.request.body)
        except BaseException as e:
            return {}

    def response(self,result=None,code=200,errors={}):
        return JsonResponse({'code':code,'result':result,'errors':errors})

class ClientView(APIView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ClientView,self).dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        _ip = kwargs.get('ip','')
        _json = self.get_json()
        host = Host.create_or_replace(_ip,_json.get('name',''),_json.get('mac', ''),_json.get('os',''),
                                      _json.get('arch',''),_json.get('mem',0), _json.get('cpu',0),_json.get('disk','{}'))
        print(host)
        return self.response(host.as_dict())

class ResourceView(APIView):
    def post(self,request,*args,**kwargs):
        _ip = kwargs.get('ip','')
        _json = self.get_json()
        Resource.create_obj(_ip,_json.get('cpu'),_json.get('mem'))
        return self.response()
