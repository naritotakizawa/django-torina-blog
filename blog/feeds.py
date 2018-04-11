from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from .models import Post, SiteDetail


class LatestEntriesFeed(Feed):
    """最新記事feed."""

    link = reverse_lazy('blog:index')

    @property
    def site(self):
        """サイト詳細情報の遅延ロード"""
        if not hasattr(self, '_site'):
            site = Site.objects.get(pk=settings.SITE_ID)
            mysite, _ = SiteDetail.objects.get_or_create(site=site)
            self._site = mysite
        return self._site

    def title(self):
        return self.site.title

    def description(self):
        return self.site.description

    def items(self):
        """記事一覧."""
        return Post.objects.filter(
            is_publick=True).order_by('-created_at')[:10]

    def item_title(self, item):
        """記事タイトル."""
        return item.title

    def item_description(self, item):
        """記事の説明."""
        # 記事の説明フィールド
        return item.get_description()

    def item_link(self, item):
        """記事へのリンク."""
        return reverse('blog:detail', args=[item.pk])
