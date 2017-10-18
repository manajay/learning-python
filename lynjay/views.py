from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render , get_object_or_404
from .models import Post , Category
from comments.forms import CommentForm

import markdown
# Create your views here.

def index(request):
    # 不加 - 则是正序
    post_list = Post.objects.all().order_by("-created_time")
    return render(request, 'blog/index.html',
                  context={"title":"博客首页",
                                   "welcome":"Lynjay在这里,欢迎访问我的博客首页!",
                           "post_list": post_list})

# 注意views的视图处理函数中的参数名称 对应的是 urls 文件的正则匹配 参数
def detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    # 重新渲染post.body
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # form
    form = CommentForm()
    # comment_list
    comment_list = post.comment_set.all()

    # 传递的数据
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }
    return render(request,'blog/detail.html',
                  context=context)

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