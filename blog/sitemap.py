from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse_lazy
from .models import Post, Category, Tag


class PostSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Post.objects.filter(is_publick=True)

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse_lazy('blog:detail', kwargs={'pk': obj.pk})


class CategorySitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse_lazy('blog:category', kwargs={'category': obj.name})


class TagSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse_lazy('blog:tag', kwargs={'tag': obj.name})


class StaticSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return ['blog:index', 'blog:tag_list']

    def location(self, obj):
        return reverse_lazy(obj)
