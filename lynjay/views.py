from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404
from .models import Post , Category
import markdown
# Create your views here.

def index(request):
    # 不加 - 则是正序
    post_list = Post.objects.all().order_by("-created_time")
    return render(request, 'blog/index.html',
                  context={"title":"博客首页",
                                   "welcome":"Lynjay在这里,欢迎访问我的博客首页!",
                           "post_list": post_list})


def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    # 重新渲染post.body
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return render(request,'blog/detail.html',
                  context={'post': post})

def archives(request,year,month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month).order_by('-created_time')
    return render(request,"blog/index.html",context={
        'post_list': post_list
    })

def category(request,pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request,'blog/index.html',context={
        'post_list': post_list
    })