import json

from django.http import JsonResponse

from backend.func.token import check_admin, check_token
from backend.models import Comment, Tag


def admin_change_status(request):
    """
    修改状态
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
        if data.get('type'):
            type = data.get('type')
        else:
            return JsonResponse({'code': 400, 'msg': 'type不能为空'})
        if data.get('id'):
            id = data.get('id')
        else:
            return JsonResponse({'code': 400, 'msg': 'id不能为空'})
        if data.get('status') or data.get('status') == False:
            status = data.get('status')
        else:
            return JsonResponse({'code': 400, 'msg': 'status不能为空'})

        if type == 'comment':
            Comment.objects.filter(id=id).update(is_check=status)
        elif type == 'tag':
            Tag.objects.filter(id=id).update(status=status)
        else:
            return JsonResponse({'code': 400, 'msg': 'type错误'})
        return JsonResponse({'code': 200, 'msg': '修改成功'})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
