# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 10:18
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : host.py
# @Software: PyCharm

from .base import BaseThread
from utils import sysutil
class Host(BaseThread):
    def __init__(self,queue):
        super(Host, self).__init__('host',5,queue)

    def make_event(self):
        return {
            'type' : self._type,
            'url' : 'client/{0}/'.format(sysutil.get_addr()),
            'msg' : {
                'name' : sysutil.get_name(),
                'mac' : sysutil.get_mac(),
                'os' : sysutil.get_os(),
                'arch' : sysutil.get_arch(),
                'mem' : sysutil.get_mem(),
                'cpu' : sysutil.get_cpu(),
                'disk' : sysutil.get_disk()
            }
        }