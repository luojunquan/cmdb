#encoding: utf-8
from django.utils import timezone

from .models import Host

class AssetValidator():

    @classmethod
    def valid_update(cls, params):
        is_valid = True
        host = None
        errors = {}
        try:
            host = Host.objects.get(pk=params.get('id', '').strip())
        except BaseException as e:
            errors['id'] = '服务器信息不存在'
            is_valid = False
            return is_valid, host, errors
        host.os = params.get('os','')
        host.name = params.get('name','')
        return is_valid, host, errors

    @classmethod
    def valid_create(cls, params):
        is_valid = True
        host = Host()
        errors = {}
        host.name = params.get('name', '').strip()
        host.os = params.get('os','').strip()
        return is_valid, host, errors
