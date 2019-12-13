# -*- coding: utf-8 -*-
# @Time    : 2019/12/12 16:49
# @Author  : Luoxiaojian
# @Email   : ljq906416@gmail.com
# @File    : agentd.py
# @Software: PyCharm

import argparse
import logging
import time
from queue import Queue

import os

from plugins.ens import ENS
from plugins.host import Host
from gconf import Config

from plugins.resource import Resource

logger = logging.getLogger(__name__)

def main(config):
    ths = []
    ths.append(ENS(config))
    ths.append(Host(config))
    ths.append(Resource(config))
    for th in ths:
        th.start()

    while True:
        time.sleep(3)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H','--host',type=str,default='127.0.0.1',help='Server Addr')
    parser.add_argument('-P', '--port', type=int, default=8888, help='Server Port')
    parser.add_argument('-V', '--verbose', action='store_true', help='DEBUG INFO')

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    fmt = '%(asctime)s - %(name)s - %(levelname)s:%(message)s'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pid = os.getpid()

    logging.basicConfig(
        level = level,
        format = fmt,
        filemode = 'w',
        filename = os.path.join(base_dir,'logs','agentd.log')
    )
    logger.info('agent started: [%s]',pid)
    config = Config
    setattr(config,'SERVER','{0}:{1}'.format(args.host,args.port))
    setattr(config,'QUEUE',Queue())

    main(config)
