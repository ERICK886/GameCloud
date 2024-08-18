import json
import os
import sys

import pymysql
from django import db
from django.http import JsonResponse

from backend.func.config import set_config


def system_start_install(request):
    """
    开始安装系统
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        mysql = data.get('mysql')
        site = data.get('site')
        admin = data.get('admin')
        if site.get('domain'):
            domain = site.get('domain')
            if domain.endswith('/'):
                domain = domain[:-1]
            set_config('SITE_URL', domain)
        else:
            set_config('SITE_URL', '')

        if site.get('name'):
            set_config('SITE_NAME', site.get('name'))
        else:
            set_config('SITE_NAME', '小技资源网')

        if site.get('desc'):
            set_config('SITE_DESCRIPTION', site.get('desc'))
        else:
            set_config('SITE_DESCRIPTION', '')

        if site.get('keywords'):
            set_config('SITE_KEYWORDS', site.get('keywords'))
        else:
            set_config('SITE_KEYWORDS', '')
        if mysql.get('host') and mysql.get('port') and mysql.get('user') and mysql.get(
                'password') and mysql.get('database'):
            host = mysql.get('host')
            port = mysql.get('port')
            user = mysql.get('user')
            password = mysql.get('password')
            database = mysql.get('database')
            conn = None
            try:
                conn = pymysql.connect(host=host, port=int(port), user=user, password=password,
                                       db=database)
            except pymysql.MySQLError:
                conn = None
                return JsonResponse({'code': 400, 'msg': '数据库连接失败，请检查配置信息',
                                     'data': {'log': '数据库连接失败，请检查配置信息'}})
            finally:
                if conn:
                    conn.close()

            set_config('DATABASE', {
                'NAME': database,
                'USER': user,
                'PASSWORD': password,
                'HOST': host,
                'PORT': port,
            })
        if admin.get('username') and admin.get('password') and admin.get('email') and admin.get('nickname'):
            username = admin.get('username')
            password = admin.get('password')
            email = admin.get('email')
            nickname = admin.get('nickname')
            set_config('ADMIN', {
                'USERNAME': username,
                'PASSWORD': password,
                'EMAIL': email,
                'NICKNAME': nickname
            })

        try:
            python_path = sys.executable
            cmd = f'{python_path} ./manage.py migrate'
            out = os.popen(cmd)
            output = out.read()
            return JsonResponse({'code': 200, 'msg': '安装成功', 'data': {'log': output}})
        except db.utils.OperationalError:
            return JsonResponse({'code': 400, 'msg': '安装失败', 'data': {'log': '数据库连接失败'}})
        except Exception as e:
            return JsonResponse({'code': 400, 'msg': '安装失败', 'data': {'log': e}})
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误', 'data': {}})
