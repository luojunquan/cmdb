#encoding: utf-8
from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import User
from .validators import UserValidator

def index(request):
    if not request.session.get('user'):
        return redirect('user:login')

    return render(request, 'user/index.html', {
        'users' : User.objects.all()
    })


def login(request):
    if 'GET' == request.method:
        return render(request, 'user/login.html')
    else:
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = UserValidator.valid_login(name, password)
        if user:
            request.session['user'] = user.as_dict()
            return redirect('user:index') 
        else:
            return render(request, 'user/login.html', {
                'name': name,
                'errors' : {'default' : '用户名或密码错误'}
            })


def logout(request):
    request.session.flush()
    return redirect('user:login')


def delete(request):
    if not request.session.get('user'):
        return redirect('user:login')

    uid = request.GET.get('uid', '')
    User.delete_by_id(uid)

    return redirect('user:index')


def view(request):
    if not request.session.get('user'):
        return redirect('user:login')

    uid = request.GET.get('uid', '')
    return render(request, 'user/view.html', {
        'user' : User.objects.get(pk=uid)
    })


def update(request):
    if not request.session.get('user'):
        return redirect('user:login')

    is_valid, user, errors = UserValidator.valid_update(request.POST)
    if is_valid:
        user.save()
        return redirect('user:index')
    else:
        return render(request, 'user/view.html', {
            'user' : user,
            'errors' : errors,
            })


def create(request):
    if not request.session.get('user'):
        return redirect('user:login')

    if 'GET' == request.method:
        return render(request, 'user/create.html')

    else:
        is_valid, user, errors = UserValidator.valid_create(request.POST)
        if is_valid:
            user.save()
            return redirect('user:index')
        else:
            return render(request, 'user/create.html', {
                'user' : user,
                'errors' : errors,
                })

'''
{
    code: 200(创建成功), 400(数据验证失败), 403(用户未登陆)
    result: {}
    text: ''
    errors: 
}
'''
def create_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403})

    is_valid, user, errors = UserValidator.valid_create(request.POST)
    if is_valid:
        user.save()
        return JsonResponse({'code' : 200})
    else:
        return JsonResponse({'code' : 400, 'errors' : errors})


def delete_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403})

    uid = request.GET.get('id', '')
    User.delete_by_id(uid)

    return JsonResponse({'code' : 200})


def get_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403})
    uid = request.GET.get('id', '')
    try:
        user = User.objects.get(id=uid)
        return JsonResponse({'code' : 200, 'result' : user.as_dict() })
    except ObjectDoesNotExist as e:
        return JsonResponse({'code' : 400, 'errors' : {'id' : '操作对象不存在'}})


def update_ajax(request):
    if not request.session.get('user'):
        return JsonResponse({'code' : 403})
    is_valid, user, errors = UserValidator.valid_update(request.POST)
    if is_valid:
        user.save()
        return JsonResponse({'code' : 200})
    else:
        return JsonResponse({'code' : 400, 'errors' : errors})