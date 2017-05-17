from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post, SiteDetail

try:
    mysite = SiteDetail.objects.latest('pk')
except SiteDetail.DoesNotExist:
    mysite = None


class LatestEntriesFeed(Feed):
    title = mysite.title or ''
    link = '/'
    description = mysite.description or ''

    def items(self):
        return Post.objects.filter(
            is_publick=True).order_by('-created_at')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        message = "カテゴリ:{0} タグ:{1}"
        category = item.category
        tags = " ".join(tag.name for tag in item.tag.all())
        message = message.format(category, tags)
        return message

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return reverse('blog:detail', args=[item.pk])
