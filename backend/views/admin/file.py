from django.http import JsonResponse

from backend.func.config import get_config
from backend.func.crypto import hash_md5
from backend.func.token import check_token, check_admin
from backend.models import Image, Video, Cover


def admin_cover_upload(request):
    """
    管理员上传封面
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
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'code': 400, 'msg': '请选择文件'})
        else:
            file_name = file.name.split('.')[0]
            file_suffix = file.name.split('.')[-1]
            file_name = hash_md5(file_name)
            while Cover.objects.filter(name=file_name).exists():
                file_name = hash_md5(file_name)
            file.name = file_name + '.' + file_suffix
            cover = Cover.objects.create(
                name=file_name,
                cover=file
            )
            site_url = get_config('SITE_URL')
            return JsonResponse(
                {'code': 200, 'msg': '上传成功',
                 'data': {'url': site_url + '/uploads' + cover.cover.url, 'id': cover.id}})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_image_upload(request):
    """
    管理员上传图片
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
        file = request.FILES.get('file')

        if not file:
            return JsonResponse({'code': 400, 'msg': '请选择文件'})
        else:
            file_name = file.name.split('.')[0]
            file_suffix = file.name.split('.')[-1]
            file_name = hash_md5(file_name)
            while Image.objects.filter(name=file_name).exists():
                file_name = hash_md5(file_name)
            file.name = file_name + '.' + file_suffix
            img = Image.objects.create(
                name=file_name,
                image=file
            )
            site_url = get_config('SITE_URL')
            return JsonResponse(
                {'code': 200, 'msg': '上传成功', 'data': {'url': site_url + '/uploads' + img.image.url, 'id': img.id}})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})


def admin_video_upload(request):
    """
    管理员上传视频
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
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'code': 400, 'msg': '请选择文件'})
        else:
            file_name = file.name.split('.')[0]
            file_suffix = file.name.split('.')[-1]
            if file_suffix not in ['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'rmvb', '3gp', 'mpeg', 'mpg', 'webm',
                                   'ogg', 'm4v', 'm4a', 'wav', 'aac', 'flac', 'mp3', 'wav', 'oga', 'wma', ]:
                return JsonResponse({'code': 400, 'msg': '不支持的视频格式'})
            file_name = hash_md5(file_name)
            while Video.objects.filter(name=file_name).exists():
                file_name = hash_md5(file_name)
            file.name = file_name + '.' + file_suffix
            video = Video.objects.create(
                name=file_name,
                video=file
            )
            site_url = get_config('SITE_URL')
            return JsonResponse(
                {'code': 200, 'msg': '上传成功',
                 'data': {'url': site_url + '/uploads' + video.video.url, 'id': video.id}})

    return JsonResponse({'code': 400, 'msg': '请求方式错误'})
