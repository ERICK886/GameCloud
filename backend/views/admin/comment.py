import json

from django.http import JsonResponse
import datetime
from backend.func.token import check_token, check_admin
from backend.models import Comment


def admin_comment_get(request):
    """
    管理员获取评论
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

        comment_list = []
        comments = Comment.objects.filter(user__nickname__contains=kwd).order_by(order + orderby)
        for comment in comments:
            comment_list.append({
                'id': comment.id,
                'content': comment.content,
                'create_time': datetime.datetime.strftime(comment.create_time, '%Y-%m-%d %H:%M'),
                'is_check': comment.is_check,
                'reply': {
                    'id': comment.reply.id,
                    'content': comment.reply.content,
                    'is_check': comment.reply.is_check,
                } if comment.reply else '',
                'resource': {
                    'id': comment.resource.id,
                    'name': comment.resource.name,
                    'status': comment.resource.status,
                },
                'user': {
                    'id': comment.user.id,
                    'nickname': comment.user.nickname,
                    'username': comment.user.username,
                },
            })
        return JsonResponse({'code': 200, 'msg': '获取成功', 'data': comment_list})
    else:
        return JsonResponse({'code': 405, 'msg': '请求方法错误'})
