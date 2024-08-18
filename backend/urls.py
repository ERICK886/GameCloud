from django.urls import path

from backend.views import admin, home, download, config

urlpatterns = [
    # 检查配置
    path('config/check/', config.config_check),
    # 安装
    path('system/start/install/', home.system_start_install),
    # 用户登录
    path('admin/signin/', admin.admin_sign_in),
    path('admin/signup/', admin.admin_sign_up),
    # 分类操作
    path('admin/category/get/', admin.admin_category_get),
    path('admin/category/add/', admin.admin_category_add),
    path('admin/category/edit/', admin.admin_category_edit),
    path('admin/category/delete/', admin.admin_category_delete),
    # 标签操作
    path('admin/tag/get/', admin.admin_tag_get),
    path('admin/tag/add/', admin.admin_tag_add),
    path('admin/tag/edit/', admin.admin_tag_edit),
    path('admin/tag/delete/', admin.admin_tag_delete),
    # 图片操作
    path('admin/image/upload/', admin.admin_image_upload),
    # 封面操作
    path('admin/cover/upload/', admin.admin_cover_upload),
    # 视频操作
    path('admin/video/upload/', admin.admin_video_upload),
    # 资源操作
    path('admin/resource/get/', admin.admin_resource_get),
    path('admin/resource/add/', admin.admin_resource_add),
    path('admin/resource/edit/', admin.admin_resource_edit),
    path('admin/resource/delete/', admin.admin_resource_delete),
    path('admin/resource/add/multiple/', admin.admin_resource_add_multiple),
    # 评论操作
    path('admin/comment/get/', admin.admin_comment_get),
    # 首页资源操作
    path('home/resource/get/', home.home_resource_get),
    path('home/comment/add/', home.home_comment_add),
    # 获取系统信息
    path('admin/system/info/', admin.admin_system_info),
    # 检查管理员权限
    path('admin/check/right/', admin.admin_check_right),
    # 修改状态
    path('admin/change/status/', admin.admin_change_status),
    # 下载xlsx模板
    path('download/xlsx/template/', download.download_xlsx_template),
]
