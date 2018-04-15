"""admin.py"""
from django.contrib.sites.models import Site
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from .models import (
    Post, Category, Tag, Comment, ReComment,
    Link, Analytics, Ads, SiteDetail, PopularPost, Image, File
)


class SiteDetailInline(admin.StackedInline):
    """サイト詳細情報のインライン"""
    model = SiteDetail


class SiteAdmin(admin.ModelAdmin):
    """Siteモデルを、管理画面でSiteDetailもインラインで表示できるように"""
    inlines = [SiteDetailInline]


class ImageInline(admin.TabularInline):
    """記事内画像のインライン"""
    model = Image
    extra = 3


class FileInline(GenericTabularInline):
    """記事内添付ファイルのインライン"""
    model = File
    extra = 3


class PostAdmin(admin.ModelAdmin):
    """記事を、管理画面で画像とファイルIもインラインで埋め込む"""
    inlines = [ImageInline, FileInline]


admin.autodiscover()  # Siteアプリのadmin.pyを頑張って探す
admin.site.unregister(Site)  # インラインにするため一度解除
admin.site.register(Site, SiteAdmin)  # インライン
admin.site.register(Post, PostAdmin)  # インライン
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Comment)
admin.site.register(ReComment)
admin.site.register(Analytics)
admin.site.register(Ads)
admin.site.register(PopularPost)
admin.site.register(File)