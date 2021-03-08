from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# 分类（Category）  “一”
class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 标签            “多”
class Tag(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 文章            “多”
class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='标题')
    body = models.TextField(verbose_name='正文')
    created_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modified_time = models.DateTimeField(verbose_name='更新时间')
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='摘要')

    # 一 对 多 模型：一篇文章对应一个分类, 一个分类下可以有多篇文章
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    # 多 对 多 模型：一篇文章对应多个标签，一个标签下也有可能有多篇文章
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    # 一 对 多 模型：一篇文章只能有一个作者，一个作者可以写多篇文章
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('article:detail', kwargs={'pk':self.pk})

    # 阅读量
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])




