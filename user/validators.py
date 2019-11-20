#encoding: utf-8
from django.utils import timezone

from .models import User, encrypt_password

class Validator(object):

    @classmethod
    def is_integer(cls, value):
        try:
            int(value)
            return True
        except BaseException as e:
            return False


class UserValidator(Validator):

    @classmethod
    def valid_login(cls, name, password):
        user = None
        try:
            user = User.objects.get(name=name)
        except BaseException as e:
            pass

        if user is None:
            return None

        if user.password == encrypt_password(password):
            return user
        
        return None
        
    @classmethod
    def valid_name_unique(cls, name, id=None):
        user = None
        try:
            user = User.objects.get(name=name)
        except BaseException as e:
            pass

        if user is None:
            return True
        else:
            return str(user.id) == str(id)

    @classmethod
    def valid_update(cls, params):
        is_valid = True
        user = None
        errors = {}
        try:
            user = User.objects.get(pk=params.get('id', '').strip())
        except BaseException as e:
            errors['id'] = '用户信息不存在'
            is_valid = False
            return is_valid, user, errors


        name = params.get('name', '').strip()

        if name == '':
            errors['name'] = '用户名不能为空'
            is_valid = False
        elif not cls.valid_name_unique(name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False
        else:
            user.name = name

        age = params.get('age', '0').strip()
        if not cls.is_integer(age):
            errors['age'] = '年龄格式错误'
            is_valid = False
        else:
            user.age = int(age)

        user.tel = params.get('tel', '')
        user.sex = int(params.get('sex', '0'))

        return is_valid, user, errors

    @classmethod
    def valid_create(cls, params):
        is_valid = True
        user = User()
        errors = {}

        user.name = params.get('name', '').strip()


        if user.name == '':
            is_valid = False
            errors['name'] = '用户名不能为空'
        else:
            try:
                User.objects.get(user.name)
                is_valid = False
                errors['name'] = '用户名重复'
            except BaseException as e:
                pass

        user.age = params.get('age', '0').strip()
        if not user.age.isdigit():
            errors['age'] = '年龄格式错误'
            is_valid = False

        user.tel = params.get('tel', '')
        user.sex = int(params.get('sex', '0'))
        user.password = params.get('password', '').strip()

        if user.password == '' or params.get('other_password') != user.password:
            is_valid = False
            errors['password'] = '密码不能为空, 且两次输入密码必须相同'
        else:
            user.password = encrypt_password(user.password)
        
        user.create_time = timezone.now()
        return is_valid, user, errors
