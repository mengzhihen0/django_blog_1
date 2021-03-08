from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post,Category,Tag
import markdown, re
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    # return HttpResponse("hello")
    # title = '我的博客首页'
    # welcome = '欢迎来到我的博客首页'
    # return render(request, 'article/index.html',locals())
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'article/index.html', locals())


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 阅读量 +1
    post.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 'markdown.extensions.toc',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'article/detail.html', locals())


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'article/index.html', context={'post_list': post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'article/index.html', context={'post_list': post_list})

def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'article/index.html', context={'post_list': post_list})
