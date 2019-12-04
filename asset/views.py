#encoding: utf-8
import smtplib
from datetime import timedelta
import time
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from django.db import connection
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

#告警
def get_alarm(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403})
    try:
        _id = request.GET.get('id', 0)
        host = Host.objects.get(pk=_id)
        alarm_ip = host.ip
        cursor = connection.cursor()
        #当前时间60分钟之内cpu使用率超过6%的次数超过2次，即产生报警，将当前时间和ip反馈到前端
        alarm_ip_time=cursor.execute('select ip,count(*) from asset_resource where (created_time between date_add(now(), interval - 60 minute) and  now()) and cpu>6 and ip=%s group by ip having count(*) >2',(alarm_ip,))
        ret = cursor.fetchall()
        now_time = timezone.now().strftime('%Y-%m-%d %H:%M')
        if alarm_ip_time == 0:
            return JsonResponse({'code': 303})
        else:
            # for ip in ret:
            #     sendEmail('服务器'+ip[0]+'连续30分钟CPU使用率超过％６，请尽快处理')
            return JsonResponse({'code': 200, 'result': {'ip': [ip[0] for ip in ret], 'cnt': [cnt[1] for cnt in ret],'now_time': now_time}})
    except ObjectDoesNotExist as e:
        return JsonResponse({'code' : 400})

#发送邮件
def sendEmail(content):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # SMTP服务器
    mail_user = "1406221797@qq.com"  # 用户名
    mail_pass = "*******"  # 授权密码，非登录密码
    sender = '1406221797@qq.com'  # 发件人邮箱(最好写全, 不然会失败)
    receivers = ['luojunquan_gz@139.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    title = '服务器告警邮件'  # 邮件主题
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)