from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    # 表单的内部类 Meta 里指定一些和表单相关的东西
    class Meta:
        model = Comment
        fields = ['name','email','url','text']