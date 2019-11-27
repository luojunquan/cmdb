#encoding: utf-8

from datetime import timedelta
import time

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from  .validators import AssetValidator
from .models import Host, Resource

def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    return render(request, 'asset/index.html')


def list_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})
    result= [host.as_dict() for host in Host.objects.all()]
    return JsonResponse({'code' : 200, 'result' : result})

def delete_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})
    _id = request.GET.get('id', 0)
    try:
        Host.objects.get(pk=_id).delete()
    except ObjectDoesNotExist as e:
        pass
    return JsonResponse({'code' : 200})

#点击编辑按钮时获取服务器信息
def get_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403, 'result' : []})
    _id = request.GET.get('id', 0)
    try:
        host = Host.objects.get(pk=_id)
        return JsonResponse({'code' : 200, 'result' : host.as_dict() })
    except ObjectDoesNotExist as e:
        return JsonResponse({'code' : 400})

#dialog编辑完成以后进行更新提交
def update_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403})
    print(request.POST)
    is_valid, asset, errors = AssetValidator.valid_update(request.POST)
    if is_valid:
        asset.save()
        return JsonResponse({'code' : 200})
    else:
        return JsonResponse({'code' : 400, 'errors' : errors})

#echarts监控传给前台的数据
def resource_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code': 403, 'result': []})
    try:
        _id = request.GET.get('id', 0)
        host = Host.objects.get(pk=_id)
        end_time = timezone.now()
        #获取最近6小时的数据
        start_time = end_time - timedelta(hours=6)
        # order_by进行排序，升序
        resources = Resource.objects.filter(ip=host.ip, created_time__gte=start_time).order_by('created_time')
        # 转换成key和value===》time:{cpu、内存}===》{'2019-11-27 15:48': {'cpu': 7.0, 'mem': 67.71}}
        tmp_resources = {}
        for resource in resources:
            tmp_resources[resource.created_time.strftime('%Y-%m-%d %H:%M')] = {'cpu': resource.cpu, 'mem': resource.mem}
        xAxis = []
        CPU_datas = []
        MEM_datas = []

        while start_time <= end_time:
            key = start_time.strftime('%Y-%m-%d %H:%M')
            resource = tmp_resources.get(key, {})
            xAxis.append(key)
            CPU_datas.append(resource.get('cpu', 0))
            MEM_datas.append(resource.get('mem', 0))
            # X轴每5分钟显示一次数据
            start_time += timedelta(minutes=5)

        # for resource in resources:
        #     xAxis.append(time.strftime('%Y-%m-%d %H:%M', time.localtime(resource.created_time.timestamp())))
        #     CPU_datas.append(resource.cpu)
        #     MEM_datas.append(resource.mem)

        return JsonResponse({'code': 200, 'result': {'xAxis': xAxis, 'CPU_datas': CPU_datas, 'MEM_datas': MEM_datas}})
    except ObjectDoesNotExist as e:
        return JsonResponse({'code': 400})