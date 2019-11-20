#encoding: utf-8

import hashlib
from django.db import models


def encrypt_password(password):
    if not isinstance(password, bytes):
        password = str(password).encode()

    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()


class User(models.Model):
    name = models.CharField(max_length=32, null=False, default='') # => name varchar(32) not null default ''
    password = models.CharField(max_length=512, null=False, default='')
    age = models.IntegerField(null=False, default=0) # => age int not null default 0
    tel = models.CharField(max_length=32, null=False, default='')
    sex = models.BooleanField(null=False, default=True) 
    create_time = models.DateTimeField(null=False)
    addr = models.CharField(max_length=120, null=False, default='')


    @classmethod
    def delete_by_id(cls, id):
        return cls.objects.filter(id=id).delete()
        

    def as_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'age' : self.age,
            'tel' : self.tel,
            'sex' : self.sex
        }