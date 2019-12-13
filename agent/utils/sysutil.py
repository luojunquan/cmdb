# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 10:48
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : sysutil.py
# @Software: PyCharm
import platform
import socket
import uuid

import psutil


def get_name():
    return socket.gethostname()
def get_addr():
    return socket.gethostbyname(socket.gethostname())
def get_mac():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])
def get_arch():
    return platform.architecture()[0]
def get_cpu():
    return psutil.cpu_count()
def get_mem():
    return psutil.virtual_memory().total
def get_disk():
    disk = []
    for part in psutil.disk_partitions():
        disk.append({'name': part.device,'total':psutil.disk_usage(part.device).total})
    return disk
def get_cpu_precent():
    return psutil.cpu_percent()
def get_mem_precent():
    return psutil.virtual_memory().percent
def get_os():
    return platform.platform()
if __name__ == '__main__':
    print(get_addr())
    print(get_arch())
    print(get_cpu())
    print(get_cpu_precent())
    print(get_disk())
    print(get_mac())
    print(get_mem_precent())