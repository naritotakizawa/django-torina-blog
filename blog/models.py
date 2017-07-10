"""models.py."""
from django.db import models
from django.utils import timezone


class Category(models.Model):
    """カテゴリー."""

    name = models.CharField('カテゴリ名', max_length=255)
    description = models.TextField('概要', blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.name


class Tag(models.Model):
    """タグ."""

    name = models.CharField('タグ名', max_length=255)
    description = models.TextField('概要', blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.name


class Post(models.Model):
    """ブログのポスト."""

    title = models.CharField('タイトル', max_length=255)
    text = models.TextField('本文')
    category = models.ForeignKey(
        Category, verbose_name='カテゴリ', on_delete=models.PROTECT, null=True)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    thumnail = models.ImageField(
        'サムネイル', upload_to='thumnail/', blank=True, null=True)
    is_publick = models.BooleanField('公開可能か?', default=True)
    friend_posts = models.ManyToManyField(
        'self', verbose_name='関連記事', blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.title

    def get_next(self):
        """次の記事."""
        next_post = Post.objects.filter(
            is_publick=True, created_at__gt=self.created_at
        ).order_by('-created_at')
        if next_post:
            return next_post.last()
        return None

    def get_prev(self):
        """前の記事."""
        prev_post = Post.objects.filter(
            is_publick=True, created_at__lt=self.created_at
        ).order_by('-created_at')
        if prev_post:
            return prev_post.first()
        return None


class Comment(models.Model):
    """コメント."""

    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('コメント')
    icon = models.ImageField(
        'サムネイル', upload_to='com_icon/', blank=True, null=True)
    target = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='対象記事')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.text[:10]


class ReComment(models.Model):
    """返信コメント."""

    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('コメント')
    icon = models.ImageField(
        'サムネイル', upload_to='com_icon/', blank=True, null=True)
    target = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.text[:10]


class Link(models.Model):
    """リンク."""

    name = models.CharField('リンク名', max_length=255)
    adrs = models.CharField('アドレス', max_length=255)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.name


class Analytics(models.Model):
    """アナリティクスの情報."""

    name = models.CharField('アナリティクス', max_length=255, blank=True)
    html = models.TextField('アナリティクスHTML', blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.name


class Ads(models.Model):
    """広告関連."""

    name = models.CharField('広告名', max_length=255, blank=True)
    html = models.TextField('広告HTML', blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.name


class SiteDetail(models.Model):
    """サイトの詳細."""

    title = models.CharField('タイトル', max_length=255, blank=True)
    description = models.CharField('サイトの説明', max_length=255, blank=True)
    author = models.CharField('管理者', max_length=255, blank=True)
    author_mail = models.EmailField('管理者アドレス', max_length=255, blank=True)
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        """str."""
        return self.author


class PopularPost(models.Model):
    """人気記事."""

    title = models.CharField('タイトル', max_length=255)
    url = models.CharField('URL', max_length=255)
    page_view = models.IntegerField('ページビュー数')

    def __str__(self):
        return '{0} - {1} - {2}'.format(
            self.url, self.title, self.page_view)
