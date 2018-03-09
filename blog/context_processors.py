"""contet_processor."""
from django.contrib.sites.models import Site
from django.db.models import Count
from .forms import PostSerachForm
from .models import (
    Category, Tag, Link, Analytics, Ads, SiteDetail, Comment,
    PopularPost,
)


def common(request):
    """共通contextの設定."""
    try:
        mysite = SiteDetail.objects.latest('pk')
    except SiteDetail.DoesNotExist:
        mysite = SiteDetail.objects.create(site=Site.objects.get(pk=1))  # pk=1のSiteは必ずある

    context = {
        'categories': Category.objects.annotate(
            num_posts=Count('post')).order_by('-num_posts'),
        'tags': Tag.objects.annotate(
            num_posts=Count('post')).order_by('-num_posts')[:10],
        'comments': Comment.objects.annotate(
            num_recomments=Count('recomment')).order_by('-created_at')[:10],

        'links': Link.objects.all(),
        'analytics': Analytics.objects.all(),
        'ads': Ads.objects.all(),
        'global_form': PostSerachForm(request.GET),
        'mysite': mysite,
        'popular_post_list': PopularPost.objects.order_by('-page_view'),
    }
    return context
