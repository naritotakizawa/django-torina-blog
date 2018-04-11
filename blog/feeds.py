"""feedに関するモジュール."""
from django.conf import settings
from django.contrib.syndication.views import Feed
from django.urls import reverse, reverse_lazy
from .models import Post, SiteDetail

mysite = SiteDetail.objects.get(site__pk=settings.SITE_ID)


class LatestEntriesFeed(Feed):
    """最新記事feed."""

    title = mysite.title
    link = reverse_lazy('blog:index')
    description = mysite.description

    def items(self):
        """記事一覧."""
        return Post.objects.filter(
            is_publick=True).order_by('-created_at')[:10]

    def item_title(self, item):
        """記事タイトル."""
        return item.title

    def item_description(self, item):
        """記事の説明."""
        # 記事の説明フィールドがあればそれを、なければカテゴリとタグ名を
        return item.get_description()

    def item_link(self, item):
        """記事へのリンク."""
        return reverse('blog:detail', args=[item.pk])
