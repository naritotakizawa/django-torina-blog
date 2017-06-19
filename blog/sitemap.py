"""sitemap."""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy
from .models import Post, Category, Tag


class PostSitemap(Sitemap):
    """記事のサイトマップ."""

    changefreq = 'never'
    priority = 0.5

    def items(self):
        """記事一覧データ."""
        return Post.objects.filter(is_publick=True).order_by('-created_at')

    def lastmod(self, obj):
        """更新日."""
        return obj.created_at

    def location(self, obj):
        """url."""
        return reverse_lazy('blog:detail', kwargs={'pk': obj.pk})


class CategorySitemap(Sitemap):
    """カテゴリのサイトマップ."""

    changefreq = 'never'
    priority = 0.5

    def items(self):
        """カテゴリ一覧データ."""
        return Category.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        """更新日."""
        return obj.created_at

    def location(self, obj):
        """url."""
        return reverse_lazy('blog:category', kwargs={'category': obj.name})


class TagSitemap(Sitemap):
    """タグのサイトマップ."""

    changefreq = 'never'
    priority = 0.5

    def items(self):
        """タグ一覧データ."""
        return Tag.objects.all().order_by('-created_at')

    def lastmod(self, obj):
        """更新日."""
        return obj.created_at

    def location(self, obj):
        """url."""
        return reverse_lazy('blog:tag', kwargs={'tag': obj.name})


class StaticSitemap(Sitemap):
    """静的なサイトマップ."""

    changefreq = 'never'
    priority = 0.5

    def items(self):
        """静的ページの一覧."""
        return ['blog:index', 'blog:tag_list']

    def location(self, obj):
        """URL."""
        return reverse_lazy(obj)
