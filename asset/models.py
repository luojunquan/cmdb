#encoding: utf-8

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime

class Host(models.Model):
    name = models.CharField(max_length=128, null=False, default='')
    ip = models.GenericIPAddressField(null=False, default='0.0.0.0')
    mac = models.CharField(max_length=32, null=False, default='')
    os = models.CharField(max_length=64, null=False, default='')
    arch = models.CharField(max_length=16, null=False, default='')
    mem = models.BigIntegerField(null=False, default=0)
    cpu = models.IntegerField(null=False, default=0)
    disk = models.CharField(max_length=512, null=False, default='{}')

    sn = models.CharField(max_length=128, null=False, default='')
    user = models.CharField(max_length=128, null=False, default='')
    remark = models.TextField(null=False, default='')
    purchase_time = models.DateTimeField(null=False)
    over_insurance_time = models.DateTimeField(null=False)

    created_time = models.DateTimeField(null=False, auto_now_add=True)
    last_time = models.DateTimeField(null=False)

    @classmethod
    def create_or_replace(cls, ip, name, mac, os, arch, mem, cpu, disk):
        obj = None
        try:
            obj = cls.objects.get(ip=ip)
        except ObjectDoesNotExist as e:
            obj = cls()
            obj.ip = ip
            obj.purchase_time = timezone.now()
            obj.over_insurance_time = timezone.now()

        obj.name = name
        obj.mac = mac
        obj.os = os
        obj.arch = arch
        obj.mem = mem
        obj.cpu = cpu
        obj.disk = disk

        obj.last_time = timezone.now()
        obj.save()
        return obj

    def as_dict(self):
        return {
            'id':self.id,
            'ip':self.ip,
            'name':self.name,
            'os':self.os,
            'cpu':self.cpu,
            'mac': self.mac,
            'arch':self.arch,
            'mem':self.mem,
            'disk':self.disk,
            'purchase_time':self.purchase_time,
            'over_insurance_time':self.over_insurance_time,
            'created_time':self.created_time,
            'last_time':self.last_time,
        }
        # rt = {}
        # for k, v in self.__dict__.items():
        #     if isinstance(v, (int, float, bool, str, datetime.datetime)):
        #         rt[k] = v
        # return rt


class Resource(models.Model):
    ip = models.GenericIPAddressField(null=False, default='0.0.0.0')
    cpu = models.FloatField(null=False, default=0)
    mem = models.FloatField(null=False, default=0)
    created_time = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_obj(cls, ip, cpu, mem):
        resource = Resource()
        resource.ip = ip
        resource.cpu = cpu
        resource.mem = mem
        resource.save()
        return resource