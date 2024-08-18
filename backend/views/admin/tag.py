import datetime
import json

from django.http import JsonResponse

from backend.func.token import check_token, check_admin
from backend.models import Tag


def admin_tag_get(request):
    """
    管理员获取标签
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
        tag_list = []
        tags = Tag.objects.filter(name__icontains=kwd).order_by(order + orderby)
        for tag in tags:
            tag_list.append({
                'id': tag.id,
                'name': tag.name,
                'slug': tag.slug,
                'description': tag.description,
                'status': tag.status,
                'create_time': datetime.datetime.strftime(tag.create_time, '%Y-%m-%d %H:%M:%S'),
                'update_time': datetime.datetime.strftime(tag.update_time, '%Y-%m-%d %H:%M:%S'),
            })
        return JsonResponse({'code': 200, 'msg': '获取成功', 'data': tag_list})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_tag_add(request):
    """
    管理员添加标签
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
                return JsonResponse({'code': 400, 'msg': '标签名不能为空'})
            if not data.get('slug'):
                return JsonResponse({'code': 400, 'msg': '标签别名不能为空'})
            if Tag.objects.filter(name=data.get('name')).exists():
                return JsonResponse({'code': 400, 'msg': '标签名已存在'})

            Tag.objects.create(name=data.get('name'), slug=data.get('slug'), description=data.get('description'),
                               status=data.get('status'))
            return JsonResponse({'code': 200, 'msg': '添加成功'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_tag_edit(request):
    """
    管理员编辑标签
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
            if not data.get('id'):
                return JsonResponse({'code': 400, 'msg': '标签id不能为空'})
            if not data.get('name'):
                return JsonResponse({'code': 400, 'msg': '标签名不能为空'})
            if not data.get('slug'):
                return JsonResponse({'code': 400, 'msg': '标签别名不能为空'})

            tag = Tag.objects.get(id=data.get('id'))
            if tag.id == 1:
                return JsonResponse({'code': 400, 'msg': '默认标签不能编辑'})
            if data.get('description'):
                tag.description = data.get('description')
            else:
                tag.description = ''
            tag.name = data.get('name')
            tag.slug = data.get('slug')
            tag.status = data.get('status')
            tag.save()
            return JsonResponse({'code': 200, 'msg': '编辑成功'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_tag_delete(request):
    """
    管理员删除标签
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
            if not data.get('id'):
                return JsonResponse({'code': 400, 'msg': '标签id不能为空'})
            tag = Tag.objects.get(id=data.get('id'))
            if tag.id == 1:
                return JsonResponse({'code': 400, 'msg': '默认标签不能删除'})
            tag.resource_set.clear()
            tag.delete()
            return JsonResponse({'code': 200, 'msg': '删除成功'})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '参数错误'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
