from django import template
from ..models import Post
from ..models import Category
from django.db.models.aggregates import Count
register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by("-created_time")[:num]


@register.simple_tag
def archives():
    return Post.objects.dates("created_time", "month", order="DESC")


@register.simple_tag
def get_categories():
    # 查询表达式（双下划线）
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)

