import datetime
import json

from django.http import JsonResponse

from backend.func.token import check_token, check_admin
from backend.models import Category, Resource


def admin_category_get(request):
    """
    管理员获取分类
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
        data = json.loads(request.body.decode('utf-8'))
        if data.get('kwd'):
            kwd = data.get('kwd')
        else:
            kwd = ''
        if data.get('order'):
            order = data.get('order')
        else:
            order = 'asc'
        if data.get('orderby'):
            orderby = data.get('orderby')
        else:
            orderby = 'id'

        if order == 'asc':
            order = ''
        else:
            order = '-'
        category_list = []
        categories = Category.objects.filter(name__icontains=kwd).order_by(order + orderby)
        for category in categories:
            category_list.append({
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
                'description': category.description,
                'status': category.status,
                'create_time': datetime.datetime.strftime(category.create_time, '%Y-%m-%d %H:%M:%S'),
                'update_time': datetime.datetime.strftime(category.update_time, '%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'code': 200, 'msg': '获取成功', 'data': category_list})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_category_add(request):
    """
    管理员添加分类
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
        try:
            data = json.loads(request.body.decode('utf-8'))
            if not data.get('name'):
                return JsonResponse({'code': 400, 'msg': '分类名不能为空'})
            if not data.get('slug'):
                return JsonResponse({'code': 400, 'msg': '分类别名不能为空'})
            Category.objects.create(name=data.get('name'), slug=data.get('slug'))
            return JsonResponse({'code': 200, 'msg': '添加成功'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_category_edit(request):
    """
    管理员编辑分类
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
        try:
            data = json.loads(request.body.decode('utf-8'))
            if not data.get('name'):
                return JsonResponse({'code': 400, 'msg': '分类名不能为空'})
            if not data.get('slug'):
                return JsonResponse({'code': 400, 'msg': '分类别名不能为空'})
            category = Category.objects.get(id=data.get('id'))
            if category.id == 1:
                return JsonResponse({'code': 400, 'msg': '默认分类不能编辑'})
            if data.get('description'):
                category.description = data.get('description')
            else:
                category.description = ''
            category.name = data.get('name')
            category.slug = data.get('slug')
            category.status = data.get('status')
            category.save()
            return JsonResponse({'code': 200, 'msg': '修改成功'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_category_delete(request):
    """
    管理员删除分类
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
        try:
            data = json.loads(request.body.decode('utf-8'))
            if data.get('categoryId'):
                if data.get('categoryId') == 1:
                    return JsonResponse({'code': 400, 'msg': '默认分类不能删除'})
                del_category = Category.objects.get(id=data.get('categoryId'))
                resource = Resource.objects.get(category=del_category)
                resource.category = Category.objects.get(id=1)
                resource.save()
                del_category.delete()
                return JsonResponse({'code': 200, 'msg': '删除成功'})
            else:
                return JsonResponse({'code': 400, 'msg': '分类id不能为空'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
