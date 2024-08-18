import json
import os
from django.http import JsonResponse

from backend.func.comment import get_reply_list
from backend.func.config import get_config
from backend.models import Resource


def home_resource_get(request):
    """
    首页资源获取
    :param request:
    :return:
    """
    if request.method == 'POST':
        site_url = get_config('SITE_URL')
        data = json.loads(request.body.decode('utf-8'))
        if data.get('resourceId'):
            resource = Resource.objects.filter(id=data.get('resourceId')).first()
            comments_list = []
            comments = resource.comment_set.all().filter(reply__isnull=True)
            for comment in comments:
                replies = get_reply_list(resource.comment_set.all().filter(reply__isnull=False), comment)
                comments_list.append({
                    'id': comment.id,
                    'content': comment.content,
                    'user': {
                        'id': comment.user.id,
                        'avatar': site_url + '/uploads' + comment.user.avatar.url,
                        'nickname': comment.user.nickname,
                        'username': comment.user.username
                    },
                    'is_check': comment.is_check,
                    'reply': replies,
                    'create_time': comment.create_time.strftime('%Y-%m-%d %H:%M'),
                    'update_time': comment.update_time.strftime('%Y-%m-%d %H:%M')
                })
            return JsonResponse({
                'code': 200,
                'msg': '获取成功',
                'data': {
                    'id': resource.id,
                    'name': resource.name,
                    'description': resource.description,
                    'content': resource.content,
                    'active_code': resource.active_code,
                    'url': {
                        'aliyun_url': resource.aliyun_url,
                        'baidu_url': resource.baidu_url,
                        'tianyi_url': resource.tianyi_url,
                    },
                    'category': {
                        'id': resource.category.id,
                        'name': resource.category.name,
                        'slug': resource.category.slug,
                        'description': resource.category.description,
                        'status': resource.category.status,
                        'create_time': resource.category.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'update_time': resource.category.update_time.strftime('%Y-%m-%d %H:%M:%S')
                    },
                    'cover': site_url + '/uploads' + resource.cover.cover.url,
                    'status': resource.status,
                    'tags': [{
                        'id': tag.id,
                        'name': tag.name,
                        'slug': tag.slug,
                        'description': tag.description,
                        'status': tag.status,
                        'create_time': tag.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'update_time': tag.update_time.strftime('%Y-%m-%d %H:%M:%S')
                    } for tag in resource.tags.all()],
                    'videos': [{
                        'id': video.id,
                        'name': video.name,
                        'video': site_url + '/uploads' + video.video.url,
                        'create_time': video.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'update_time': video.update_time.strftime('%Y-%m-%d%H:%M:%S')
                    } for video in resource.videos.all()],
                    'images': [{
                        'id': image.id,
                        'name': image.name,
                        'image': site_url + '/uploads' + image.image.url,
                        'create_time': image.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                        'update_time': image.update_time.strftime('%Y-%m-%d%H:%M:%S')
                    } for image in resource.images.all()],
                    'comments': comments_list,
                    'create_time': resource.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time': resource.update_time.strftime('%Y-%m-%d%H:%M:%S')
                }
            })
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
            orderby = 'update_time'

        if order == 'asc':
            order = ''
        else:
            order = '-'

        resource_list = []
        resources = Resource.objects.filter(name__icontains=kwd).order_by(order + orderby).filter(status=True)
        for resource in resources:
            resource_list.append({
                'id': resource.id,
                'name': resource.name,
                'description': resource.description,
                'active_code': resource.active_code,
                'aliyun_url': resource.aliyun_url,
                'baidu_url': resource.baidu_url,
                'tianyi_url': resource.tianyi_url,
                'category': {
                    'id': resource.category.id,
                    'name': resource.category.name,
                    'slug': resource.category.slug,
                    'description': resource.category.description,
                    'status': resource.category.status,
                    'create_time': resource.category.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time': resource.category.update_time.strftime('%Y-%m-%d %H:%M:%S')
                },
                'cover': site_url + '/uploads' + resource.cover.cover.url,
                'status': resource.status,
                'tags': [{
                    'id': tag.id,
                    'name': tag.name,
                    'slug': tag.slug,
                    'description': tag.description,
                    'status': tag.status,
                    'create_time': tag.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'update_time': tag.update_time.strftime('%Y-%m-%d %H:%M:%S')
                } for tag in resource.tags.all()],
                'create_time': resource.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'update_time': resource.update_time.strftime('%Y-%m-%d%H:%M:%S')
            })
        return JsonResponse({'code': 200, 'msg': '获取成功', 'data': resource_list})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
