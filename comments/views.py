from django.shortcuts import render , get_object_or_404 , redirect
from lynjay.models import Post
from .models import Comment
from .forms import CommentForm

# Create your views here.
def post_comment(request,post_pk):
    # 获取Comment需要关联的Post
    post = get_object_or_404(Post,pk=post_pk)

    # 拦截请求的method
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象
        commentForm = CommentForm(request.POST)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if commentForm.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库
            comment = commentForm.save(commit=False)
            comment.post = post
            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = post.comment_set.all()
            context = {
                'post': post,
                'comment': comment,
                'comment_list': comment_list
            }
            return render(request,'blog/detail.html',context = context)

    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)




