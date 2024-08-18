import json

from django.http import JsonResponse

from GameCloud.settings import BASE_DIR


def config_check(request):
    """
    检查配置文件是否有信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        # 读取配置文件
        config_path = BASE_DIR / 'config.json'
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                if config != {}:
                    return JsonResponse({'code': 200, 'msg': '配置文件存在', 'data': True})
                else:
                    return JsonResponse({'code': 400, 'msg': '配置文件未配置', 'data': False})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '配置文件不存在', 'data': False})
    else:
        return JsonResponse({'code': 500, 'msg': '请求方式错误', 'data': False})
