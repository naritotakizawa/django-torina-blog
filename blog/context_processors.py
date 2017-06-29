"""contet_processor."""
from django.db.models import Count
from .forms import PostSerachForm
from .models import Category, Tag, Link, Analytics, Ads, SiteDetail, Comment


def common(request):
    """blogで使うcontextの設定."""
    try:
        mysite = SiteDetail.objects.latest('pk')
    except SiteDetail.DoesNotExist:
        mysite = None

    context = {
        # 紐付いているポストの数が多い順に10個
        # tag.num_posts で数を表示できる
        'categories': Category.objects.annotate(
            num_posts=Count('post')).order_by('-num_posts'),
        'tags': Tag.objects.annotate(
            num_posts=Count('post')).order_by('-num_posts')[:10],

        'links': Link.objects.all(),
        'analytics': Analytics.objects.all(),
        'ads': Ads.objects.all(),
        'global_form': PostSerachForm(request.GET),
        'mysite': mysite,
        #'comments': Comment.objects.order_by('-created_at')[:10],
        'comments': Comment.objects.annotate(
            num_recomments=Count('recomment')).order_by('-created_at')[:10],

    }
    return context
