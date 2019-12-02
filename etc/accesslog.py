# -*- coding: utf-8 -*-
# @Time    : 2019/12/1 13:53
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : accesslog.py
# @Software: PyCharm
import pymysql

from webanalysis.models import AccessLog

params = {
    'host' : '127.0.0.1',
    'port' : 3306,
    'db' : 'cmdb_kk',
    'user' : 'root',
    'passwd' : 'Admin123!',
    'charset' : 'utf8'
}
SQL = 'INSERT INTO webanalysis_accesslog(hostname,log_recording, cache_server, user_ip, user_request_ip,http_methond,http_url,http_status_code,cache_server_port,cache_to_user_flow,back_to_source_ip) VALUES(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s);'
if __name__ == '__main__':
    path='access'
    with open(path,'rt') as fhandler:
        # cursor = connection.cursor()
        cnt = 0
        for line in fhandler:
            nodes = line.split('|')
            #log_recording:   日志记录时间
            log = AccessLog()
            log.file_id = file
            args = (
                nodes[63],nodes[0],nodes[1],nodes[2],
                nodes[3], nodes[4], nodes[9], nodes[11],
                nodes[13], nodes[14], nodes[20],
            )
            print(SQL)
            print(args)
            cursor.execute()
            # cursor.execute(SQL, args)
            db.commit
            cursor.close()
            db.close()
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
