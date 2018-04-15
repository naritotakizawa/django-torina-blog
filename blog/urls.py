from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .feeds import LatestEntriesFeed
from .sitemap import (
    PostSitemap, TagSitemap,
    CategorySitemap, StaticSitemap
)

app_name = 'blog'

sitemaps = {
    'post': PostSitemap,
    'category': CategorySitemap,
    'tag': TagSitemap,
    'static': StaticSitemap,
}


urlpatterns = [
    path('', views.PostIndexView.as_view(), name='index'),

    path('ping/', views.ping, name='ping'),

    path('alltag/', views.TagListView.as_view(), name='tag_list'),

    path('detail/<int:pk>/', views.PostDetailView.as_view(), name='detail'),

    path('category/<str:category>/', views.CategoryView.as_view(), name='category'),

    path('tag/<str:tag>/', views.TagView.as_view(), name='tag'),

    path('comment/<int:pk>/', views.CommentCreateView.as_view(), name='comment'),
    path('recomment/<int:pk>/', views.ReCommentCreateView.as_view(), name='recomment'),
    path('file_download/<int:pk>/', views.file_download, name='file_download'),


    path('private/', views.PostPrivateIndexView.as_view(), name='private'),

    path('latest/feed/', LatestEntriesFeed(), name='feed'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
