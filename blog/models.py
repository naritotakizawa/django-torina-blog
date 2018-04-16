import os
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils import timezone


# サイト詳細情報のテーマカラーの選択肢
SITE_COLORS = (
    ('primary', '青色'),
    ('secondary', '灰色'),
    ('success', '緑色'),
    ('info', '水色'),
    ('warning', '黄色'),
    ('danger', '赤'),
    ('dark', '黒'),
)

DEFAULT_HEADER_TEXT = """\
このブログはDjangoとBootstrap4で作成されました
[filter url]https://github.com/naritotzawa/django-torina-blog<split>Githubのソースコード[end]\
"""


class Category(models.Model):
    """カテゴリー"""
    name = models.CharField('カテゴリ名', max_length=255)

    def __str__(self):
        """str."""
        return self.name


class Tag(models.Model):
    """タグ"""
    name = models.CharField('タグ名', max_length=255)

    def __str__(self):
        """str."""
        return self.name


class Post(models.Model):
    """記事"""
    title = models.CharField('タイトル', max_length=255)
    text = models.TextField('本文')
    category = models.ForeignKey(
        Category, verbose_name='カテゴリ', on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    thumnail = models.ImageField(
        'サムネイル', upload_to='post_thumbnail/%Y/%m/%d/', blank=True, null=True)
    is_publick = models.BooleanField('公開可能か?', default=True)
    friend_posts = models.ManyToManyField(
        'self', verbose_name='関連記事', blank=True)
    description = models.TextField('記事の説明', blank=True)
    files = GenericRelation('File')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.title

    def get_description(self):
        if self.description:
            return self.description
        else:
            description = 'カテゴリ:{0} タグ:{1}'
            category = self.category
            tags = ' '.join(tag.name for tag in self.tag.all())
            description = description.format(category, tags)
            return description

    def get_next(self):
        """次の記事を取得する(日付)

        パフォーマンス的に、無駄が多い処理ですが、APIとして一応残しておきます。
        """
        next_post = Post.objects.filter(
            is_publick=True, created_at__gt=self.created_at
        ).order_by('-created_at')
        if next_post:
            return next_post.last()
        return None

    def get_prev(self):
        """前の記事を取得する(日付)

        パフォーマンス的に、無駄が多い処理ですが、APIとして一応残しておきます。
        """
        prev_post = Post.objects.filter(
            is_publick=True, created_at__lt=self.created_at
        ).order_by('-created_at')
        if prev_post:
            return prev_post.first()
        return None


class Comment(models.Model):
    """コメント"""
    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('コメント')
    icon = models.ImageField(
        'サムネイル', upload_to='comment_thumbnail/%Y/%m/%d/', blank=True, null=True)
    target = models.ForeignKey(
        Post, on_delete=models.CASCADE, verbose_name='対象記事')
    files = GenericRelation('File')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:10]

    def get_filename(self):
        """ファイル名を取得する"""
        return os.path.basename(self.file.url)


class ReComment(models.Model):
    """返信コメント"""
    name = models.CharField('名前', max_length=255, default='名無し')
    text = models.TextField('コメント')
    icon = models.ImageField(
        'サムネイル', upload_to='recomment_thumbnail/%Y/%m/%d//', blank=True, null=True)
    target = models.ForeignKey(
        Comment, on_delete=models.CASCADE, verbose_name='対象コメント')
    files = GenericRelation('File')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return self.text[:10]

    def get_filename(self):
        """ファイル名を取得する"""
        return os.path.basename(self.file.url)


class Link(models.Model):
    """リンク"""
    name = models.CharField('リンク名', max_length=255)
    adrs = models.CharField('アドレス', max_length=255)

    def __str__(self):
        return self.name


class Analytics(models.Model):
    """アナリティクスの情報"""
    name = models.CharField('アナリティクス', max_length=255, blank=True)
    html = models.TextField('アナリティクスHTML', blank=True)

    def __str__(self):
        return self.name


class Ads(models.Model):
    """広告関連"""
    name = models.CharField('広告名', max_length=255, blank=True)
    html = models.TextField('広告HTML', blank=True)

    def __str__(self):
        return self.name


class SiteDetail(models.Model):
    """サイトの詳細情報"""
    site = models.OneToOneField(Site, verbose_name='Site', on_delete=models.PROTECT)
    title = models.CharField('タイトル', max_length=255, default='サンプルのタイトル')
    header_text = models.TextField('ヘッダーのテキスト', max_length=255, default=DEFAULT_HEADER_TEXT)
    description = models.TextField('サイトの説明', max_length=255, default='サンプルの説明')
    author = models.CharField('管理者', max_length=255, default='サンプルの管理者')
    author_mail = models.EmailField('管理者アドレス', max_length=255, default='your_mail@gmail.com')
    color = models.CharField('サイトテーマ色', choices=SITE_COLORS, default='primary', max_length=30)

    def __str__(self):
        return self.author


class PopularPost(models.Model):
    """人気記事"""
    title = models.CharField('タイトル', max_length=255)
    url = models.CharField('URL', max_length=255)
    page_view = models.IntegerField('ページビュー数')

    def __str__(self):
        return '{0} - {1} - {2}'.format(
            self.url, self.title, self.page_view)


class Image(models.Model):
    """記事に紐づく画像ファイル"""
    title = models.CharField('タイトル', max_length=255, blank=True)
    post = models.ForeignKey(
        Post, verbose_name='記事', on_delete=models.PROTECT,
    )
    src = models.ImageField('画像', upload_to='images/%Y/%m/%d/', help_text='送信後、一度保存してください。')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return '間接リンク:[filter imgpk]{0}[end] 直接リンク:[filter img]{1}[end]'.format(self.pk, self.src.url)


class File(models.Model):
    """記事やコメントに紐づく添付ファイル"""
    title = models.CharField('タイトル', max_length=255, blank=True)
    src = models.FileField('添付ファイル', upload_to='files/%Y/%m/%d/')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField('作成日', default=timezone.now)

    def __str__(self):
        return 'モデル:{} pk:{} url:{}'.format(self.content_type, self.object_id, self.src.url)

    def get_filename(self):
        """ファイル名を取得する"""
        return os.path.basename(self.src.url)
