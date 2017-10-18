from django.db import models

# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField(blank=True)
    text = models.TextField()
    # 当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间
    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('lynjay.Post')

    def __str__(self):
        return self.text[:20]