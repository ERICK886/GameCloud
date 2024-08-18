import json

from django.http import JsonResponse

from backend.func.token import *
from backend.models import User


def admin_sign_in(request):
    """
    管理员登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.password == password:
                token = create_token(user)
                return JsonResponse({'code': 200, 'msg': '登录成功', 'data': {'token': token, 'admin': user.is_admin}})
            else:
                return JsonResponse({'code': 400, 'msg': '密码错误'})
        else:
            return JsonResponse({'code': 400, 'msg': '用户不存在'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_sign_up(request):
    """
    管理员注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        password = data.get('password')
        nickname = data.get('nickname')
        if User.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'msg': '用户已存在'})
        else:
            user = User.objects.create(username=username, password=password, nickname=nickname)
            token = create_token(user)
            return JsonResponse({'code': 200, 'msg': '注册成功', 'data': {'token': token}})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_check_right(request):
    """
    检查管理员权限
    :param request:
    :return:
    """
    token = request.headers.get('Authorization')
    payload, flag = check_token(token)
    if request.method == 'POST':
        if not flag:
            return JsonResponse({'code': 401, 'msg': 'token认证失败'})
        if not check_admin(token):
            return JsonResponse({'code': 401, 'msg': '您不是管理员'})
        return JsonResponse({'code': 200, 'msg': '认证成功'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
