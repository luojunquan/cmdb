# -*- coding: utf-8 -*-
# @Time    : 2019/12/1 11:41
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : todb.py
# @Software: PyCharm
import json
import time
import datetime

from django.core.management import BaseCommand
from  django.conf import settings
import os

from webanalysis.models import AccessLog


class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        path = os.path.join(settings.BASE_DIR,'media','notices')
        while True:
            lists = os.listdir(path)
            for filename in lists:
                notice = None
                path_notice = os.path.join(path,filename)
                with open(path_notice,'rt') as fhandler:
                    notice = json.loads(fhandler.read())
                try:
                    self.parse(notice)
                except BaseException as e:
                    print(e)
                os.unlink(path_notice)
            time.sleep(5)

    def parse(self, notice):
        file_id = notice['id']
        path = notice['path']
        UTC_FORMAT = "%Y%m%dT%H%M%SZ"
        with open(path, 'rt') as fhandler:
            # print(fhandler)
            for line in fhandler:
                try:
                    nodes = line.split('|')
                    log = AccessLog()
                    log.file_id = file_id
                    log.hostname = nodes[63]
                    #进行UTC时间的转换，因为日志的时间格式是UTC格式，
                    log_recording = datetime.datetime.strptime(nodes[0],UTC_FORMAT)
                    localtime = log_recording + datetime.timedelta(hours=8)
                    log.log_recording = localtime.strftime('%Y-%m-%d %H:%M:%S')
                    log.cache_server = nodes[1]
                    log.user_ip = nodes[2]
                    log.user_request_ip = nodes[3]
                    log.http_methond = nodes[4]
                    log.http_request_host = nodes[6]
                    log.http_url = nodes[9]
                    log.http_status_code = nodes[11]
                    log.cache_server_port = nodes[13]
                    log.cache_to_user_flow = nodes[14]
                    log.back_to_source_ip = nodes[20]
                    log.save()
                except BaseException as e:
                    print(e)
        print('parse over:{0}'.format(path))
                # args = (
                #     nodes[63], nodes[0], nodes[1], nodes[2],
                #     nodes[3], nodes[4], nodes[9], nodes[11],
                #     nodes[13], nodes[14], nodes[20],
                # )
                # print('log_recording:::::'+nodes[0])
                # #cache_server:   缓存服务器IP地址
                # print('cache_server:::::'+nodes[1])
                # #user_ip:   用户IP地址发起请求的用户的源IP地址
                # print('user_ip:::::'+nodes[2])
                # #user_request_ip：   用户请求的服务器IP地址
                # print('user_request_ip:::::'+nodes[3])
                # #http_methond:      HTTP请求的Method字段内容
                # print('http_methond:::::'+nodes[4])
                # #http_url:     HTTP请求的Uri字段内容
                # print('http_url:::::'+nodes[9])
                # #http_status_code:      缓存设备向用户返回的HTTP应答的Status-code字段内容
                # print('http_status_code:::::'+nodes[11])
                # #cache_server_port:      程序为用户提供服务的端口号,缓存服务器端口
                # print('cache_server_port:::::'+nodes[13])
                # # cache_to_user_flow:   本次请求缓存向用户吐出的流量
                # print('cache_to_user_flow:::::'+nodes[14])
                # # back_to_source_ip:    回源IP
                # print('back_to_source_ip:::::'+nodes[20])
                # # hostname:   主机名
                # print('hostname:::::'+nodes[63])
                #