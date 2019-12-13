# -*- coding: utf-8 -*-
# @Time    : 2019/12/13 17:04
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : resource.py
# @Software: PyCharm
from .base import BaseThread
from utils import sysutil

class Resource(BaseThread):

    def __init__(self, config):
        super(Resource, self).__init__('resource', 5, config)

    def make_event(self):
        return {
            'type' : self._type,
            'url' : 'client/{0}/resource/'.format(sysutil.get_addr()),
            'msg' : {
                'cpu' : sysutil.get_cpu_precent(),
                'mem' : sysutil.get_mem_precent(),
            }
        }
