"""admin.py"""
from django.contrib.sites.models import Site
from django.contrib import admin
from .models import (
    Post, Category, Tag, Comment, ReComment,
    Link, Analytics, Ads, SiteDetail, PopularPost, Image, File
)


class SiteDetailInline(admin.StackedInline):
    model = SiteDetail


class SiteAdmin(admin.ModelAdmin):
    inlines = [SiteDetailInline]


class ImageInline(admin.TabularInline):
    model = Image
    extra = 3


class FileInline(admin.TabularInline):
    model = File
    extra = 3


class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInline, FileInline]


admin.autodiscover()  # Siteアプリのadmin.pyを頑張って探す
admin.site.unregister(Site)  # インラインにするため一度解除
admin.site.register(Site, SiteAdmin)  # インライン!
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Comment)
admin.site.register(ReComment)
admin.site.register(Analytics)
admin.site.register(Ads)
admin.site.register(PopularPost)
