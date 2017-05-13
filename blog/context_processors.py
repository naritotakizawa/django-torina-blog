from .forms import PostSerachForm
from .models import Category, Tag, Link, Analytics, Ads, SiteDetail, Comment


def common(request):

    try:
        mysite = SiteDetail.objects.latest('pk')
    except SiteDetail.DoesNotExist:
        mysite = None

    context = {
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'links': Link.objects.all(),
        'analytics': Analytics.objects.all(),
        'ads': Ads.objects.all(),
        'global_form': PostSerachForm(request.GET),
        'mysite': mysite,
        'comments': Comment.objects.order_by('-created_at')[:10],
    }
    return context
