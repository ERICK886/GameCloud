import sys

import django
from django.http import JsonResponse

from backend.func.token import check_token, check_admin
from backend.models import User, Tag, Category, Resource


def admin_system_info(request):
    """
    管理员获取系统信息
    :param request:
    :return:
    """
    token = request.headers.get('Authorization')
    payload, flag = check_token(token)
    if not flag:
        return JsonResponse({'code': 401, 'msg': 'token认证失败'})
    if not check_admin(token):
        return JsonResponse({'code': 401, 'msg': '权限不足'})
    if request.method == 'POST':
        python_version = sys.version
        # 获取当前django版本
        django_version = django.get_version()
        users = User.objects.all().count()
        tags = Tag.objects.all().count()
        categories = Category.objects.all().count()
        resources = Resource.objects.all().count()
        return JsonResponse({'code': 200, 'msg': 'success', 'data': {
            'python_version': python_version.split(' ')[0],
            'django_version': django_version,
            'users': users,
            'tags': tags,
            'categories': categories,
            'resources': resources
        }})
    else:
        return JsonResponse({'code': 405, 'msg': '请求方法错误'})
