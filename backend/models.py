from django.db import models

table_prefix = 'rc_'


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name='标签名')
    slug = models.SlugField(max_length=100, verbose_name='标签别名')
    description = models.TextField(verbose_name='标签描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + 'tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名')
    slug = models.SlugField(max_length=100, verbose_name='分类别名')
    description = models.TextField(verbose_name='分类描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + 'category'
        verbose_name = '分类'
        verbose_name_plural = verbose_name


class Image(models.Model):
    name = models.CharField(max_length=100, verbose_name='图片名')
    description = models.TextField(verbose_name='图片描述', null=True, blank=True)
    image = models.ImageField(upload_to='image/%Y/%m/%d/', verbose_name='图片')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + 'image'
        verbose_name = '图片'
        verbose_name_plural = verbose_name


class Video(models.Model):
    name = models.CharField(max_length=100, verbose_name='视频名')
    description = models.TextField(verbose_name='视频描述', null=True, blank=True)
    video = models.FileField(upload_to='video/%Y/%m/%d/', verbose_name='视频')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + 'video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name


class Cover(models.Model):
    name = models.CharField(max_length=100, verbose_name='封面名')
    description = models.TextField(verbose_name='封面描述')
    cover = models.ImageField(upload_to='cover/%Y/%m/%d/', verbose_name='封面', default='cover/default.png')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + 'cover'
        verbose_name = '封面'
        verbose_name_plural = verbose_name


class Resource(models.Model):
    name = models.CharField(max_length=100, verbose_name='资源名')
    description = models.TextField(verbose_name='资源描述', default='')
    content = models.TextField(verbose_name='资源内容', default='')
    baidu_url = models.URLField(verbose_name='百度云链接', default='')
    tianyi_url = models.URLField(verbose_name='天翼云链接', default='')
    aliyun_url = models.URLField(verbose_name='阿里云链接', default='')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, verbose_name='分类')
    tags = models.ManyToManyField(Tag, blank=True, null=True, verbose_name='标签')
    active_code = models.CharField(max_length=100, verbose_name='激活码')
    cover = models.ForeignKey(Cover, on_delete=models.CASCADE, default=1, verbose_name='封面')
    status = models.BooleanField(default=True, verbose_name='状态')
    images = models.ManyToManyField(Image, blank=True, null=True, verbose_name='图片')
    videos = models.ManyToManyField(Video, blank=True, null=True, verbose_name='视频')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        db_table = table_prefix + 'resource'
        verbose_name = '资源'
        verbose_name_plural = verbose_name


class User(models.Model):
    username = models.CharField(max_length=100, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    nickname = models.CharField(max_length=100, verbose_name='昵称')
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d/', default='avatar/default.png', blank=True, null=True,
                               verbose_name='头像')
    is_active = models.BooleanField(default=False, verbose_name='是否激活')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.username

    class Meta:
        db_table = table_prefix + 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, verbose_name='资源')
    content = models.TextField(verbose_name='评论内容')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='回复')
    is_check = models.BooleanField(default=False, verbose_name='是否审核')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.content

    class Meta:
        db_table = table_prefix + 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
