from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from comments.forms import CommentForm
from django.db.models import Q
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import markdown
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator

class IndexView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "post_list"
    paginate_by = 3


class CategoryView(IndexView):
    context_object_name = "post_list"

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 覆写了父类的 get_queryset 方法。该方法默认获取指定模型的全部列表数据
        return super(CategoryView, self).get_queryset().filter(category=cate)


class ArchiveView(IndexView):
    def get_queryset(self):
        archive_year = self.kwargs.get('year')
        archive_month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().\
            filter(created_time__year=archive_year, created_time__month=archive_month)


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        post = self.object
        post.increase_views()
        return response

    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
        return post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        post = self.object
        comment_list = post.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


def about(request):
    return render(request, 'blog/about.html', context={})


# 跳转到联系页
def contact(request):
    return render(request, 'blog/contact.html', context={})


# 发送了联系我的表单请求
def contact_me(request):
    return render(request, 'blog/contact.html', context={})


# 字典的键之所以叫 query 是因为我们的表单中搜索框 input 的 name 属性的值是 query
def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        return render(request, 'blog/index.html', context={
            'error_msg': '请输入关键词'
        })
    else:
        # 前缀 i 表示不区分大小写。这里 i-contains 是查询表达式（Field lookups）
        post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
        return render(request, 'blog/index.html', context={
            'error_msg': error_msg,
            'post_list': post_list
        })
