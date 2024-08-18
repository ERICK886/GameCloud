import json

from django.http import JsonResponse

from backend.func.token import check_token
from backend.models import Comment


def home_comment_add(request):
    """
    添加评论
    :param request:
    :return:
    """
    token = request.headers.get('Authorization')
    payload, flag = check_token(token)
    if not flag:
        return JsonResponse({'code': 401, 'msg': 'token认证失败'})
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        if not data.get('comment'):
            return JsonResponse({'code': 400, 'msg': '评论内容不能为空'})
        if not data.get('resourceId'):
            return JsonResponse({'code': 400, 'msg': '资源id不能为空'})

        if data.get('replyId'):
            reply = Comment.objects.get(id=data.get('replyId'))
            Comment.objects.create(
                content=data.get('comment'),
                resource_id=data.get('resourceId'),
                user_id=payload.get('id'),
                reply=reply,
                is_check=True,
            )
            return JsonResponse({'code': 200, 'msg': '回复成功', })
        else:
            Comment.objects.create(
                content=data.get('comment'),
                resource_id=data.get('resourceId'),
                user_id=payload.get('id'),
                is_check=True,
            )
            return JsonResponse({'code': 200, 'msg': '评论成功'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
