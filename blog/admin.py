"""admin.py"""
from django.contrib import admin
from .models import (
    Post, Category, Tag, Comment,
    Link, Analytics, Ads, SiteDetail
)


class OneDataAdmin(admin.ModelAdmin):
    """DBに1つだけデータを格納したいモデルは、これを使う."""

    def has_add_permission(self, request):
        """1件以上データがあればFalseを返す."""
        return False if self.model.objects.count() > 0 else True


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Link)
admin.site.register(Comment)
admin.site.register(Analytics)
admin.site.register(Ads)
admin.site.register(SiteDetail, OneDataAdmin)
