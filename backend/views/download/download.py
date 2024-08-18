import os

from django.http import HttpResponse, JsonResponse

from GameCloud.settings import BASE_DIR


def download_xlsx_template(request):
    """
    下载xlsx模板
    :param request:
    :return:
    """
    if request.method == 'GET':
        file_path = BASE_DIR / 'files/批量导入上传样例.xlsx'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="批量导入上传样例.xlsx"'
            response['Content-Length'] = str(os.path.getsize(file_path))
            return response
    else:
        return JsonResponse({'code': 400, 'msg': '请求方式错误'})
