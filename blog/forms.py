"""forms.py."""
from django import forms
from .models import Comment, ReComment


class PostSerachForm(forms.Form):
    """記事検索フォーム."""

    keyword = forms.CharField(label='キーワード', required=False)

    def __init__(self, *args, **kwargs):
        """init."""
        super().__init__(*args, **kwargs)
        self.fields['keyword'].widget.attrs['class'] = 'form-control'
        self.fields['keyword'].widget.attrs['placeholder'] = 'クイックサーチ'


class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム."""

    class Meta:
        """Meta."""

        model = Comment
        fields = ('name', 'text', 'icon')

    def __init__(self, *args, **kwargs):
        """init."""
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['icon'].widget.attrs['class'] = 'form-control-file'


class ReCommentCreateForm(forms.ModelForm):
    """返信コメント投稿フォーム."""

    class Meta:
        """Meta."""

        model = ReComment
        fields = ('name', 'text', 'icon')

    def __init__(self, *args, **kwargs):
        """init."""
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['icon'].widget.attrs['class'] = 'form-control-file'

