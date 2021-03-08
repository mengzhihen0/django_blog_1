from django.db import models
from django.utils import timezone

class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)

    # 一 对 多:一篇文章可以有多个评论
    post = models.ForeignKey('article.Post', verbose_name='文章', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])

