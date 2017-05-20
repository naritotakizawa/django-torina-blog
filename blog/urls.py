from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from . import views
from .feeds import LatestEntriesFeed
from .sitemap import (
    PostSitemap, TagSitemap,
    CategorySitemap, StaticSitemap
)
sitemaps = {
    'post': PostSitemap,
    'category': CategorySitemap,
    'tag': TagSitemap,
    'static': StaticSitemap,
}


urlpatterns = [
    url(r'^$', views.PostIndexView.as_view(), name='index'),

    url(r'^ping/$', views.ping, name='ping'),

    url(r'^alltag/$', views.TagListView.as_view(), name='tag_list'),

    url(r'^detail/(?P<pk>[0-9]+)/$',
        views.PostDetailView.as_view(), name='detail'),

    url(r'^category/(?P<category>.*)/$',
        views.CategoryView.as_view(), name='category'),

    url(r'^tag/(?P<tag>.*)/$',
        views.TagView.as_view(), name='tag'),

    url(r'^comment/(?P<pk>[0-9]+)/$',
        views.CommentCreateView.as_view(), name='comment'),

    url(r'^private/$', views.PostPrivateIndexView.as_view(), name='private'),

    url(r'^latest/feed/$', LatestEntriesFeed(), name='feed'),
    url(r'^sitemap\.xml$', sitemap, {
        'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
